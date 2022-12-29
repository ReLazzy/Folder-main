import os
from tkinter import *
from tkinter import filedialog as fd
from tkinter.messagebox import showerror, showwarning, showinfo
import canvas
from tkinter import ttk
import time

from PIL import Image, ImageTk, ImageDraw

import general
import utils

flag = False


class ChooseFileBtn:
    def __init__(self, root, side, file_path_textbox):
        self.b = ttk.Button(root, text='Выбрать файл', style='My.TButton')
        self.b.bind('<Button-1>', lambda event, path=file_path_textbox: self.callback(event, path))
        self.b.pack(side=side)
        self.path_str = 'data/invertor2.cif'

    def callback(self, event, file_path_textbox):
        self.path_str = fd.askopenfilename()
        file_path_textbox.delete(0, END)
        file_path_textbox.insert(0, self.path_str)


class ShowSolutionBtn:
    def __init__(self, root, side, chosen_elem):
        self.b = ttk.Button(root, text='Показать решение', style='My.TButton', width=16)
        self.b.bind('<Button-1>', lambda event: self.callback(event))
        self.elem = chosen_elem
        self.b.pack(side=side, pady=10)

    def callback(self, event):
        if self.elem != "report":
            im = Image.open("images/" + self.elem + "[solution].jpg")
            im.show()


class CalculateBtn:
    def __init__(self, root, side, file_btn, root_frame, list_keys):
        self.b = ttk.Button(root, text='Рассчитать схему', style='My.TButton', width=43)
        self.b.bind('<Button-1>',
                    lambda event, file=file_btn, root_frame=root_frame, list_keys=list_keys: self.callback(event, file,
                                                                                                           root_frame,
                                                                                                           list_keys))
        self.b.pack(side=side)
        self.importantDict = {}

    def callback(self, event, file, root_frame, list_keys):
        global flag

        self.b.config(text='Выполняется расчет...')

        try:
            showinfo(title="MIR", message="Выполняется расчет, пожалуйста подождите")
            self.importantDict = general.calculate_scheme(file.path_str)
            create_frame(root_frame, list_keys, self.importantDict)

        except:
            showerror(title="MIR", message="Упс, произошла ошибка")

        self.b.config(text='Рассчитать схему')


class ChosenComBox:
    def __init__(self, root, list_keys, side, chart_holder, importantDict, label, button):
        self.chosen_elem = StringVar(value='all_trans')
        self.combobox = ttk.Combobox(root, textvariable=self.chosen_elem)
        self.combobox['values'] = list_keys
        self.combobox['state'] = 'readonly'

        self.img = Image.open('images/' + 'all_trans' + '[chart].jpg')
        self.img = self.img.resize((300, 300), Image.Resampling.LANCZOS)
        self.chart_image = ImageTk.PhotoImage(self.img)

        chart_holder['image'] = self.chart_image

        label['text'] = str(importantDict['squares_dict'][str(self.chosen_elem.get())][1]) + " %"

        self.combobox.bind("<<ComboboxSelected>>",
                           lambda event, img=chart_holder, label=label, squares_dict=importantDict['squares_dict'],
                                  button=button, report_dict=importantDict['report_dict']: self.callback(event,
                                                                                                         img,
                                                                                                         label,
                                                                                                         squares_dict,
                                                                                                         button,
                                                                                                         report_dict))
        self.combobox.pack(side=side)

    def callback(self, event, img, label, squares_dict, button, report_dict):
        print(str(event.widget.get()))
        self.img = Image.open('images/' + str(event.widget.get()) + '[chart].jpg')
        self.img = self.img.resize((300, 300), Image.Resampling.LANCZOS)
        self.chart_image = ImageTk.PhotoImage(self.img)
        img['image'] = self.chart_image
        button.elem = str(event.widget.get())
        print(button.elem)
        if (str(event.widget.get()) == 'report'):
            button.b['state'] = 'disabled'
            percents = utils.return_report(report_dict)
            label['font'] = 'helvetica 12'
        else:
            button.b['state'] = 'normal'
            percents = str(squares_dict[str(self.chosen_elem.get())][1]) + " %"
        label['text'] = percents


class LineFrame:
    def __init__(self, root, pady=0, padx=0, width=600, height=0, side=TOP):
        self.line = Frame(root, background='#004D40', width=width, height=height)
        self.line.pack(pady=pady, padx=padx, side=side)


class CheckBox:
    def __init__(self, root, side, key, checkboxes_dict):
        self.var = BooleanVar()
        self.var.set(int(checkboxes_dict[key]))
        self.key = key
        self.checkbox = ttk.Checkbutton(root, text=self.key, style="My.TCheckbutton",
                                        variable=self.var,
                                        onvalue=1, offvalue=0,
                                        command=lambda checkboxes_dict=checkboxes_dict: self.show(
                                            checkboxes_dict))
        self.checkbox.pack(anchor=W, side=side, pady=10, padx=10)

    def show(self, checkboxes_dict):
        checkboxes_dict[self.key] = bool(self.var.get())


class ShowFinalBtn:
    def __init__(self, root, side, importantDict, layers_keys_dict, color_keys_dict):
        self.b = ttk.Button(root, text='Нарисовать картинку', style='My.TButton', width=43)
        self.b.bind('<Button-1>', lambda event, importantDict=importantDict, layers_keys_dict=layers_keys_dict,
                                         color_keys_dict=color_keys_dict: self.callback(event, importantDict,
                                                                                        layers_keys_dict,
                                                                                        color_keys_dict))

        self.b.pack(side=side)

    def callback(self, event, importantDict, layers_keys_dict, colors_keys_dict):
        im = Image.new("RGB", (importantDict['width'], importantDict["height"]), (255, 255, 255))
        draw = ImageDraw.Draw(im, "RGBA")
        canvas.draw_frame(layers_keys_dict, importantDict["adj_rects"], draw)

        canvas.draw_chosen_elements(colors_keys_dict, importantDict["elements_dict"], importantDict["adj_rects"],
                                    importantDict["border_rect"], draw)

        im = im.rotate(180).transpose(Image.Transpose.FLIP_LEFT_RIGHT)

        im.save("images/final.jpg", quality=95)

        # вывод финальной картиночки
        im.show()


# def create_diagrams_block():
list_keys = (
    "n_trans",
    "p_trans",
    "all_trans",
    "n_channels",
    "p_channels",
    "all_channels",
    "m1_metal",
    "m2_metal",
    "all_metal",
    "si",
    "scheme",
    "borders",
    "blanks",
    "report",
)

layers_keys_dict_first = {
    "NA": True,
    "P": True,
    "SI": True,
    "SN": True,
    "SP": True,
    "M2": True,
    "M1": True,
    "CM1": False,
}
# # собираем левые чекбоксы
layers_keys_dict_second = {
    "CNA": False,
    "CPA": False,
    "CPE": False,
    "CNE": False,
    "B1": False,
    "KN": False,
    "CSI": False,
    "CW": False,
}
# собираем правые чекбоксы
elements_keys_dict = {
    "SI_CONNECTIONS": True,
    "P_TRANSISTORS": True,
    "N_TRANSISTORS": True,
    "P_CHANNELS": True,
    "N_CHANNELS": True,
    "M1_METAL": True,
    "M2_METAL": True,
    "BORDER_RECT": False,
}


def create_checkbox_list(root, checkboxes_list, keys_dict):
    for a in keys_dict:
        checkboxes_list.append(CheckBox(root, TOP, a, keys_dict))


def create_frame(root, list_keys, importantDict):
    middle_frame = Frame(root, width=550)
    chart_image_frame = Frame(middle_frame)
    charts_menu_frame = Frame(middle_frame)

    chart_holder = ttk.Label(chart_image_frame)

    label_percents = ttk.Label(charts_menu_frame, font='helvetica 20', foreground="#004D40")
    button = ShowSolutionBtn(charts_menu_frame, TOP, 'all_trans')
    combox = ChosenComBox(charts_menu_frame, list_keys, TOP, chart_holder, importantDict,
                          label_percents, button)

    chart_holder.pack(side=TOP)
    label_percents.pack(side=TOP, pady=10)
    middle_frame.pack(side=TOP)
    chart_image_frame.pack(side=LEFT)
    charts_menu_frame.pack(side=RIGHT, padx=10)
    lineFrame = LineFrame(root, pady=10, side=TOP)

    bottom_frame = Frame(root, width=550)
    outline_checkboxes_frame = Frame(bottom_frame)
    outline_checkboxes_frame_first = Frame(outline_checkboxes_frame)
    outline_checkboxes_frame_second = Frame(outline_checkboxes_frame)
    color_checkboxes_frame = Frame(bottom_frame)

    outline_text_label = ttk.Label(outline_checkboxes_frame, text="Контуры:", foreground="#004D40", font="helvetica 14")
    color_text_label = ttk.Label(color_checkboxes_frame, text="Закрасить:", foreground="#004D40", font="helvetica 14")

    outline_checkboxes_list_first = []
    outline_checkboxes_list_second = []
    color_checkboxes_list = []

    outline_text_label.pack(side=TOP, pady=10)
    color_text_label.pack(side=TOP, pady=10)

    create_checkbox_list(outline_checkboxes_frame_first, outline_checkboxes_list_first, layers_keys_dict_first)
    create_checkbox_list(outline_checkboxes_frame_second, outline_checkboxes_list_second, layers_keys_dict_second)
    create_checkbox_list(color_checkboxes_frame, color_checkboxes_list, elements_keys_dict)

    outline_checkboxes_frame_first.pack(side=LEFT)
    outline_checkboxes_frame_second.pack(side=RIGHT)

    outline_checkboxes_frame.pack(side=LEFT)
    vertical_line = LineFrame(bottom_frame, padx=10, width=0, height=200, side=LEFT)
    color_checkboxes_frame.pack(side=BOTTOM)

    bottom_frame.pack(side=TOP, pady=10)
    final_btn = ShowFinalBtn(root, TOP, importantDict, layers_keys_dict_first | layers_keys_dict_second,
                             elements_keys_dict)
    def on_closing():
        print("Выводится при попытке закрытия окна2")
        root.destroy()
        

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
    print("[f[f]] при попытке закрытия окна2")




def main():
    global flag
    global list_keys
    workspace_dir = os.getcwd()

    window = Tk()
    window.title("Добро пожаловать в MIR")
    window.geometry('700x950')

    choose_btn_style = ttk.Style()
    checkbox_style = ttk.Style()

    top_frame = Frame(window, width=550)
    file_search_frame = Frame(top_frame)

    checkbox_style.configure("My.TCheckbutton", font="helvetica 10",  # шрифт
                             foreground="#004D40", )
    choose_btn_style.configure("My.TButton",  # имя стиля
                               font="helvetica 12",  # шрифт
                               foreground="#004D40",  # цвет текста
                               padding=10,
                               width=14,
                               # отступы
                               background="#B2DFDB",

                               )  # фоновый цвет

    lbl = Label(file_search_frame, text="Файл", font="helvetica 14", foreground="#004D40", )
    lbl.pack(side=LEFT)

    file_path_textbox = ttk.Entry(file_search_frame, font="helvetica 12",
                                  foreground="#004D40", )
    file_path_textbox.pack(side=LEFT, padx=10, pady=0)
    file_path_textbox.insert(0, 'Введите путь к файлу')

    file_search_frame.pack(side=TOP, padx=10, pady=10)

    btn_file_dir = ChooseFileBtn(file_search_frame, LEFT, file_path_textbox)
    btn_calc = CalculateBtn(top_frame, TOP, btn_file_dir, window, list_keys)

    top_frame.pack(side=TOP)

    line_frame1 = LineFrame(window, pady=10, side=TOP)

    def on_closing():
        print("Выводится при попытке закрытия окна")
        window.destroy()  # Закрыть окно

    window.protocol("WM_DELETE_WINDOW", on_closing)
    window.mainloop()


if __name__ == '__main__':
    main()
