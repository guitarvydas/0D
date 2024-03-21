

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
