class OhmJS_Instance_Data:
    def _init_ (self):
        self.grammarname = None
        self.grammarfilename = None
        self.semanticsfilename = None
        self.s = None

def ohmjs_instantiate (reg, owner, name, template_data):
    instance_name = gensym ("OhmJS")
    inst = OhmJS_Instance_Data () # all fields have zero value before any messages are received
    return make_leaf (instance_name, owner, inst, ohmjs_handle)

def ohmjs_maybe (eh, inst, causingMsg):
    if None != inst.grammarname and None != inst.grammarfilename and None != inst.semanticsfilename and None != inst.s:
        cmd = "0d/python/std/ohmjs.js {inst.grammarname} {inst.grammarfilename} {inst.semanticsfilename}"
        [captured_output, err] = run_command (cmd, inst.s)

        errstring = trimws (err)
        if len (errstring) == 0:
            send_string (eh, "", trimws (captured_output), causingMsg)
        else:
            send_string (eh, "✗", errstring, causingMsg)
        inst.grammarName = None
        inst.grammarfilename = None
        inst.semanticsfilename = None
        inst.s = None

def ohmjs_handle (eh, msg):
    inst = eh.instance_data
    if msg.port == "grammar name":
        inst.grammarname = clone_string (msg.datum.srepr ())
        ohmjs_maybe (eh, inst, msg)
    elif msg.port == "grammar":
        inst.grammarfilename = clone_string (msg.datum.srepr ())
        ohmjs_maybe (eh, inst, msg)
    elif msg.port == "semantics":
        inst.semanticsfilename = clone_string (msg.datum.srepr ())
        ohmjs_maybe (eh, inst, msg)
    elif msg.port == "input":
        inst.s = clone_string (msg.datum.srepr ())
        ohmjs_maybe (eh, inst, msg)
    else:
        emsg = f"!!! ERROR: OhmJS got an illegal message port {msg.port}"
        send_string (eh, "✗", emsg, msg)



