

def main ():
    arg_array = parse_command_line_args ()
    arg = arg_array [0]
    main_container_name = arg_array [1]
    diagram_names = arg_array [2]
    palette = initialize_component_palette (diagram_names, components_to_include_in_project)
    run_demo (palette, arg, main_container_name, diagram_names, start_function)

def start_function (arg, main_container):
    arg = new_datum_string (arg)
    msg = make_message("", arg)
    inject (main_container, msg)


def components_to_include_in_project (reg):
    register_component (reg, Template (name = "strtest", instantiator = strtest))


def strtest_handler (eh, msg):
    send_string (eh, "", "test", msg)

def strtest (reg, owner, name, template_data):
    name_with_id = gensym ("strtest")
    return make_leaf (name_with_id, owner, None, strtest_handler)

main ()