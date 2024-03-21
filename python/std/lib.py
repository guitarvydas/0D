import sys

# usage: app arg main diagram_filename1 diagram_filename2 ...
def parse_command_line_args ():
    # return a 3-element array [arg, main_container_name, [diagram_names]]
    if (len (sys.argv) < (3+1)):
        load_error ("usage: app <arg> <main tab name> <diagram file name 1> ...")
        return None
    else:
        arg = sys.argv [1]
        main_container_name = sys.argv [2]
        diagram_source_files = sys.argv [3:]
        return [arg, main_container_name, diagram_source_files]

def initialize_component_palette (diagram_source_files, project_specific_components_subroutine):
    reg = make_component_registry ()
    for diagram_source in diagram_source_files:
        collect_process_leaves (reg, diagram_source)
        all_containers_within_single_file = json2internal (diagram_source)
        for container in all_containers_within_single_file:
            register_component (reg, Template (name=container.name , template_data=container, instantiator=container_instantiator))
    initialize_stock_components (reg)
    project_specific_components (reg) # add user specified components (probably only leaves)
    return reg


def print_error_maybe (main_container):
    error_port = "✗"
    err = fetch_first_output (main_container, error_port)
    if found and (0 < len (trimws (err))):
        print ("--- !!! ERRORS !!! ---")
        print_specific_output (main_container, error_port, False)


# debugging helpers

def dump_outputs (main_container):
    print ()
    print ("--- Outputs ---")
    print_output_list (main_container)

def dump_hierarchy (main_container):
    print ()
    print ("--- Hierarchy ---")
    print (build_hierarchy (main_container))

def build_hierarchy (c):
    s = ""
    for child in c.children:
        s = f"{s}{build_hierarchy (child)}"
    return f"\n({c.name}{s})"

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
    load_errors = true

def runtime_error (s):
    global runtime_errors
    print (s)
    runtime_errors = true

    
