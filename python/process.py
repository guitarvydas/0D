def generate_shell_components (reg, container_list):
    # [
    #     {'file': 'simple0d.drawio', 'name': 'main', 'children': [{'name': 'Echo', 'id': 5}], 'connections': [...]},
    #     {'file': 'simple0d.drawio', 'name': '...', 'children': [], 'connections': []}
    # ]
    if None != container_list:
        for diagram in container_list:
            # loop through every component in the diagram and look for names that start with "$"
            # {'file': 'simple0d.drawio', 'name': 'main', 'children': [{'name': 'Echo', 'id': 5}], 'connections': [...]},
            for child_descriptor in diagram ['children']:
                if first_char_is (child_descriptor ["name"], "$"):
                    name = child_descriptor ["name"]
                    cmd = name [1:].strip ()
                    generated_leaf = Template (name=name, instantiator=shell_out_instantiate, template_data=cmd)
                    register_component (reg, generated_leaf)
                elif first_char_is (child_descriptor ["name"], "'"):
                    name = child_descriptor ["name"]
                    s = name [1:]
                    generated_leaf = Template (name=name, instantiator=string_constant_instantiate, template_data=s)
                    register_component (reg, generated_leaf)

def first_char (s):
    return s[0]

def first_char_is (s, c):
    return c == first_char (s)
    
