package std

import "core:fmt"
import zd "../0d"

fakepipename_instantiate :: proc(name: string, owner : ^zd.Eh) -> ^zd.Eh {
    instance_name := gensym ("fakepipe")
    return zd.make_leaf (instance_name, owner, nil, fakepipename_handle)
}

fakepipename_handle :: proc(eh: ^zd.Eh, msg: ^zd.Message) {
    @(static) rand := 0
    rand += 1 // not very random, but good enough - 'rand' must be unique within a single run
    zd.send_string (eh, "output", fmt.aprintf ("/tmp/fakepipe%d", rand), msg)
}

