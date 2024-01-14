/*

This example demonstrates taking a `.drawio` file and compiling
it to JSON

*/
package das2json

import "core:fmt"
import "core:os"
import "core:encoding/json" 
import "core:path/filepath"
import "core:slice"

import "syntax"


main :: proc() {
    diagram_name, main_container_name := parse_command_line_args ()
    fname := drawio2json (diagram_name)
}


drawio2json :: proc (container_xml : string) -> string {

    decls, err := syntax.parse_drawio_mxgraph(container_xml)
    assert(err == .None, "Failed parsing container XML")
    diagram_json, _ := json.marshal(decls, {pretty=true, use_spaces=true})
    nwritten : int
    sjson := string (diagram_json)
    mode: int = 0
    fname := fmt.aprintf ("%v.json", filepath.base (container_xml))
    when os.OS == .Linux || os.OS == .Darwin {
	// NOTE(justasd): 644 (owner read, write; group read; others read)
	mode = os.S_IRUSR | os.S_IWUSR | os.S_IRGRP | os.S_IROTH
    }
    fd, open_errnum := os.open (path = fname, flags =  os.O_WRONLY|os.O_CREATE|os.O_TRUNC, mode = mode)
    if open_errnum == 0 {
	numchars, write_errnum := os.write (fd, transmute([]u8)sjson)
	if write_errnum != 0 {
	    fmt.eprintf ("write failure %v\n", os.get_last_error ())
	}
    }
    os.close (fd)
    return fname
}

parse_command_line_args :: proc () -> (diagram_source_file, main_container_name: string) {
    diagram_source_file = slice.get(os.args, 1) or_else "<?>"
    main_container_name = slice.get(os.args, 2) or_else "main"
    
    if !os.exists(diagram_source_file) {
        fmt.println("Source diagram file", diagram_source_file, "does not exist.")
        os.exit(1)
    }
    return diagram_source_file, main_container_name
}


