def run (pregistry, root_project, root_0D, arg, main_container_name, diagram_source_files, injectfn,
              show_hierarchy=True, show_connections=True, show_traces=True, show_all_outputs=True):
    set_environment (root_project, root_0D)
    # get entrypoint container
    main_container = get_component_instance(pregistry, main_container_name, owner=None)
    if None == main_container:
        load_error (f"Couldn't find container with page name {main_container_name} in files {diagram_source_files} (check tab names, or disable compression?)")
    if show_hierarchy:
        dump_hierarchy (main_container)
    if show_connections:
        dump_connections (main_container)
    if not load_errors:
        injectfn (root_project, root_0D, arg, main_container)
    if show_all_outputs:
        dump_outputs (main_container)
    else:
        print_error_maybe (main_container)
        print_specific_output (main_container, port="", stderr=False)
    if show_traces:
        print ("--- routing traces ---")
        print (routing_trace_all (main_container))
    if show_all_outputs:
        print ("--- done ---")

