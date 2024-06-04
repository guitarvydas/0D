counter = 0

def gensym (s):
    global counter
    name_with_id = f"{s}{subscripted_digit (counter)}"
    counter += 1
    return name_with_id

def subscripted_digit (n):
    if n == 0:
        return "₀"
    elif n == 1:
        return "₁"
    elif n == 2:
        return "₂"
    elif n == 3:
        return "₃"
    elif n == 4:
        return "₄"
    elif n == 5:
        return "₅"
    elif n == 6:
        return "₆"
    elif n == 7:
        return "₇"
    elif n == 8:
        return "₈"
    elif n == 9:
        return "₉"
    else:
        return f"₊{n}"
    
class Datum:
  def __init__(self):
    self.data = None
    self.clone = None
    self.reclaim = None
    self.srepr = None
    self.kind = None
    self.raw = None

def new_datum_string (s):
    d = Datum ()
    d.data = s
    d.clone = lambda : clone_datum_string (d)
    d.reclaim = lambda : reclaim_datum_string (d)    
    d.srepr = lambda : srepr_datum_string (d)
    d.raw = lambda : raw_datum_string (d)    
    d.kind = lambda : "string"
    return d

def clone_datum_string (d):
  d = new_datum_string (d.data)
  return d

def reclaim_datum_string (src):
  pass

def srepr_datum_string (d):
  return d.data

def raw_datum_string (d):
  return bytearray (d.data,'UTF-8')



def new_datum_bang ():
    p = Datum ()
    p.data = True
    p.clone = lambda : clone_datum_bang (p)
    p.reclaim = lambda : reclaim_datum_bang (p)
    p.srepr = lambda : srepr_datum_bang ()
    p.raw = lambda : raw_datum_bang ()    
    p.kind = lambda : "bang"
    return p

def clone_datum_bang (d):
    return new_datum_bang ()


def reclaim_datum_bang (d):
    pass

def srepr_datum_bang ():      
    return "!"

def raw_datum_bang ():
    return []



def new_datum_tick ():      
    p = new_datum_bang ()
    p.kind = lambda : "tick"
    p.clone = lambda : new_datum_tick ()
    p.srepr = lambda : srepr_datum_tick ()
    p.raw = lambda : raw_datum_tick ()
    return p


def srepr_datum_tick ():
    return "."


def raw_datum_tick ():      
    return []


def new_datum_bytes (b):      
    p = Datum ()
    p.data = b[:]
    p.clone = clone_datum_bytes
    p.reclaim = lambda : reclaim_datum_bytes (p)
    p.srepr = lambda : srepr_datum_bytes (b)
    p.raw = lambda : raw_datum_bytes (b)
    p.kind = lambda : "bytes"
    return p


def clone_datum_bytes (src):      
    p = Datum ()
    p = src
    p.data = src.clone ()
    return p


def reclaim_datum_bytes (src):      
    pass


def srepr_datum_bytes (d):
    return d.data.decode ('utf-8')


def raw_datum_bytes (d):
    return d.data



def new_datum_handle (h):
    return new_datum_int (h)

def new_datum_int (i):      
    p = Datum ()
    p.data = i
    p.clone = lambda : clone_int (i)
    p.reclaim = lambda : reclaim_int (i)
    p.srepr = lambda: srepr_datum_int (i)
    p.raw = lambda : raw_datum_int (i)
    p.kind = lambda : "int"
    return p


def clone_int (i):      
    p = Datum ()
    p = new_datum_int (i)
    return p


def reclaim_int (src):      
    pass

def srepr_datum_int (i):
  return str (i)

def raw_datum_int (i):      
    return i
# Message passed to a leaf component.
#
# `port` refers to the name of the incoming or outgoing port of this component.
# `datum` is the data attached to this message.
class Message:
    def __init__ (self, port, datum):
        self.port = port
        self.datum = datum

def clone_port (s):
    return clone_string (s)


# Utility for making a `Message`. Used to safely "seed" messages
# entering the very top of a network.

def make_message (port, datum):
    p = clone_string (port)
    m = Message (port=p, datum=datum.clone ())
    return m

# Clones a message. Primarily used internally for "fanning out" a message to multiple destinations.
def message_clone (message):
    m = Message (port=clone_port (message.port), datum=message.datum.clone ())
    return m

# Frees a message.
def destroy_message (msg):
    # during debug, don't destroy any message, since we want to trace messages, thus, we need to persist ancestor messages
    pass

def destroy_datum (msg):
    pass

def destroy_port (msg):
    pass

#####

def format_message (m):
    if m == None:
        return "None"
    else:
        return f'⟪“{m.port}”⦂“{m.datum.srepr ()}”⟫'

# dynamic routing descriptors

drInject = "inject"
drSend = "send"
drInOut = "inout"
drForward = "forward"
drDown = "down"
drUp = "up"
drAcross = "across"
drThrough = "through"

# See "class free programming" starting at 45:01 of https://www.youtube.com/watch?v=XFTOG895C7c

def make_Routing_Descriptor (action=None, component=None, port=None, message=None):
    return {
        "action": action,
        "component": component,
        "port": port,
        "message": message
        }



####
def make_Send_Descriptor (component=None, port=None, message=None, cause_port=None, cause_message=None):
    rdesc = make_Routing_Descriptor (action=drSend, component=component, port=port, message=message)
    return {
        "action": drSend,
        "component": rdesc ["component"],
        "port": rdesc ["port"],
        "message": rdesc ["message"],
        "cause_port": cause_port,
        "cause_message": cause_message,
        "fmt": fmt_send
        }

def log_send (sender, sender_port, msg, cause_msg):
    send_desc = make_Send_Descriptor (component=sender, port=sender_port, message=msg, cause_port=cause_msg.port, cause_message=cause_msg)
    append_routing_descriptor (container=sender.owner, desc=send_desc)

def log_send_string (sender, sender_port, msg, cause_msg):
    send_desc = make_Send_Descriptor (sender, sender_port, msg, cause_msg.port, cause_msg)
    append_routing_descriptor (container=sender.owner, desc=send_desc)



def fmt_send (desc, indent):
    return ""
    #return f'\n{indent}⋯ {desc ["component"].name}.“{desc ["cause_port"]}” ∴ {desc ["component"].name}.“{desc ["port"]}” {format_message (desc ["message"])}'
def fmt_send_string (desc, indent):
    return fmt_send (desc, indent)


####
def make_Forward_Descriptor (component=None, port=None, message=None, cause_port=None, cause_message=None):
    rdesc = make_Routing_Descriptor (action=drSend, component=component, port=port, message=message)
    fmt_forward = lambda desc : ''
    return {
        "action": drForward,
        "component": rdesc ["component"],
        "port": rdesc ["port"],
        "message": rdesc ["message"],
        "cause_port": cause_port,
        "cause_message": cause_message,
        "fmt": fmt_forward
        }

def log_forward (sender, sender_port, msg, cause_msg):
    pass # when needed, it is too frequent to bother logging

def fmt_forward (desc):
    print (f"*** Error fmt_forward {desc}")
    quit ()

####
def make_Inject_Descriptor (receiver=None, port=None, message=None):
    rdesc = make_Routing_Descriptor (action=drInject, component=receiver, port=port, message=message)
    return {
        "action": drInject,
        "component": rdesc ["component"],
        "port": rdesc ["port"],
        "message": rdesc ["message"],
        "fmt" : fmt_inject
        }

def log_inject (receiver, port, msg):
    inject_desc = make_Inject_Descriptor (receiver=receiver, port=port, message=msg)
    append_routing_descriptor (container=receiver, desc=inject_desc)

def fmt_inject (desc, indent):
    return f'\n{indent}⟹  {desc ["component"].name}.“{desc ["port"]}” {format_message (desc ["message"])}'


####
def make_Down_Descriptor (container=None, source_port=None, source_message=None, target=None, target_port=None, target_message=None):
    return {
        "action": drDown,
        "container": container,
        "source_port": source_port,
        "source_message": source_message,
        "target": target,
        "target_port": target_port,
        "target_message": target_message,
        "fmt" : fmt_down
        }

def log_down (container=None, source_port=None, source_message=None, target=None, target_port=None, target_message=None):
    rdesc = make_Down_Descriptor (container, source_port, source_message, target, target_port, target_message)
    append_routing_descriptor (container, rdesc)

def fmt_down (desc, indent):
    return f'\n{indent}↓ {desc ["container"].name}.“{desc ["source_port"]}” ➔ {desc ["target"].name}.“{desc ["target_port"]}” {format_message (desc ["target_message"])}'


####
def make_Up_Descriptor (source=None, source_port=None, source_message=None, container=None, container_port=None, container_message=None):
    return {
        "action": drUp,
        "source": source,
        "source_port": source_port,
        "source_message": source_message,
        "container": container,
        "container_port": container_port,
        "container_message": container_message,
        "fmt" : fmt_up
        }

def log_up (source=None, source_port=None, source_message=None, container=None, target_port=None, target_message=None):
    rdesc = make_Up_Descriptor (source, source_port, source_message, container, target_port, target_message)
    append_routing_descriptor (container, rdesc)

def fmt_up (desc, indent):
    return f'\n{indent}↑ {desc ["source"].name}.“{desc ["source_port"]}” ➔ {desc ["container"].name}.“{desc ["container_port"]}” {format_message (desc ["container_message"])}'


####
def make_Across_Descriptor (container=None, source=None, source_port=None, source_message=None, target=None, target_port=None, target_message=None):
    return {
        "action": drAcross,
        "container": container,
        "source": source,
        "source_port": source_port,
        "source_message": source_message,
        "target": target,
        "target_port": target_port,
        "target_message": target_message,
        "fmt" : fmt_across
        }

def log_across (container=None, source=None, source_port=None, source_message=None, target=None, target_port=None, target_message=None):
    rdesc = make_Across_Descriptor (container, source, source_port, source_message, target, target_port, target_message)
    append_routing_descriptor (container, rdesc)

def fmt_across (desc, indent):
    return f'\n{indent}→ {desc["source"].name}.“{desc ["source_port"]}” ➔ {desc ["target"].name}.“{desc ["target_port"]}”  {format_message (desc ["target_message"])}'


####
def make_Through_Descriptor (container=None, source_port=None, source_message=None, target_port=None, message=None):
    return {
        "action": drThrough,
        "container": container,
        "source_port": source_port,
        "source_message": source_message,
        "target_port": target_port,
        "message": message,
        "fmt" : fmt_through
        }

def log_through (container=None, source_port=None, source_message=None, target_port=None, message=None):
    rdesc = make_Through_Descriptor (container, source_port, source_message, target_port, message)
    append_routing_descriptor (container, rdesc)

def fmt_through (desc, indent):
    return f'\n{indent}⇶ {desc  ["container"].name}.“{desc ["source_port"]}” ➔ {desc ["container"].name}.“{desc ["target_port"]}” {format_message (desc ["message"])}'

####
def make_InOut_Descriptor (container=None, component=None, in_message=None, out_port=None, out_message=None):
    return {
        "action": drInOut,
        "container": container,
        "component": component,
        "in_message": in_message,
        "out_message": out_message,
        "fmt" : fmt_inout
        }

def log_inout (container=None, component=None, in_message=None):
    if component.outq.empty ():
        log_inout_no_output (container=container, component=component, in_message=in_message)
    else:
        log_inout_recursively (container=container, component=component, in_message=in_message, out_messages=list (component.outq.queue))

def log_inout_no_output (container=None, component=None, in_message=None):
    rdesc = make_InOut_Descriptor (container=container, component=component, in_message=in_message)
    append_routing_descriptor (container, rdesc)

def log_inout_single (container=None, component=None, in_message=None, out_message=None):
    rdesc = make_InOut_Descriptor (container=container, component=component, in_message=in_message, out_message=out_message)
    append_routing_descriptor (container, rdesc)

def log_inout_recursively (container=None, component=None, in_message=None, out_messages=[]):
    if [] == out_messages:
        pass
    else:
        m = out_messages [0]
        rest = out_messages [1:]
        log_inout_single (container=container, component=component, in_message=in_message, out_message=m)
        log_inout_recursively (container=container, component=component, in_message=in_message, out_messages=rest)

def fmt_inout (desc, indent):
    outm = desc ["out_message"]
    if None == outm:
        return f'\n{indent}  ⊥'
    else:
        return f'\n{indent}  ∴ {desc ["component"].name} {format_message (outm)}'

def log_tick (container=None, component=None, in_message=None):
    pass

        
####
def routing_trace_all (container):
    indent = ""
    lis = list (container.routings.queue)
    return recursive_routing_trace (container, lis, indent)

def recursive_routing_trace (container, lis, indent):
    if [] == lis:
        return ''
    else:
        desc = first (lis)
        formatted = desc ["fmt"] (desc, indent)
        return formatted + recursive_routing_trace (container, rest (lis), indent + '  ')

####
def first (arr): # called "car" in Lisp
    return (arr [0])

def rest (arr): # called "cdr" in Lisp
    return (arr [1:])



enumDown = 0
enumAcross = 1
enumUp = 2
enumThrough = 3

def container_instantiator (reg, owner, container_name, desc):
    global enumDown, enumUp, enumAcross, enumThrough
    container = make_container (container_name, owner)
    children = []
    children_by_id = {} # not strictly necessary, but, we can remove 1 runtime lookup by "compiling it out" here
    # collect children
    for child_desc in desc ["children"]:
        child_instance = get_component_instance (reg, child_desc ["name"], container)
        children.append (child_instance)
        children_by_id [child_desc ["id"]] = child_instance
    container.children = children
    self = container
    
    connectors = []
    for proto_conn in desc ["connections"]:
        source_component = None
        target_component = None
        connector = Connector ()
        if proto_conn ['dir'] == enumDown:
            # JSON: {'dir': 0, 'source': {'name': '', 'id': 0}, 'source_port': '', 'target': {'name': 'Echo', 'id': 12}, 'target_port': ''},
            connector.direction = "down"
            connector.sender = Sender (self.name, self, proto_conn ['source_port'])
            target_component = children_by_id [proto_conn ['target'] ['id']]
            if (target_component == None):
                load_error (f"internal error: .Down connection target internal error {proto_conn['target']}")
            else:
                connector.receiver = Receiver (target_component.name, target_component.inq, proto_conn ['target_port'], target_component)
                connectors.append (connector)
        elif proto_conn ["dir"] == enumAcross:
            connector.direction = "across"
            source_component = children_by_id [proto_conn ['source']['id']]
            target_component = children_by_id [proto_conn ['target'] ['id']]
            if source_component == None:
                load_error (f"internal error: .Across connection source not ok {proto_conn ['source']}")
            else:
                connector.sender = Sender (source_component.name, source_component, proto_conn ['source_port'])
                if target_component == None:
                    load_error (f"internal error: .Across connection target not ok {proto_conn.target}")
                else:
                    connector.receiver = Receiver (target_component.name, target_component.inq, proto_conn ['target_port'], target_component)
                    connectors.append (connector)
        elif proto_conn ['dir'] == enumUp:
            connector.direction = "up"
            source_component = children_by_id [proto_conn ['source']['id']]
            if source_component == None:
                print (f"internal error: .Up connection source not ok {proto_conn ['source']}")
            else:
                connector.sender = Sender (source_component.name, source_component, proto_conn ['source_port'])
                connector.receiver = Receiver (self.name, container.outq, proto_conn ['target_port'], self)
                connectors.append (connector)
        elif proto_conn ['dir'] == enumThrough:
            connector.direction = "through"
            connector.sender = Sender (self.name, self, proto_conn ['source_port'])
            connector.receiver = Receiver (self.name, container.outq, proto_conn ['target_port'], self)
            connectors.append (connector)
            
    container.connections = connectors
    return container

# The default handler for container components.
def container_handler (container, message):
    route (container=container, from_component=container, message=message) # references to 'self' are replaced by the container during instantiation
    while any_child_ready (container):
        step_children (container, message)

# Frees the given container and associated data.
def destroy_container (eh):      
    pass

def fifo_is_empty (fifo):      
    return fifo.empty ()

# Routing connection for a container component. The `direction` field has
# no affect on the default message routing system - it is there for debugging
# purposes, or for reading by other tools.
class Connector:
    def __init__ (self):
        self.direction = None # down, across, up, through
        self.sender = None
        self.receiver = None

# `Sender` is used to "pattern match" which `Receiver` a message should go to,
# based on component ID (pointer) and port name.
class Sender:
    def __init__ (self, name, component, port):
        self.name = name
        self.component = component # from
        self.port = port # from's port

# `Receiver` is a handle to a destination queue, and a `port` name to assign
# to incoming messages to this queue.
class Receiver:
    def __init__ (self, name, queue, port, component):
        self.name = name
        self.queue = queue # queue (input | output) of receiver
        self.port = port # destination port
        self.component = component # to (for bootstrap debug)

# Checks if two senders match, by pointer equality and port name matching.
def sender_eq (s1, s2):
    same_components = (s1.component == s2.component)
    same_ports = (s1.port == s2.port)
    return same_components and same_ports

# Delivers the given message to the receiver of this connector.
def deposit (parent, conn, message):
    new_message = make_message (port=conn.receiver.port, datum=message.datum)
    log_connection (parent, conn, new_message)
    push_message (parent, conn.receiver.component, conn.receiver.queue, new_message)


def force_tick (parent, eh):
    tick_msg = make_message (".", new_datum_tick ())
    push_message (parent, eh, eh.inq, tick_msg)
    return tick_msg


def push_message (parent, receiver, inq, m):      
    inq.put (m)
    parent.visit_ordering.put (receiver)


def is_self (child, container):
    # in an earlier version "self" was denoted as None
    return child == container

def step_child (child, msg):
    before_state = child.state
    child.handler(child, msg)
    after_state = child.state
    return [before_state == "idle" and after_state != "idle", 
            before_state != "idle" and after_state != "idle",
            before_state != "idle" and after_state == "idle"]

def save_message (eh, msg):
    eh.saved_messages.put (msg)

def fetch_saved_message_and_clear (eh):
    return eh.saved_messages.get ()

def step_children (container, causingMessage):      
    container.state = "idle"
    for child in list (container.visit_ordering.queue):
        # child == container represents self, skip it
        if (not (is_self (child, container))):
            if (not (child.inq.empty ())):
                msg = child.inq.get ()
                [began_long_run, continued_long_run, ended_long_run] = step_child (child, msg)
                if began_long_run:
                    save_message (child, msg)
                elif continued_long_run:
                    pass
                elif ended_long_run:
                    log_inout (container=container, component=child, in_message=fetch_saved_message_and_clear (child))
                else:
                    log_inout (container=container, component=child, in_message=msg)
                destroy_message(msg)
            else:
                if (child.state != "idle"):
                    msg = force_tick (container, child)
                    child.handler(child, msg)
                    log_tick (container=container, component=child, in_message=msg)
                    destroy_message(msg)
            
            if (child.state == "active"):
                # if child remains active, then the container must remain active and must propagate "ticks" to child
                container.state = "active"
            
            while (not (child.outq.empty ())):
                msg = child.outq.get ()
                route(container, child, msg)
                destroy_message(msg)

def attempt_tick (parent, eh):
    if eh.state != "idle":
        force_tick (parent, eh)

def is_tick (msg):      
    return "tick" == msg.datum.kind ()

# Routes a single message to all matching destinations, according to
# the container's connection network.
def route (container, from_component, message):
    was_sent = False # for checking that output went somewhere (at least during bootstrap)
    if is_tick (message):
        for child in container.children:    
            attempt_tick (container, child, message)
        was_sent = True
    else:
        fromname = ""
        if (not (is_self (from_component, container))):
            fromname = from_component.name
        from_sender = Sender (name=fromname, component=from_component, port=message.port)
        
        for connector in container.connections:
            if sender_eq (from_sender, connector.sender):   
                deposit (container, connector, message)
                was_sent = True
    if not (was_sent): 
        print ("\n\n*** Error: ***")
        dump_possible_connections (container)
        print_routing_trace (container)
        print ("***")
        print (f"{container.name}: message '{message.port}' from {fromname} dropped on floor...")
        print ("***")
        exit ()

def dump_possible_connections (container):      
    print (f"*** possible connections for {container.name}:")
    for connector in container.connections:
        print (f"{connector.direction} ❲{connector.sender.name}❳.“{connector.sender.port}” -> ❲{connector.receiver.name}❳.“{connector.receiver.port}”")

def any_child_ready (container):
    for child in container.children:
        if child_is_ready(child):
            return True
    return False

def child_is_ready (eh):      
    return (not (eh.outq.empty ())) or (not (eh.inq.empty ())) or ( eh.state != "idle") or (any_child_ready (eh))

def print_routing_trace (eh):
    print (routing_trace_all (eh))

def append_routing_descriptor (container, desc):
    container.routings.put (desc)
    
####
def log_connection (container, connector, message):
    if "down" == connector.direction:
        log_down (container=container, source_port=connector.sender.port, target=connector.receiver.component, target_port=connector.receiver.port,
                  target_message=message)
    elif "up" == connector.direction:
        log_up (source=connector.sender.component, source_port=connector.sender.port, container=container, target_port=connector.receiver.port,
                  target_message=message)
    elif "across" == connector.direction:
        log_across (container=container,
                    source=connector.sender.component, source_port=connector.sender.port,
                    target=connector.receiver.component, target_port=connector.receiver.port, target_message=message)
    elif "through" == connector.direction:
        log_through (container=container, source_port=connector.sender.port, source_message=None,
                     target_port=connector.receiver.port, message=message)
    else:
        print (f"*** FATAL error: in log_connection /{connector.direction}/ /{message.port}/ /{message.datum.srepr ()}/")
        exit ()
        
####
def container_injector (container, message):
    log_inject (receiver=container, port=message.port, msg=message)
    container_handler (container, message)
import os
import json
import sys

class Component_Registry:
    def __init__ (self):
        self.templates = {}

class Template:
    def __init__ (self, name="", template_data=None, instantiator=None):
        self.name = name
        self.template_data = template_data
        self.instantiator = instantiator
        
def read_and_convert_json_file (filename):
    try:
        with open(filename, 'r') as file:
            json_data = file.read()
            routings = json.loads(json_data)
            return routings
    except FileNotFoundError:
        print (f"File not found: {filename}")
        return None
    except json.JSONDecodeError as e:
        print (f"Error decoding JSON in file: {e}")
        return None

def json2internal (container_xml):
    fname = os.path.basename (container_xml)
    routings = read_and_convert_json_file (fname)
    return routings

def delete_decls (d):
    pass

def make_component_registry ():
    return Component_Registry ()

def register_component (reg, template, ok_to_overwrite=False):
    name = mangle_name (template.name)
    if name in reg.templates and not ok_to_overwrite:
        load_error (f"Component {template.name} already declared")
    reg.templates[name] = template
    return reg

def register_multiple_components (reg, templates):
    for template in templates:
        register_component (reg, template)

def get_component_instance (reg, full_name, owner):
    template_name = mangle_name (full_name)
    if template_name in reg.templates:
        template = reg.templates[template_name]
        if (template == None):
            load_error (f"Registry Error: Can't find component {template_name} (does it need to be declared in components_to_include_in_project?")
            return None
        else:
            owner_name = ""
            instance_name = f"{template_name}"
            if None != owner:
                owner_name = owner.name
                instance_name = f"{owner_name}.{template_name}"
            else:
                instance_name = f"{template_name}"
            instance = template.instantiator (reg, owner, instance_name, template.template_data)
            instance.depth = calculate_depth (instance)
            return instance
    else:
            load_error (f"Registry Error: Can't find component {template_name} (does it need to be declared in components_to_include_in_project?")
            return None

def calculate_depth (eh):
    if eh.owner == None:
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

import subprocess

def generate_shell_components (reg, container_list):
    # [
    #     {'file': 'simple0d.drawio', 'name': 'main', 'children': [{'name': 'Echo', 'id': 5}], 'connections': [...]},
    #     {'file': 'simple0d.drawio', 'name': '...', 'children': [], 'connections': []}
    # ]
    if None != container_list:
        for diagram in container_list:
            # loop through every component in the diagram and look for names that start with "$"
            # {'file': 'simple0d.drawio', 'name': 'main', 'children': [{'name': 'Echo', 'id': 5}], 'connections': [...]},
            for child_descriptor in diagram ['children']:
                if first_char_is (child_descriptor ["name"], "$"):
                    name = child_descriptor ["name"]
                    cmd = name [1:].strip ()
                    generated_leaf = Template (name=name, instantiator=shell_out_instantiate, template_data=cmd)
                    register_component (reg, generated_leaf)
                elif first_char_is (child_descriptor ["name"], "'"):
                    name = child_descriptor ["name"]
                    s = name [1:]
                    generated_leaf = Template (name=name, instantiator=string_constant_instantiate, template_data=s)
                    register_component (reg, generated_leaf, ok_to_overwrite=True)

def first_char (s):
    return s[0]

def first_char_is (s, c):
    return c == first_char (s)
    
# this needs to be rewritten to use the low-level "shell_out" component, this can be done solely as a diagram without using python code here
# I'll keep it for now, during bootstrapping, since it mimics what is done in the Odin prototype - both need to be revamped
def run_command (eh, cmd, s):
    ret = subprocess.run (cmd, capture_output=True, input=s, encoding='utf-8')
    if  not (ret.returncode == 0):
        if ret.stderr != None:
            return ["", ret.stderr]
        else:
            return ["", f"error in shell_out {ret.returncode}"]
    else:
        return [ret.stdout, None]
    
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
    def __init__ (self):
        self.name = ""
        self.inq = queue.Queue ()
        self.outq = queue.Queue ()
        self.owner = None
        self.saved_messages = queue.LifoQueue () ## stack of saved message(s)
        self.inject = injector_NIY
        self.children = []
        self.visit_ordering = queue.Queue ()
        self.connections = []
        self.routings = queue.Queue ()
        self.handler = None
        self.instance_data = None
        self.state = "idle"
        # bootstrap debugging
        self.kind = None # enum { container, leaf, }
        self.trace = False # set 'True' if logging is enabled and if this component should be traced, (False means silence, no tracing for this component)
        self.depth = 0 # hierarchical depth of component, 0=top, 1=1st child of top, 2=1st child of 1st child of top, etc.

# Creates a component that acts as a container. It is the same as a `Eh` instance
# whose handler function is `container_handler`.
def make_container (name, owner):
    eh = Eh ()
    eh.name = name
    eh.owner = owner
    eh.handler = container_handler
    eh.inject = container_injector
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
    msg = make_message(port, datum)
    log_send (sender=eh, sender_port=port, msg=msg, cause_msg=causingMessage)
    put_output (eh, msg)


def send_string (eh, port, s, causingMessage):
    datum = new_datum_string (s)
    msg = make_message(port=port, datum=datum)
    log_send_string (sender=eh, sender_port=port, msg=msg, cause_msg=causingMessage)
    put_output (eh, msg)


def forward (eh, port, msg):
    fwdmsg = make_message(port, msg.datum)
    log_forward (sender=eh, sender_port=port, msg=msg, cause_msg=msg)
    put_output (eh, msg)

def inject (eh, msg):
    eh.inject (eh, msg)

# Returns a list of all output messages on a container.
# For testing / debugging purposes.
def output_list (eh):
    return eh.outq


# Utility for printing an array of messages.
def print_output_list (eh):
    for m in list (eh.outq.queue):
        print (format_message (m))

def spaces (n):
    s = ""
    for i in range (n):
        s = s + " "
    return s

def set_active (eh):      
    eh.state = "active"

def set_idle (eh):      
    eh.state = "idle"

# Utility for printing a specific output message.
def fetch_first_output (eh, port):
    for msg in list (eh.outq.queue):
        if (msg.port == port):
            return msg.datum
    return None

def print_specific_output (eh, port, stderr):
    datum = fetch_first_output (eh, port)
    if datum != None:
        if stderr:              # I don't remember why I found it useful to print to stderr during bootstrapping, so I've left it in...
            f = sys.stderr
        else:
            f = sys.stdout
        print (datum.srepr (), file=f)

def put_output (eh, msg):
    eh.outq.put (msg)
    
def injector_NIY (eh, msg):
    print (f'Injector not implemented for this component "{eh.name}" kind={eh.kind} port="{msg.port}"')
    exit ()
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
import sys

# usage: app ${_00_} ${_0D_} arg main diagram_filename1 diagram_filename2 ...
# where ${_00_} is the root directory for the project
# where ${_0D_} is the root directory for 0D (e.g. 0D/odin or 0D/python)

def parse_command_line_args ():
    # return a 5-element array [root_project, root_0D, arg, main_container_name, [diagram_names]]
    if (len (sys.argv) < (5+1)):
        load_error ("usage: ${_00_} ${_0D_} app <arg> <main tab name> <diagram file name 1> ...")
        return None
    else:
        root_project = sys.argv [1]
        root_0D = sys.argv [2]
        arg = sys.argv [3]
        main_container_name = sys.argv [4]
        diagram_source_files = sys.argv [5:]
        return [root_project, root_0D, arg, main_container_name, diagram_source_files]

def initialize_component_palette (root_project, root_0D, diagram_source_files, project_specific_components_subroutine):
    reg = make_component_registry ()
    for diagram_source in diagram_source_files:
        all_containers_within_single_file = json2internal (diagram_source)
        generate_shell_components (reg, all_containers_within_single_file)
        for container in all_containers_within_single_file:
            register_component (reg, Template (name=container ['name'] , template_data=container, instantiator=container_instantiator))
    initialize_stock_components (reg)
    project_specific_components_subroutine (root_project, root_0D, reg) # add user specified components (probably only leaves)
    return reg


def print_error_maybe (main_container):
    error_port = "✗"
    err = fetch_first_output (main_container, error_port)
    if (err != None) and (0 < len (trimws (err))):
        print ("--- !!! ERRORS !!! ---")
        print_specific_output (main_container, error_port, False)


# debugging helpers

def dump_outputs (main_container):
    print ()
    print ("--- Outputs ---")
    print_output_list (main_container)

def trace_outputs (main_container):
    print ()
    print ("--- Message Traces ---")
    print_routing_trace (main_container)

def dump_hierarchy (main_container):
    print ()
    print (f"--- Hierarchy ---{(build_hierarchy (main_container))}")

def build_hierarchy (c):
    s = ""
    for child in c.children:
        s = f"{s}{build_hierarchy (child)}"
    indent = ""
    for i in range (c.depth):
        indent = indent + "  "
    return f"\n{indent}({c.name}{s})"

def dump_connections (c):
    print ()
    print (f"--- connections ---")
    dump_possible_connections (c)
    for child in c.children:
        print ()
        dump_possible_connections (child)

#
def trimws (s):
    # remove whitespace from front and back of string
    return s.strip ()

def clone_string (s):
    return s

load_errors = False
runtime_errors = False

def load_error (s):
    global load_errors
    print (s)
    quit ()
    load_errors = True

def runtime_error (s):
    global runtime_errors
    print (s)
    quit ()
    runtime_errors = True

    
def fakepipename_instantiate (reg, owner, name, template_data):
    instance_name = gensym ("fakepipe")
    return make_leaf (instance_name, owner, None, fakepipename_handler)

rand = 0
def fakepipename_handler (eh, msg):
    global rand
    rand += 1 # not very random, but good enough - 'rand' must be unique within a single run
    send_string (eh, "", f"/tmp/fakepipe{rand}", msg)

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



# all of the the built-in leaves are listed here
# future: refactor this such that programmers can pick and choose which (lumps of) builtins are used in a specific project

def initialize_stock_components (reg):
    register_component (reg, Template ( name = "1then2", instantiator = deracer_instantiate))
    register_component (reg, Template ( name = "?", instantiator = probe_instantiate))
    register_component (reg, Template ( name = "?A", instantiator = probeA_instantiate))
    register_component (reg, Template ( name = "?B", instantiator = probeB_instantiate))
    register_component (reg, Template ( name = "?C", instantiator = probeC_instantiate))
    register_component (reg, Template ( name = "trash", instantiator = trash_instantiate))

    register_component (reg, Template ( name = "Low Level Read Text File", instantiator = low_level_read_text_file_instantiate))
    register_component (reg, Template ( name = "Ensure String Datum", instantiator = ensure_string_datum_instantiate))

    register_component (reg, Template ( name = "syncfilewrite", instantiator = syncfilewrite_instantiate))
    register_component (reg, Template ( name = "stringconcat", instantiator = stringconcat_instantiate))
    # for fakepipe
    register_component (reg, Template ( name = "fakepipename", instantiator = fakepipename_instantiate))
    # for transpiler (ohmjs)
    register_component (reg, Template ( name = "OhmJS", instantiator = ohmjs_instantiate))
    # register_component (reg, string_constant ("RWR"))
    # register_component (reg, string_constant ("0d/python/std/rwr.ohm"))
    # register_component (reg, string_constant ("0d/python/std/rwr.sem.js"))
# run prints only the output on port "output", whereas run_demo prints all outputs
def run (pregistry,  root_project, root_0D, arg, main_container_name, diagram_source_files, injectfn):
    set_environment (root_project, root_0D)
    # get entrypoint container
    main_container = get_component_instance(pregistry, main_container_name, owner=None)
    if None == main_container:
        load_error (f"Couldn't find container with page name {main_container_name} in files {diagram_source_files} (check tab names, or disable compression?)")
    if not load_errors:
        injectfn (root_project, root_0D, arg, main_container)
    print_error_maybe (main_container)
    dump_outputs (main_container)

def run_demo (pregistry, root_project, root_0D, arg, main_container_name, diagram_source_files, injectfn,
              show_hierarchy=True, show_connections=True, show_traces=True):
    set_environment (root_project, root_0D)
    # get entrypoint container
    main_container = get_component_instance(pregistry, main_container_name, owner=None)
    if None == main_container:
        load_error (f"Couldn't find container with page name {main_container_name} in files {diagram_source_files} (check tab names, or disable compression?)")
    if show_hierarchy:
        dump_hierarchy (main_container)
    if show_connections:
        dump_connections (main_container)
    if not load_errors:
        injectfn (root_project, root_0D, arg, main_container)
    dump_outputs (main_container)
    if show_traces:
        print ("--- routing traces ---")
        print (routing_trace_all (main_container))
    print ("--- done ---")

