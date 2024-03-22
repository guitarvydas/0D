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
    elif n == 2:
        return "₂"
    elif n == 3:
        return "₃"
    elif n == 4:
        return "₄"
    elif n == 5:
        return "₅"
    elif n == 6:
        return "₆"
    elif n == 7:
        return "₇"
    elif n == 8:
        return "₈"
    elif n == 9:
        return "₉"
    else:
        return f"₊{n}"
    
