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

