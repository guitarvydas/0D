package std
import "core:os"
import "core:log"
import "core:runtime"
import "core:fmt"
import "core:slice"
import "core:strings"

import zd ".."

// run prints only the output on port "output", whereas run_demo prints all outputs
run :: proc (r : ^zd.Component_Registry, arg: string, main_container_name : string, diagram_source_files : [dynamic]string, injectfn : #type proc (string, ^zd.Eh)) {
    pregistry := r
    // get entrypoint container
    main_container, ok := zd.get_component_instance(pregistry, main_container_name, owner=nil)
    fmt.assertf(
        ok,
        "Couldn't find container with page name %s in files %s (check tab names, or disable compression?)\n",
        main_container_name,
        diagram_source_files,
    )
    injectfn (arg, main_container)
    print_error_maybe (main_container)
    print_output (main_container)
}

run_all_outputs :: proc (r : ^zd.Component_Registry, arg: string, main_container_name : string, diagram_source_files : [dynamic]string, injectfn : #type proc (string, ^zd.Eh)) {
    pregistry := r
    // get entrypoint container
    main_container, ok := zd.get_component_instance(pregistry, main_container_name, owner=nil)
    fmt.assertf(
        ok,
        "Couldn't find container with page name %s in files %s (check tab names, or disable compression?)\n",
        main_container_name,
        diagram_source_files,
    )
    injectfn (arg, main_container)
    print_error_maybe (main_container)
    dump_outputs (main_container)
}

run_demo :: proc (r : ^zd.Component_Registry, arg, main_container_name : string, diagram_source_files : [dynamic]string, injectfn : #type proc (string, ^zd.Eh)) {
    pregistry := r
    // get entrypoint container
    main_container, ok := zd.get_component_instance(pregistry, main_container_name, owner=nil)
    fmt.assertf(
        ok,
        "Couldn't find container with page name %s in files %s (check tab names, or disable compression?)\n",
        main_container_name,
        diagram_source_files,
    )
    injectfn (arg, main_container)
    dump_outputs (main_container)
    fmt.println("\n\n--- done ---")
}



run_demo_debug :: proc (r : ^zd.Component_Registry, arg: string, main_container_name : string, diagram_source_files : [dynamic]string, injectfn : #type proc (string, ^zd.Eh)) {
    pregistry := r
    // get entrypoint container
    main_container, ok := zd.get_component_instance(pregistry, main_container_name, owner=nil)
    fmt.assertf(
        ok,
        "Couldn't find main container with page name %s in files %s (check tab names, or disable compression?)\n",
        main_container_name,
        diagram_source_files,
    )

    dump_hierarchy (main_container)

    injectfn (arg, main_container)

    dump_outputs (main_container)
    dump_stats (pregistry)

    fmt.println("\n\n--- done ---")
}

