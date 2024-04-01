class OhmJS_Instance_Data:
    def __init__ (self):
        self.pathname_0D_ = None
        self.grammar_name = None
        self.grammar_filename = None
        self.semantics_filename = None
        self.s = None

def ohmjs_instantiate (reg, owner, name, template_data):
    instance_name = gensym ("OhmJS")
    inst = OhmJS_Instance_Data () # all fields have zero value before any messages are received
    return make_leaf (instance_name, owner, inst, ohmjs_handle)

def ohmjs_maybe (eh, inst, causingMsg):
    if None != inst.pathname_0D_ and None != inst.grammar_name and None != inst.grammar_filename and None != inst.semantics_filename and None != inst.s:
        cmd = [f"{inst.pathname_0D_}/std/ohmjs.js", f"{inst.grammar_name}", f"{inst.grammar_filename}", f"{inst.semantics_filename}"]
        [captured_output, err] = run_command (eh, cmd, inst.s)

        if err == None:
            err = ""
        errstring = trimws (err)
        if len (errstring) == 0:
            send_string (eh, "", trimws (captured_output), causingMsg)
        else:
            send_string (eh, "✗", errstring, causingMsg)
        inst.pathname_0D_ = None
        inst.grammar_name = None
        inst.grammar_filename = None
        inst.semantics_filename = None
        inst.s = None

def ohmjs_handle (eh, msg):
    inst = eh.instance_data
    if msg.port == "0D path":
        inst.pathname_0D_ = clone_string (msg.datum.srepr ())
        ohmjs_maybe (eh, inst, msg)
    elif msg.port == "grammar name":
        inst.grammar_name = clone_string (msg.datum.srepr ())
        ohmjs_maybe (eh, inst, msg)
    elif msg.port == "grammar":
        inst.grammar_filename = clone_string (msg.datum.srepr ())
        ohmjs_maybe (eh, inst, msg)
    elif msg.port == "semantics":
        inst.semantics_filename = clone_string (msg.datum.srepr ())
        ohmjs_maybe (eh, inst, msg)
    elif msg.port == "input":
        inst.s = clone_string (msg.datum.srepr ())
        ohmjs_maybe (eh, inst, msg)
    else:
        emsg = f"!!! ERROR: OhmJS got an illegal message port {msg.port}"
        send_string (eh, "✗", emsg, msg)



