def val_in_range(val, min, max):
    if val > max:
        val = max
    elif val < min:
        val = min

    return val

def xor(bool1, bool2):
    return (bool1 and not bool2) or (not bool1 and bool2)