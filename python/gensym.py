counter = 0

def gensym (s):
    global counter
    counter += 1
    name_with_id = f"{s}◦{counter}"
    return name_with_id

