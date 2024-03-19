# Data for an asyncronous component - effectively, a function with input
# and output queues of messages.
#
# Components can either be a user-supplied function ("leaf"), or a "container"
# that routes messages to child components according to a list of connections
# that serve as a message routing table.
#
# Child components themselves can be leaves or other containers.
#
# `handler` invokes the code that is attached to this component.
#
# `instance_data` is a pointer to instance data that the `leaf_handler`
# function may want whenever it is invoked again.
#

import queue
import sys

# Eh_States :: enum { idle, active }

class Eh:
    def _init_ (self):
        self.name
        self.input = queue.Queue ()
        self.output = queue.Queue ()
        self.owner = none
        self.children = []
        self.visit_ordering = queue.Queue ()
        self.connections = []
        self.accepted = queue.LifoQueue ()  # ordered list of messages received (most recent message is first)
        self.handler = none
        self.instance_data = none
        self.state = "idle"
        # bootstrap debugging
        self.kind = none # enum { container, leaf, }
        self.trace = false # set 'true' if logging is enabled and if this component should be traced, (false means silence, no tracing for this component)
        self.depth = 0 # hierarchical depth of component, 0=top, 1=1st child of top, 2=1st child of 1st child of top, etc.

# Creates a component that acts as a container. It is the same as a `Eh` instance
# whose handler function is `container_handler`.
def make_container (name, owner):
    eh = Eh ()
    eh.name = name
    eh.owner = owner
    eh.handler = container_handler
    eh.state = "idle"
    eh.kind = "container"
    return eh


# Creates a new leaf component out of a handler function, and a data parameter
# that will be passed back to your handler when called.
def make_leaf (name, owner, instance_data, handler):
    eh = Eh ()
    eh.name = f"{owner.name}.{name}"
    eh.owner = owner
    eh.handler = handler
    eh.instance_data = instance_data
    eh.state = "idle"
    eh.kind = "leaf"
    return eh

# Sends a message on the given `port` with `data`, placing it on the output
# of the given component.
def send (eh,port,datum,causingMessage):      
    cause = make_cause (eh, causingMessage)
    msg = make_message(port, datum, cause)
    eh.output.put (msg)


def send_string (eh,port,s,causingMessage):      
    cause = make_cause (eh, causingMessage)
    datum = new_datum_string (s)
    msg = make_message(port, datum, cause)
    eh.output.put (msg)


def forward (eh,port,msg):      
    fwdmsg = make_message(port, msg.datum, make_cause (eh, msg))
    eh.output.put (fwdmsg)

# Returns a list of all output messages on a container.
# For testing / debugging purposes.
def output_list (eh):
    return eh.output

# The default handler for container components.
def container_handler (eh,message):      
    route (eh, nil, message)
    if any_child_ready (eh):
        eh.step_children (message)

# Frees the given container and associated data.
def destroy_container (eh):      
    pass

def fifo_is_empty (fifo):      
    return fifo.empty ()

# Routing connection for a container component. The `direction` field has
# no affect on the default message routing system - it is there for debugging
# purposes, or for reading by other tools.
class Connector:
    def _init_ (self):
        self.direction = none # down, across, up, through
        self.sender = none
        self.receiver = none

# `Sender` is used to "pattern match" which `Receiver` a message should go to,
# based on component ID (pointer) and port name.
class Sender:
    def _init_ (self, name, component, port):
        self.name = name
        self.component = component # from
        self.port = port # from's port

# `Receiver` is a handle to a destination queue, and a `port` name to assign
# to incoming messages to this queue.
class Receiver:
    def _init_ (self, name, queue, port, component):
        self.name = name
        self.queue = queue # queue (input | output) of receiver
        self.port = port # destination port
        self.component = component # to (for bootstrap debug)

# Checks if two senders match, by pointer equality and port name matching.
def sender_eq (s1, s2):
    return (s1.component == s2.component) and (s1.port == s2.port)

# Delivers the given message to the receiver of this connector.
def deposit (parent, c, message):      
    new_message = message_clone(message)
    new_message.port = c.receiver.port
    push_message (parent, c.receiver.component, c.receiver.queue, new_message)


def force_tick (parent, eh, causingMessage):      
    tick_msg = make_message (".", new_datum_tick (), make_cause (eh, causingMessage))
    push_message (parent, eh, eh.input, tick_msg)
    return tick_msg


def push_message (parent, receiver, inq, m):      
    inq.put (m)
    parent.visit_ordering.put (receiver)


def step_children (container, causingMessage):      
    container.state = "idle"
    for child in container.visit_ordering:
        # child == none represents self, skip it
        if (child != none): 
            if (not (child.input.empty ())):
                msg = child.input.get ()
            else:
                if (child.state != "idle"):
                    msg = force_tick (container, child, causingMessage)
                    memo_accept (container, msg)
            
            child.handler(child, msg)
            destroy_message(msg)
            
            if (child.state == "active"):
                # if child remains active, then the container must remain active and must propagate "ticks" to child
                container.state = "active"
            
            while (not (child.output.empty ())):
                msg = child.output.get ()
                route(container, child, msg)
                destroy_message(msg)

def attempt_tick (parent, eh, causingMessage):      
    if eh.state != "idle":
        force_tick (parent, eh, causingMessage)

def is_tick (msg):      
    return "tick" == msg.datum.kind ()

# Routes a single message to all matching destinations, according to
# the container's connection network.
def route (container, from_component, message):      
    was_sent = false # for checking that output went somewhere (at least during bootstrap)
    if is_tick (message):
        for child in container.children:    
            attempt_tick (container, child, message)
        was_sent = true
    else:
        fromname = ""
        if from_component != none:
            fname = from_component.name
        from_sender = Sender (fname, from_component, message.port)
        
        for connector in container.connections:
            if sender_eq(from_sender, connector.sender):   
                deposit(container, connector, message)
                was_sent = true
    if not (was_sent): 
        print ("\n\n*** Error: ***")
        print (f"{container.name}: message '{message.port}' from {from_component.name} dropped on floor...")
        dump_possible_connections (container)
        print ("***")
    
def dump_possible_connections (container):      
    print ("*** possible connections:")
    for connector in container.connections:
        print ("{connector.direction} ❲connector.sender.name❳.❲connector.sender.port❳ -> ❲connector.receiver.name❳")

def any_child_ready (container):
    for child in container.children:
        if child_is_ready(child):
            return true

def child_is_ready (eh):      
    return (not (eh.output.empty ())) or (not (eh.input.empty ())) or ( eh.state != "idle") or (any_child_ready (eh))


# Utility for printing an array of messages.
def print_output_list (eh):
    print (eh.output)

def set_active (eh):      
    eh.state = "active"

def set_idle (eh):      
    eh.state = "idle"

# Utility for printing a specific output message.
def fetch_first_output (eh, port):
    for msg in eh.output:
        if (msg.port == port):
            return msg.datum
    return none

def print_specific_output (eh, port, stderr):
    datum = fetch_first_output (eh, port)
    if datum != none:
        if stderr:              # I don't remember why I found it useful to print to stderr during bootstrapping, so I've left it in...
            f = sys.stderr
        else:
            f = sys.stdout
        print (datum.srepr (), file=f)

def memo_accept (eh, msg):      
    # PENGTODO: this is MVI, it can be done better ... PE: rewrite this to be less inefficient
    eh.accepted.put (msg)
