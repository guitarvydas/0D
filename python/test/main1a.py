

def main ():
    arg_array = parse_command_line_args ()
    root_project = arg_array [0] 
    root_0D = arg_array [1]
    arg = arg_array [2]
    main_container_name = arg_array [3]
    diagram_names = arg_array [4]
    palette = initialize_component_palette (root_project, root_0D, diagram_names, components_to_include_in_project)
    run_demo (palette, root_project, root_0D, arg, main_container_name, diagram_names, start_function)

def start_function (root_project, root_0D, arg, main_container):
    arg = new_datum_string (arg)
    msg = make_message("", arg)
    inject (main_container, msg)


def components_to_include_in_project (root_project, root_0D, reg):
    # for dev0, dev1
    register_component (reg, Template (name = "Echo", instantiator = Echo))
    # for dev1a
    register_component (reg, Template (name = "A", instantiator = A))
    register_component (reg, Template (name = "B", instantiator = B))
    register_component (reg, Template (name = "C", instantiator = C))


def Echo_handler (eh, msg):
    send_string (eh, "", msg.datum.srepr (), msg)

def Echo (reg, owner, name, template_data):
    name_with_id = gensym ("Echo")
    return make_leaf (name_with_id, owner, None, Echo_handler)

def A_handler (eh, msg):
    send_string (eh, "Aout", "a", msg)
    #send_string (eh, "Aout", msg.datum.srepr (), msg)

def A (reg, owner, name, template_data):
    name_with_id = gensym ("A")
    return make_leaf (name_with_id, owner, None, A_handler)

def B_handler (eh, msg):
    send_string (eh, "Bout", "b", msg)
    #send_string (eh, "Bout", msg.datum.srepr (), msg)

def B (reg, owner, name, template_data):
    name_with_id = gensym ("B")
    return make_leaf (name_with_id, owner, None, B_handler)

def C_handler (eh, msg):
    send_string (eh, "Cout", "c", msg)
    #send_string (eh, "Cout", msg.datum.srepr (), msg)

def C (reg, owner, name, template_data):
    name_with_id = gensym ("C")
    return make_leaf (name_with_id, owner, None, C_handler)

main ()
