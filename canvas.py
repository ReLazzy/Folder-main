colors = {
    "P": (0, 0, 255),
    "N": (255, 0, 0),
    "NA": (255, 0, 0),
    "SI": (0, 255, 110),
    "SN": (173, 255, 47),
    "SP": (127, 255, 212),
    "M2": (0, 191, 255),
    "M1": (255, 215, 0),
    "CM1": (255, 215, 0),
    "CNA": (255, 0, 0),
    "CPA": (0, 0, 255),
    "CPE": (0, 0, 255),
    "CNE": (255, 0, 0),
    "B1": (0, 0, 0),
    "KN": (0, 0, 0),
    "CSI": (0, 0, 0),
    "CW": (0, 0, 0),
    "P_TRANSISTORS": (0, 0, 255),
    "N_TRANSISTORS": (255, 0, 0),
    "P_CHANNELS": (127, 255, 212),
    "N_CHANNELS": (173, 255, 47),
    "M2_METAL": (0, 191, 255),
    "M1_METAL": (255, 215, 0),
    "BORDER_RECT": (0, 0, 0),
}


def draw_border(rect, draw):
    draw.rectangle(
        (rect.right, rect.top, rect.left, rect.bottom),
        outline=(0, 0, 0),
        width=3,
    )


def draw_layer(rects, layer, draw):
    for a in rects[layer]:
        draw.rectangle((a.left, a.bottom, a.right, a.top), outline=colors[layer], width=2)


def draw_rects(rects, color, opacity, draw):
    for a in rects:
        draw.rectangle(
            (a.left, a.bottom, a.right, a.top),
            fill=(colors[color] + (opacity,)),
            outline=(colors[color]),
            width=2,
        )


def fill_rects(rects, color, draw):
    for a in rects:
        draw.rectangle(
            (a.left, a.bottom, a.right, a.top),
            fill=color,
            outline=color,
            width=0,
        )


def draw_chosen_layers(key_dict, adj_rects, draw):
    for a in key_dict:
        if key_dict[a]:
            draw_layer(adj_rects, a, draw)


def draw_chosen_elements(key_dict, elements_dict, draw):
    for a in key_dict:
        if key_dict[a]:
            draw_rects(elements_dict[a], a, 127, draw)


def draw_si_connections(rects, n_channels, p_channels, draw):
    draw_rects(rects["SI"], "SI", 127, draw)
    draw_rects(rects["SP"], "SI", 127, draw)
    draw_rects(rects["SN"], "SI", 127, draw)
    fill_rects(n_channels, (255, 255, 255), draw)
    fill_rects(p_channels, (255, 255, 255), draw)

    # fill_rects(rects["SI"], colors["SI"], draw)
    # fill_rects(rects["SP"], colors["SI"],  draw)
    # fill_rects(rects["SN"], colors["SI"],  draw)
    # fill_rects(n_channels, (255, 255, 255), draw)
    # fill_rects(p_channels, (255, 255, 255), draw)


def draw_frame(layers_keys_dict, adj_rects, draw):
    draw_chosen_layers(layers_keys_dict, adj_rects, draw)


def draw_chosen_elements(elements_keys_dict, elements_dict, adj_rects, border_rect, draw):
    for a in elements_keys_dict:
        if elements_keys_dict[a]:
            if a == "SI_CONNECTIONS":
                draw_si_connections(adj_rects, elements_dict["N_CHANNELS"], elements_dict["P_CHANNELS"], draw)
            elif a == "BORDER_RECT":
                draw_border(border_rect, draw)
            else:
                draw_rects(elements_dict[a], a, 127, draw)
