package std
import zd ".."

// all of the the built-in leaves are listed here
// future: refactor this such that programmers can pick and choose which (lumps of) builtins are used in a specific project

initialize_stock_components :: proc (leaves: ^[dynamic]zd.Template) {
    zd.append_leaf (leaves, name = "1then2", instantiate = deracer_instantiate)
    zd.append_leaf (leaves, name = "?", instantiate = probe_instantiate)
    zd.append_leaf (leaves, name = "?A", instantiate = probeA_instantiate)
    zd.append_leaf (leaves, name = "?B", instantiate = probeB_instantiate)
    zd.append_leaf (leaves, name = "?C", instantiate = probeC_instantiate)
    zd.append_leaf (leaves, name = "trash", instantiate = trash_instantiate)
    zd.append_leaf (leaves, name = "Low Level Read Text File", instantiate = low_level_read_text_file_instantiate)
    zd.append_leaf (leaves, name = "Read Text From FD", instantiate = read_text_from_fd_instantiate)
    zd.append_leaf (leaves, name = "Open Text File", instantiate = open_text_file_instantiate)
    zd.append_leaf (leaves, name = "Ensure String Datum", instantiate = ensure_string_datum_instantiate)
    zd.append_leaf (leaves, name = "syncfilewrite", instantiate = syncfilewrite_instantiate)
    zd.append_leaf (leaves, name = "Bang", instantiate = bang_instantiate)
    zd.append_leaf (leaves, name = "stringconcat", instantiate = stringconcat_instantiate)// for fakepipe
    zd.append_leaf (leaves, name = "fakepipename", instantiate = fakepipename_instantiate)// for transpiler (ohmjs)
    zd.append_leaf (leaves, name = "OhmJS", instantiate = ohmjs_instantiate)
    zd.append_leaf (leaves, string_constant ("RWR"))
    zd.append_leaf (leaves, string_constant ("0d/odin/std/rwr.ohm"))
    zd.append_leaf (leaves, string_constant ("0d/odin/std/rwr.sem.js"))
}
