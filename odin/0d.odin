package zd

import "core:container/queue"
import "core:fmt"
import "core:mem"
import "core:runtime"
import "core:strings"
import "core:intrinsics"
import "core:log"

Bang :: struct {}
log_all :: 0
log_full_handlers :: 4
log_light_handlers :: 5

// Data for an asyncronous component - effectively, a function with input
// and output queues of messages.
//
// Components can either be a user-supplied function ("leaf"), or a "container"
// that routes messages to child components according to a list of connections
// that serve as a message routing table.
//
// Child components themselves can be leaves or other containers.
//
// `handler` invokes the code that is attached to this component.
//
// `instance_data` is a pointer to instance data that the `leaf_handler`
// function may want whenever it is invoked again.
//
Eh_States :: enum { idle, active }
Eh :: struct {
    name:         string,
    input:        FIFO,
    output:       FIFO,
    owner:        ^Eh,
    children:     []^Eh,
    connections:  []Connector,
    handler:      #type proc(eh: ^Eh, message: ^Message),
    instance_data: any,
    state:       Eh_States,
    kind: enum { container, leaf, }, // for debug
    trace:        bool, // set 'true' if logging is enabled and if this component should be traced, (false means silence, no tracing for this component)
    depth:        int, // hierarchical depth of component, 0=top, 1=1st child of top, 2=1st child of 1st child of top, etc.
}


// Creates a component that acts as a container. It is the same as a `Eh` instance
// whose handler function is `container_handler`.
make_container :: proc(name: string, owner : ^Eh) -> ^Eh {
    eh := new(Eh)
    eh.name = name
    eh.owner = owner
    eh.handler = container_handler
    eh.state = .idle
    eh.kind = .container
    return eh
}

// Creates a new leaf component out of a handler function, and optionally a user
// data parameter that will be passed back to your handler when it is run.

make_leaf_with_no_instance_data :: proc(name: string, owner : ^Eh, handler: proc(^Eh, ^Message)) -> ^Eh {
    return make_leaf (name, owner, nil, handler)
}

// Creates a new leaf component out of a handler function, and a data parameter
// that will be passed back to your handler when called.
make_leaf :: proc(name: string, owner: ^Eh, instance_data: any, handler: proc(^Eh, ^Message)) -> ^Eh {
    eh := new(Eh)
    eh.name = fmt.aprintf ("%s.%s", owner.name, name)
    eh.owner = owner
    eh.handler = handler
    eh.instance_data = instance_data
    eh.state = .idle
    eh.kind = .leaf
    return eh
}

// Sends a message on the given `port` with `data`, placing it on the output
// of the given component.
send :: proc(eh: ^Eh, port: string, datum: ^Datum, causingMessage : ^Message) {
    cause := make_cause (eh, causingMessage)
    sendf(eh, "SEND 0x%p %v%s(%s)[%v]", eh, indent (eh), eh.name, port, cause)
    msg := make_message(port, datum, cause)
    fifo_push(&eh.output, msg)
}

send_string :: proc(eh: ^Eh, port: string, s : string, causingMessage : ^Message) {
    cause := make_cause (eh, causingMessage)
    sendf(eh, "SEND 0x%p %v%s(%s) [%v]", eh, indent (eh), eh.name, port, cause.message.port)
    datum := new_datum_string (s)
    msg := make_message(port, datum, cause)
    fifo_push(&eh.output, msg)
}

forward :: proc(eh: ^Eh, port: string, msg: ^Message) {
    sendf(eh, "FORWARD 0x%p %v%s->%v", eh, indent (eh), eh.name, port)
    fwdmsg := make_message(port, msg.datum, make_cause (eh, msg))
    fifo_push(&eh.output, fwdmsg)
}

// Returns a list of all output messages on a container.
// For testing / debugging purposes.
output_list :: proc(eh: ^Eh, allocator := context.allocator) -> []^Message {
    list := make([]^Message, eh.output.len)

    iter := make_fifo_iterator(&eh.output)
    for msg, i in fifo_iterate(&iter) {
        list[i] = msg
    }

    return list
}

// The default handler for container components.
container_handler :: proc(eh: ^Eh, message: ^Message) {
    route(eh, nil, message)
    for any_child_ready(eh) {
        step_children(eh, message)
    }
}

// Frees the given container and associated data.
destroy_container :: proc(eh: ^Eh) {
    drain_fifo :: proc(fifo: ^FIFO) {
        for fifo.len > 0 {
            msg, _ := fifo_pop(fifo)
            destroy_message(msg)
        }
    }
    drain_fifo(&eh.input)
    drain_fifo(&eh.output)
    free(eh)
}

// Wrapper for corelib `queue.Queue` with FIFO semantics.
FIFO       :: queue.Queue(^Message)
fifo_push  :: queue.push_back
fifo_pop   :: queue.pop_front_safe

fifo_is_empty :: proc(fifo: FIFO) -> bool {
    return fifo.len == 0
}

FIFO_Iterator :: struct {
    q:   ^FIFO,
    idx: uint,
}

make_fifo_iterator :: proc(q: ^FIFO) -> FIFO_Iterator {
    return {q, 0}
}

fifo_iterate :: proc(iter: ^FIFO_Iterator) -> (item: ^Message, idx: uint, ok: bool) {
    if iter.q.len == 0 {
        ok = false
        return
    }

    i := (uint(iter.idx)+iter.q.offset) % len(iter.q.data)
    if iter.idx < iter.q.len {
        ok = true
        idx = iter.idx
        iter.idx += 1
        #no_bounds_check item = iter.q.data[i]
    }
    return
}

// Routing connection for a container component. The `direction` field has
// no affect on the default message routing system - it is there for debugging
// purposes, or for reading by other tools.
Connector :: struct {
    direction: Direction,
    sender:    Sender,
    receiver:  Receiver,
}

Direction :: enum {
    Down,
    Across,
    Up,
    Through,
}

// `Sender` is used to "pattern match" which `Receiver` a message should go to,
// based on component ID (pointer) and port name.
Sender :: struct {
    name: string,
    component: ^Eh,
    port:      Port_Type,
}

// `Receiver` is a handle to a destination queue, and a `port` name to assign
// to incoming messages to this queue.
Receiver :: struct {
    name: string,
    queue: ^FIFO,
    port:  Port_Type,
}

// Checks if two senders match, by pointer equality and port name matching.
sender_eq :: proc(s1, s2: Sender) -> bool {
    return s1.component == s2.component && s1.port == s2.port
}

// Delivers the given message to the receiver of this connector.
deposit :: proc(c: Connector, message: ^Message) {
    new_message := message_clone(message)
    new_message.port = c.receiver.port
    fifo_push(c.receiver.queue, new_message)
}

light_receivef :: proc(eh : ^Eh, fmt_str: string, args: ..any, location := #caller_location) {
    if (eh.trace) {
	log.logf(cast(runtime.Logger_Level)log_light_handlers,   fmt_str, ..args, location=location)
    }
}
full_receivef :: proc(eh : ^Eh, fmt_str: string, args: ..any, location := #caller_location) {
    if (eh.trace) {
	log.logf(cast(runtime.Logger_Level)log_full_handlers,   fmt_str, ..args, location=location)
    }
}

sendf :: proc(eh : ^Eh, fmt_str: string, args: ..any, location := #caller_location) {
    if (eh.trace) {
	log.logf(cast(runtime.Logger_Level)log_all,   fmt_str, ..args, location=location)
    }
}

outputf :: proc(eh : ^Eh, fmt_str: string, args: ..any, location := #caller_location) {
    if (eh.trace) {
	log.logf(cast(runtime.Logger_Level)log_all,   fmt_str, ..args, location=location)
    }
}

format_debug_based_on_depth :: proc (depth : int, name : string, port: string) -> string {
    if depth < 3 {
	return fmt.aprintf ("%s <- [%s]", name, port)
    } else {
	return "..."
    }
}	    

step_children :: proc(container: ^Eh, causingMessage: ^Message) {
    container.state = .idle
    for child in container.children {
        msg: ^Message
        ok: bool

        switch {
        case child.input.len > 0:
            msg, ok = fifo_pop(&child.input)
	case child.state != .idle:
	    ok = true
	    msg = force_tick (child, causingMessage)
        }

        if ok {
            //light_receivef(child, ".%v.%v%s <- [%s]", child.depth, indent (child), child.name, msg.port)
            light_receivef(child, ".%v.%v%s", child.depth, indent (child), format_debug_based_on_depth (child.depth, child.name, msg.port))
            full_receivef(child, "HANDLE  0x%p %v%s <- %v (%v)", child, indent (child), child.name, msg, msg.datum.kind ())
            child.handler(child, msg)
            destroy_message(msg)
        }

	if child.state == .active {
	    container.state = .active
	}

        for child.output.len > 0 {
            msg, _ = fifo_pop(&child.output)
            outputf(child, "OUTPUT 0x%p %v%s -> [%s]", child, indent (child), child.name, msg.port)
            route(container, child, msg)
            destroy_message(msg)
        }
    }
}

force_tick :: proc (eh: ^Eh, causingMessage: ^Message) -> ^Message{
    tick_msg := make_message (".", new_datum_tick (), make_cause (eh, causingMessage))
    fifo_push (&eh.input, tick_msg)
    return tick_msg
}

attempt_tick :: proc (eh: ^Eh, causingMessage: ^Message) {
    if eh.state != .idle {
	force_tick (eh, causingMessage) // ignore return value
    }
}

is_tick :: proc (msg : ^Message) -> bool {
    return "tick" == msg.datum.kind ()
}


// Routes a single message to all matching destinations, according to
// the container's connection network.
route :: proc(container: ^Eh, from: ^Eh, message: ^Message) {
    was_sent := false // for checking that output went somewhere (at least during bootstrap)
    if is_tick (message) {
	for child in container.children {
	    attempt_tick (child, message)
	}
	was_sent = true
    } else {
	fname := ""
	if from != nil  {
	    fname = from.name
	}
	from_sender := Sender{fname, from, message.port}
	
	for connector in container.connections {
            if sender_eq(from_sender, connector.sender) {
		deposit(connector, message)
		was_sent = true
            }
	}
    }
    if ! was_sent {
	fmt.printf ("\n\n*** Error: ***")
	fmt.printf ("\n %v: message '%v' from %v dropped on floor...\n%v [%v]\n\n", container.name, message.port, from.name, message.datum.repr (message.datum), message.cause)
	dump_possible_connections (container)
	fmt.printf ("\n***\n")
    }
}

dump_possible_connections :: proc (container: ^Eh) {
    if false {
	fmt.printf ("\n*** possible connections:")
	for connector in container.connections {
	    fmt.printf ("\n\n%v", connector)
	}
    }
}

any_child_ready :: proc(container: ^Eh) -> (ready: bool) {
    for child in container.children {
        if child_is_ready(child) {
            return true
        }
    }
    return false
}

child_is_ready :: proc(eh: ^Eh) -> bool {
    return !fifo_is_empty(eh.output) || !fifo_is_empty(eh.input) || eh.state!= .idle || any_child_ready (eh)
}

// Utility for printing an array of messages.
print_output_list :: proc(eh: ^Eh) {
    write_rune   :: strings.write_rune
    write_string :: strings.write_string

    sb: strings.Builder
    defer strings.builder_destroy(&sb)

    write_rune(&sb, '[')

    iter := make_fifo_iterator(&eh.output)
    for msg, idx in fifo_iterate(&iter) {
        if idx > 0 {
            write_string(&sb, ",\n")
        }
	cause := msg.cause
	{
	    mds : string
	    tempstr := msg.datum.repr (msg.datum)
	    if false { //len (tempstr) > 20 {
		mds = fmt.aprintf ("%v...", tempstr[:19])
	    } else {
		mds = tempstr
	    }
            fmt.sbprintf(&sb, "{{«%v»: %v}}", 
			 msg.port, mds) //cause.who.name, cause.message.port)
	}
    }
    strings.write_rune(&sb, ']')

    fmt.println(strings.to_string(sb))
}

set_active :: proc (eh: ^Eh) {
    eh.state = .active
}

set_idle :: proc (eh: ^Eh) {
    eh.state = .idle
}

// Utility for printing a specific output message.
fetch_first_output :: proc (eh :^Eh, port: Port_Type) -> (^Datum, bool) {
    iter := make_fifo_iterator(&eh.output)
    for msg, idx in fifo_iterate(&iter) {
	if msg.port == port {
	    return msg.datum, true
	}
    }
    return nil, false
}

print_specific_output :: proc(eh: ^Eh, port: string, stderr : bool) {
    sb: strings.Builder
    defer strings.builder_destroy(&sb)

    datum, found := fetch_first_output (eh, port)
    if found {
	fmt.sbprintf(&sb, "%v", datum.repr (datum))
	if stderr {
	    fmt.eprintln(strings.to_string(sb))
	} else {
	    fmt.println(strings.to_string(sb))
	}
    }
}

indent :: proc (eh : ^Eh) -> string {
    if eh.owner == nil {
	return ""
    } else {
	return fmt.aprintf ("    %s", indent (eh.owner))
    }
}

