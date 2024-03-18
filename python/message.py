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
