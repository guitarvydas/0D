import os
import json
import sys

class Component_Registry:
    def __init__ (self):
        self.templates = {}

class Template:
    def __init__ (self, name="", template_data=None, instantiator=None):
        self.name = name
        self.template_data = template_data
        self.instantiator = instantiator
        
def read_and_convert_json_file (filename):
    try:
        with open(filename, 'r') as file:
            json_data = file.read()
            routings = json.loads(json_data)
            return routings
    except FileNotFoundError:
        print (f"File not found: {filename}")
        return None
    except json.JSONDecodeError as e:
        print (f"Error decoding JSON in file: {e}")
        return None

def json2internal (container_xml):
    fname = os.path.basename (container_xml)
    routings = read_and_convert_json_file (fname)
    return routings

def delete_decls (d):
    pass

def make_component_registry ():
    return Component_Registry ()

def register_component (reg, template, ok_to_overwrite=False):
    name = mangle_name (template.name)
    if name in reg.templates and not ok_to_overwrite:
        load_error (f"Component {template.name} already declared")
    reg.templates[name] = template
    return reg

def register_multiple_components (reg, templates):
    for template in templates:
        register_component (reg, template)

def get_component_instance (reg, full_name, owner):
    template_name = mangle_name (full_name)
    if template_name in reg.templates:
        template = reg.templates[template_name]
        if (template == None):
            load_error (f"Registry Error: Can't find component {template_name} (does it need to be declared in components_to_include_in_project?")
            return None
        else:
            owner_name = ""
            instance_name = f"{template_name}"
            if None != owner:
                owner_name = owner.name
                instance_name = f"{owner_name}.{template_name}"
            else:
                instance_name = f"{template_name}"
            instance = template.instantiator (reg, owner, instance_name, template.template_data)
            instance.depth = calculate_depth (instance)
            return instance
    else:
            load_error (f"Registry Error: Can't find component {template_name} (does it need to be declared in components_to_include_in_project?")
            return None

def calculate_depth (eh):
    if eh.owner == None:
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

