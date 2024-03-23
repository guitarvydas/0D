import sys
import re
import subprocess

def string_constant (str):      
    quoted_name = f"'{str}'"
    return Template (name = quoted_name, instantiator = literal_instantiate)


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
    return make_leaf (name=name_with_id, owner=owner, instance_data=None, handle=trash_handler)
def trash_handler (eh, msg):
    # to appease dumped-on-floor checker
    pass


####
def literal_instantiate (instance_name, owner):      
    name = re.sub (r"^.*'", "", instance_name)  # strip parent names from front
    quoted = re.sub ("<br>", "\n", name) # replace HTML newlines with real newlines
    name_with_id = gensym (quoted)
    pstr = string_make_persistent (quoted)
    return make_leaf (name=name_with_id, owner=owner, instance_data=pstr, handle=literal_handler)


def literal_handler (eh, msg):      
    send_string (eh, "⍺", eh.instance_data, msg)


####

class TwoMessages:
    def __init__ (self, first=None, second=None):
        pass

# Deracer_States :: enum { idle, waitingForFirst, waitingForSecond }

class Deracer_Instance_Data:
    def __init__ (self, state="idle", buffer=[]):
        pass

def reclaim_Buffers_from_heap (inst):      
    pass

def deracer_instantiate (reg, owner, name, template_data):      
    name_with_id = gensym ("deracer")
    inst = Deracer_Instance_Data ()
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
    f = open (fname)
    if f != None:
        data = f.read ()
        if data!= None:
            send_string (eh, "", data, msg)
        else:
            emsg = f"read error on file {fname}"
            send_string (eh, "✗", emsg, msg)
        f.close ()
    else:
        emsg = f"open error on file {f}"
        send_string (eh, "✗", emsg, msg)
    



####
def ensure_string_datum_instantiate (reg, owner, name, template_data):      
    name_with_id = gensym("Ensure String Datum")
    return make_leaf (name_with_id, owner, None, ensure_string_datum_handler)


def ensure_string_datum_handler (eh, msg):      
    if isinstance (msg.datum, str):
        forward (eh, "", msg)
    else:
        emsg = f"*** ensure: type error (expected a string datum) but got {msg.datum}"
        send_string (eh, "✗", emsg, msg)
    


####

class Syncfilewrite_Data:
    def __init__ (self):
        filename = ""

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
        f = open (inst.filename)
        if f != None:
            f.write (msg.datum)
            f.close ()
        else:
            send_string (eh, "✗", f"open error on file {inst.filename}", msg)

####

class StringConcat_Instance_Data:
    def __init__ (self):
        buffer1 = None
        buffer2 = None
        count = 0

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

def shell_out_instantiate (reg, owner, name, template_data):
    name_with_id = gensym ("shell_out")
    cmd = template_data.split ()
    return make_leaf (name_with_id, owner, cmd, shell_out_handler)

def shell_out_handler (eh, msg):
    cmd = eh.instance_data
    s = msg.datum.srepr ()
    ret = subprocess.run (cmd, capture_output=True, input=s, encoding='utf-8')
    if not (ret.returncode == 0):
        if ret.stderr != None:
            send_string (eh, "✗", ret.stderr, msg)
        else:
            send_string (eh, "✗", "error in shell_out {ret.returncode}", msg)
    else:
        send_string (eh, "", ret.stdout, msg)

####

def string_make_persistent (s):
    return s
def string_clone (s):
    return s
