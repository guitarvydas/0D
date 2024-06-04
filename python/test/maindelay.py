def main ():
    arg_array = parse_command_line_args ()
    root_project = arg_array [0] 
    root_0D = arg_array [1]
    arg = arg_array [2]
    main_container_name = arg_array [3]
    diagram_names = arg_array [4]
    palette = initialize_component_palette (root_project, root_0D, diagram_names, components_to_include_in_project)
    run_demo (palette, root_project, root_0D, arg, main_container_name, diagram_names, start_function,
              show_hierarchy=False, show_connections=False, show_traces=False)

def start_function (root_project, root_0D, arg, main_container):
    arg = new_datum_string (arg)
    msg = make_message("", arg)
    inject (main_container, msg)


def components_to_include_in_project (root_project, root_0D, reg):
    register_component (reg, Template (name = "Echo", instantiator = Echo))
    register_component (reg, Template (name = "Sleep", instantiator = sleep))


def Echo_handler (eh, msg):
    send_string (eh, "", msg.datum.srepr (), msg)

def Echo (reg, owner, name, template_data):
    name_with_id = gensym ("Echo")
    return make_leaf (name_with_id, owner, None, Echo_handler)


SLEEPDELAY = 1000000

class Sleep_Info:
    def __init__ (self, counter=0, saved_message=None):
        self.counter = counter
        self.saved_message = saved_message

def first_time (m):
    return not is_tick (m)

def sleep_handler (eh, msg):
    info = eh.instance_data
    if first_time (msg):
        info.saved_message = msg
        set_active (eh) ## tell engine to keep running this component with 'ticks'
    count = info.counter
    count += 1
    if count >= SLEEPDELAY:
        set_idle (eh) ## tell engine that we're finally done
        forward (eh=eh, port="", msg=info.saved_message)
        count = 0
    info.counter = count

def sleep (reg, owner, name, template_data):
    name_with_id = gensym ("sleep")
    info = Sleep_Info ()
    return make_leaf (name_with_id, owner, info, sleep_handler)

main ()
