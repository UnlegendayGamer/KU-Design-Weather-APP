def delete_part_of_string(original_str, to_replace_str):
    index = original_str.find(to_replace_str)

    #if substring isnt found, return original string
    if index != -1:
        return original_str[:index] + original_str[index + len(to_replace_str):]
    
    return original_str

print(delete_part_of_string("hello world", "llo wo"))
