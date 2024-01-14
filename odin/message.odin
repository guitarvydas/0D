package zd

import "core:fmt"
import "core:log"
import "core:mem"
import "core:strings"

// Message passed to a leaf component.
//
// `port` refers to the name of the incoming or outgoing port of this component.
// `datum` is the data attached to this message.
Message :: struct {
    port:  Port_Type,
    datum: ^Datum,
    cause: ^Cause, // who+message that caused this message
}

Cause :: struct {
    // trail to help trace message provenance
    // each message is tagged with a Cause that describes who sent the message and what message
    // was handled by "who" in causing this message to be sent
    who : ^Eh,
    message : ^Message
}

Port_Type :: string


clone_port :: proc (s : string) -> Port_Type {
    p : Port_Type = strings.clone (s) // clone to heap
    return p
}


// Utility for making a `Message`. Used to safely "seed" messages
// entering the very top of a network.

make_message :: proc(port: Port_Type, datum: ^Datum, cause: ^Cause) -> ^Message {
    p := clone_port (port)
    m := new (Message)
    m.port  = p
    m.datum = datum.clone (datum)
    m.cause = cause
    return m
}

// Clones a message. Primarily used internally for "fanning out" a message to multiple destinations.
message_clone :: proc(message: ^Message) -> ^Message {
    m := new (Message)
    m.port = clone_port (message.port)
    m.datum = message.datum.clone (message.datum)
    m.cause = message.cause
    return m
}

// Frees a message.
destroy_message :: proc(msg: ^Message) {
    destroy_port (msg)
    destroy_datum (msg)
}

destroy_datum :: proc (msg: ^Message) {
    //log.errorf("TODO: destroy datum %v, but don't know how yet\n", typeid_of (type_of (d)))
}

destroy_port :: proc (msg: ^Message) {
    // TODO: implement GC or refcounting and avoid duplication of data when cloning
    // TODO: don't know how to destroy a string
}


make_cause :: proc (eh : ^Eh, msg : ^Message) -> ^Cause {
    // create a persistent Cause in the heap, return a pointer to it
    cause := new (Cause)
    cause.who = eh
    cause.message = msg
    return cause
}
