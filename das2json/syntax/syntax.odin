/*

This package contains utilities for taking files and data and parsing them
into 0d declarations, as decribed in `decls.odin`, that should be able to
be used by any 0d runtime or compiler.

Right now, the only supported input format is uncompressed draw.io mxGraph
diagrams. Eventually support could be added for other formats, XML, JSON, ...

*/
package syntax

import "core:os"
import "core:encoding/xml"
import "../../ir"

Error :: enum {
    None,
    FileRead,
    XML,
}

parse_drawio_mxgraph :: proc(path: string) -> (decls: []ir.Container_Decl, err: Error) {
    file, file_ok := os.read_entire_file(path)
    if !file_ok {
        return {}, .FileRead
    }

    xml, xml_err := xml.parse(file)
    if xml_err != .None {
        return {}, .XML
    }

    decl_array := make([dynamic]ir.Container_Decl)

    for elem in xml.elements {
        if elem.ident == "root" {
            page := page_from_elem(xml, elem)
            decl := container_decl_from_page(page)
            decl.file = path
            append(&decl_array, decl)
        }
    }

    return decl_array[:], .None
}
