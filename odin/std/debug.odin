package std

import "core:log"
import "core:fmt"
import zd "../0d"

log_hierarchy :: proc (c : ^zd.Eh) {
    fmt.eprintf ("%s\n", build_hierarchy (c))
}

build_hierarchy :: proc (c : ^zd.Eh) -> string {
    s := ""
    for child in c.children {
	s = fmt.aprintf ("%s%s", s, build_hierarchy (child))
    }
    return fmt.aprintf ("\n(%s%s)", c.name, s)
}
