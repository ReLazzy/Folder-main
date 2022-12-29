from PIL import Image, ImageDraw
from matplotlib import pyplot as plt

import canvas
from rect import Rect

charts_colors = ["tomato", "cornflowerblue", "gold", "orchid", "#b2ff6b", "#77BFE2"]


def get_canvas_size(rects):
    min_left = 10000000
    min_bottom = 10000000
    max_right = -1000000
    max_top = -1000000

    for a in rects:
        for b in rects[a]:
            if b.left < min_left:
                min_left = b.left
            if b.bottom < min_bottom:
                min_bottom = b.bottom
            if b.right > max_right:
                max_right = b.right
            if b.top > max_top:
                max_top = b.top

    width = max_right - min_left
    height = max_top - min_bottom

    return min_left, min_bottom, max_right, max_top, width, height


def adjust_coordinates(rects, width, height, min_left, min_bottom, k):
    adj_rects = rects.copy()

    for a in rects:
        adj_rects[a] = []
        for b in rects[a]:
            adj_rects[a].append(
                Rect(
                    (b.right - min_left) // k,
                    (b.left - min_left) // k,
                    (b.top - min_bottom) // k,
                    (b.bottom - min_bottom) // k,
                )
            )
    width = width // k
    height = height // k
    return adj_rects, width, height


def get_borders(rects):
    min_left = 10000000
    min_bottom = 10000000
    max_right = -1000000
    max_top = -1000000
    for b in rects["B1"]:
        if b.left < min_left:
            min_left = b.left
        if b.bottom < min_bottom:
            min_bottom = b.bottom
        if b.right > max_right:
            max_right = b.right
        if b.top > max_top:
            max_top = b.top
    return min_left, min_bottom, max_right, max_top


def rects_intersection(rect1, rect2):
    if rect1.right < rect2.left:
        return False
    if rect1.left > rect2.right:
        return False
    if rect1.top < rect2.bottom:
        return False
    if rect1.bottom > rect2.top:
        return False

    x1 = max(rect1.left, rect2.left)
    x2 = min(rect1.right, rect2.right)
    y1 = max(rect1.bottom, rect2.bottom)
    y2 = min(rect1.top, rect2.top)

    if abs(x1 - x2) * abs(y1 - y2) > 0:
        return Rect(x1, x2, y1, y2)

    return False


def intersecton_with_layer(element, layer_array):
    key = False
    for i in layer_array:
        intersection = rects_intersection(element, i)
        if intersection:
            key = True
            break
    return key, intersection


def get_transistors(rects):
    n_transistors = []
    p_transistors = []
    n_channels = []
    p_channels = []
    for i in rects["NA"]:
        key, intersection = intersecton_with_layer(i, rects["SP"])
        if key:
            p_transistors.append(i)
            p_channels.append(intersection)
            continue
        key, intersection = intersecton_with_layer(i, rects["SN"])
        if key:
            n_transistors.append(i)
            n_channels.append(intersection)
            continue
        else:
            continue
    return p_transistors, n_transistors, p_channels, n_channels


def filter_by_border(rects, border_rect):
    filtered_rects = {}
    for i in rects:
        filtered_rects[i] = []
        for j in rects[i]:
            if (border_rect.is_inside(j)) or (rects_intersection(border_rect, j) == False):
                continue
            else:
                filtered_rects[i].append(Rect(j.right, j.left, j.top, j.bottom))
    return filtered_rects


def arrays_union_square(width, height, border_rect, filename, *arrays):
    im = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(im, "RGB")
    for i in arrays:
        canvas.fill_rects(i, (119, 191, 226), draw)
    count = 0

    for pixel in im.getdata():

        if pixel == (119, 191, 226):
            count += 1
    canvas.draw_border(border_rect, draw)
    s1 = "images/"
    s2 = ".jpg"
    a = "".join([s1, filename, s2])
    im.rotate(180).transpose(Image.Transpose.FLIP_LEFT_RIGHT).save("images/" + filename + "[solution].jpg", quality=95)
    return count


def si_connections_square(width, height, border_rect, rects, n_channels, p_channels):
    sn_connections = []
    sp_connections = []
    # n_channels = []
    # p_channels = []

    im = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(im, "RGB")
    canvas.fill_rects(rects["SI"], (119, 191, 226), draw)
    canvas.fill_rects(rects["SP"], (119, 191, 226), draw)
    canvas.fill_rects(rects["SN"], (119, 191, 226), draw)
    canvas.fill_rects(n_channels, (255, 255, 255), draw)
    canvas.fill_rects(p_channels, (255, 255, 255), draw)
    count = 0
    for pixel in im.getdata():
        if pixel == (119, 191, 226):
            count += 1
    canvas.draw_border(border_rect, draw)
    im.rotate(180).transpose(Image.Transpose.FLIP_LEFT_RIGHT).save("images/si[solution].jpg", quality=95)
    return count


def useful_si_square(width, height, border_rect, rects, n_transistors, p_transistors):
    im = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(im, "RGB")
    canvas.fill_rects(rects["SI"], (119, 191, 226), draw)
    canvas.fill_rects(rects["SP"], (119, 191, 226), draw)
    canvas.fill_rects(rects["SN"], (119, 191, 226), draw)
    canvas.fill_rects(n_transistors, (255, 255, 255), draw)
    canvas.fill_rects(p_transistors, (255, 255, 255), draw)
    count = 0
    for pixel in im.getdata():
        if pixel == (119, 191, 226):
            count += 1
    canvas.draw_border(border_rect, draw)
    im.rotate(180).transpose(Image.Transpose.FLIP_LEFT_RIGHT).save("images/useful_si[solution].jpg", quality=95)
    return count


def useful_alloy_square(width, height, border_rect, n_channels, p_channels, n_transistors, p_transistors):
    im = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(im, "RGB")
    canvas.fill_rects(n_transistors, (119, 191, 226), draw)
    canvas.fill_rects(p_transistors, (119, 191, 226), draw)
    canvas.fill_rects(n_channels, (255, 255, 255), draw)
    canvas.fill_rects(p_channels, (255, 255, 255), draw)
    count = 0
    for pixel in im.getdata():
        if pixel == (119, 191, 226):
            count += 1
    canvas.draw_border(border_rect, draw)
    im.rotate(180).transpose(Image.Transpose.FLIP_LEFT_RIGHT).save("images/useful_alloy[solution].jpg", quality=95)
    return count


def useful_metal_square(width, height, border_rect, rects, n_transistors, p_transistors):
    im = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(im, "RGB")
    canvas.fill_rects(rects["M1"], (119, 191, 226), draw)
    canvas.fill_rects(rects["M2"], (119, 191, 226), draw)
    canvas.fill_rects(rects["SI"], (255, 255, 255), draw)
    canvas.fill_rects(rects["SP"], (255, 255, 255), draw)
    canvas.fill_rects(rects["SN"], (255, 255, 255), draw)
    canvas.fill_rects(n_transistors, (255, 255, 255), draw)
    canvas.fill_rects(p_transistors, (255, 255, 255), draw)
    count = 0
    for pixel in im.getdata():
        if pixel == (119, 191, 226):
            count += 1
    canvas.draw_border(border_rect, draw)
    im.rotate(180).transpose(Image.Transpose.FLIP_LEFT_RIGHT).save("images/useful_metal[solution].jpg", quality=95)
    return count


def get_all_elements(adj_rects, border_rect):
    p_transistors, n_transistors, p_channels, n_channels = get_transistors(adj_rects)
    elements_dict = {
        "P_TRANSISTORS": p_transistors,
        "N_TRANSISTORS": n_transistors,
        "P_CHANNELS": p_channels,
        "N_CHANNELS": n_channels,
        "M2_METAL": adj_rects["M2"],
        "M1_METAL": adj_rects["M1"],
        "BORDER_RECT": border_rect,
    }
    return elements_dict


def print_all_elements(elements_dict):
    for a in elements_dict:
        print("=============", a, "=============")
        if type(elements_dict[a]) == list:
            for i in elements_dict[a]:
                i.printCoords()
        else:
            elements_dict[a].printCoords()


def get_all_squares(elements_dict, rects, width, height):
    square_of_n_trans = arrays_union_square(
        width, height, elements_dict["BORDER_RECT"], "n_trans", elements_dict["N_TRANSISTORS"]
    )

    square_of_n_channels = arrays_union_square(
        width, height, elements_dict["BORDER_RECT"], "n_channels", elements_dict["N_CHANNELS"]
    )

    square_of_p_trans = arrays_union_square(
        width, height, elements_dict["BORDER_RECT"], "p_trans", elements_dict["P_TRANSISTORS"]
    )

    square_of_p_channels = arrays_union_square(
        width, height, elements_dict["BORDER_RECT"], "p_channels", elements_dict["P_CHANNELS"]
    )

    square_of_all_trans = arrays_union_square(
        width, height, elements_dict["BORDER_RECT"], "all_trans", elements_dict["P_TRANSISTORS"],
        elements_dict["N_TRANSISTORS"]
    )

    square_of_all_channels = arrays_union_square(
        width, height, elements_dict["BORDER_RECT"], "all_channels", elements_dict["P_CHANNELS"],
        elements_dict["N_CHANNELS"]
    )

    square_of_m1_metal = arrays_union_square(
        width, height, elements_dict["BORDER_RECT"], "m1_metal", elements_dict["M1_METAL"], elements_dict["M1_METAL"]
    )

    square_of_m2_metal = arrays_union_square(
        width, height, elements_dict["BORDER_RECT"], "m2_metal", elements_dict["M2_METAL"], elements_dict["M2_METAL"]
    )

    square_of_all_metal = arrays_union_square(
        width, height, elements_dict["BORDER_RECT"], "all_metal", elements_dict["M1_METAL"], elements_dict["M2_METAL"]
    )

    square_of_si_connections = si_connections_square(
        width, height, elements_dict["BORDER_RECT"], rects, elements_dict["N_CHANNELS"], elements_dict["P_CHANNELS"]
    )

    square_of_scheme = arrays_union_square(
        width,
        height,
        elements_dict["BORDER_RECT"],
        "scheme",
        rects["NA"],
        # rects["P"],
        rects["SI"],
        rects["SN"],
        rects["SP"],
        rects["M1"],
        rects["M2"],
    )

    square_of_borders = elements_dict["BORDER_RECT"].square

    square_of_blanks = square_of_borders - square_of_scheme

    square_of_useful_si = useful_si_square(
        width, height, elements_dict["BORDER_RECT"], rects, elements_dict["N_TRANSISTORS"],
        elements_dict["P_TRANSISTORS"]
    )

    square_of_useful_alloy = useful_alloy_square(
        width,
        height,
        elements_dict["BORDER_RECT"],
        elements_dict["N_CHANNELS"],
        elements_dict["P_CHANNELS"],
        elements_dict["N_TRANSISTORS"],
        elements_dict["P_TRANSISTORS"],
    )

    square_of_useful_metal = useful_metal_square(
        width, height, elements_dict["BORDER_RECT"], rects, elements_dict["N_TRANSISTORS"],
        elements_dict["P_TRANSISTORS"]
    )

    squares_dict = {
        "n_trans": [square_of_n_trans, round(square_of_n_trans / square_of_borders * 100, 2)],
        "p_trans": [square_of_p_trans, round(square_of_p_trans / square_of_borders * 100, 2)],
        "all_trans": [square_of_all_trans, round(square_of_all_trans / square_of_borders * 100, 2)],
        "n_channels": [square_of_n_channels, round(square_of_n_channels / square_of_borders * 100, 2)],
        "p_channels": [square_of_p_channels, round(square_of_p_channels / square_of_borders * 100, 2)],
        "all_channels": [square_of_all_channels, round(square_of_all_channels / square_of_borders * 100, 2)],
        "m1_metal": [square_of_m1_metal, round(square_of_m1_metal / square_of_borders * 100, 2)],
        "m2_metal": [square_of_m2_metal, round(square_of_m2_metal / square_of_borders * 100, 2)],
        "all_metal": [square_of_all_metal, round(square_of_all_metal / square_of_borders * 100, 2)],
        "si": [square_of_si_connections, round(square_of_si_connections / square_of_borders * 100, 2)],
        "scheme": [square_of_scheme, round(square_of_scheme / square_of_borders * 100, 2)],
        "borders": [square_of_borders, round(square_of_borders / square_of_borders * 100, 2)],
        "blanks": [square_of_blanks, round(square_of_blanks / square_of_borders * 100, 2)],
    }

    report_dict = {
        "useful_alloy": [square_of_useful_alloy, round(square_of_useful_alloy / square_of_borders * 100, 2)],
        "all_channels": [square_of_all_channels, round(square_of_all_channels / square_of_borders * 100, 2)],
        "useful_si": [square_of_useful_si, round(square_of_useful_si / square_of_borders * 100, 2)],
        "useful_metal": [square_of_useful_metal, round(square_of_useful_metal / square_of_borders * 100, 2)],
        "blanks": [square_of_blanks, round(square_of_blanks / square_of_borders * 100, 2)],
    }

    get_squares_charts(squares_dict)

    get_report_chart(report_dict)

    return squares_dict, report_dict


def get_squares_charts(squares_dict):
    for a in squares_dict:
        # print("square of ", a, " = ", squares_dict[a][0], ", ", squares_dict[a][1], "%")

        # Creating dataset

        names = [a, "rest"]
        data = [squares_dict[a][1], squares_dict["borders"][1] - squares_dict[a][1]]

        # Creating plot
        fig = plt.figure(figsize=(10, 7))
        plt.pie(data, autopct="%.2f", labels=names, colors=charts_colors, textprops={"fontsize": 14})

        # show plot
        plt.savefig("images/" + a + "[chart].jpg", bbox_inches="tight")


def get_report_chart(report_dict):
    names = []
    data = []
    for a in report_dict:
        names.append(a)
        data.append(report_dict[a][1])
    fig = plt.figure(figsize=(10, 7))
    plt.pie(data, autopct="%.2f", labels=names, colors=charts_colors, textprops={"fontsize": 14})

    # show plot
    plt.savefig("images/report[chart].jpg", bbox_inches="tight")


def print_squares(squares_dict):
    print("============ SQUARES =============")
    for a in squares_dict:
        print("square of ", a, " = ", squares_dict[a][0], ", ", squares_dict[a][1], "%")


def print_square(element, squares_dict):
    print("============ SQUARE =============")
    print("square of ", element, " = ", squares_dict[element][0], ", ", squares_dict[element][1], "%")


# def return_square(element, squares_dict):
#     s = str(squares_dict[element][1]) + " %"
#     return s


def print_report(report_dict):
    print("============ REPORT =============")
    print("alloy", " = ", report_dict["useful_alloy"][0], ", ", report_dict["useful_alloy"][1], "%")
    print("channels", " = ", report_dict["all_channels"][0], ", ", report_dict["all_channels"][1], "%")
    print("useful_si", " = ", report_dict["useful_si"][0], ", ", report_dict["useful_si"][1], "%")
    print("useful_metal", " = ", report_dict["useful_metal"][0], ", ", report_dict["useful_metal"][1], "%")
    print("blanks", " = ", report_dict["blanks"][0], ", ", report_dict["blanks"][1], "%")


def return_report(report_dict):
    alloy = "alloy = " + str(report_dict["useful_alloy"][1]) + "%" + '\n'
    channels = "channels = " + str(report_dict["all_channels"][1]) + "%" + '\n'
    useful_si = "useful_si = " + str(report_dict["useful_si"][1]) + "%" + '\n'
    useful_metal = "useful_metal = " + str(report_dict["useful_metal"][1]) + "%" + '\n'
    blanks = "blanks = " + str(report_dict["blanks"][1]) + "%"
    return alloy + channels + useful_si + useful_metal + blanks


def show_solution(picture):
    im = Image.open("images/" + picture + "[solution].jpg")
    im.show()


def show_chart(picture):
    im = Image.open("images/" + picture + "[chart].jpg")
    im.show()


def show_report_chart():
    im = Image.open("images/report[chart].jpg")
    im.show()


def show_final_picture():
    im = Image.open("images/final.jpg")
    im.show()
