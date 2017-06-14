# -*- coding: utf-8 -*-
from Tkinter import *
from tkFileDialog import *
from lxml import etree
from shutil import copyfile

import ttk
from tkColorChooser import askcolor
import Tkinter as Tk
import sys
import datetime
import re
import os
import calendar
import tkMessageBox

try:
    import scribus
    from scribus import *
except ImportError:
    print('This Python script is written for the Scribus scripting interface.')

# Translation day/month
localization = {
    'Catalan':
        [['Gener', 'Febrer', 'Març', 'Abril', 'Maig',
          'Juny', 'Juliol', 'Agost', 'Setembre',
          'Octubre', 'Novembre', 'Desembre'],
         ['Dilluns', 'Dimarts', 'Dimecres', 'Dijous', 'Divendres', 'Dissabte', 'Diumenge']],
    'Catalan-short':
        [['Gener', 'Febrer', 'Març', 'Abril', 'Maig',
          'Juny', 'Juliol', 'Agost', 'Setembre',
          'Octubre', 'Novembre', 'Desembre'],
         ['Dl', 'Dm', 'Dc', 'Dj', 'Dv', 'Ds', 'Dg']],
    # Catalan by "Cesc Morata" <atarom@gmail.com>
    'Czech':
        [['Leden', 'Únor', 'Březen', 'Duben', 'Květen',
          'Červen', 'Červenec', 'Srpen', 'Září',
          'Říjen', 'Listopad', 'Prosinec'],
         ['Pondělí', 'Úterý', 'Středa', 'Čtvrtek', 'Pátek', 'Sobota', 'Neděle']],
    'Czech-short':
        [['Leden', 'Únor', 'Březen', 'Duben', 'Květen',
          'Červen', 'Červenec', 'Srpen', 'Září',
          'Říjen', 'Listopad', 'Prosinec'],
         ['Po', 'Út', 'St', 'Čt', 'Pá', 'So', 'Ne']],
    # Croatian by daweed
    'Croatian':
        [['Siječanj', 'Veljača', 'Ožujak', 'Travanj', 'Svibanj',
          'Lipanj', 'Srpanj', 'Kolovoz', 'Rujan',
          'Listopad', 'Studeni', 'Prosinac'],
         ['Ponedjeljak', 'Utorak', 'Srijeda', 'Četvrtak', 'Petak', 'Subota', 'Nedjelja']],

    'Dutch':
        [['Januari', 'Februari', 'Maart', 'April',
          'Mei', 'Juni', 'Juli', 'Augustus', 'September',
          'Oktober', 'November', 'December'],
         ['Maandag', 'Dinsdag', 'Woensdag', 'Donderdag', 'Vrijdag', 'Zaterdag', 'Zondag']],
    # Dutch by "Christoph Schäfer" <christoph-schaefer@gmx.de>
    'English':
        [['January', 'February', 'March', 'April',
          'May', 'June', 'July', 'August', 'September',
          'October', 'November', 'December'],
         ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']],
    'English-short':
        [['January', 'February', 'March', 'April', 'May',
          'June', 'July', 'August', 'September', 'October',
          'November', 'December'],
         ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']],
    'Finnish':
        [['Tammikuu', 'Helmikuu', 'Maaliskuu', 'Huhtikuu',
          'Toukokuu', 'Kesäkuu', 'Heinäkuu', 'Elokuu', 'Syyskuu',
          'Lokakuu', 'Marraskuu', 'Joulukuu'],
         ['ma', 'ti', 'ke', 'to', 'pe', 'la', 'su']],
    'French':
        [['Janvier', u'F\xe9vrier', 'Mars', 'Avril',
          'Mai', 'Juin', 'Juillet', u'Ao\xfbt', 'Septembre',
          'Octobre', 'Novembre', u'D\xe9cembre'],
         ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']],
    'German':
        [['Januar', 'Februar', u'M\xe4rz', 'April',
          'Mai', 'Juni', 'Juli', 'August', 'September',
          'Oktober', 'November', 'Dezember'],
         ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']],
    'German (Austrian)':
        [[u'J\xe4nner', 'Feber', u'M\xe4rz', 'April',
          'Mai', 'Juni', 'Juli', 'August', 'September',
          'Oktober', 'November', 'Dezember'],
         ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']],
    # Hungarian by Gergely Szalay szalayg@gmail.com
    'Hungarian':
        [['Január', 'Február', 'Március', 'Április',
          'Május', 'Június', 'Július', 'Augusztus', 'Szeptember',
          'Október', 'November', 'December'],
         ['Hétfő', 'Kedd', 'Szerda', 'Csütörtök', 'Péntek', 'Szombat', 'Vasárnap']],
    'Italian':
        [['Gennaio', 'Febbraio', 'Marzo', 'Aprile',
          'Maggio', 'Giugno', 'Luglio', 'Agosto', 'Settembre',
          'Ottobre', 'Novembre', 'Dicembre'],
         [u'Luned\xec', u'Marted\xec', u'Mercoled\xec', u'Gioved\xec', u'Venerd\xec', 'Sabato', 'Domenica']],
    # Norwegian by Joacim Thomassen joacim@net.homelinux.org
    'Norwegian':
        [['Januar', 'Februar', 'Mars', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November',
          'Desember'],
         ['Mandag', 'Tirsdag', 'Onsdag', 'Torsdag', 'Fredag', 'Lørdag', 'Søndag']],
    # Polish by "Łukasz [DeeJay1] Jernaś" <deejay1@nsj.srem.pl>
    'Polish':
        [['Styczeń', 'Luty', 'Marzec', 'Kwiecień', 'Maj',
          'Czerwiec', 'Lipiec', 'Sierpień', 'Wrzesień',
          'Październik', 'Listopad', 'Grudzień'],
         ['Poniedziałek', 'Wtorek', 'Środa', 'Czwartek', 'Piątek', 'Sobota', 'Niedziela']],
    'Portuguese':
        [['Janeiro', 'Fevereiro', u'Mar\xe7o', 'Abril',
          'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro',
          'Outubro', 'Novembro', 'Dezembro'],
         ['Segunda-feira', u'Ter\xe7a-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', u'S\xe1bado', 'Domingo']],
    # Romanian by Costin Stroie <costinstroie@eridu.eu.org>
    'Romanian':
        [['Ianuarie', 'Februarie', 'Martie', 'Aprilie',
          'Mai', 'Iunie', 'Iulie', 'August', 'Septembrie',
          'Octombrie', 'Noiembrie', 'Decembrie'],
         ['Luni', 'Mar\xc8\x9bi', 'Miercuri', 'Joi', 'Vineri', 'S\xc3\xa2mb\xc4\x83t\xc4\x83', 'Duminic\xc4\x83']],
    'Russian':
        [['Январь', 'Февраль', 'Март', 'Апрель',
          'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь',
          'Октябрь', 'Ноябрь', 'Декабрь'],
         ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']],
    'Slovak':
        [['Január', 'Február', 'Marec', 'Apríl',
          'Máj', 'Jún', 'Júl', 'August', 'September',
          'Október', 'November', 'December'],
         ['Pondelok', 'Utorok', 'Streda', 'Štvrtok', 'Piatok', 'Sobota', 'Nedeľa']],
    'Slovak-short':
        [['Január', 'Február', 'Marec', 'Apríl',
          'Máj', 'Jún', 'Júl', 'August', 'September',
          'Október', 'November', 'December'],
         ['Po', 'Ut', 'St', 'Št', 'Pi', 'So', 'Ne']],
    'Spanish':
        [['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo',
          'Junio', 'Julio', 'Agosto', 'Septiembre',
          'Octubre', 'Noviembre', 'Diciembre'],
         ['Lunes', 'Martes', u'Mi\xe9rcoles', 'Jueves', 'Viernes', u'S\xe1bado', 'Domingo']],
    'Swedish':
        [['Januari', 'Februari', 'Mars', 'April', 'Maj', 'Juni', 'Juli', 'Augusti', 'September', 'Oktober', 'November',
          'December'],
         ['Måndag', 'Tisdag', 'Onsdag', 'Torsdag', 'Fredag', 'Lördag', 'Söndag']]
}

size_document = {
    'A0': [2383.94, 3370.39], 'A1': [1683.78, 2383.94], 'A2': [1190.55, 1683.78], 'A3': [841.89, 1190.55],
    'A4': [595.28, 841.89], 'A5': [419.53, 595.28], 'A6': [297.64, 419.53], 'A7': [209.76, 297.64],
    'A8': [147.40, 209.76], 'A9': [104.88, 147.40], 'B0': [2834.65, 4008.19], 'B1': [2004.09, 2834.65],
    'B2': [1417.32, 2004.09], 'B3': [1000.63, 1417.32], 'B4': [708.66, 1000.63], 'B5': [498.90, 708.66],
    'B6': [354.33, 498.90], 'B7': [249.45, 354.33], 'B8': [175.75, 249.45], 'B9': [124.72, 175.75],
    'B10': [87.87, 124.72], 'COMM10E': [297.00, 684.00], 'DLE': [311.81, 623.62], 'LEGAL': [612.00, 1008.00],
    'LETTER': [612.00, 792.00]
}

sizex = 650
sizey = 350
posx = 300
posy = 200


def show_error(err):
    tkMessageBox.showinfo('Error', err)


class BoxObject:
    """ BoxObject represent some attribute from PAGEOBJECT from scribus file. """
    def __init__(self, xpos, ypos, width, height, anname, img=False, font='', font_style='', font_size='', color=''):
        self.xpos = xpos
        self.ypos = ypos
        self.width = width
        self.height = height
        self.anname = anname
        self.img = img
        self.font = font
        self.font_style = font_style
        self.font_size = font_size
        self.color = color

    def attrib_font(self, font, font_style, font_size, color):
        self.font = font
        self.font_style = font_style
        self.font_size = font_size
        self.color = color


class Document:
    """ Document contains all attribute useful about master page, margin, etc."""
    def __init__(self, path_file, lang, first_day, size):
        self.path_file = path_file
        self.lang = lang
        self.day_order = localization[self.lang][1]

        if first_day == calendar.SUNDAY:
            dl = self.day_order[:6]
            dl.insert(0, self.day_order[6])
            self.day_order = dl
        self.mycal = calendar.Calendar(first_day)

        self.pagex = 0.0
        self.pagey = 0.0
        self.page_width = 0.0
        self.page_height = 0.0
        self.border_left = 0.0
        self.border_right = 0.0
        self.border_top = 0.0
        self.border_bottom = 0.0
        self.size = size
        self.orientation = IntVar()
        self.nb_day_usual_week = 7
        self.begin_day = 0
        self.nb_days = 0
        self.nb_week = 0

        self.box_container = []

        self.doc_parsing()

    def doc_parsing(self):
        # parse le fichier selectionne
        tree = etree.parse(self.path_file)
        # ecrit dans box_container les objets du model
        # les objets recoivent les attributs des PAGEOBJECT tel que la taille, la position et le nom
        for val in tree.xpath("/SCRIBUSUTF8NEW/DOCUMENT/MASTERPAGE"):
            self.pagex = float(val.get("PAGEXPOS"))
            self.pagey = float(val.get("PAGEYPOS"))
            self.page_width = float(val.get("PAGEWIDTH"))
            self.page_height = float(val.get("PAGEHEIGHT"))
            self.orientation = int(val.get("Orientation"))
            self.border_left = float(val.get("BORDERLEFT"))
            self.border_right = float(val.get("BORDERRIGHT"))
            self.border_top = float(val.get("BORDERTOP"))
            self.border_bottom = float(val.get("BORDERBOTTOM"))
            # self.size = str(val.get("Size"))

        for val in tree.xpath("/SCRIBUSUTF8NEW/DOCUMENT/PAGEOBJECT"):
            if val.get("ANNAME") == "image_box":
                new = BoxObject(float(val.get("XPOS")) - self.pagex, float(val.get("YPOS")) - self.pagey,
                                float(val.get("WIDTH")), float(val.get("HEIGHT")), val.get("ANNAME"), True)
            else:
                new = BoxObject(float(val.get("XPOS")) - self.pagex, float(val.get("YPOS")) - self.pagey,
                                float(val.get("WIDTH")), float(val.get("HEIGHT")), val.get("ANNAME"))
            self.box_container.append(new)

    def set_month(self, year, month):
        # Returns weekday of first day of the month and number of days in month, for the specified year and month
        (self.begin_day, self.nb_days) = calendar.monthrange(year, month)
        # Calcule le nombre de semaine du mois courant
        self.nb_week = 1
        spend_days = 0
        i = self.begin_day
        while spend_days < self.nb_days:
            if i >= 7:
                i = 0
                self.nb_week += 1
            spend_days += 1
            i += 1


class TkCalendar(Tk.Frame):
    # update the current page of the wizard
    def update(self):
        # print(self.frame_master_current_page)  # show in terminal the number of the current page

        if self.frame_master_current_page == 1:
            # months
            # a suprimer
            self.frame2_listbox_language.select_set(9)
            self.action_get_language(None)
            if len(self.frame2_config_month_string_selected) == 0:
                tkMessageBox.showinfo("Error", "At least one month must be selected.")
                self.action_decrement()
                return

        self.frame_master_all_frames[self.frame_master_last_page].pack_forget()  # remove the last current page

        # If page == 2
        if self.frame_master_current_page == 2:
            if self.frame1_config_model_name != '':
                type_ele = re.compile('element=\'(.*)\'')
                tree = etree.parse(self.frame1_config_model_path + self.frame1_config_model_name)
                keys = tree.getroot()
                for key in keys:
                    val = key.attrib['KEYWORDS']
                elements = re.findall(type_ele, val)
                self.frame3_listbox_font_elements = re.split(",", elements[0])
                # print(self.frame3_listbox_font_elements)
                self.frame3_listbox_font.delete(0, END)
                for i in self.frame3_listbox_font_elements:
                    self.frame3_listbox_font.insert(END, i)
            # print self.frame3_listbox_font_elements
            for i, val in enumerate(self.frame3_listbox_font_elements):
                self.font_list[val] = []
                self.font_list[val].append(self.font_var.get())
                self.font_list[val].append(self.font_style_var.get())
                self.font_list[val].append(self.font_size)
                self.font_list[val].append(self.font_color.get())
            # print self.font_list

        # if page == 1
        if self.frame_master_current_page <= 0:
            self.frame_master_current_page = 0
            self.bottom_button[0].config(state=DISABLED)
            self.bottom_button[2].config(state=DISABLED)
        else:
            if self.frame_master_current_page >= self.frame_master_max_page - 1:
                self.frame_master_current_page = self.frame_master_max_page - 1
                self.bottom_button[1].config(state=DISABLED)
                self.bottom_button[2].config(state=ACTIVE)
            else:
                self.bottom_button[1].config(state=ACTIVE)
                self.bottom_button[2].config(state=DISABLED)
                self.bottom_button[0].config(state=ACTIVE)

        self.frame_master_all_frames[self.frame_master_current_page].pack()
        self.frame_master_last_page = self.frame_master_current_page
        self.canvas.yview_moveto(0.0)
        self.scrollbar_middle.set(0.0, 1.0)

    # import file .sla
    def action_import_model(self):
        try:
            filename = askopenfilename(title="Open your file",
                                       filetypes=[('scribus files', '.sla'), ('all files', '.*')])
            if filename is None:
                raise ValueError
            copyfile(filename, self.frame1_config_model_path + os.path.basename(filename))
        except Exception as e:
            show_error("Can not import file. Err :" + str(e))

    # import an ICS file
    def action_import_ics(self):
        try:
            filename = askopenfilename(title="Open your file",
                                       filetypes=[('ics files', '.ics'), ('all files', '.*')])
            if filename is None:
                raise ValueError
            ics_file = open(filename, "r")
            self.frame2_config_file_i_c_s = ics_file.read()
            ics_file.close()
        except Exception as e:
            show_error("Can not import file. Err :" + str(e))

    # go to next page
    def action_increment(self):
        self.frame_master_current_page = self.frame_master_current_page + 1
        self.update()

    # go to previous page
    def action_decrement(self):
        self.frame_master_current_page = self.frame_master_current_page - 1
        self.update()

    # get all elements of the wizard inside a canvas.
    def action_canvas(self, event):
        tup = self.scrollbar_middle.get()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        if tup[0] == 0 and tup[1] == 1:
            self.canvas.yview_moveto(0.0)

    # define the scroll
    def action_mouse_weel(self, event):
        if event.num == 5:
            event.delta = -120
        elif event.num == 4:
            event.delta = 120
        print(datetime.datetime.now())
        tup = self.scrollbar_middle.get()
        if tup[0] != 0 or tup[1] != 1:
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        print(event.num)

    # update preview with the selected model
    def action_get_models(self, event):
        # get selected line index
        self.model_index_selected = self.frame1_listbox_models.curselection()[0]
        self.frame1_config_model_name = self.frame1_listbox_models.get(self.model_index_selected)
        model_name = self.frame1_config_model_name[0:-4]

        try:
            self.photo = PhotoImage(file="format/" + model_name + ".png")
            self.previewCanvas.itemconfigure(self.photo_img, image=self.photo, anchor=NW)
            self.previewCanvas.image = self.photo
        except Exception as e:
            show_error("Can not update image from model. Err :" + str(e))

    # update the list of months with the right language
    def action_get_language(self, event):
        # get selected line index
        self.frame2_config_language_index_selected = self.frame2_listbox_language.curselection()[0]

        if self.frame2_config_language_index_selected is None:
            return
        months = localization[self.frame2_listbox_language.get(self.frame2_config_language_index_selected)][0]
        self.frame2_config_language_string_selected = self.frame2_listbox_language.get(
            self.frame2_config_language_index_selected)
        self.lang = self.frame2_config_language_string_selected  # used for action_finnish
        self.frame2_listbox_month.delete(0, END)
        for i in months:
            self.frame2_listbox_month.insert(END, i)

        # a suprimer après test
        self.frame2_listbox_month.select_set(8, 9)
        self.action_select_month(None)

    # get selected month
    def action_select_month(self, event):
        self.frame2_config_month_index_selected = self.frame2_listbox_month.curselection()
        self.frame2_config_month_string_selected = []
        for month in self.frame2_config_month_index_selected:
            self.frame2_config_month_index_selected = month
            self.frame2_config_month_string_selected.append(int(month))

    # define title label
    def make_top(self):
        self.top = Frame(self)
        self.top.grid(row=0, column=0)
        self.top_label = Label(self.top, text="Calendar wizard 2")
        self.top_label.pack()

    # define the middle gridPane
    def make_middle(self):
        self.middle = Frame(self, width=sizex-50, height=sizey-50, padx=20, pady=20)
        self.middle.grid(row=1, column=0)

        self.canvas = Canvas(self.middle, width=sizex-50, height=sizey-50)
        self.canvas.pack()

        self.canvas_frame = Frame(self.canvas, width=sizex-50, height=sizey-50, padx=10, pady=10)
        self.canvas_frame.pack(padx=10, pady=10)
        self.canvas_frame.bind("<Configure>", self.action_canvas)

        self.scrollbar_middle = Scrollbar(self.middle, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar_middle.set)

        self.scrollbar_middle.pack(side="right", fill="y")
        self.canvas.pack(side="left")
        self.canvas.create_window((0, 0), window=self.canvas_frame, anchor='nw')

        if sys.platform == "Windows":
            self.canvas.bind_all("<MouseWheel>", self.action_mouse_weel)
        elif sys.platform == "Linux":
            self.canvas.bind_all("<Button-4>", self.action_mouse_weel)
            self.canvas.bind_all("<Button-5>", self.action_mouse_weel)

    def action_select_type(self, event):
        self.frame1_config_type_index_selected = self.frame1_listbox_types.curselection()[0]
        search_type = self.frame1_listbox_types.get(self.frame1_config_type_index_selected)
        self.frame1_config_type_string_selected = search_type
        type_cal = re.compile('type=\'.*' + search_type + '.*\'')
        # On cherche dans le repertoire avec les modeles
        available_models = []

        #  On parcours tous les documents qui se terminent par .sla dans le
        #  repertoire qui contient les modeles
        for model in os.listdir(self.frame1_config_model_path):
            if model.endswith(".sla"):

                #  On parse chaque modele pour voir quels sont les keywords definis
                tree = etree.parse(self.frame1_config_model_path + model)
                keys = tree.getroot()
                for key in keys:
                    val = key.attrib['KEYWORDS']
                    #  Si on trouve un type de calendrier dans les KEYWORDS du document
                    #  on recupere ce modele pour l'afficher dans l'etape suivante
                    avail = re.findall(type_cal, val)
                    if avail:
                        available_models.append(model)
        # print available_models

        self.frame1_listbox_models.delete(0, END)
        for i in available_models:
            self.frame1_listbox_models.insert(END, i)

    # show button Previous, Next, and finnish
    def make_bottom(self):
        self.bottom = Frame(self)
        self.bottom.grid(row=2, column=0)
        self.bottom_button = [Button(self.bottom, text="Previous", padx=10, command=self.action_decrement),
                              Button(self.bottom, text="Next", padx=20, command=self.action_increment),
                              Button(self.bottom, padx=20, text="Finnish", command=self.action_finnish),
                              Button(self.bottom, padx=20, text="Cancel", command=self.quit)]
        for i in range(0, 4):
            self.bottom_button[i].grid(padx=10, pady=10, row=0, column=i)

    def select_all_month(self):
        self.frame2_listbox_month.select_set(0, END)
        self.action_select_month(None)

    def select_all_elements(self):
        self.frame3_listbox_font.select_set(0, END)

    def unselect_all_month(self):
        self.frame2_listbox_month.selection_clear(0, END)
        self.action_select_month(None)

    def get_short_day(self):
        self.short_day_name = bool(self.check_option_short_day.get())

    def get_next_short_day(self):
        self.next_short_day_name = bool(self.check_option_next_short_day.get())

    def get_prev_short_day(self):
        self.prev_short_day_name = bool(self.check_option_prev_short_day.get())

    def get_prev_day(self):
        self.prev_day_name = self.check_option_prev_day.get()

    def get_next_day(self):
        self.next_day_name = self.check_option_next_day.get()

    def action_finnish(self):
        # a virer apres test
        if self.frame1_config_model_name == '':
            self.frame1_config_model_name = 'month-LANDSCAPE.sla'
            # self.frame1_config_model_name = 'month.sla'

        # Create the document with DocumentClass
        my_document = Document(self.frame1_config_model_path + self.frame1_config_model_name, self.lang,
                               self.week_var.get(), self.size.get())

        # resize all box with proportion of new document if orientation or size has been changed:
        if my_document.orientation == 1:
            new_page_size_height, new_page_size_width = size_document[my_document.size]
        else:
            new_page_size_width, new_page_size_height = size_document[my_document.size]

        if my_document.page_height != new_page_size_height and my_document.page_width != new_page_size_width:
            for i in my_document.box_container:
                i.xpos = (new_page_size_width * i.xpos) / my_document.page_width
                i.ypos = (new_page_size_height * i.ypos) / my_document.page_height
                i.width = (new_page_size_width * i.width) / my_document.page_width
                i.height = (new_page_size_height * i.height) / my_document.page_height

            my_document.border_right = (new_page_size_width * my_document.border_right) / my_document.page_width
            my_document.border_bottom = (new_page_size_height * my_document.border_bottom) / my_document.page_height
            my_document.border_left = (new_page_size_width * my_document.border_left) / my_document.page_width
            my_document.border_top = (new_page_size_height * my_document.border_top) / my_document.page_height

        # Attrib all font to right container
        for i in my_document.box_container:
            i.attrib_font(self.font_list[i.anname][0],
                          self.font_list[i.anname][1],
                          self.font_list[i.anname][2],
                          self.font_list[i.anname][3])

        try:
            # Create the Scribus New Document with right proportions
            if not newDocument((size_document[my_document.size][0], size_document[my_document.size][1]),
                               (my_document.border_left, my_document.border_right, my_document.border_top,
                                my_document.border_bottom), my_document.orientation, 1, UNIT_POINTS, NOFACINGPAGES,
                                FIRSTPAGELEFT, 1):
                print 'Create a new document first, please'
                return

            createParagraphStyle(name=self.p_style_date, alignment=ALIGN_RIGHT)
            createParagraphStyle(name=self.p_style_days_box, alignment=ALIGN_RIGHT)
            createParagraphStyle(name=self.p_style_month_box)
            createParagraphStyle(name=self.p_style_week_box, alignment=ALIGN_RIGHT)

            progressTotal(len(self.frame2_config_month_string_selected))
            # run is used for scribus progressbar
            # re-draw from the model
            for run, month in enumerate(self.frame2_config_month_string_selected):
                newPage(-1)
                for i in my_document.box_container:
                    month_variable = month
                    if i.img is False:
                        # init le nombre de semaine et de jour du mois
                        if i.anname[0:4] == "next":
                            month_variable += 1
                            my_document.set_month(self.year_var, month_variable + 1)
                            cal = my_document.mycal.monthdatescalendar(self.year_var, month_variable + 1)
                        elif i.anname[0:4] == "prev":
                            month_variable -= 1
                            if month_variable < 0:
                                year = self.year_var - 1
                                my_document.set_month(year, month_variable+12)
                                cal = my_document.mycal.monthdatescalendar(self.year_var, month_variable+12)
                            else:
                                my_document.set_month(self.year_var, month_variable)
                                cal = my_document.mycal.monthdatescalendar(self.year_var, month_variable)
                        else:
                            my_document.set_month(self.year_var, month_variable + 1)
                            cal = my_document.mycal.monthdatescalendar(self.year_var, month_variable + 1)

                        # draw and fill all days strings
                        if i.anname == "week_box" or i.anname == "next_week_box":
                            for j, name in enumerate(my_document.day_order):
                                cel = createText((j * i.width / my_document.nb_day_usual_week) + i.xpos, i.ypos,
                                                 i.width / my_document.nb_day_usual_week, i.height,
                                                 str(i.anname) + str(run) + '_' + str(j))
                                # setFont(...)
                                # setFontSize(...)
                                print i.font
                                print i.font_size
                                if self.short_day_name is True and i.anname == "week_box" or \
                                   self.next_short_day_name is True and i.anname == "next_week_box" or \
                                   self.prev_short_day_name is True and i.anname == "prev_week_box":
                                    setText(str(name[0:3] + '.'), cel)
                                else:
                                    setText(str(name), cel)
                                setStyle(self.p_style_week_box, cel)
                                selectText(0, 0, str(i.anname) + str(run) + '_' + str(j))
                                setFont(i.font, str(i.anname) + str(run) + '_' + str(j))
                                setFontSize(i.font_size, str(i.anname) + str(run) + '_' + str(j))
                                setTextColor(i.color, str(i.anname) + str(run) + '_' + str(j))
                        # draw and fill all days_box
                        elif i.anname == "days_box" or i.anname == "next_days_box":
                            h = 0
                            st = 0
                            for j, week in enumerate(cal):
                                for day in week:
                                    cel = createText(h * i.width / my_document.nb_day_usual_week + i.xpos,
                                                     j * i.height / my_document.nb_week + i.ypos,
                                                     i.width / my_document.nb_day_usual_week,
                                                     i.height / my_document.nb_week,
                                                     str(i.anname) + str(run) + '_' + str(st))
                                    if self.prev_day_name is 1 and day.month < month_variable + 1:
                                        setText(str(day.day), cel)
                                    if self.next_day_name is 1 and day.month > month_variable + 1:
                                        setText(str(day.day), cel)
                                    if day.month == month_variable + 1:
                                        setText(str(day.day), cel)
                                    setStyle(self.p_style_days_box, cel)
                                    selectText(0, 0, str(i.anname) + str(run) + '_' + str(st))
                                    setFont(i.font, str(i.anname) + str(run) + '_' + str(st))
                                    setFontSize(i.font_size, str(i.anname) + str(run) + '_' + str(st))
                                    setTextColor(i.color, str(i.anname) + str(run) + '_' + str(st))
                                    h += 1
                                    st += 1
                                h = 0
                        elif i.anname == "month_box" or i.anname == "next_month_box":
                            cel = createText(i.xpos, i.ypos, i.width, i.height, str(i.anname) + str(run))
                            setText(localization[self.lang][0][month_variable], cel)
                            setStyle(self.p_style_month_box, cel)
                            selectText(0, 0, str(i.anname) + str(run))
                            setFont(i.font, str(i.anname) + str(run))
                            setFontSize(i.font_size, str(i.anname) + str(run))
                            setTextColor(i.color, str(i.anname) + str(run))
                        # draw and fill name_week_box
                        elif i.anname == "name_week_box" or i.anname == "next_name_week_box":
                            cel = createText(i.xpos, i.ypos, i.width, i.height, str(i.anname) + str(run))
                            setText("#", cel)
                            setStyle(self.p_style_date, cel)
                            selectText(0, 0, str(i.anname) + str(run))
                            setFont(i.font, str(i.anname) + str(run))
                            setFontSize(i.font_size, str(i.anname) + str(run))
                            setTextColor(i.color, str(i.anname) + str(run))
                        # draw and fill all num_week_box
                        elif i.anname == "num_week_box" or i.anname == "next_num_week_box":
                            for j, week in enumerate(cal):
                                cel = createText(i.xpos, j * i.height / my_document.nb_week + i.ypos, i.width,
                                                 i.height / my_document.nb_week, str(i.anname) + str(j) + str(run))
                                # imprime le numéro de la semaine sur l'année
                                setText(str(datetime.date(self.year_var, week[0].month, week[0].day).isocalendar()[1]),
                                        cel)
                                setStyle(self.p_style_date, cel)
                                selectText(0, 0, str(i.anname) + str(j) + str(run))
                                setFont(i.font, str(i.anname) + str(j) + str(run))
                                setFontSize(i.font_size, str(i.anname) + str(j) + str(run))
                                setTextColor(i.color, str(i.anname) + str(j) + str(run))
                        else:
                            cel = createText(i.xpos, i.ypos, i.width, i.height, str(i.anname) + str(run))
                            setText(str(1), cel)
                            setStyle(self.p_style_date, cel)
                            if i.font is not '' and i.font_size is not '':
                                selectText(0, 0, str(i.anname) + str(run))
                                setFont(i.font, str(i.anname) + str(run))
                                setFontSize(i.font_size, str(i.anname) + str(run))
                                setTextColor(i.color, str(i.anname) + str(run))
                    else:
                        createImage(i.xpos, i.ypos, i.width, i.height, str(i.anname) + str(run))
                run += 1
                progressSet(run)
            # delete first empty page
            deletePage(1)

        except Exception as e:
            print e
            self.quit()
        try:
            self.quit()
        except:
            pass
        return

    def my_test(self):
        print size_document[self.size.get()][1]

    def get_year(self):
        self.year_var = int(self.frame2_spinbox_year.get())

    def get_font_size(self):
        self.font_size = int(self.frame3_spinbox_size.get())

    def action_attrib(self):
        try:
            for i in self.frame3_listbox_font.curselection():
                self.font_list[self.frame3_listbox_font_elements[i]] = []
                self.font_list[self.frame3_listbox_font_elements[i]].append(self.font_var.get())
                self.font_list[self.frame3_listbox_font_elements[i]].append(self.font_style_var.get())
                self.font_list[self.frame3_listbox_font_elements[i]].append(self.font_size)
                self.font_list[self.frame3_listbox_font_elements[i]].append(self.font_color.get())
        except:
            print "no"
        print self.font_list

    def make_frames(self):
        # ELEMENT MIDDLE FRAME 1
        frame1_root = Frame(self.canvas_frame)

        frame1_frame_types = Frame(frame1_root)
        frame1_frame_types.grid(row=0, column=0, columnspan=1, sticky=W + E + N + S)
        Label(frame1_frame_types, text="Types").pack(padx=10, pady=10)
        self.frame1_listbox_types = Tk.Listbox(frame1_frame_types, width=20, exportselection=0)
        self.frame1_listbox_types.insert(Tk.END, "Day")
        self.frame1_listbox_types.insert(Tk.END, "Week")
        self.frame1_listbox_types.insert(Tk.END, "Month")
        self.frame1_listbox_types.insert(Tk.END, "Year")
        self.frame1_listbox_types.bind('<<ListboxSelect>>', self.action_select_type)
        self.frame1_listbox_types.pack()

        frame1_frame_models = Frame(frame1_root)
        frame1_frame_models.grid(row=0, column=1, columnspan=1, sticky=W + E + N + S)
        Label(frame1_frame_models, text="Models").pack(padx=10, pady=10)
        self.frame1_listbox_models = Tk.Listbox(frame1_frame_models, width=20, exportselection=0)
        self.frame1_listbox_models.bind('<<ListboxSelect>>', self.action_get_models)
        self.frame1_listbox_models.pack()

        frame1_frame_import = Frame(frame1_root)
        frame1_frame_import.grid(row=1, column=0, rowspan=1, columnspan=1, sticky=W + E + N + S, padx=15, pady=15)
        Label(frame1_frame_import, text="Models import").pack(ipady=5)
        frame1_button_import = Button(frame1_frame_import, text="import .sla", command=self.action_import_model)
        frame1_button_import.pack()

        # Button(frame1_frame_import, text="my_test", command=self.my_test).pack()

        frame1_frame_orientation = Frame(frame1_root)
        frame1_frame_orientation.grid(row=1, column=1, rowspan=1, columnspan=1, sticky=W + E + N + S, padx=15, pady=15)

        Label(frame1_frame_orientation, text="Size").pack(ipady=5)
        frame1_combobox_size = ttk.Combobox(frame1_frame_orientation, textvariable=self.size, width=15)

        keys = size_document.keys()
        keys.sort()
        size_keys = []
        for i in keys:
            size_keys.append(i)
        frame1_combobox_size['values'] = size_keys
        frame1_combobox_size.current(4)
        frame1_combobox_size.pack(pady=5, anchor='w')

        frame1_frame_empty = Frame(frame1_root)
        frame1_frame_empty.grid(row=3, column=1, rowspan=3, columnspan=2, sticky=W + E + N + S)

        frame1_frame_preview = Frame(frame1_root)
        frame1_frame_preview.grid(row=0, column=2, rowspan=6, columnspan=1, padx=20, sticky=W + E + N + S)
        Label(frame1_frame_preview, text="Preview").pack(padx=10, pady=10)

        self.photo = PhotoImage(file="format/month.png")
        self.previewCanvas = Canvas(frame1_frame_preview, width=200, height=200)
        self.photo_img = self.previewCanvas.create_image(0, 0, anchor=NW, image=self.photo)
        self.previewCanvas.pack()

        # ELEMENT MIDDLE FRAME 2
        frame2_root = Frame(self.canvas_frame)

        frame2_list_language = Frame(frame2_root)
        frame2_list_language.grid(row=0, rowspan=3, column=0, sticky=W + E + N + S)
        Label(frame2_list_language, text="Languages").pack(padx=10, pady=10)

        scrollbar_listbox_language = Scrollbar(frame2_list_language, orient=VERTICAL)
        self.frame2_listbox_language = Tk.Listbox(frame2_list_language, yscrollcommand=scrollbar_listbox_language.set)
        scrollbar_listbox_language.config(command=self.frame2_listbox_language.yview)
        scrollbar_listbox_language.pack(anchor='n', side=RIGHT, ipady=63)  # place scrollbar near to the listbox

        keys = localization.keys()
        keys.sort()
        for i in keys:
            self.frame2_listbox_language.insert(END, i)
        self.frame2_listbox_language.bind('<<ListboxSelect>>', self.action_get_language)
        self.frame2_listbox_language.pack()

        frame2_button = Button(frame2_list_language, text="Import ICS",
                               command=self.action_import_ics, padx=30, pady=10)
        frame2_button.pack(pady=20)

        frame2_checkbox = Frame(frame2_root)
        frame2_empty = Frame(frame2_root)
        frame2_empty.grid(row=0, column=2, pady=20, sticky=W + N + E + S)

        frame2_label = Frame(frame2_root)
        frame2_label.grid(row=1, column=2, padx=10, sticky=W + N + E + S)
        frame2_checkbox.grid(row=1, column=3, sticky=W + N + E + S)

        Label(frame2_label, text="Show previous days:").pack(padx=4, pady=4, anchor='w')
        Label(frame2_label, text="Show next days:").pack(padx=4, pady=4, anchor='w')
        Label(frame2_label, text="Short day name:").pack(padx=4, pady=4, anchor='w')
        Label(frame2_label, text="Next short day name:").pack(padx=4, pady=4, anchor='w')
        Label(frame2_label, text="Prev short day name:").pack(padx=4, pady=4, anchor='w')
        Label(frame2_label, text='Week begins with:').pack(padx=4, pady=4, anchor='w')
        Label(frame2_label, text='Year:').pack(padx=4, pady=20, anchor='w')

        Checkbutton(frame2_checkbox, variable=self.check_option_prev_day,
                    command=self.get_prev_day).pack(padx=3, pady=3, anchor='w')
        Checkbutton(frame2_checkbox, variable=self.check_option_next_day,
                    command=self.get_next_day).pack(padx=3, pady=3, anchor='w')
        Checkbutton(frame2_checkbox, variable=self.check_option_short_day,
                    command=self.get_short_day).pack(padx=3, pady=3, anchor='w')
        Checkbutton(frame2_checkbox, variable=self.check_option_next_short_day,
                    command=self.get_next_short_day).pack(padx=3, pady=3, anchor='w')
        Checkbutton(frame2_checkbox, variable=self.check_option_prev_short_day,
                    command=self.get_prev_short_day).pack(padx=3, pady=3, anchor='w')

        Radiobutton(frame2_checkbox, text='Mon', variable=self.week_var, value=calendar.MONDAY).pack()
        Radiobutton(frame2_checkbox, text='Sun', variable=self.week_var, value=calendar.SUNDAY).pack()

        self.frame2_spinbox_year = Spinbox(frame2_checkbox, width=5, from_=0, to=2132, wrap=True,
                                           textvariable=self.year_var, command=self.get_year)
        self.frame2_spinbox_year.delete(0, 1600)
        self.frame2_spinbox_year.insert(0, self.year_var)
        self.frame2_spinbox_year.pack(padx=3, pady=6, anchor='w')

        frame2_preview = Frame(frame2_root)
        frame2_preview.grid(row=0, rowspan=3, column=4, sticky=W + E + N + S)
        Label(frame2_preview, text="Month").pack(padx=10, pady=10)
        self.scrollbar_listbox_month = Scrollbar(frame2_preview, orient=VERTICAL)
        self.frame2_listbox_month = Listbox(frame2_preview, selectmode='multiple', exportselection=0,
                                            yscrollcommand=self.scrollbar_listbox_month.set)
        self.frame2_listbox_month.bind('<<ListboxSelect>>', self.action_select_month)
        self.scrollbar_listbox_month.config(command=self.frame2_listbox_month.yview)
        self.scrollbar_listbox_month.pack(anchor='ne', side=RIGHT, ipady=62)  # place scrollbar near to the listbox
        self.frame2_listbox_month.pack()
        Button(frame2_preview, text="Select All", command=self.select_all_month).pack(padx=10, pady=10)
        Button(frame2_preview, text="Un-select All", command=self.unselect_all_month).pack(padx=5, pady=5)

        # ELEMENT MIDDLE FRAME 3
        frame3_root = Frame(self.canvas_frame)
        frame3_root.rowconfigure(1, weight=1)

        frame3_frame_list = Frame(frame3_root)
        frame3_frame_list.grid(row=0, column=0, rowspan=3, sticky=W + E + N + S)
        Label(frame3_frame_list, text="Elements").pack(padx=10, pady=10)
        self.frame3_listbox_font = Listbox(frame3_frame_list, selectmode='multiple', exportselection=0)
        self.frame3_listbox_font.bind('<<ListboxSelect>>')
        self.frame3_listbox_font.pack()
        Button(frame3_frame_list, text='Uniform Font', command=self.select_all_elements).pack(pady=20, anchor='center')

        frame3_frame_font_title = Frame(frame3_root)
        frame3_frame_font_label = Frame(frame3_root)
        frame3_frame_font_combobox = Frame(frame3_root)
        frame3_frame_font_title.grid(row=0, column=1, columnspan=2, sticky=W + E + N)
        frame3_frame_font_label.grid(row=1, column=1, sticky=N + W + E + S)
        frame3_frame_font_combobox.grid(row=1, column=2, sticky=W + E + N + S)

        Label(frame3_frame_font_title, text="Font Family").pack(padx=20, pady=20)
        Label(frame3_frame_font_label, text="Family:").pack(padx=15, pady=10, anchor='nw')
        Label(frame3_frame_font_label, text="Style:").pack(padx=15, pady=10, anchor='nw')
        Label(frame3_frame_font_label, text="Size:").pack(padx=15, pady=10, anchor='nw')
        Label(frame3_frame_font_label, text="Color:").pack(padx=15, pady=10, anchor='nw')

        frame3_combobox_font = ttk.Combobox(frame3_frame_font_combobox, textvariable=self.font_var)
        try:
            frame3_combobox_font['values'] = scribus.getFontNames()
        except:
            frame3_combobox_font['values'] = ('Arial', 'Comic', 'Times New Roman')

        frame3_combobox_font.current(0)
        frame3_combobox_font.bind("<<ComboboxSelected>>")
        frame3_combobox_font.pack(pady=10, anchor='w')

        frame3_combobox_font_style = ttk.Combobox(frame3_frame_font_combobox, textvariable=self.font_style_var)
        try:
            frame3_combobox_font_style['values'] = scribus.getFontStyle()
        except:
            frame3_combobox_font_style['values'] = ('Bold', 'Italic')

        frame3_combobox_font_style.current(1)
        frame3_combobox_font_style.bind("<<ComboboxSelected>>")
        frame3_combobox_font_style.pack(pady=10, anchor='w')

        self.frame3_spinbox_size = Spinbox(frame3_frame_font_combobox, wrap=True, from_=2, to=512,
                                           textvariable=self.font_size, command=self.get_font_size)
        self.frame3_spinbox_size.delete(0, 2)
        self.frame3_spinbox_size.insert(0, self.font_size)
        self.frame3_spinbox_size.pack(pady=10, anchor='w')

        self.frame3_combobox_color = ttk.Combobox(frame3_frame_font_combobox, textvariable=self.font_color)
        try:
            self.frame3_combobox_color['values'] = scribus.getColorNames()
        except:
            self.frame3_combobox_color['values'] = ('Black', 'Red', 'Yellow')
        self.frame3_combobox_color.current(0)
        self.frame3_combobox_color.bind("<<ComboboxSelected>>")
        self.frame3_combobox_color.pack(pady=10, anchor='center')

        Button(frame3_frame_font_combobox, text='Attribute Font', command=self.action_attrib).pack(pady=10,
                                                                                                   anchor='center')

        self.frame_master_all_frames = [frame1_root, frame2_root, frame3_root]

    def quit(self):
        self.destroy()
        self.parent.destroy()

    def __init__(self, parent):
        Tk.Frame.__init__(self, parent)
        # configuration variable global
        self.parent = parent

        # variable for the GUI
        self.top = Frame()
        self.middle = Frame()
        self.canvas_frame = Frame()
        self.bottom = Frame()
        self.top_label = Label()
        self.canvas = Canvas()
        self.previewCanvas = Canvas()
        self.photo_img = Canvas()
        self.scrollbar_middle = Scrollbar()
        self.scrollbar_listbox_month = Scrollbar()
        self.frame1_listbox_models = Listbox()
        self.frame2_listbox_language = Listbox()
        self.frame2_listbox_month = Listbox()
        self.frame3_listbox_font = Listbox()
        self.frame1_button_import = Button()
        self.frame2_spinbox_year = Spinbox()
        self.frame3_spinbox_size = Spinbox()
        self.bottom_button = []
        self.frame_master_all_frames = []
        self.frame_master_last_page = 0
        self.frame_master_max_page = 3
        self.frame_master_current_page = 0
        self.frame1_config_model_name = ''
        self.frame1_config_model_path = './models/'
        self.frame1_config_type_string_selected = ''
        self.frame1_config_type_index_selected = IntVar()
        self.frame1_listbox_types = Listbox()
        self.model_index_selected = IntVar()
        self.check_option_prev_day = IntVar()
        self.check_option_next_day = IntVar()
        self.check_option_short_day = IntVar()
        self.check_option_next_short_day = IntVar()
        self.check_option_prev_short_day = IntVar()
        self.frame2_config_language_string_selected = 'English'
        self.frame2_config_language_index_selected = 0
        self.frame2_config_month_index_selected = []
        self.frame2_config_month_string_selected = []
        self.frame3_listbox_font_elements = []
        self.frame2_config_file_i_c_s = ''
        self.photo = PhotoImage()

        # variable about the calendar information
        self.now = datetime.datetime.now()
        self.year_var = self.now.year
        self.first_day = calendar.SUNDAY

        # variable about option for the calendar
        self.months = []
        self.lang = 'English'
        self.week_var = IntVar()
        self.short_day_name = BooleanVar()
        self.next_short_day_name = BooleanVar()
        self.prev_short_day_name = BooleanVar()
        self.prev_day_name = BooleanVar()
        self.next_day_name = BooleanVar()
        self.week_number = BooleanVar()
        self.font_var = StringVar()
        self.font_style_var = StringVar()
        self.font_color = StringVar()
        self.font_size = 12
        self.font_list = {}

        # variable for scribus setStyles
        self.p_style_date = "Date"  # paragraph styles
        self.p_style_days_box = "Weekday"
        self.p_style_month_box = "Month"
        self.p_style_week_box = "WeekNo"
        self.layer_img = 'Calendar image'
        self.layer_cal = 'Calendar'
        self.master_page = "Weekdays"

        self.size = StringVar()

        # Some init method
        self.make_top()
        self.make_middle()
        self.make_bottom()
        self.make_frames()
        self.update()


def main():
    """ Application/Dialog loop with Scribus sauce around """
    # try:
    print('Running script...')
    try:
        progressReset()
    except:
        pass
    root = Tk.Tk()
    TkCalendar(root).pack(side="top", fill="both", expand=True)
    root.mainloop()

# except:
# 	print("failed")
# finally:
# 	if haveDoc() > 0:
# 		redrawAll()
# 	statusMessage('Done.')
# 	progressReset()


if __name__ == '__main__':
    main()
