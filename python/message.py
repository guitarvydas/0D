# Message passed to a leaf component.
#
# `port` refers to the name of the incoming or outgoing port of this component.
# `datum` is the data attached to this message.
class Message:
    def __init__ (self, port, datum, direction=None, cause=None):
        self.port = port
        self.datum = datum
        self.cause = cause
        self.direction = direction

class Cause:
    def __init__ (self, who, message):
        # trail to help trace message provenance
        # each message is tagged with a Cause that describes who sent the message and what message
        # was handled by "who" in causing this message to be sent (since, the cause is a message,
        # cause also contains a message, and provenance can be traced recursively back
        # all the way back to the beginning of time)
        self.who = who
        self.message = message

def clone_port (s):
    return clone_string (s)


# Utility for making a `Message`. Used to safely "seed" messages
# entering the very top of a network.

def make_message (port, datum, direction=None, cause=None):
    p = clone_string (port)
    m = Message (port=p, datum=datum.clone (), direction=direction, cause=cause)
    return m

# Clones a message. Primarily used internally for "fanning out" a message to multiple destinations.
def message_clone (message):
    m = Message (port=clone_port (message.port), datum=message.datum.clone (), cause=message.cause)
    return m

# Frees a message.
def destroy_message (msg):
    # during debug, don't destroy any message, since we want to trace messages, thus, we need to persist ancestor messages
    pass

def destroy_datum (msg):
    pass

def destroy_port (msg):
    pass

def make_cause (eh, msg):
    # create a persistent Cause in the heap, return a pointer to it
    cause = Cause (who=eh, message=msg)
    return cause

#####

def format_message (m):
    if m == None:
        return "None"
    else:
        if m.cause == None:
            return f'⟪“{m.port}”₋“{m.datum.srepr ()}”₋⊥⟫'
        else:
            return f'⟪“{m.port}”₋“{m.datum.srepr ()}”₋…⟫'

def full_format_message (m):
    if m == None:
        return "None"
    else:
        if m.cause == None:
            return f'⟪“{m.port}”₋“{m.datum.srepr ()}”₋⊥⟫'
        elif None == m.cause.who:
            return f'⟪“{m.port}”₋“{m.datum.srepr ()}”₋[{m.direction},None,{format_message (m.cause.message)}]⟫'
        else:
            return f'⟪“{m.port}”₋“{m.datum.srepr ()}”₋[{m.direction},{m.cause.who.name},{format_message (m.cause.message)}]⟫'


def message_tracer (eh, msg, indent):
    m = format_message (msg)
    I = '[top]'
    if None != eh:
        I = f'{eh.name}'
    if msg.cause == None:
        return f'\n{indent}{m} was injected into ‛{I}‘'
    else:
        who = msg.cause.who
        str_causing_msg = format_message (msg.cause.message)
        cause_msg = msg.cause.message
        if who == None:
            return f"\n{indent}‛{I}‘ sent {m} because it received {str_causing_msg} from None {message_tracer (who, cause_msg, indent + '  ')}"
        else:
            sender = who.name
            if msg.direction == "down":
                return f"\n{indent}‛{I}‘ sent {m} because it received {str_causing_msg} from ‛{sender}‘{message_tracer (who, cause_msg, indent + '  ')}"
            elif msg.direction == "up":
                return f"\n{indent}‛{I}‘ output {m} because ‛{sender}‘ output {str_causing_msg}{message_tracer (who, cause_msg, indent + '  ')}"
            elif msg.direction == "across":
                return f"\n{indent}‛{I}‘ sent {m} because it received {str_causing_msg} from ‛{sender}‘{message_tracer (who, cause_msg, indent + '  ')}"
            elif msg.direction == "through":
                return f"\n{indent}‛{I}‘ through-output {m} because {I} received {str+causing_msg} from '{sender}‘{message_tracer (who, cause_msg, indent + '  ')}"
            else:
                return f"\n{indent}‛{I}‘ sent {m} because it received {str_causing_msg} from ‛{sender}‘{message_tracer (who, cause_msg, indent + '  ')}"

        
