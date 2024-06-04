# all of the the built-in leaves are listed here
# future: refactor this such that programmers can pick and choose which (lumps of) builtins are used in a specific project

def initialize_stock_components (reg):
    register_component (reg, Template ( name = "1then2", instantiator = deracer_instantiate))
    register_component (reg, Template ( name = "?", instantiator = probe_instantiate))
    register_component (reg, Template ( name = "?A", instantiator = probeA_instantiate))
    register_component (reg, Template ( name = "?B", instantiator = probeB_instantiate))
    register_component (reg, Template ( name = "?C", instantiator = probeC_instantiate))
    register_component (reg, Template ( name = "trash", instantiator = trash_instantiate))

    register_component (reg, Template ( name = "Low Level Read Text File", instantiator = low_level_read_text_file_instantiate))
    register_component (reg, Template ( name = "Ensure String Datum", instantiator = ensure_string_datum_instantiate))

    register_component (reg, Template ( name = "syncfilewrite", instantiator = syncfilewrite_instantiate))
    register_component (reg, Template ( name = "stringconcat", instantiator = stringconcat_instantiate))
    # for fakepipe
    register_component (reg, Template ( name = "fakepipename", instantiator = fakepipename_instantiate))
    # for transpiler (ohmjs)
    register_component (reg, Template ( name = "OhmJS", instantiator = ohmjs_instantiate))
    # register_component (reg, string_constant ("RWR"))
    # register_component (reg, string_constant ("0d/python/std/rwr.ohm"))
    # register_component (reg, string_constant ("0d/python/std/rwr.sem.js"))
