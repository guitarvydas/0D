class Component_Registry:
    def _init_ (self):
        self.templates = {}
        self.stats = Registry_Stats ()

class Template:
    def _init_ (self):
        self.name = ""
        self.template_data = none # like "class data" in OOP - same data for every instance of this kind ; none for Leaf, routing for Container
        self.instantiator = none
        
def read_and_convert_json_file (filename):
    try:
        with open(filename, 'r') as file:
            json_data = file.read()
            routings = json.loads(json_data)
            return routings
    except FileNotFoundError:
        print("File not found:", filename)
        return None
    except json.JSONDecodeError as e:
        print("Error decoding JSON in file:", e)
        return None

def json2internal (container_xml):
    fname = os.path.basename (container_xml)
    routings = read_and_convert_json_file (fname)
    return routings

def delete_decls (d):
    pass

def make_component_registry ():
    return Component_Registry ()

def register_component (reg, template):
    name = mangle_name (template.name)
    if name in reg.templates:
        load_error (f"Component {template.name} already declared")
    reg.templates[name] = template
    return reg

def register_multiple_components (reg, templates):
    for template in templates:
        register_component (reg, template)

def get_component_instance (reg, full_name, owner):
    template_name = parse_name (full_name)
    template = reg.templates[template_name]
    if (template == none):
        load_error (f"Registry Error: Can't find component {template_name} (does it need to be declared in components_to_include_in_project?")
        return none
    else:
        instance_name = f"{owner.name}.{template_name}"
        instance = template.instantiate (reg, owner, component_name, template.decl)
        instance.depth = calculate_depth (instance)
        return instance

def calculate_depth (eh):
    if eh.owner == none:
        return 0
    else:
        return 1 + calculate_depth (eh.owner)
    
def dump_registry (reg):
    print ()
    print ("*** PALETTE ***")
    for c in reg.templates:
        print (c.name)
    print ("***************")
    print ()

def print_stats (reg):
    print (f"registry statistics: {reg.stats}")

def mangle_name (s):
    # trim name to remove code from Container component names - deferred until later (or never)
    return s

