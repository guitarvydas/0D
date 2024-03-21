# all of the the built-in leaves are listed here
# future: refactor this such that programmers can pick and choose which (lumps of) builtins are used in a specific project

def initialize_stock_components (reg):
    register_component (reg, Template ( name = "1then2", instantiate = deracer_instantiate))
    register_component (reg, Template ( name = "?", instantiate = probe_instantiate))
    register_component (reg, Template ( name = "?A", instantiate = probeA_instantiate))
    register_component (reg, Template ( name = "?B", instantiate = probeB_instantiate))
    register_component (reg, Template ( name = "?C", instantiate = probeC_instantiate))
    register_component (reg, Template ( name = "trash", instantiate = trash_instantiate))

    register_component (reg, Template ( name = "Low Level Read Text File", instantiate = low_level_read_text_file_instantiate))
    register_component (reg, Template ( name = "Read Text From FD", instantiate = read_text_from_fd_instantiate))
    register_component (reg, Template ( name = "Open Text File", instantiate = open_text_file_instantiate))
    register_component (reg, Template ( name = "Ensure String Datum", instantiate = ensure_string_datum_instantiate))

    register_component (reg, Template ( name = "syncfilewrite", instantiate = syncfilewrite_instantiate))
    register_component (reg, Template ( name = "Bang", instantiate = bang_instantiate))
    register_component (reg, Template ( name = "stringconcat", instantiate = stringconcat_instantiate))
    # for fakepipe
    register_component (reg, Template ( name = "fakepipename", instantiate = fakepipename_instantiate))
    # for transpiler (ohmjs)
    register_component (reg, Template ( name = "OhmJS", instantiate = ohmjs_instantiate))
    register_component (reg, string_constant ("RWR"))
    register_component (reg, string_constant ("0d/odin/std/rwr.ohm"))
    register_component (reg, string_constant ("0d/odin/std/rwr.sem.js"))
