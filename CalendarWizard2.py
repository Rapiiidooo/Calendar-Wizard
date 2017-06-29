# -*- coding: utf-8 -*-
from Tkinter import *
from tkFileDialog import *
from lxml import etree
from shutil import copyfile

import ttk
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
    def __init__(self, xpos, ypos, width, height, anname, img, text, font='', font_size='', color='', line_color=''):
        self.xpos = xpos
        self.ypos = ypos
        self.width = width
        self.height = height
        self.anname = anname
        self.img = img
        self.font = font
        self.font_size = font_size
        self.color = color
        self.line_color = line_color
        self.path_img = ''
        self.fit_to_box = False
        self.keep_proportion = False
        self.text = text

    def attrib_font(self, font, font_size, color, line_color):
        self.font = font
        self.font_size = font_size
        self.color = color
        self.line_color = line_color


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
        self.nb_max_days_in_month = 31
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
        i = 0
        text = ''
        for parent in tree.xpath("/SCRIBUSUTF8NEW/DOCUMENT"):
            for val in parent.xpath("//MASTERPAGE"):
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
            for j, box in enumerate(parent.xpath("//PAGEOBJECT")):
                # try to catch text only inside "containers.."
                if box.get("ANNAME") == "containers" + str(i):
                    text = box.xpath("//PAGEOBJECT/ITEXT")[i]
                    text = text.get("CH")
                    i += 1

                if box.get("ANNAME") == "image_box":
                    new = BoxObject(float(box.get("XPOS")) - self.pagex, float(box.get("YPOS")) - self.pagey,
                                    float(box.get("WIDTH")), float(box.get("HEIGHT")), box.get("ANNAME"), True, text)
                else:
                    new = BoxObject(float(box.get("XPOS")) - self.pagex, float(box.get("YPOS")) - self.pagey,
                                    float(box.get("WIDTH")), float(box.get("HEIGHT")), box.get("ANNAME"), False, text)
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
            # a supprimer
            self.frame2_listbox_language.select_set(9)
            self.action_get_language(None)

        if self.frame_master_current_page == 2:
            # months
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
                    self.font_list[val].append(self.font_size)
                    self.font_list[val].append(self.font_color.get())
                    self.font_list[val].append(self.line_color.get())
                # print self.font_list
                self.frame3_listbox_font.select_set(0)
                self.on_font_select(None)

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
            self.preview_canvas.itemconfigure(self.photo_img, image=self.photo, anchor=NW)
            self.preview_canvas.image = self.photo
        except Exception as e:
            show_error("Can not update image from model. Err :" + str(e))

    # update the list of months with the right language
    def action_get_language(self, event):
        # get selected line index
        self.frame2_config_language_index_selected = None
        try:
            self.frame2_config_language_index_selected = self.frame2_listbox_language.curselection()[0]
        except:
            pass

        if self.frame2_config_language_index_selected is None:
            return
        months = localization[self.frame2_listbox_language.get(self.frame2_config_language_index_selected)][0]
        self.frame2_config_language_string_selected = self.frame2_listbox_language.get(
            self.frame2_config_language_index_selected)
        self.lang = self.frame2_config_language_string_selected  # used for action_finish
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

    # show button Previous, Next, and finish
    def make_bottom(self):
        self.bottom = Frame(self)
        self.bottom.grid(row=2, column=0)
        self.bottom_button = [Button(self.bottom, text="Previous", padx=10, command=self.action_decrement),
                              Button(self.bottom, text="Next", padx=20, command=self.action_increment),
                              Button(self.bottom, padx=20, text="Finish", command=self.action_finish),
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

    def create_day_calendar(self, my_document):
        createParagraphStyle(name=self.p_style_year, alignment=1)  # alignment=1 == center
        createParagraphStyle(name=self.p_style_days, alignment=ALIGN_RIGHT)
        createParagraphStyle(name=self.p_style_month, alignment=1)
        createParagraphStyle(name=self.p_style_week, alignment=1)
        createParagraphStyle(name=self.p_style_name_week, alignment=ALIGN_RIGHT)
        createParagraphStyle(name=self.p_style_num_week, alignment=ALIGN_RIGHT)

        for imonth, month in enumerate(self.frame2_config_month_string_selected):
            my_document.set_month(self.year_var, month)
            cal = my_document.mycal.monthdatescalendar(self.year_var, month)





    def create_week_calendar(self, my_document):
        createParagraphStyle(name=self.p_style_year, alignment=1)  # alignment=1 == center
        createParagraphStyle(name=self.p_style_days, alignment=ALIGN_RIGHT)
        createParagraphStyle(name=self.p_style_month, alignment=1)
        createParagraphStyle(name=self.p_style_week, alignment=1)
        createParagraphStyle(name=self.p_style_name_week, alignment=ALIGN_RIGHT)
        createParagraphStyle(name=self.p_style_num_week, alignment=ALIGN_RIGHT)

        # imonth is used for scribus progressbar
        # re-draw new document from the model base

        # for day in week:
        # imprime le numéro de la semaine sur l'année
        # datetime.date(self.year_var, week[0].month, week[0].day).isocalendar()[1]
        run = 0
        for imonth, month in enumerate(self.frame2_config_month_string_selected):
            progressSet(imonth)
            my_document.set_month(self.year_var, month)
            cal = my_document.mycal.monthdatescalendar(self.year_var, month)

            for week in cal:
                newPage(-1)

                nb_days_in_current_week = 0
                for day in week:
                    if self.prev_day_name is 1 and day.month < month:
                        nb_days_in_current_week += 1
                    if self.next_day_name is 1 and day.month > month:
                        nb_days_in_current_week += 1
                    if day.month == month:
                        nb_days_in_current_week += 1

                for i in my_document.box_container:
                    if i.anname == "month_box":

                        cel = createText(i.xpos, i.ypos, i.width, i.height, str(i.anname) + str(run))

                        iday = 0
                        if self.prev_day_name is not 1 and week[iday].month < month:
                            if week[iday].month < month:
                                while week[iday].month != month:
                                    iday += 1

                        setText("\n" + str(week[iday].day) + "\t" + localization[self.lang][0][week[iday].month] + "\t"
                                + str(self.year_var), cel)
                        setStyle(self.p_style_month, cel)
                        selectText(0, 0, cel)
                        setFont(i.font, cel)
                        setFontSize(i.font_size, cel)
                        setTextColor(i.color, cel)
                        if i.line_color != 'None':
                            setLineColor(i.line_color, cel)
                    elif i.anname == "week_box":
                        j = 0
                        for iday, day in enumerate(week):
                            if day.month == month or self.prev_day_name is 1 and day.month < month \
                                    or self.next_day_name is 1 and day.month > month:
                                cel = createText(i.xpos + j * (i.width / nb_days_in_current_week),
                                                 i.ypos,
                                                 i.width / nb_days_in_current_week,
                                                 i.height,
                                                 str(i.anname) + str(run))
                                setText("\n" + my_document.day_order[iday] + "\t" + str(day.day), cel)
                                setStyle(self.p_style_week, cel)
                                selectText(0, 0, cel)
                                setFont(i.font, cel)
                                setFontSize(i.font_size, cel)
                                setTextColor(i.color, cel)
                                if i.line_color != 'None':
                                    setLineColor(i.line_color, cel)
                                j += 1
                    elif i.anname[0:19] == "containers_week_box":
                        j = 0
                        for iday, day in enumerate(week):
                            if day.month == month or self.prev_day_name is 1 and day.month < month \
                                    or self.next_day_name is 1 and day.month > month:
                                cel = createText(i.xpos + j * (i.width / nb_days_in_current_week),
                                                 i.ypos,
                                                 i.width / nb_days_in_current_week,
                                                 i.height,
                                                 str(i.anname) + str(run))
                                j += 1
                    elif i.anname[0:9] == "container":
                        cel = createText(i.xpos, i.ypos, i.width, i.height, str(i.anname) + str(run))
                        setText("\n" + i.text, cel)
                        setStyle(self.p_style_month, cel)
                        selectText(0, 0, cel)
                        setFont(i.font, cel)
                        setFontSize(i.font_size, cel)
                        setTextColor(i.color, cel)
                        if i.line_color != 'None':
                            setLineColor(i.line_color, cel)
                    else:
                        cel = createText(i.xpos, i.ypos, i.width, i.height, str(i.anname) + str(run))
                        selectText(0, 0, cel)
                        setFont(i.font, cel)
                        setFontSize(i.font_size, cel)
                        setTextColor(i.color, cel)
                        if i.line_color != 'None':
                            setLineColor(i.line_color, cel)
                # boucle pour actualisé le string de numéro de fin de semaine
                while self.next_day_name is not 1 and week[iday].month > month:
                    iday -= 1
                insertText(" / " + str(week[iday].day) + "\t" + localization[self.lang][0][week[iday].month] +
                           "\t" + str(self.year_var), -1, "month_box" + str(run))
                run += 1
        # delete first empty page
        progressSet(imonth+1)
        deletePage(1)

    def create_month_calendar(self, my_document):
        createParagraphStyle(name=self.p_style_year, alignment=1)  # alignment=1 == center
        createParagraphStyle(name=self.p_style_days, alignment=ALIGN_RIGHT)
        createParagraphStyle(name=self.p_style_month, alignment=1)
        createParagraphStyle(name=self.p_style_week, alignment=1)
        createParagraphStyle(name=self.p_style_name_week, alignment=ALIGN_RIGHT)
        createParagraphStyle(name=self.p_style_num_week, alignment=ALIGN_RIGHT)

        # run is used for scribus progressbar
        # re-draw new document from the model base
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
                            my_document.set_month(year, month_variable + 12)
                            cal = my_document.mycal.monthdatescalendar(self.year_var, month_variable + 12)
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
                            if self.short_day_name is True and i.anname == "week_box" or \
                               self.next_short_day_name is True and i.anname == "next_week_box" or \
                               self.prev_short_day_name is True and i.anname == "prev_week_box":
                                setText("\n" + str(name[0:3] + '.'), cel)
                            else:
                                setText("\n" + str(name), cel)
                            setStyle(self.p_style_week, cel)
                            selectText(0, 0, cel)
                            setFont(i.font, cel)
                            setFontSize(i.font_size, cel)
                            setTextColor(i.color, cel)
                        if i.line_color != 'None':
                            setLineColor(i.line_color, cel)
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
                                setStyle(self.p_style_days, cel)
                                selectText(0, 0, str(i.anname) + str(run) + '_' + str(st))
                                setFont(i.font, str(i.anname) + str(run) + '_' + str(st))
                                setFontSize(i.font_size, str(i.anname) + str(run) + '_' + str(st))
                                setTextColor(i.color, str(i.anname) + str(run) + '_' + str(st))
                                if i.line_color != 'None':
                                    setLineColor(i.line_color, cel)
                                h += 1
                                st += 1
                            h = 0
                    elif i.anname == "month_box" or i.anname == "next_month_box":
                        cel = createText(i.xpos, i.ypos, i.width, i.height, str(i.anname) + str(run))
                        setText("\n" + localization[self.lang][0][month_variable], cel)
                        setStyle(self.p_style_month, cel)
                        selectText(0, 0, cel)
                        setFont(i.font, cel)
                        setFontSize(i.font_size, cel)
                        setTextColor(i.color, cel)
                        if i.line_color != 'None':
                            setLineColor(i.line_color, cel)
                    # draw and fill name_week_box
                    elif i.anname == "name_week_box" or i.anname == "next_name_week_box":
                        cel = createText(i.xpos, i.ypos, i.width, i.height, str(i.anname) + str(run))
                        setText("\n" + "#", cel)
                        setStyle(self.p_style_name_week, cel)
                        selectText(0, 0, cel)
                        setFont(i.font, cel)
                        setFontSize(i.font_size, cel)
                        setTextColor(i.color, cel)
                        if i.line_color != 'None':
                            setLineColor(i.line_color, cel)
                    # draw and fill all num_week_box
                    elif i.anname == "num_week_box" or i.anname == "next_num_week_box":
                        for j, week in enumerate(cal):
                            cel = createText(i.xpos, j * i.height / my_document.nb_week + i.ypos, i.width,
                                             i.height / my_document.nb_week, str(i.anname) + str(j) + str(run))
                            # imprime le numéro de la semaine sur l'année
                            setText("\n" + str(datetime.date(self.year_var, week[0].month, week[0].day).isocalendar()[1]),
                                    cel)
                            setStyle(self.p_style_num_week, cel)
                            selectText(0, 0, cel)
                            setFont(i.font, cel)
                            setFontSize(i.font_size, cel)
                            setTextColor(i.color, cel)
                            if i.line_color != 'None':
                                setLineColor(i.line_color, cel)
                    else:
                        cel = createText(i.xpos, i.ypos, i.width, i.height, str(i.anname) + str(run))
                else:
                    createImage(i.xpos, i.ypos, i.width, i.height, str(i.anname) + str(run))
                    if i.path_img != "":
                        print i.path_img
                        loadImage(i.path_img, str(i.anname) + str(run))
                        setScaleImageToFrame(i.fit_to_box, i.keep_proportion, str(i.anname) + str(run))
            run += 1
            progressSet(run)
        # delete first empty page
        deletePage(1)

    def create_year_calendar(self, my_document):
        createParagraphStyle(name=self.p_style_year, alignment=1)  # alignment=1 == center
        createParagraphStyle(name=self.p_style_days, alignment=ALIGN_LEFT)
        createParagraphStyle(name=self.p_style_month, alignment=1)
        createParagraphStyle(name=self.p_style_week, alignment=1)
        createParagraphStyle(name=self.p_style_name_week, alignment=ALIGN_RIGHT)
        createParagraphStyle(name=self.p_style_num_week, alignment=ALIGN_RIGHT)

        # run is used for scribus progressbar
        # re-draw new document from the model base
        newPage(-1)
        run = 0
        for i in my_document.box_container:
            if i.anname == "year_box":
                cel = createText(i.xpos, i.ypos, i.width, i.height, str(i.anname))
                setText("\n" + str(self.year_var), cel)
                setStyle(self.p_style_year, cel)
                selectText(0, 0, cel)
                setFont(i.font, cel)
                setFontSize(i.font_size, cel)
                setTextColor(i.color, cel)
                if i.line_color != 'None':
                    setLineColor(i.line_color, cel)
            elif i.anname == "month_box":
                nb_month = len(self.frame2_config_month_string_selected)
                for imonth, month in enumerate(self.frame2_config_month_string_selected):
                    cel = createText(i.xpos + (imonth * (i.width / nb_month)),
                                     i.ypos,
                                     i.width / nb_month,
                                     i.height,
                                     str(i.anname) + str(imonth))
                    setText(localization[self.lang][0][month], cel)
                    setStyle(self.p_style_month, cel)
                    selectText(0, 0, cel)
                    setFont(i.font, cel)
                    setFontSize(i.font_size, cel)
                    setTextColor(i.color, cel)
                    if i.line_color != 'None':
                        setLineColor(i.line_color, cel)
            elif i.anname == "days_and_week_box":
                nb_month = len(self.frame2_config_month_string_selected)
                for imonth, month in enumerate(self.frame2_config_month_string_selected):
                    # init mois courant
                    my_document.set_month(self.year_var, month + 1)
                    cal = my_document.mycal.monthdatescalendar(self.year_var, month + 1)

                    st = 0
                    for j, week in enumerate(cal):
                        for iday, day in enumerate(week):
                            if day.month == month + 1:
                                # days name
                                cel = createText(i.xpos + imonth * (i.width / nb_month),
                                                 i.ypos + st * (i.height / my_document.nb_max_days_in_month),
                                                 i.width / nb_month / 4,
                                                 i.height / my_document.nb_max_days_in_month,
                                                 str(i.anname) + str(run) + '_' + str(st))
                                if self.short_day_name is True:
                                    setText(str(my_document.day_order[iday][0:1]), cel)
                                else:
                                    setText(str(my_document.day_order[iday]), cel)
                                setStyle(self.p_style_week, cel)
                                selectText(0, 0, cel)
                                setFont(i.font, cel)
                                setFontSize(i.font_size, cel)
                                setTextColor(i.color, cel)
                                if i.line_color != 'None':
                                    setLineColor(i.line_color, cel)

                                # days numbers
                                cel = createText(i.xpos + imonth * (i.width / nb_month) + i.width / nb_month / 4,
                                                 i.ypos + st * (i.height / my_document.nb_max_days_in_month),
                                                 i.width / nb_month - i.width / nb_month / 4,
                                                 i.height / my_document.nb_max_days_in_month,
                                                 str(i.anname) + str(run) + '_' + str(st))
                                setText(str(day.day), cel)
                                setStyle(self.p_style_days, cel)
                                selectText(0, 0, cel)
                                setFont(i.font, cel)
                                setFontSize(i.font_size, cel)
                                setTextColor(i.color, cel)
                                if i.line_color != 'None':
                                    setLineColor(i.line_color, cel)
                                st += 1
                    run += 1
                    progressSet(run)
            for imonth, month in enumerate(self.frame2_config_month_string_selected):
                if i.img is False:
                    # init le nombre de semaine et de jour du mois
                    my_document.set_month(self.year_var, month + 1)
                    cal = my_document.mycal.monthdatescalendar(self.year_var, month + 1)
                    # draw and fill all days strings
                    if i.anname == "week_box" + str(imonth):
                        for j, name in enumerate(my_document.day_order):
                            cel = createText((j * i.width / my_document.nb_day_usual_week) + i.xpos, i.ypos,
                                             i.width / my_document.nb_day_usual_week, i.height,
                                             str(i.anname) + str(j))
                            if self.short_day_name is True and i.anname == "week_box" + str(imonth):
                                setText(str(name[0:2] + '.'), cel)
                            else:
                                setText(str(name), cel)
                            setStyle(self.p_style_week, cel)
                            selectText(0, 0, cel)
                            setFont(i.font, cel)
                            setFontSize(i.font_size, cel)
                            setTextColor(i.color, cel)
                            if i.line_color != 'None':
                                setLineColor(i.line_color, cel)
                    # draw and fill all days_box
                    elif i.anname == "days_box" + str(imonth):
                        h = 0
                        st = 0
                        for j, week in enumerate(cal):
                            for day in week:
                                cel = createText(h * i.width / my_document.nb_day_usual_week + i.xpos,
                                                 j * i.height / my_document.nb_week + i.ypos,
                                                 i.width / my_document.nb_day_usual_week,
                                                 i.height / my_document.nb_week,
                                                 str(i.anname) + str(st))
                                if day.month == month + 1:
                                    setText(str(day.day), cel)
                                setStyle(self.p_style_days, cel)
                                selectText(0, 0, cel)
                                setFont(i.font, cel)
                                setFontSize(i.font_size, cel)
                                setTextColor(i.color, cel)
                                if i.line_color != 'None':
                                    setLineColor(i.line_color, cel)
                                h += 1
                                st += 1
                            h = 0
                    elif i.anname == "month_box" + str(imonth):
                        cel = createText(i.xpos, i.ypos, i.width, i.height, str(i.anname))
                        setText(localization[self.lang][0][month], cel)
                        setStyle(self.p_style_month, cel)
                        selectText(0, 0, cel)
                        setFont(i.font, cel)
                        setFontSize(i.font_size, cel)
                        setTextColor(i.color, cel)
                        if i.line_color != 'None':
                            setLineColor(i.line_color, cel)
                    # draw and fill name_week_box
                    elif i.anname == "name_week_box" + str(imonth):
                        cel = createText(i.xpos, i.ypos, i.width, i.height, str(i.anname))
                        setText("\n" + "#", cel)
                        setStyle(self.p_style_name_week, cel)
                        selectText(0, 0, cel)
                        setFont(i.font, cel)
                        setFontSize(i.font_size, cel)
                        setTextColor(i.color, cel)
                        if i.line_color != 'None':
                            setLineColor(i.line_color, cel)
                    # draw and fill all num_week_box
                    elif i.anname == "num_week_box" + str(imonth):
                        for j, week in enumerate(cal):
                            cel = createText(i.xpos, j * i.height / my_document.nb_week + i.ypos, i.width,
                                             i.height / my_document.nb_week, str(i.anname) + str(j))
                            # imprime le numéro de la semaine sur l'année
                            setText("\n" + str(datetime.date(self.year_var, week[0].month, week[0].day).isocalendar()[1]),
                                    cel)
                            setStyle(self.p_style_num_week, cel)
                            selectText(0, 0, cel)
                            setFont(i.font, cel)
                            setFontSize(i.font_size, cel)
                            setTextColor(i.color, cel)
                            if i.line_color != 'None':
                                setLineColor(i.line_color, cel)
                    else:
                        pass
                else:
                    createImage(i.xpos, i.ypos, i.width, i.height, str(i.anname))
                    if i.path_img != "":
                        print i.path_img
                        loadImage(i.path_img, str(i.anname))
                        setScaleImageToFrame(i.fit_to_box, i.keep_proportion, str(i.anname))
                run += 1
            try:
                progressSet(run)
            except:
                pass
        # delete first empty page
        deletePage(1)

    def action_finish(self):
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
            try:
                if i.anname == 'image_box':
                    i.path_img = self.path_image
                    i.fit_to_box = self.fit_to_box
                    i.keep_proportion = self.keep_proportion
                else:
                    i.attrib_font(self.font_list[i.anname][0],
                                  self.font_list[i.anname][1],
                                  self.font_list[i.anname][2],
                                  self.font_list[i.anname][3])
            except Exception as e:
                show_error("Box name not found in KEYWORD. " + str(e))
        try:
            # Create the Scribus New Document with right proportions
            if not newDocument((size_document[my_document.size][0], size_document[my_document.size][1]),
                               (my_document.border_left, my_document.border_right, my_document.border_top,
                                my_document.border_bottom), my_document.orientation, 1, UNIT_POINTS, NOFACINGPAGES,
                                FIRSTPAGELEFT, 1):
                print 'Create a new document first, please'
                return

            if self.frame1_config_type_string_selected == 'Day':
                self.create_day_calendar(my_document)
                pass
            elif self.frame1_config_type_string_selected == 'Week':
                progressTotal(len(self.frame2_config_month_string_selected))
                self.create_week_calendar(my_document)
            elif self.frame1_config_type_string_selected == 'Month':
                progressTotal(len(self.frame2_config_month_string_selected))
                self.create_month_calendar(my_document)
            elif self.frame1_config_type_string_selected == 'Year':
                progressTotal(len(my_document.box_container) * len(self.frame2_config_month_string_selected))
                self.create_year_calendar(my_document)

        except Exception as e:
            show_error(str(e))
            self.quit()
        try:
            self.quit()
        except Exception as e:
            print e
            pass
        return

    def get_year(self):
        self.year_var = int(self.frame2_spinbox_year.get())

    def get_font_size(self):
        self.font_size = int(self.frame3_spinbox_size.get())

    def get_fit_to_box(self):
        self.fit_to_box = bool(self.check_option_fit_to_box.get())

    def get_keep_proportion(self):
        self.keep_proportion = bool(self.check_option_keep_proportion.get())

    def action_attrib(self):
        # insert dans self.font_list toutes les valeurs de police que l'utilisateurs a choisi pour tel element
        try:
            for i in self.frame3_listbox_font.curselection():
                self.font_list[self.frame3_listbox_font_elements[i]] = []
                self.font_list[self.frame3_listbox_font_elements[i]].append(self.font_var.get())
                self.font_list[self.frame3_listbox_font_elements[i]].append(self.font_size)
                self.font_list[self.frame3_listbox_font_elements[i]].append(self.font_color.get())
                self.font_list[self.frame3_listbox_font_elements[i]].append(self.line_color.get())
        except Exception as e:
            show_error("Error while attributing font..." + str(e))

    def get_style_from_font_string(self, mstr):
        # traitement de la police, transfere le style dans s
        self.font = mstr
        s = ""
        if " Regular" in self.font:
            s += "Regular"
            self.font = self.font.replace(" Regular", "")
        if " Bold" in self.font:
            s += " Bold"
            self.font = self.font.replace(" Bold", "")
        if " Italic" in self.font:
            s += " Italic"
            self.font = self.font.replace(" Italic", "")
        if " Oblique" in self.font:
            s += " Oblique"
            self.font = self.font.replace(" Oblique", "")
        return s

    def on_font_select(self, event):
        # refresh le Text de font preview d'après les fonts family box
        s = self.get_style_from_font_string(self.font_var.get())
        if "Regular" in s:
            if self.line_color.get() != 'None':
                self.frame3_frame_font_text.configure(font=(self.font[0:-8], self.font_size),
                                                      foreground=self.font_color.get(),
                                                      highlightbackground=self.line_color.get(),
                                                      highlightcolor=self.line_color.get(),
                                                      highlightthickness=1)
            else:
                self.frame3_frame_font_text.configure(font=(self.font[0:-8], self.font_size),
                                                      foreground=self.font_color.get(),
                                                      highlightthickness=0)
        else:
            if self.line_color.get() != 'None':
                self.frame3_frame_font_text.configure(font=(self.font, self.font_size, s.lower()),
                                                      foreground=self.font_color.get(),
                                                      highlightbackground=self.line_color.get(),
                                                      highlightcolor=self.line_color.get(),
                                                      highlightthickness=1)
            else:
                self.frame3_frame_font_text.configure(font=(self.font[0:-8], self.font_size),
                                                      foreground=self.font_color.get(),
                                                      highlightthickness=0)

    def unshow_frame3_image(self):
        self.frame3_frame_font_title_font.grid(row=0, column=1, columnspan=2, sticky=W + E + N)
        self.frame3_frame_font_title_preview.grid(row=0, column=3, rowspan=3, sticky=W + E + N)
        self.frame3_frame_font_label.grid(row=1, column=1, sticky=N + W + E + S)
        self.frame3_frame_font_combobox.grid(row=1, column=2, sticky=W + E + N + S)
        self.frame3_frame_img_button.grid_forget()
        self.frame3_frame_img_preview.grid_forget()

    def show_frame3_image(self):
        self.frame3_frame_font_title_font.grid_forget()
        self.frame3_frame_font_title_preview.grid_forget()
        self.frame3_frame_font_label.grid_forget()
        self.frame3_frame_font_combobox.grid_forget()
        self.frame3_frame_img_button.grid(row=0, column=1, rowspan=2, sticky=W + E + N + S)
        self.frame3_frame_img_preview.grid(row=0, column=2, rowspan=2, sticky=W + E + N + S)

    def on_font_select_listbox(self, event):
        if self.frame1_config_model_name != '':
            if self.frame3_listbox_font.curselection()[0] >= 0:
                # refresh le label de font preview avec les fonts attribuer precedement
                i = self.frame3_listbox_font.curselection()[0]

                if "image_box" in self.frame3_listbox_font_elements[i]:
                    self.show_frame3_image()
                else:
                    self.unshow_frame3_image()

                s = self.get_style_from_font_string(self.font_list[self.frame3_listbox_font_elements[i]][0])
                # verifie le style de font
                if "Regular" in self.font_list[self.frame3_listbox_font_elements[i]][0]:
                    # Si le contour du cadre n'est pas None
                    if self.font_list[self.frame3_listbox_font_elements[i]][3] != 'None':
                        self.frame3_frame_font_text.configure(
                            font=(self.font, self.font_list[self.frame3_listbox_font_elements[i]][1]),
                            foreground=self.font_list[self.frame3_listbox_font_elements[i]][2],
                            highlightbackground=self.font_list[self.frame3_listbox_font_elements[i]][3],
                            highlightcolor=self.font_list[self.frame3_listbox_font_elements[i]][3],
                            highlightthickness=1)
                    else:
                        self.frame3_frame_font_text.configure(
                            font=(self.font, self.font_list[self.frame3_listbox_font_elements[i]][1]),
                            foreground=self.font_list[self.frame3_listbox_font_elements[i]][2],
                            highlightthickness=0)
                else:
                    if self.font_list[self.frame3_listbox_font_elements[i]][3] != 'None':
                        self.frame3_frame_font_text.configure(
                            font=(self.font, self.font_list[self.frame3_listbox_font_elements[i]][1], s),
                            foreground=self.font_list[self.frame3_listbox_font_elements[i]][2],
                            highlightbackground=self.font_list[self.frame3_listbox_font_elements[i]][3],
                            highlightcolor=self.font_list[self.frame3_listbox_font_elements[i]][3],
                            highlightthickness=1)
                    else:
                        self.frame3_frame_font_text.configure(
                            font=(self.font, self.font_list[self.frame3_listbox_font_elements[i]][1], s),
                            foreground=self.font_list[self.frame3_listbox_font_elements[i]][2],
                            highlightthickness=0)
                # refresh les fonts family box d'après les valeurs attribuer
                self.frame3_combobox_font.set(self.font_list[self.frame3_listbox_font_elements[i]][0])
                self.frame3_spinbox_size.delete(0, self.font_size)
                self.frame3_spinbox_size.insert(0, self.font_list[self.frame3_listbox_font_elements[i]][1])
                self.frame3_combobox_color.set(self.font_list[self.frame3_listbox_font_elements[i]][2])
                self.frame3_combobox_line_color.set(self.font_list[self.frame3_listbox_font_elements[i]][3])
            else:
                if self.line_color.get() != 'None':
                    self.frame3_frame_font_text.configure(font=(self.font_var.get(), self.font_size),
                                                          foreground=self.font_color.get(),
                                                          highlightbackground=self.line_color.get(),
                                                          highlightcolor=self.line_color.get(),
                                                          highlightthickness=1)
                else:
                    self.frame3_frame_font_text.configure(font=(self.font_var.get(), self.font_size),
                                                          foreground=self.font_color.get(),
                                                          highlightthickness=0)

    def get_image(self):
        try:
            filename = askopenfilename(title="Open your image",
                                       filetypes=[('Image File', '.jpg'), ('Image File', '.jpeg'),
                                                  ('Image File', '.png'), ('Image File', '.bmp'), ('all files', '.*')])
            # In case of error or cancel
            if len(filename) <= 0:
                filename = "croix.png"
            else:
                self.path_image = filename

            self.photo_frame3 = PhotoImage(file=filename)
            # resize img
            while self.photo_frame3.width() > 200 and self.photo_frame3.width() > 150:
                print self.photo_frame3.width()
                print self.photo_frame3.height()
                self.photo_frame3 = self.photo_frame3.subsample(8)

            self.preview_canvas_frame3.itemconfigure(self.photo_img_frame3, image=self.photo_frame3, anchor=NW)
            self.preview_canvas_frame3.image = self.photo_frame3
        except Exception as e:
            show_error("An error has encountered while opening image. Err :" + str(e))

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
        self.preview_canvas = Canvas(frame1_frame_preview, width=200, height=200)
        self.photo_img = self.preview_canvas.create_image(0, 0, anchor=NW, image=self.photo)
        self.preview_canvas.pack()

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
        self.frame3_listbox_font = Listbox(frame3_frame_list, exportselection=0)
        self.frame3_listbox_font.bind('<<ListboxSelect>>', self.on_font_select_listbox)
        self.frame3_listbox_font.pack()
        Button(frame3_frame_list, text='Uniform Font', command=self.select_all_elements).pack(pady=20, anchor='center')

        self.frame3_frame_font_title_font = Frame(frame3_root)
        self.frame3_frame_font_title_preview = Frame(frame3_root)
        self.frame3_frame_font_label = Frame(frame3_root)
        self.frame3_frame_font_combobox = Frame(frame3_root)
        self.frame3_frame_img_button = Frame(frame3_root)
        self.frame3_frame_img_preview = Frame(frame3_root)
        self.frame3_frame_font_title_font.grid(row=0, column=1, columnspan=2, sticky=W + E + N)
        self.frame3_frame_font_title_preview.grid(row=0, column=3, rowspan=3, sticky=W + E + N)
        self.frame3_frame_font_label.grid(row=1, column=1, sticky=N + W + E + S)
        self.frame3_frame_font_combobox.grid(row=1, column=2, sticky=W + E + N + S)

        Label(self.frame3_frame_img_button, text="").pack(pady=15)
        Button(self.frame3_frame_img_button, text='Choose Image', command=self.get_image).pack(padx=30, pady=15)
        Label(self.frame3_frame_img_button, text="Fit to Container :").pack(padx=30)
        Checkbutton(self.frame3_frame_img_button, variable=self.check_option_fit_to_box,
                    command=self.get_fit_to_box).pack(padx=30)
        Label(self.frame3_frame_img_button, text="Keep Proportion :").pack(padx=30)
        Checkbutton(self.frame3_frame_img_button, variable=self.check_option_keep_proportion,
                    command=self.get_keep_proportion).pack(padx=30)
        self.photo_frame3 = PhotoImage(file="croix.png")
        self.preview_canvas_frame3 = Canvas(self.frame3_frame_img_preview, width=200, height=150)
        self.photo_img_frame3 = self.preview_canvas_frame3.create_image(0, 0, anchor=NW, image=self.photo_frame3)
        self.preview_canvas_frame3.pack(pady=50)

        Label(self.frame3_frame_font_title_preview, text="Preview").pack(padx=20, pady=20)
        Label(self.frame3_frame_font_title_font, text="Font Family").pack(padx=20, pady=20)
        Label(self.frame3_frame_font_label, text="Font:").pack(padx=15, pady=10, anchor='nw')
        Label(self.frame3_frame_font_label, text="Size:").pack(padx=15, pady=10, anchor='nw')
        Label(self.frame3_frame_font_label, text="Color:").pack(padx=15, pady=10, anchor='nw')
        Label(self.frame3_frame_font_label, text="Outline:").pack(padx=15, pady=10, anchor='nw')

        self.frame3_combobox_font = ttk.Combobox(self.frame3_frame_font_combobox, textvariable=self.font_var)
        try:
            self.frame3_combobox_font['values'] = scribus.getFontNames()
        except:
            self.frame3_combobox_font['values'] = ('Arial Regular', 'Arial Bold', 'Comic Regular', 'Comic Bold', 'Comic Italic', 'Comic Bold Italic', 'Times New Roman')

        self.frame3_combobox_font.current(0)
        self.frame3_combobox_font.bind("<<ComboboxSelected>>", self.on_font_select)
        self.frame3_combobox_font.pack(pady=10, anchor='w')

        self.frame3_spinbox_size = Spinbox(self.frame3_frame_font_combobox, wrap=True, from_=2, to=512,
                                           textvariable=self.font_size, command=self.get_font_size)
        self.frame3_spinbox_size.delete(0, 2)
        self.frame3_spinbox_size.insert(0, self.font_size)
        self.frame3_spinbox_size.bind('<ButtonPress>', self.on_font_select)
        self.frame3_spinbox_size.pack(pady=10, anchor='w')

        self.frame3_combobox_color = ttk.Combobox(self.frame3_frame_font_combobox, textvariable=self.font_color)
        try:
            self.frame3_combobox_color['values'] = scribus.getColorNames()
        except:
            self.frame3_combobox_color['values'] = ('Black', 'Red', 'Yellow')
        self.frame3_combobox_color.current(0)
        self.frame3_combobox_color.bind("<<ComboboxSelected>>", self.on_font_select)
        self.frame3_combobox_color.pack(pady=10, anchor='center')

        self.frame3_combobox_line_color = ttk.Combobox(self.frame3_frame_font_combobox, textvariable=self.line_color)
        get_enable_color = []
        try:
            get_enable_color = scribus.getColorNames()
            get_enable_color.insert(0, 'None')
        except:
            get_enable_color = ['Black', 'Red', 'Yellow']
            get_enable_color.insert(0, 'None')
        self.frame3_combobox_line_color['values'] = get_enable_color
        self.frame3_combobox_line_color.current(0)
        self.frame3_combobox_line_color.bind("<<ComboboxSelected>>", self.on_font_select)
        self.frame3_combobox_line_color.pack(pady=10, anchor='center')

        Button(self.frame3_frame_font_combobox, text='Attribute Font', command=self.action_attrib).pack(pady=10,
                                                                                                        anchor='center')

        self.frame3_frame_font_text = Text(self.frame3_frame_font_title_preview, height=40/self.font_size,
                                           width=100/self.font_size)
        self.frame3_frame_font_text.insert(END, 'Aa\nBb\nCc')
        self.frame3_frame_font_text.pack(padx=10, pady=15)

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
        self.frame3_frame_font_title_font = Frame()
        self.frame3_frame_font_title_preview = Frame()
        self.frame3_frame_font_label = Frame()
        self.frame3_frame_font_combobox = Frame()
        self.frame3_frame_img_button = Frame()
        self.frame3_frame_img_preview = Frame()
        self.top_label = Label()
        self.canvas = Canvas()
        self.preview_canvas = Canvas()
        self.preview_canvas_frame3 = Canvas()
        self.photo_img = Canvas()
        self.photo_img_frame3 = Canvas()
        self.scrollbar_middle = Scrollbar()
        self.scrollbar_listbox_month = Scrollbar()
        self.frame1_listbox_models = Listbox()
        self.frame2_listbox_language = Listbox()
        self.frame2_listbox_month = Listbox()
        self.frame3_listbox_font = Listbox()
        self.frame1_button_import = Button()
        self.frame2_spinbox_year = Spinbox()
        self.frame3_spinbox_size = Spinbox()
        self.frame3_combobox_color = ttk.Combobox()
        self.frame3_combobox_font = ttk.Combobox()
        self.frame3_combobox_line_color = ttk.Combobox()
        self.bottom_button = []
        self.frame_master_all_frames = []
        self.frame_master_last_page = 0
        self.frame_master_max_page = 3
        self.frame_master_current_page = 0
        self.frame1_config_model_name = ''
        self.frame1_config_model_path = './models/'
        self.frame1_config_type_string_selected = 'Month'
        self.frame1_config_type_index_selected = IntVar()
        self.frame1_listbox_types = Listbox()
        self.model_index_selected = IntVar()
        self.check_option_prev_day = IntVar()
        self.check_option_next_day = IntVar()
        self.check_option_short_day = IntVar()
        self.check_option_next_short_day = IntVar()
        self.check_option_prev_short_day = IntVar()
        self.check_option_fit_to_box = IntVar()
        self.check_option_keep_proportion = IntVar()
        self.frame2_config_language_string_selected = 'English'
        self.frame2_config_language_index_selected = 0
        self.frame2_config_month_index_selected = []
        self.frame2_config_month_string_selected = []
        self.frame3_listbox_font_elements = []
        self.frame2_config_file_i_c_s = ''
        self.frame3_frame_font_text = Text()
        self.photo = PhotoImage()
        self.photo_frame3 = PhotoImage()

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
        self.fit_to_box = False
        self.keep_proportion = False
        self.font = StringVar()
        self.font_var = StringVar()
        self.font_color = StringVar()
        self.line_color = StringVar()
        self.path_image = ""
        self.font_size = 12
        self.font_list = {}

        # variable for scribus # paragraph styles
        self.p_style_year = "Year"
        self.p_style_days = "Days"
        self.p_style_month = "Month"
        self.p_style_week = "Week"
        self.p_style_name_week = "NameWeek"
        self.p_style_num_week = "NumWeek"

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
    root.resizable(width=False, height=False)
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
