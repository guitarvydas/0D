

def main ():
    arg_array = parse_command_line_args ()
    arg = arg_array [0]
    main_container_name = arg_array [1]
    diagram_names = arg_array [2]
    palette = initialize_component_palette (diagram_names, components_to_include_in_project)
    run_demo (palette, arg, main_container_name, diagram_names, start_function)

def start_function (arg, main_container):
    arg = new_datum_string (arg)
    msg = make_message("TOPin", arg, None )
    main_container.handler(main_container, msg)


def components_to_include_in_project (reg):
    register_component (reg, Template (name = "A", instantiator = A))
    register_component (reg, Template (name = "B", instantiator = B))
    register_component (reg, Template (name = "C", instantiator = C))


def A_handler (eh, msg):
    send_string (eh, "Aout", msg.datum.srepr (), msg)

def A (reg, owner, name, template_data):
    name_with_id = gensym ("A")
    return make_leaf (name_with_id, owner, None, A_handler)

def B_handler (eh, msg):
    send_string (eh, "Bout", msg.datum.srepr (), msg)

def B (reg, owner, name, template_data):
    name_with_id = gensym ("B")
    return make_leaf (name_with_id, owner, None, B_handler)

def C_handler (eh, msg):
    send_string (eh, "Cout", msg.datum.srepr (), msg)

def C (reg, owner, name, template_data):
    name_with_id = gensym ("C")
    return make_leaf (name_with_id, owner, None, C_handler)

main ()
