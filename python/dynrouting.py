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

