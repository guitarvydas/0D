# run prints only the output on port "output", whereas run_demo prints all outputs
def run (pregistry, arg, main_container_name, diagram_source_files, injectfn):
    # get entrypoint container
    main_container = get_component_instance(pregistry, main_container_name, owner=nil)
    if None == main_container:
        load_error (f"Couldn't find container with page name {main_container_name} in files {diagram_source_files} (check tab names, or disable compression?)")
    injectfn (arg, main_container)
    print_error_maybe (main_container)
    print_output (main_container)

def run_all_outputs (pregistry, arg, main_container_name, diagram_source_files, injectfn):
    # get entrypoint container
    main_container = get_component_instance(pregistry, main_container_name, owner=nil)
    if None == main_container:
        load_error (f"Couldn't find container with page name {main_container_name} in files {diagram_source_files} (check tab names, or disable compression?)")
    injectfn (arg, main_container)
    print_error_maybe (main_container)
    dump_outputs (main_container)

def run_demo (pregistry, arg, main_container_name, diagram_source_files, injectfn):
    # get entrypoint container
    main_container = get_component_instance(pregistry, main_container_name, owner=nil)
    if None == main_container:
        load_error (f"Couldn't find container with page name {main_container_name} in files {diagram_source_files} (check tab names, or disable compression?)")
    injectfn (arg, main_container)
    dump_outputs (main_container)
    print ("--- done ---")

def run_demo_debug (pregistry, arg, main_container_name, diagram_source_files, injectfn):
    # get entrypoint container
    main_container = get_component_instance(pregistry, main_container_name, owner=nil)
    if None == main_container:
        load_error (f"Couldn't find container with page name {main_container_name} in files {diagram_source_files} (check tab names, or disable compression?)")
    dump_hierarchy (main_controller)
    injectfn (arg, main_container)
    dump_outputs (main_container)
    print ("--- done ---")
