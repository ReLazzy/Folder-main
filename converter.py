from rect import Rect


def getPointsFromString(i):
    x1 = int(i[: i.find(" ")])
    i = i[i.find(" ") + 1 :]
    y1 = int(i[: i.find(" ")])
    i = i[i.find(" ") + 1 :]
    x2 = int(i[: i.find(" ")])
    i = i[i.find(" ") + 1 :]
    y2 = int(i[: i.find(" ")])
    i = i[i.find(" ") + 1 :]
    x3 = int(i[: i.find(" ")])
    i = i[i.find(" ") + 1 :]
    y3 = int(i[: i.find(" ")])
    i = i[i.find(" ") + 1 :]
    x4 = int(i[: i.find(" ")])
    i = i[i.find(" ") + 1 :]
    y4 = int(i)
    i = i[i.find(" ") + 1 :]

    left = 0
    right = 0
    top = 0
    bottom = 0

    if x1 < x2:
        left = x1
        right = x2
    elif x2 < x1:
        left = x2
        right = x1
    elif x3 < x1:
        left = x3
        right = x1
    else:
        left = x1
        right = x3

    if y1 < y2:
        bottom = y1
        top = y2
    elif y2 < y1:
        bottom = y2
        top = y1
    elif y3 < y1:
        bottom = y3
        top = y1
    else:
        bottom = y1
        top = y3
    return (left, right, top, bottom)


def getRectsFromPoints(result):
    classes = {}
    for a in result:
        current_marker_array = list(dict.fromkeys(result[a]))

        classes[a] = []

        for i in current_marker_array:
            left, right, top, bottom = getPointsFromString(i)
            classes[a].append(Rect(right, left, top, bottom))
    return classes


def showRects(classes):
    for a in classes:
        counter = 1
        for i in classes[a]:
            print(
                a,
                "[",
                counter,
                "]",
                ": ",
                (i.left, i.bottom),
                (i.left, i.top),
                (i.right, i.top),
                (i.right, i.bottom),
            )
            counter += 1
