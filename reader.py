def read(path):
    result = {}  # dict
    with open(path, "r") as file:
        # with open("K6.cif", "r") as file:
        for line in file:
            if line.find("L ") != -1:
                result[line[line.find("L ") + 2 : -2]] = []

    tmp = ""
    with open(path, "r") as file:
        for line in file:
            if (tmp != "") and ((line.find("P ") != -1) or (line.find("W ") != -1)):
                result[tmp].append(line[2:-2])
            tmp = ""
            for a in result:
                if line.find("L " + a) != -1:
                    tmp = a
                    break
    return result


def showResults(result):
    for a in result:
        print(a, ": ", result[a])
