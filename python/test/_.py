counter = 0

def gensym (s):
    global counter
    counter += 1
    name_with_id = f"{s}◦{counter}"
    return name_with_id

class Datum:
  def __init__(self):
    self.data = none
    self.clone = none
    self.reclaim = none
    self.srepr = none
    self.kind = none
    self.raw = none

def new_datum_string (s):
    d = Datum ()
    d.data = s
    d.clone = clone_datum_string
    d.reclaim = reclaim_datum_string    
    d.srepr = srepr_datum_string    
    d.raw = raw_datum_string    
    d.kind = "string"
    return d

def clone_datum_string (src):
  d = Datum ()
  d = src
  return d

def reclaim_datum_string (src):
  pass

def srepr_datum_string (d):
  return d.srepr ()

def raw_datum_string (d):
  return d.data



def new_datum_bang ():
    p = Datum ()
    p.data = true
    p.clone = clone_datum_bang
    p.reclaim = reclaim_datum_bang
    p.srepr = srepr_datum_bang    
    p.raw = raw_datum_bang    
    p.kind = "bang"
    return p

def clone_datum_bang (src):      
    return new_datum_bang ()


def reclaim_datum_bang (src):      
    pass

def srepr_datum_bang (src):      
    return "!"

def raw_datum_bang (src):      
    return "!"



def new_datum_tick ():      
    p = new_datum_bang ()
    p.kind = "tick"
    p.clone = new_datum_tick
    p.raw = raw_datum_tick
    return p


def srepr_datum_tick (src):      
    return "."


def raw_datum_tick (src):      
    return "."


def new_datum_bytes (b):      
    p = Datum ()
    p.data = b.clone ()
    p.clone = clone_datum_bytes
    p.reclaim = reclaim_datum_bytes
    p.srepr = srepr_datum_v
    p.raw = raw_datum_bytes
    p.kind = "bytes"
    return p


def clone_datum_bytes (src):      
    p = Datum ()
    p = src
    p.data = src.clone ()
    return p


def reclaim_datum_bytes (src):      
    pass


def srepr_datum_v (src):      
    return src.asString ()


def raw_datum_bytes (src):      
    return src.data



def new_datum_handle (h):
    p = Datum ()
    p.data = h
    p.clone = clone_handle
    p.reclaim = reclaim_handle
    p.srepr = srepr_datum_v
    p.raw = raw_datum_handle
    p.kind = "handle"
    return p

def clone_handle (src):      
    p = Datum ()
    p = src
    return p


def reclaim_handle (src):      
    pass


def raw_datum_handle (src):      
    return src

def new_datum_int (i):      
    p = Datum ()
    p.data = i
    p.clone = clone_int
    p.reclaim = reclaim_int
    p.srepr = srepr_datum_v
    p.raw = raw_datum_int
    p.kind = "int"
    return p


def clone_int (src):      
    p = Datum ()
    p = src
    p.data = src.data
    return p


def reclaim_int (src):      
    pass


def raw_datum_int (src):      
    return src.data
# Message passed to a leaf component.
#
# `port` refers to the name of the incoming or outgoing port of this component.
# `datum` is the data attached to this message.
class Message:
    def _init_ (self, port, datum, cause):
        self.port = port
        self.datum = datum
        self.cause = cause

class Cause:
    def _init_ (self, who, message):
        # trail to help trace message provenance
        # each message is tagged with a Cause that describes who sent the message and what message
        # was handled by "who" in causing this message to be sent (since, the cause is a message,
        # cause also contains a message, and provenance can be traced recursively back
        # all the way back to the beginning of time)
        self.who = who
        self.message = message

def clone_port (s):
    return s.clone ()


# Utility for making a `Message`. Used to safely "seed" messages
# entering the very top of a network.

def make_message (port, datum, cause):
    p = port.clone ()
    m = Message ()
    m.port  = p
    m.datum = datum.clone ()
    m.cause = cause
    return m

# Clones a message. Primarily used internally for "fanning out" a message to multiple destinations.
def message_clone (message):
    m = Message ()
    m.port = port.clone ()
    m.datum = message.datum.clone ()
    m.cause = message.cause
    return m

# Frees a message.
def destroy_message (msg):
    pass

def destroy_datum (msg):
    pass

def destroy_port (msg):
    pass

def make_cause (eh, msg):
    # create a persistent Cause in the heap, return a pointer to it
    cause = Cause ()
    cause.who = eh
    cause.message = msg
    return cause

def container_instantiator (reg, owner, container_name, decl):
    container = make_container (container_name, owner)
    children = []
    children_by_id = {} # not strictly necessary, but, we can remove 1 runtime lookup by "compiling it out" here
    # collect children
    for child_decl in decl.children:
        child_instance = get_component_instance (reg, child_decl.name, container)
        children.append (child_instance)
        children_by_id [child_decl.id] = child_instance

    connectors = []
    for proto_conn in decl.connections:
        source_component = none
        target_component = none
        connector = Connector ()
        if proto_conn.dir == "down":
            # JSON: {'dir': 0, 'source': {'name': '', 'id': 0}, 'source_port': '', 'target': {'name': 'Echo', 'id': 12}, 'target_port': ''},
            connector.direction = "down"
            connector.sender = Sender ("", nil, proto_conn.port)
            target_component = children_by_id [proto_conn.target.id]
            if (target_component == none):
                load_error (f"internal error: .Down connection target internal error {proto_conn.target}")
            else:
                connector.receiver = Receiver (target_component.name, target_component.input, c.target_port, target_component)
        elif proto_conn.dir == "across":
            connector.direction = "across"
            source_component = child_id_map [proto_conn.source.id]
            target_component = child_id_map [proto_conn.target.id]
            if source_component == none:
                load_error (f"internal error: .Across connection source not ok {proto_conn.source}")
            else:
                connector.sender = Sender (source_component.name, source_component, c.source_port)
                if target_component == none:
                    load_error (f"internal error: .Across connection target not ok {proto_conn.target}")
                else:
                    connector.receiver = Receiver (target_component.name, target_component.input, c.target_port, target_component)
        elif proto_conn.dir == "up":
            connector.direction = "up"
            source_component = child_id_map[c.source.id]
            if source_component == none:
                print (f"internal error: .Up connection source not ok {proto_conn.source}")
            else:
                connector.sender = Sender (source_component.name, source_component, c.source_port)
                connector.receiver = Receiver ("", container.output, proto_conn.target_port, nil)
        elif proto_conn.dir == "through":
            connector.direction = "through"
            connector.sender = Sender ("", nil, proto_conn.source_port)
            connector.receiver = Receiver ("", container.output, proto_conn.target_port, nil)
            source_component = container
            target_component = container
            
        if (source_component != none) and (target_component != none):
            connectors.append (connector)
        container.connections = connectors
        return container
class Component_Registry:
    def _init_ (self):
        self.templates = {}

class Template:
    def _init_ (self, name="", template_data=none, instantiator=none):
        pass
        
def read_and_convert_json_file (filename):
    try:
        with open(filename, 'r') as file:
            json_data = file.read()
            routings = json.loads(json_data)
            return routings
    except FileNotFoundError:
        print("File not found:", filename)
        return None
    except json.JSONDecodeError as e:
        print("Error decoding JSON in file:", e)
        return None

def json2internal (container_xml):
    fname = os.path.basename (container_xml)
    routings = read_and_convert_json_file (fname)
    return routings

def delete_decls (d):
    pass

def make_component_registry ():
    return Component_Registry ()

def register_component (reg, template):
    name = mangle_name (template.name)
    if name in reg.templates:
        load_error (f"Component {template.name} already declared")
    reg.templates[name] = template
    return reg

def register_multiple_components (reg, templates):
    for template in templates:
        register_component (reg, template)

def get_component_instance (reg, full_name, owner):
    template_name = parse_name (full_name)
    template = reg.templates[template_name]
    if (template == none):
        load_error (f"Registry Error: Can't find component {template_name} (does it need to be declared in components_to_include_in_project?")
        return none
    else:
        instance_name = f"{owner.name}.{template_name}"
        instance = template.instantiate (reg, owner, component_name, template.decl)
        instance.depth = calculate_depth (instance)
        return instance

def calculate_depth (eh):
    if eh.owner == none:
        return 0
    else:
        return 1 + calculate_depth (eh.owner)
    
def dump_registry (reg):
    print ()
    print ("*** PALETTE ***")
    for c in reg.templates:
        print (c.name)
    print ("***************")
    print ()

def print_stats (reg):
    print (f"registry statistics: {reg.stats}")

def mangle_name (s):
    # trim name to remove code from Container component names - deferred until later (or never)
    return s

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
import sys

counter = 0
def gensym (s):      
    global counter
    counter += 1
    name_with_id = f"{s}◦{counter}"
    return name_with_id


def string_constant (str):      
    quoted_name = f"'{str}'"
    return Template (name = quoted_name, instantiator = literal_instantiate)


####

def probe_instantiate (name, owner):      
    name_with_id = gensym ("?")
    return make_leaf (name=name_with_id, owner=owner, instance_data=nil, handler=probe_handler)

def probeA_instantiate (name, owner):      
    name_with_id = gensym ("?A")
    return make_leaf (name=name_with_id, owner=owner, instance_data=nil, handler=probe_handler)

def probeB_instantiate (name, owner):      
    name_with_id = gensym("?B")
    return make_leaf (name=name_with_id, owner=owner, instance_data=nil, handler=probe_handler)

def probeC_instantiate (name, owner):      
    name_with_id = gensym("?C")
    return make_leaf (name=name_with_id, owner=owner, instance_data=nil, handler=probe_handler)

def probe_handler (eh, msg):
    s = msg.datum.srepr ()
    print (f"... probe {eh.name}: {s}", file=sys.stderr)

    
def trash_instantiate (name, owner):      
    name_with_id = gensym ("trash")
    return zd.make_leaf (name=name_with_id, ownder=owner, instance_data=nil, handle=trash_handler)
def trash_handler (eh, msg):
    # to appease dumped-on-floor checker
    pass


####
def literal_instantiate (instance_name, owner):      
    name = re.sub (r"^.*'", "", instance_name)  # strip parent names from front
    quoted = re.sub ("<br>", "\n", name) # replace HTML newlines with real newlines
    name_with_id = gensym (quoted)
    pstr = string_make_persistent (quoted)
    return zmake_leaf (name=name_with_id, owner=owner, instance_data=pstr, handle=literal_handler)


def literal_handler (eh, msg):      
    send_string (eh, "⍺", eh.instance_data, msg)


####

class TwoMessages:
    def _init_ (self, first=None, second=None):
        pass

# Deracer_States :: enum { idle, waitingForFirst, waitingForSecond }

class Deracer_Instance_Data:
    def _init_ (self, state="idle", buffer=[]):
        pass

def reclaim_Buffers_from_heap (inst):      
    pass

def deracer_instantiate (name, owner):      
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
        fmt.assertf (false, "bad state for deracer %v\n", eh.state)
    



####

def low_level_read_text_file_instantiate (name, owner):      
    name_with_id = gensym("Low Level Read Text File")
    return make_leaf (name_with_id, owner, nil, low_level_read_text_file_handler)


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
def ensure_string_datum_instantiate (name, owner):      
    name_with_id = gensym("Ensure String Datum")
    return make_leaf (name_with_id, owner, nil, ensure_string_datum_handler)


def ensure_string_datum_handler (eh, msg):      
    if isinstance (msg.datum, str):
        forward (eh, "", msg)
    else:
        emsg = f"*** ensure: type error (expected a string datum) but got {msg.datum}"
        send_string (eh, "✗", emsg, msg)
    


####

class Syncfilewrite_Data:
    def _init_ (self):
        filename = ""

# temp copy for bootstrap, sends "done" (error during bootstrap if not wired)

def syncfilewrite_instantiate (name, owner):      
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
    def _init_ (self):
        buffer1 = None
        buffer2 = None
        count = 0

def stringconcat_instantiate (name, owner):      
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



def string_make_persistent (s):
    return s
def string_clone (s):
    return s
import sys

# usage: app arg main diagram_filename1 diagram_filename2 ...
def parse_command_line_args ():
    # return a 3-element array [arg, main_container_name, [diagram_names]]
    if (len (sys.argv) < (3+1)):
        load_error ("usage: app <arg> <main tab name> <diagram file name 1> ...")
        return None
    else:
        arg = sys.argv [1]
        main_container_name = sys.argv [2]
        diagram_source_files = sys.argv [3:]
        return [arg, main_container_name, diagram_source_files]

def initialize_component_palette (diagram_source_files, project_specific_components_subroutine):
    reg = make_component_registry ()
    for diagram_source in diagram_source_files:
        collect_process_leaves (reg, diagram_source)
        all_containers_within_single_file = json2internal (diagram_source)
        for container in all_containers_within_single_file:
            register_component (reg, Template (name=container.name , template_data=container, instantiator=container_instantiator))
    initialize_stock_components (reg)
    project_specific_components (reg) # add user specified components (probably only leaves)
    return reg


def print_error_maybe (main_container):
    error_port = "✗"
    err = fetch_first_output (main_container, error_port)
    if found and (0 < len (trimws (err))):
        print ("--- !!! ERRORS !!! ---")
        print_specific_output (main_container, error_port, false)


# debugging helpers

def dump_outputs (main_container):
    print ()
    print ("--- Outputs ---")
    print_output_list (main_container)

def dump_hierarchy (main_container):
    print ()
    print ("--- Hierarchy ---")
    print (build_hierarchy (main_container))

def build_hierarchy (c):
    s = ""
    for child in c.children:
        s = f"{s}{build_hierarchy (child)}"
    return f"\n({c.name}{s})"

#
def trimws (s):
    # remove whitespace from front and back of string
    return s.strip ()

def clone_string (s):
    return s

load_errors = false
runtime_errors = false

def load_error (s):
    global load_errors
    print (s)
    load_errors = true

def runtime_error (s):
    global runtime_errors
    print (s)
    runtime_errors = true

    
def fakepipename_instantiate (name, owner):
    instance_name = gensym ("fakepipe")
    return make_leaf (instance_name, owner, nil, fakepipename_handler)

rand = 0
def fakepipename_handler (eh, msg):
    global rand
    rand += 1 # not very random, but good enough - 'rand' must be unique within a single run
    send_string (eh, "", f"/tmp/fakepipe{rand}", msg)

# all of the the built-in leaves are listed here
# future: refactor this such that programmers can pick and choose which (lumps of) builtins are used in a specific project

def initialize_stock_components (reg):
    register_component (reg, Template ( name = "1then2", instantiate = deracer_instantiate)
    register_component (reg, Template ( name = "?", instantiate = probe_instantiate)
    register_component (reg, Template ( name = "?A", instantiate = probeA_instantiate)
    register_component (reg, Template ( name = "?B", instantiate = probeB_instantiate)
    register_component (reg, Template ( name = "?C", instantiate = probeC_instantiate)
    register_component (reg, Template ( name = "trash", instantiate = trash_instantiate)

    register_component (reg, Template ( name = "Low Level Read Text File", instantiate = low_level_read_text_file_instantiate)
    register_component (reg, Template ( name = "Read Text From FD", instantiate = read_text_from_fd_instantiate)
    register_component (reg, Template ( name = "Open Text File", instantiate = open_text_file_instantiate)
    register_component (reg, Template ( name = "Ensure String Datum", instantiate = ensure_string_datum_instantiate)

    register_component (reg, Template ( name = "syncfilewrite", instantiate = syncfilewrite_instantiate)
    register_component (reg, Template ( name = "Bang", instantiate = bang_instantiate)
    register_component (reg, Template ( name = "stringconcat", instantiate = stringconcat_instantiate)
    // for fakepipe
    register_component (reg, Template ( name = "fakepipename", instantiate = fakepipename_instantiate)
    // for transpiler (ohmjs)
    register_component (reg, Template ( name = "OhmJS", instantiate = ohmjs_instantiate)
    register_component (reg, string_constant ("RWR"))
    register_component (reg, string_constant ("0d/odin/std/rwr.ohm"))
    register_component (reg, string_constant ("0d/odin/std/rwr.sem.js"))
# run prints only the output on port "output", whereas run_demo prints all outputs
def run (pregistry, arg, main_container_name, diagram_source_files, injectfn):
    # get entrypoint container
    main_container = get_component_instance(pregistry, main_container_name, owner=nil)
    if None == main_container:
        load_error (f"Couldn't find container with page name {main_container_name} in files {diagram_source_files} (check tab names, or disable compression?)")
    injectfn (arg, main_container)
    print_error_maybe (main_container)
    print_output (main_container)

def run_all_outputs (pregistry, arg, main_container_name, diagram_source_files, injectfn):
    # get entrypoint container
    main_container = get_component_instance(pregistry, main_container_name, owner=nil)
    if None == main_container:
        load_error (f"Couldn't find container with page name {main_container_name} in files {diagram_source_files} (check tab names, or disable compression?)")
    injectfn (arg, main_container)
    print_error_maybe (main_container)
    dump_outputs (main_container)

def run_demo (pregistry, arg, main_container_name, diagram_source_files, injectfn):
    # get entrypoint container
    main_container = get_component_instance(pregistry, main_container_name, owner=nil)
    if None == main_container:
        load_error (f"Couldn't find container with page name {main_container_name} in files {diagram_source_files} (check tab names, or disable compression?)")
    injectfn (arg, main_container)
    dump_outputs (main_container)
    print ("--- done ---")

def run_demo_debug (pregistry, arg, main_container_name, diagram_source_files, injectfn):
    # get entrypoint container
    main_container = get_component_instance(pregistry, main_container_name, owner=nil)
    if None == main_container:
        load_error (f"Couldn't find container with page name {main_container_name} in files {diagram_source_files} (check tab names, or disable compression?)")
    dump_hierarchy (main_controller)
    injectfn (arg, main_container)
    dump_outputs (main_container)
    print ("--- done ---")


def main proc():
    arg_array = parse_command_line_args ()
    arg = arg_array [0]
    main_container_name = arg_array [1]
    diagram_names = arg_array [2]
    palette = initialize_component_palette (diagram_names, components_to_include_in_project)
    run_demo (palette, arg, main_container_name, diagram_names, start_function)

def start_function (arg, main_container):
    arg = new_datum_string (arg)
    msg = make_message("", arg, make_cause (main_container, nil) )
    main_container.handler(main_container, msg)


def components_to_include_in_project (reg):
    register_component (reg, Template { name = "Echo", instantiate = echo })    


def echo_handler (eh, msg):
	send_string (eh, "", msg.datum.repr (msg.datum), msg)

def echo (name, owner):
    name_with_id = std.gensym ("Echo")
    return make_leaf (name_with_id, owner, nil, echo-handler)
