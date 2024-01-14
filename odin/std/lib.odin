package std
import "core:os"
import "core:log"
import "core:runtime"
import "core:fmt"
import "core:slice"
import "core:strings"

import zd "../0d"
import "../ir"

parse_command_line_args :: proc () -> (main_container_name: string, diagram_source_files : [dynamic]string,) {
    diagram_source_files = make ([dynamic]string)
    if len (os.args) < (2+1) { // 0'th arg is the name of the program itself, we need at least 2 more args
	fmt.eprintf ("usage: app <main tab name> <diagram file name 1> <diagram file name 2> ...\n")
	os.exit (1)
    }
    main_container_name = slice.get(os.args, 1) or_else strings.clone ("main")
    for i := 2 ; i < len (os.args) ; i += 1 {
	dname, ok := slice.get (os.args, i)    
	if !ok || !os.exists(dname) {
            fmt.println("[lib] Source diagram file", dname, "does not exist.")
            os.exit(1)
	}
	dname_in_heap := new (string)
	dname_in_heap^ = dname
	append (&diagram_source_files, dname_in_heap^)
    }
    return main_container_name,  diagram_source_files
}

initialize_component_palette :: proc (diagram_source_files: [dynamic]string,
				      project_specific_components : #type proc (^[dynamic]zd.Leaf_Template)) -> zd.Component_Registry {
    leaves := make([dynamic]zd.Leaf_Instantiator)
    all_containers : [dynamic]ir.Container_Decl
    
    // set up shell leaves
    for i := 0 ; i < len (diagram_source_files) ; i += 1 {
	collect_process_leaves(diagram_source_files[i], &leaves)
    }

    // export native leaves
    zd.append_leaf (&leaves, zd.Leaf_Instantiator {
        name = "stdout",
        instantiate = stdout_instantiate,
    })
    initialize_stock_components (&leaves)
    project_specific_components (&leaves) // add user specified leaves

    for filename in diagram_source_files {
	containers_within_single_file := zd.json2internal (filename)
	for container in containers_within_single_file {
	    append (&all_containers, container)
	}
    }
    palette := zd.make_component_registry(leaves[:], all_containers)
    return palette^
}

print_output_verbose :: proc (main_container : ^zd.Eh) {
    fmt.println("\n\n--- RESULT ---")
    fmt.printf ("... response ... \n")
    zd.print_specific_output (main_container, "output", false)
}

print_output :: proc (main_container : ^zd.Eh) {
    zd.print_specific_output (main_container, "output", false)
}

print_error_maybe :: proc (main_container : ^zd.Eh) {
    error_port := "error"
    err, found := zd.fetch_first_output (main_container, error_port)
    if found && (0 < len (strings.trim (err.repr (err), " \t\n"))) {
	fmt.println("\n\n--- !!! ERRORS !!! ---")
	zd.print_specific_output (main_container, error_port, false)
    }
}


// debugging helpers

dump_hierarchy :: proc (main_container : ^zd.Eh) {
    fmt.println("\n\n--- Hierarchy ---")
    log_hierarchy (main_container)
}

dump_outputs :: proc (main_container : ^zd.Eh) {
    fmt.println("\n\n--- Outputs ---")
    zd.print_output_list(main_container)
}

dump_stats :: proc (pregistry : ^zd.Component_Registry) {
    zd.print_stats (pregistry)
}

log :: proc (level : int) -> log.Logger{
    // level:
    // zd.log_light_handlers // set this to only track handlers in Components
    // zd.log_full_handlers // set this to only track handlers, in full glory, in Components
    // zd.log_all // set this to track everything, equivalent to runtime.Logger_Level.Debug
    fmt.printf ("\n*** starting logger level %v ***\n", level)
    return log.create_console_logger(
	lowest=cast(runtime.Logger_Level)level,
        opt={.Level, .Time, .Terminal_Color},
    )
}
