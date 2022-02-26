# From https://gist.github.com/MysteriousBits/f1e649aee155111bc8efdd8f04cce54f
# Custom command flag parser
# for syntex like "-flag {option/data}"
# Arguments:
# txt(str) - the main input string: to parse datas from
# flags(list) - A list of strings: containing all the flags to parse

# return(dict): A dictionary containing the flags as the key and datas as value
# Assigns None to a key if no data is given or the flag is not found

def parse_flags(txt, flags):
    datas = {}
    for flag in flags:
        ind = txt.find(flag)
        if ind == -1 :
            # flag not found in the given string
            datas.update({flag: None})
            continue

        ind += len(flag)
        started = False
        braces_stack = 0    # To handle nested curly braces in the given string
        data = ""

        for i in range(ind, len(txt)):
            if not started:
                if txt[i] == "{":
                    started = True
                    braces_stack += 1
                elif txt[i] != " ": break
            else:
                if txt[i] == "{": braces_stack += 1
                elif txt[i] == "}":
                    braces_stack -= 1
                    if braces_stack <= 0: break
                data += txt[i]

        if data == "": datas.update({flag: None})
        else : datas.update({flag: data})

    return datas