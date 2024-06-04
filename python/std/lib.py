import sys

# usage: app ${_00_} ${_0D_} arg main diagram_filename1 diagram_filename2 ...
# where ${_00_} is the root directory for the project
# where ${_0D_} is the root directory for 0D (e.g. 0D/odin or 0D/python)

def parse_command_line_args ():
    # return a 5-element array [root_project, root_0D, arg, main_container_name, [diagram_names]]
    if (len (sys.argv) < (5+1)):
        load_error ("usage: ${_00_} ${_0D_} app <arg> <main tab name> <diagram file name 1> ...")
        return None
    else:
        root_project = sys.argv [1]
        root_0D = sys.argv [2]
        arg = sys.argv [3]
        main_container_name = sys.argv [4]
        diagram_source_files = sys.argv [5:]
        return [root_project, root_0D, arg, main_container_name, diagram_source_files]

def initialize_component_palette (root_project, root_0D, diagram_source_files, project_specific_components_subroutine):
    reg = make_component_registry ()
    for diagram_source in diagram_source_files:
        all_containers_within_single_file = json2internal (diagram_source)
        generate_shell_components (reg, all_containers_within_single_file)
        for container in all_containers_within_single_file:
            register_component (reg, Template (name=container ['name'] , template_data=container, instantiator=container_instantiator))
    initialize_stock_components (reg)
    project_specific_components_subroutine (root_project, root_0D, reg) # add user specified components (probably only leaves)
    return reg


def print_error_maybe (main_container):
    error_port = "✗"
    err = fetch_first_output (main_container, error_port)
    if (err != None) and (0 < len (trimws (err.srepr ()))):
        print ("--- !!! ERRORS !!! ---")
        print_specific_output (main_container, error_port, False)


# debugging helpers

def dump_outputs (main_container):
    print ()
    print ("--- Outputs ---")
    print_output_list (main_container)

def trace_outputs (main_container):
    print ()
    print ("--- Message Traces ---")
    print_routing_trace (main_container)

def dump_hierarchy (main_container):
    print ()
    print (f"--- Hierarchy ---{(build_hierarchy (main_container))}")

def build_hierarchy (c):
    s = ""
    for child in c.children:
        s = f"{s}{build_hierarchy (child)}"
    indent = ""
    for i in range (c.depth):
        indent = indent + "  "
    return f"\n{indent}({c.name}{s})"

def dump_connections (c):
    print ()
    print (f"--- connections ---")
    dump_possible_connections (c)
    for child in c.children:
        print ()
        dump_possible_connections (child)

#
def trimws (s):
    # remove whitespace from front and back of string
    return s.strip ()

def clone_string (s):
    return s

load_errors = False
runtime_errors = False

def load_error (s):
    global load_errors
    print (s)
    quit ()
    load_errors = True

def runtime_error (s):
    global runtime_errors
    print (s)
    quit ()
    runtime_errors = True

    
