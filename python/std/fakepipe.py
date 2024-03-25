def fakepipename_instantiate (reg, owner, name, template_data):
    instance_name = gensym ("fakepipe")
    return make_leaf (instance_name, owner, None, fakepipename_handler)

rand = 0
def fakepipename_handler (eh, msg):
    global rand
    rand += 1 # not very random, but good enough - 'rand' must be unique within a single run
    send_string (eh, "", f"/tmp/fakepipe{rand}", msg)

