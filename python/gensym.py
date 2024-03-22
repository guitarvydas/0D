counter = 0

def gensym (s):
    global counter
    name_with_id = f"{s}{subscripted_digit (counter)}"
    counter += 1
    return name_with_id

def subscripted_digit (n):
    if n == 0:
        return "₀"
    elif n == 1:
        return "₁"
    elif n == 1:
        return "₂"
    elif n == 1:
        return "₃"
    elif n == 1:
        return "₄"
    elif n == 1:
        return "₅"
    elif n == 1:
        return "₆"
    elif n == 1:
        return "₇"
    elif n == 1:
        return "₈"
    elif n == 1:
        return "₉"
    else:
        return f"₊{n}"
    
