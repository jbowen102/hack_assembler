def try_num(string_in):
    try:
        converted = int(string_in)
    except ValueError:
        return False

if try_num(raw_address):
    A_value = try_num(raw_address)
elif raw_address in jump_labels.keys():
    A_value = jump_labels[raw_address]
elif raw_address in symbol_dict.keys():
    A_value = symbol_dict[raw_address]
else:
    lower_mem_range = symbol_dict.values()[symbol_dict.values() < 16384]
    new_mem_add = max(lower_mem_range) + 1
    symbol_dict[raw_address] = new_mem_add
    A_value = new_mem_add
