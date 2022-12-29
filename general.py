import os

import converter
import reader
import utils
from rect import Rect


# ======================= ПО НАЖАТИЮ КНОПКИ "РАССЧИТАТЬ СХЕМУ" ======================


# return workspace directory
def calculate_scheme(data_path):
    workspace_dir = os.getcwd()
    images_path = '/images'
    # read arrays from file
    result = reader.read(data_path)

    # conversion into rectangles
    rects = converter.getRectsFromPoints(result)

    min_left, min_bottom, max_right, max_top, width, height = utils.get_canvas_size(rects)

    adj_rects, width, height = utils.adjust_coordinates(rects, width, height, min_left, min_bottom, 5)

    left_border, bottom_border, right_border, top_border = utils.get_borders(adj_rects)
    border_rect = Rect(top_border, bottom_border, right_border, left_border)

    adj_rects = utils.filter_by_border(adj_rects, border_rect)

    # расчет всех нужных элементов схемы
    elements_dict = utils.get_all_elements(adj_rects, border_rect)

    # utils.print_all_elements(elements_dict)

    # проверяем есть ли папка /images
    if not os.path.exists(workspace_dir + images_path):
        os.mkdir(workspace_dir + images_path)

    # расчет площадей (здесь параллельно создаются промежуточные картинки, которые сохраняются в папку images)
    squares_dict, report_dict = utils.get_all_squares(elements_dict, adj_rects, width, height)

    # заполнение картежа с выходными данными
    importantDirect = {
        "elements_dict": elements_dict,
        "adj_rects": adj_rects,
        "border_rect": border_rect,
        "width": width,
        "height": height,
        "report_dict": report_dict,
        "squares_dict": squares_dict,
    }
    return importantDirect
    # вывод ВСЕГО в консольку
    # utils.print_squares(squares_dict)

    # вывод площади одной хуйнюшки в консольку (пригодится для вывода процентов в центральную часть программы)

    # пока всё это считается, в центральной части окна крутится гифка
    # когда все рассчиталось, в центральной части окна появляется инфа о схеме, где можно нажать кнопку "Показать на картинке",
    # при нажатии на которую будет вызываться функция, соответствующая выбранному элементу из выпадающего списка, например:
    # utils.show_solution("all_metal")

    # это круговые диаграммы, их надо впихнуть на их место в интерфейсе
    # но пока что они просто показываются так же, как картинки
    # utils.show_chart("all_metal")

    # utils.print_report(report_dict)
    # utils.show_report_chart()

# ======================= ПО НАЖАТИЮ КНОПКИ "НАРИСОВАТЬ КАРТИНКУ" ======================
#
# im = Image.new("RGB", (width, height), (255, 255, 255))
# draw = ImageDraw.Draw(im, "RGBA")
#
# # собираем левые чекбоксы
#
#
# # функция рисования контуров слоёв
# canvas.draw_frame(layers_keys_dict, adj_rects, draw)
#
# # собираем правые чекбоксы
# elements_keys_dict = {
#     "SI_CONNECTIONS": True,
#     "P_TRANSISTORS": True,
#     "N_TRANSISTORS": True,
#     "P_CHANNELS": True,
#     "N_CHANNELS": True,
#     "M1_METAL": True,
#     "M2_METAL": True,
#     "BORDER_RECT": True,
# }
#
# # формирование итоговой цветной картинки
# canvas.draw_chosen_elements(elements_keys_dict, elements_dict, adj_rects, border_rect, draw)
#
# im = im.rotate(180).transpose(Image.Transpose.FLIP_LEFT_RIGHT)
#
# im.save("images/final.jpg", quality=95)
#
# # вывод финальной картиночки
# utils.show_final_picture()
