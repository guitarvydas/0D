package std

import "core:fmt"
import "core:runtime"
import "core:log"
import "core:strings"
import "core:slice"
import "core:os"
import "core:unicode/utf8"

import zd "../0d"


OhmJS_Instance_Data :: struct {
    grammarname : string, // grammar name
    grammarfilename : string, // file name of grammar in ohm-js format
    semanticsfilename : string, // file name of source text of semantics support code JavaScript namespace
    input : string, // source file to be parsed
}

ohmjs_instantiate :: proc(name: string, owner : ^zd.Eh) -> ^zd.Eh {
    instance_name := gensym ("OhmJS")
    inst := new (OhmJS_Instance_Data) // all fields have zero value before any messages are received
    return zd.make_leaf (instance_name, owner, inst^, ohmjs_handle)
}

ohmjs_maybe :: proc (eh: ^zd.Eh, inst: ^OhmJS_Instance_Data, causingMsg: ^zd.Message) {
    if "" != inst.grammarname && "" != inst.grammarfilename && "" != inst.semanticsfilename && "" != inst.input {
        cmd := fmt.aprintf ("0d/odin/std/ohmjs.js %s %s %s", inst.grammarname, inst.grammarfilename, inst.semanticsfilename)
	captured_output, err := zd.run_command (cmd, inst.input)

	errstring := strings.trim_space (err)
	if len (errstring) == 0 {
            zd.send_string (eh, "output", strings.trim_space (captured_output), causingMsg)
	} else {
	    zd.send_string (eh, "error", errstring, causingMsg)
	}
    }
}

ohmjs_handle :: proc(eh: ^zd.Eh, msg: ^zd.Message) {
    inst := &eh.instance_data.(OhmJS_Instance_Data)
    switch (msg.port) {
    case "grammar name":
	inst.grammarname = strings.clone (msg.datum.repr (msg.datum))
	ohmjs_maybe (eh, inst, msg)
    case "grammar":
	inst.grammarfilename = strings.clone (msg.datum.repr (msg.datum))
	ohmjs_maybe (eh, inst, msg)
    case "semantics":
	inst.semanticsfilename = strings.clone (msg.datum.repr (msg.datum))
	ohmjs_maybe (eh, inst, msg)
    case "input":
	inst.input = strings.clone (msg.datum.repr (msg.datum))
	ohmjs_maybe (eh, inst, msg)
	case:
        emsg := fmt.aprintf("!!! ERROR: OhmJS got an illegal message port %v", msg.port)
	zd.send_string (eh, "error", emsg, msg)
    }
}

////


