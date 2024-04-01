

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
    register_component (reg, Template (name = "strtest", instantiator = strtest))


def strtest_handler (eh, msg):
    send_string (eh, "", "test", msg)

def strtest (reg, owner, name, template_data):
    name_with_id = gensym ("strtest")
    return make_leaf (name_with_id, owner, None, strtest_handler)

main ()
