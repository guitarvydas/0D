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
