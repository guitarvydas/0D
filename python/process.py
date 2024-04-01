import subprocess

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
                    register_component (reg, generated_leaf, ok_to_overwrite=True)

def first_char (s):
    return s[0]

def first_char_is (s, c):
    return c == first_char (s)
    
# this needs to be rewritten to use the low-level "shell_out" component, this can be done solely as a diagram without using python code here
# I'll keep it for now, during bootstrapping, since it mimics what is done in the Odin prototype - both need to be revamped
def run_command (eh, cmd, s):
    ret = subprocess.run (cmd, capture_output=True, input=s, encoding='utf-8')
    if  not (ret.returncode == 0):
        if ret.stderr != None:
            return ["", ret.stderr]
        else:
            return ["", f"error in shell_out {ret.returncode}"]
    else:
        return [ret.stdout, None]
    
