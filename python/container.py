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
    
    connectors = []
    for proto_conn in desc ["connections"]:
        source_component = None
        target_component = None
        connector = Connector ()
        if proto_conn ['dir'] == enumDown:
            # JSON: {'dir': 0, 'source': {'name': '', 'id': 0}, 'source_port': '', 'target': {'name': 'Echo', 'id': 12}, 'target_port': ''},
            connector.direction = "down"
            connector.sender = Sender ("", None, proto_conn ['source_port'])
            target_component = children_by_id [proto_conn ['target'] ['id']]
            if (target_component == None):
                load_error (f"internal error: .Down connection target internal error {proto_conn['target']}")
            else:
                connector.receiver = Receiver (target_component.name, target_component.inq, proto_conn ['source_port'], target_component)
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
                connector.receiver = Receiver ("", container.outq, proto_conn ['target_port'], None)
                connectors.append (connector)
        elif proto_conn ['dir'] == enumThrough:
            connector.direction = "through"
            connector.sender = Sender ("", None, proto_conn ['source_port'])
            connector.receiver = Receiver ("", container.outq, proto_conn ['target_port'], None)
            connectors.append (connector)
            
    container.connections = connectors
    return container

# The default handler for container components.
def container_handler (eh,message):      
    route (eh, None, message)
    if any_child_ready (eh):
        step_children (eh, message)

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
def deposit (parent, c, message):      
    new_message = message_clone(message)
    new_message.port = c.receiver.port
    push_message (parent, c.receiver.component, c.receiver.queue, new_message)


def force_tick (parent, eh, causingMessage):      
    tick_msg = make_message (".", new_datum_tick (), make_cause (eh, causingMessage))
    push_message (parent, eh, eh.inq, tick_msg)
    return tick_msg


def push_message (parent, receiver, inq, m):      
    inq.put (m)
    parent.visit_ordering.put (receiver)


def step_children (container, causingMessage):      
    container.state = "idle"
    for child in list (container.visit_ordering.queue):
        # child == None represents self, skip it
        if (child != None): 
            if (not (child.inq.empty ())):
                msg = child.inq.get ()
                memo_accept (container, msg)
                child.handler(child, msg)
                destroy_message(msg)
            else:
                if (child.state != "idle"):
                    msg = force_tick (container, child, causingMessage)
                    child.handler(child, msg)
                    destroy_message(msg)
            
            if (child.state == "active"):
                # if child remains active, then the container must remain active and must propagate "ticks" to child
                container.state = "active"
            
            while (not (child.outq.empty ())):
                msg = child.outq.get ()
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
    was_sent = False # for checking that output went somewhere (at least during bootstrap)
    if is_tick (message):
        for child in container.children:    
            attempt_tick (container, child, message)
        was_sent = True
    else:
        fromname = ""
        if from_component != None:
            fromname = from_component.name
        from_sender = Sender (fromname, from_component, message.port)
        
        for connector in container.connections:
            if sender_eq (from_sender, connector.sender):   
                deposit (container, connector, message)
                was_sent = True
    if not (was_sent): 
        print ("\n\n*** Error: ***")
        print (f"{container.name}: message '{message.port}' from {fromname} dropped on floor...")
        dump_possible_connections (container)
        print ("***")
    
def dump_possible_connections (container):      
    print ("*** possible connections:")
    for connector in container.connections:
        print (f"{connector.direction} ❲{connector.sender.name}❳.❲{connector.sender.port}❳ -> ❲{connector.receiver.name}❳")

def any_child_ready (container):
    for child in container.children:
        if child_is_ready(child):
            return True
    return False

def child_is_ready (eh):      
    return (not (eh.outq.empty ())) or (not (eh.inq.empty ())) or ( eh.state != "idle") or (any_child_ready (eh))

    
