
def get_cfg_val(d1, d2, key, def_val):
    value = d1.get(key, d2.get(key, def_val))
    print(f"{key=} {value=}")
    return value
