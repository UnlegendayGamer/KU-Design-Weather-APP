def getDict(filename):
    dict1 = {}
    file = open(filename, "r")
    while True:
        content = file.readline()
        if not content:
            break
        content = content.split(" ")
        content[len(content)-1] = content[len(content)-1][:-1]
        name = content.pop(0)
        dict1[name]=content
    return dict1