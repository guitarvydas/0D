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
                    name_without_dollar = component_map ["name"] [1:]
                    generated_leaf = Template (name=name_without_dollar, instantiator=shell_out_instantiate)
                    register_component (reg, generated_leaf)

def run_command (cmd, s):
    print (f"NIY in alpha bootstrap: run_command({cmd},{s})")

def first_char (s):
    return s[0]

def first_char_is (s, c):
    return c == first_char (s)
    
