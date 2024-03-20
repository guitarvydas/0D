def stdout_instantiate (name, owner):      
    return zd.make_leaf(name, owner, nil, stdout_handle)


def stdout_handle (eh,msg):      
    fmt.printf("%#v", msg.datum)


def process_instantiate (name,owner):      
    i := strings.index_rune (name, '$')
    command_local_slice := name [i:(len (name))]
    command_string := strings.clone(strings.trim_left (command_local_slice, "$ "))
    command_string_ptr := new_clone(command_string)
    return zd.make_leaf(name, owner, command_string_ptr^, process_handle)


def process_handle (eh,msg):      
    
    utf8_string :: proc(bytes: []byte) -> (s: string, ok: bool)     
        s = string(bytes)
        ok = utf8.valid_string(s)
        return
    
    

    switch msg.port     
    case "":
	cmd := eh.instance_data.(string)
        handle := zd.process_start(cmd)
        defer zd.process_destroy_handle(handle)

        // write input, wait for finish
            
	    switch msg.datum.kind ()     
	    case "string":
                os.write(handle.input, msg.datum.raw (msg.datum))
	    case "bytes":
                os.write(handle.input, msg.datum.raw (msg.datum))
	    case "bang":
                // OK, no input, just run it
	    case:
                log.errorf("%s: Shell leaf input can handle string, bytes, or bang (got: %v)",
			   eh.name, msg.datum.kind ())
            
            os.close(handle.input)
            zd.process_wait(handle)
        

        // breaks bootstrap error check, thus, removed line: zd.send_string (eh, "done", Bang    )

        // stdout handling
            
            stdout, stdout_ok := zd.process_read_handle(handle.output)

            // stderr handling
            stderr_untrimmed, stderr_ok := zd.process_read_handle(handle.error)
	    stderr : string
            if stderr_ok     
		stderr = strings.trim_right_space(cast(string)stderr_untrimmed)
            
	    if stdout_ok && stderr_ok     
		// fire only one output port
		// on error, send both, stdout and stderr to the error port
		if len (stderr) > 0     
		    zd.send_string(eh, "✗", fmt.aprintf ("%v: %v", cmd, stderr), msg)
		 else     
                    zd.send_string (eh, "", transmute(string)stdout, msg)
		
	     else     
		// panic - we should never fail to collect stdout and stderr
		// if we come here, then something is deeply wrong with this code
		fmt.assertf (false, "PANIC: failed to retrieve outputs stdout_ok = %v stderr_ok = %v\n", stdout_ok, stderr_ok)
            
	
    




collect_process_leaves :: proc(diagram_name: string, leaves: ^[dynamic]zd.Leaf_Instantiator) {
    def ref_is_container (decls,name):      
        for d in decls     
            if d.name == name     
                return true
            
        
        return false
    

    decls := zd.json2internal (diagram_name)
    defer zd.delete_decls (decls)

    // TODO(z64): while harmless, this doesn't ignore duplicate process decls yet.

    for decl in decls {
        for child in decl.children {
            if ref_is_container(decls[:], child.name) {
                continue
            }

	    i := strings.index_rune (child.name, '$')
            if i >= 0 {
                leaf_instantiate := zd.Leaf_Instantiator {
                    name = child.name,
                    instantiate = process_instantiate,
                }
                append(leaves, leaf_instantiate)
            }
        }
    }
}

////

Command_Instance_Data :: struct {
    buffer : string
}

def command_instantiate (name,owner):      
    name_with_id := zd.gensym("command")
    instp := new (Command_Instance_Data)
    return zd.make_leaf (name_with_id, owner, instp^, command_handle)


def command_handle (eh,msg):      
    inst := eh.instance_data.(Command_Instance_Data)
    switch msg.port     
    case "command":
        inst.buffer = msg.datum.repr (msg.datum)
        received_input := msg.datum.repr (msg.datum)
        captured_output, _ := zd.run_command (inst.buffer, received_input)
        zd.send_string (eh, "", captured_output, msg)
	case:
        fmt.assertf (false, "!!! ERROR: command got an illegal message port %v", msg.port)
    


def icommand_instantiate (name,owner):      
    name_with_id := zd.gensym("icommand[%d]")
    instp := new (Command_Instance_Data)
    return zd.make_leaf (name_with_id, owner, instp^, icommand_handle)


def icommand_handle (eh,msg):      
    inst := eh.instance_data.(Command_Instance_Data)
    switch msg.port     
    case "command":
        inst.buffer = msg.datum.repr (msg.datum)
    case "":
        received_input := msg.datum.repr (msg.datum)
        captured_output, _ := zd.run_command (inst.buffer, received_input)
        zd.send_string (eh, "", captured_output, msg)
	case:
        fmt.assertf (false, "!!! ERROR: command got an illegal message port %v", msg.port)
    
