import sys
import re
import subprocess
import shlex

root_project = ""
root_0D = ""

def set_environment (rproject, r0D):
    global root_project
    global root_0D
    root_project = rproject
    root_0D = r0D

####

def probe_instantiate (reg, owner, name, template_data):      
    name_with_id = gensym ("?")
    return make_leaf (name=name_with_id, owner=owner, instance_data=None, handler=probe_handler)

def probeA_instantiate (reg, owner, name, template_data):      
    name_with_id = gensym ("?A")
    return make_leaf (name=name_with_id, owner=owner, instance_data=None, handler=probe_handler)

def probeB_instantiate (reg, owner, name, template_data):      
    name_with_id = gensym("?B")
    return make_leaf (name=name_with_id, owner=owner, instance_data=None, handler=probe_handler)

def probeC_instantiate (reg, owner, name, template_data):      
    name_with_id = gensym("?C")
    return make_leaf (name=name_with_id, owner=owner, instance_data=None, handler=probe_handler)

def probe_handler (eh, msg):
    s = msg.datum.srepr ()
    print (f"... probe {eh.name}: {s}", file=sys.stderr)

    
def trash_instantiate (reg, owner, name, template_data):      
    name_with_id = gensym ("trash")
    return make_leaf (name=name_with_id, owner=owner, instance_data=None, handler=trash_handler)
def trash_handler (eh, msg):
    # to appease dumped-on-floor checker
    pass


####

class TwoMessages:
    def __init__ (self, first=None, second=None):
        self.first = first
        self.second = second

# Deracer_States :: enum { idle, waitingForFirst, waitingForSecond }

class Deracer_Instance_Data:
    def __init__ (self, state="idle", buffer=None):
        self.state=state
        self.buffer=buffer

def reclaim_Buffers_from_heap (inst):      
    pass

def deracer_instantiate (reg, owner, name, template_data):      
    name_with_id = gensym ("deracer")
    inst = Deracer_Instance_Data (buffer=TwoMessages ())
    inst.state = "idle"
    eh = make_leaf (name=name_with_id, owner=owner, instance_data=inst, handler=deracer_handler)
    return eh

def send_first_then_second (eh, inst):
    forward (eh, "1", inst.buffer.first)
    forward (eh, "2", inst.buffer.second)
    reclaim_Buffers_from_heap (inst)


def deracer_handler (eh, msg):      
    inst = eh.instance_data
    if inst.state == "idle":
        if "1" == msg.port:
            inst.buffer.first = msg
            inst.state = "waitingForSecond"
        elif "2" == msg.port:
            inst.buffer.second = msg
            inst.state = "waitingForFirst"
        else:
            runtime_error (f"bad msg.port (case A) for deracer {msg.port}")
        
    elif inst.state == "waitingForFirst":
        if "1" == msg.port:
            inst.buffer.first = msg
            send_first_then_second (eh, inst)
            inst.state = "idle"
        else:
            runtime_error (f"bad msg.port (case B) for deracer {msg.port}")
        
    elif inst.state == "waitingForSecond":
        if "2" == msg.port:
            inst.buffer.second = msg
            send_first_then_second (eh, inst)
            inst.state = "idle"
        else:
            runtime_error (f"bad msg.port (case C) for deracer {msg.port}")
        
    else:
        runtime_error ("bad state for deracer {eh.state}")
    



####

def low_level_read_text_file_instantiate (reg, owner, name, template_data):      
    name_with_id = gensym("Low Level Read Text File")
    return make_leaf (name_with_id, owner, None, low_level_read_text_file_handler)


def low_level_read_text_file_handler (eh, msg):      
    fname = msg.datum.srepr ()
    try:
        f = open (fname)
    except Exception as e:
        f = None
    if f != None:
        data = f.read ()
        if data!= None:
            send_string (eh, "", data, msg)
        else:
            emsg = f"read error on file {fname}"
            send_string (eh, "✗", emsg, msg)
        f.close ()
    else:
        emsg = f"open error on file {fname}"
        send_string (eh, "✗", emsg, msg)
    



####
def ensure_string_datum_instantiate (reg, owner, name, template_data):      
    name_with_id = gensym("Ensure String Datum")
    return make_leaf (name_with_id, owner, None, ensure_string_datum_handler)


def ensure_string_datum_handler (eh, msg):
    if "string" == msg.datum.kind ():
        forward (eh, "", msg)
    else:
        emsg = f"*** ensure: type error (expected a string datum) but got {msg.datum}"
        send_string (eh, "✗", emsg, msg)
    


####

class Syncfilewrite_Data:
    def __init__ (self):
        self.filename = ""

# temp copy for bootstrap, sends "done" (error during bootstrap if not wired)

def syncfilewrite_instantiate (reg, owner, name, template_data):      
    name_with_id = gensym ("syncfilewrite")
    inst = Syncfilewrite_Data ()
    return make_leaf (name_with_id, owner, inst, syncfilewrite_handler)


def syncfilewrite_handler (eh, msg):      
    inst = eh.instance_data
    if "filename" == msg.port:
        inst.filename = msg.datum.srepr ()
    elif "input" == msg.port:
        contents = msg.datum.srepr ()
        f = open (inst.filename, "w")
        if f != None:
            f.write (msg.datum.srepr ())
            f.close ()
            send (eh, "done", new_datum_bang (), msg)
        else:
            send_string (eh, "✗", f"open error on file {inst.filename}", msg)

####

class StringConcat_Instance_Data:
    def __init__ (self):
        self.buffer1 = None
        self.buffer2 = None
        self.count = 0

def stringconcat_instantiate (reg, owner, name, template_data):      
    name_with_id = gensym ("stringconcat")
    instp = StringConcat_Instance_Data ()
    return make_leaf (name_with_id, owner, instp, stringconcat_handler)


def stringconcat_handler (eh, msg):
    inst = eh.instance_data
    if "1" == msg.port:
        inst.buffer1 = clone_string (msg.datum.srepr ())
        inst.count += 1
        maybe_stringconcat (eh, inst, msg)
    elif "2" == msg.port:
        inst.buffer2 = clone_string (msg.datum.srepr ())
        inst.count += 1
        maybe_stringconcat (eh, inst, msg)
    else:
        runtime_error (f"bad msg.port for stringconcat: {msg.port}")
    

def maybe_stringconcat (eh, inst, msg):      
    if (0 == len (inst.buffer1)) and (0 == len (inst.buffer2)):
        runtime_error ("something is wrong in stringconcat, both strings are 0 length")
    
    if inst.count >= 2:
        concatenated_string = ""
        if 0 == len (inst.buffer1):
            concatenated_string = inst.buffer2
        elif 0 == len (inst.buffer2):
            concatenated_string = inst.buffer1
        else:
            concatenated_string = inst.buffer1 + inst.buffer2
        
        send_string (eh, "", concatenated_string, msg)
        inst.buffer1 = None
        inst.buffer2 = None
        inst.count = 0

####

# this needs to be rewritten to use the low-level "shell_out" component, this can be done solely as a diagram without using python code here
def shell_out_instantiate (reg, owner, name, template_data):
    name_with_id = gensym ("shell_out")
    cmd = shlex.split (template_data)
    return make_leaf (name_with_id, owner, cmd, shell_out_handler)

def shell_out_handler (eh, msg):
    cmd = eh.instance_data
    s = msg.datum.srepr ()
    [stdout, stderr] = run_command (eh, cmd, s)
    if stderr != None:
        send_string (eh, "✗", stderr, msg)
    else:
        send_string (eh, "", stdout, msg)

####

def string_constant_instantiate (reg, owner, name, template_data):
    global root_project
    global root_0D
    name_with_id = gensym ("strconst")
    s = template_data
    if root_project != "":
        s  = re.sub ("_00_", root_project, s)
    if root_0D != "":
        s  = re.sub ("_0D_", root_0D, s)
    return make_leaf (name_with_id, owner, s, string_constant_handler)

def string_constant_handler (eh, msg):
    s = eh.instance_data
    send_string (eh, "", s, msg)

####

def string_make_persistent (s):
    # this is here for non-GC languages like Odin, it is a no-op for GC languages like Python
    return s
def string_clone (s):
    return s
