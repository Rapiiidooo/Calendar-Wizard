# -*- coding: utf-8 -*-
from Tkinter import *
from tkFileDialog import *
from lxml import etree
from shutil import copyfile

import ttk
# Python 2.x Version
from tkColorChooser import askcolor
from math import sqrt
# Python 3.x Version
# from tkinter.colorchooser import *
import Tkinter as tk
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

size_document = ('A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'B0', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6',
                 'B7', 'B8', 'B9', 'B10', 'C5E', 'COMM10E', 'DLE', 'EXECUTIVE', 'FOLIO', 'LEDGER', 'LEGAL', 'LETTER',
                 'TABLOID')

sizex = 650
sizey = 350
posx = 300
posy = 200

class BoxObject:
    """ BoxObject represent some attribute from PAGEOBJECT from scribus file. """
    def __init__(self, xpos, ypos, width, height, anname, img=False):
        self.xpos = xpos
        self.ypos = ypos
        self.width = width
        self.height = height
        self.anname = anname
        self.img = img


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
        self.size = "PAPER_" + size

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
        for balise in tree.xpath("/SCRIBUSUTF8NEW/DOCUMENT/PAGEOBJECT"):
            if balise.get("ANNAME") == "image_box":
                new = BoxObject(balise.get("XPOS"), balise.get("YPOS"), balise.get("WIDTH"), balise.get("HEIGHT"),
                                balise.get("ANNAME"), True)
            else:
                new = BoxObject(balise.get("XPOS"), balise.get("YPOS"), balise.get("WIDTH"), balise.get("HEIGHT"),
                                balise.get("ANNAME"))
            self.box_container.append(new)

        for balise in tree.xpath("/SCRIBUSUTF8NEW/DOCUMENT/MASTERPAGE"):
            self.pagex = balise.get("PAGEXPOS")
            self.pagey = balise.get("PAGEYPOS")
            self.page_width = balise.get("PAGEWIDTH")
            self.page_height = balise.get("PAGEHEIGHT")
            self.orientation = balise.get("Orientation")
            self.border_left = balise.get("BORDERLEFT")
            self.border_right = balise.get("BORDERRIGHT")
            self.border_top = balise.get("BORDERTOP")
            self.border_bottom = balise.get("BORDERBOTTOM")
            #self.size = str(balise.get("Size"))

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


class TkCalendar(tk.Frame):
    # update the current page of the wizard
    def update(self):
        # print(self.frame_master_current_page)  # show in terminal the number of the current page

        if self.frame_master_current_page == 2:
            # months
            if len(self.frame2_config_month_string_selected) == 0:
                tkMessageBox.showinfo("Error", "At least one month must be selected.")
                self.action_decrement()
                return

        self.frame_master_allframes[self.frame_master_last_page].pack_forget()  # remove the last current page

        # If page == 2
        if self.frame_master_current_page == 2:
            if self.frame1_config_model_name != '':
                type_ele = re.compile('element=\'(.*)\'')
                tree = etree.parse(self.frame1_config_modelpath + self.frame1_config_model_name)
                keys = tree.getroot()
                for key in keys:
                    val = key.attrib['KEYWORDS']
                elements = re.findall(type_ele, val)
                spilted_elements = re.split(",", elements[0])
                # print(spilted_elements)
                self.frame3_listbox_font.delete(0, END)
                for i in spilted_elements:
                    self.frame3_listbox_font.insert(END, i)

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

        self.frame_master_allframes[self.frame_master_current_page].pack()
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
            copyfile(filename, self.frame1_config_modelpath + os.path.basename(filename))
        except ValueError:
            self.statusVar.set("Can not import file.")

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
        except ValueError:
            self.statusVar.set("Can not import file.")

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

    def init_img(self):
        self.img_path = "format/"

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
        except:
            print "Can not update image from model"

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

    # get selected month
    def action_select_month(self, event):
        self.frame2_config_month_index_selected = self.frame2_listbox_month.curselection()
        self.frame2_config_month_string_selected = []
        for tous in self.frame2_config_month_index_selected:
            self.frame2_config_month_index_selected = tous
            self.frame2_config_month_string_selected.append(int(tous))
        # print self.frame2_config_month_string_selected

    # get color for button "Font Color"
    def action_get_color(self):
        color = askcolor()
        print color

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

    # action when clicking on a Font button in Page 3
    def action_select_font(self, event):
        print self.fontVar.get()

    # useless
    def action_select_size(self, event):
        print self.size.get()

    def action_select_type(self, event):
        self.frame1_config_type_index_selected = self.frame1_listbox_types.curselection()[0]
        search_type = self.frame1_listbox_types.get(self.frame1_config_type_index_selected)
        self.frame1_config_type_string_selected = search_type
        type_cal = re.compile('type=\'.*' + search_type + '.*\'')
        # On cherche dans le repertoire avec les modeles
        available_models = []

        #  On parcours tous les documents qui se terminent par .sla dans le
        #  repertoire qui contient les modeles
        for model in os.listdir(self.frame1_config_modelpath):
            if model.endswith(".sla"):

                #  On parse chaque modele pour voir quels sont les keywords definis
                tree = etree.parse(self.frame1_config_modelpath + model)
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
        self.short_day_name = bool(self.checkoption_short_day.get())

    def get_next_short_day(self):
        self.next_short_day_name = bool(self.checkoption_next_short_day.get())

    def get_prev_short_day(self):
        self.prev_short_day_name = bool(self.checkoption_prev_short_day.get())

    def get_prev_day(self):
        self.prev_day_name = self.checkoption_prev_day.get()

    def get_next_day(self):
        self.next_day_name = self.checkoption_next_day.get()

    def action_finnish(self):
        # a virer apres test
        if self.frame1_config_model_name == '':
            self.frame1_config_model_name = 'month-LANDSCAPE.sla'
            #self.frame1_config_model_name = 'month.sla'

        my_document = Document(self.frame1_config_modelpath + self.frame1_config_model_name, self.lang, self.week_var.get(), self.size.get())

        try:
            if not newDocument(eval(my_document.size), (float(my_document.border_left), float(my_document.border_right),
                                            float(my_document.border_top), float(my_document.border_bottom)),
                               int(my_document.orientation), 1, UNIT_POINTS, NOFACINGPAGES, FIRSTPAGELEFT, 1):
                print 'Create a new document first, please'
                return

            new_page_size_height, new_page_size_width = getPageSize()
            print "test"
            print new_page_size_height
            print new_page_size_width
            self.pStyleDate = "Date"  # paragraph styles
            self.pStyleWeekday = "Weekday"
            self.pStyleMonth = "Month"
            self.pStyleWeekNo = "WeekNo"
            createParagraphStyle(name=self.pStyleDate, alignment=ALIGN_RIGHT)
            createParagraphStyle(name=self.pStyleWeekday, alignment=ALIGN_RIGHT)
            createParagraphStyle(name=self.pStyleMonth)
            createParagraphStyle(name=self.pStyleWeekNo, alignment=ALIGN_RIGHT)

            # createText(x, y, largeur, hauteur)
            # createImage(x, y, largeur, hauteur)
            # re-draw from the model

            # resize all box with proportion of new document:
            print "height :" + my_document.page_height
            print "widht : " + my_document.page_width
            print "height2 :" + new_page_size_height
            print "widht2 : " + new_page_size_width
            if my_document.page_height != new_page_size_height and my_document.page_width != new_page_size_width:
                print "Changed"
                for i in my_document.box_container:
                    i.xpos = (new_page_size_width * i.xpos) / my_document.page_width
                    i.ypos = (new_page_size_height * i.ypos) / my_document.page_height
                    i.width = (i.width * new_page_size_width) / my_document.page_width
                    i.height = (i.height * new_page_size_height) / my_document.page_height

            progressTotal(len(self.frame2_config_month_string_selected))
            run = 0
            for month in self.frame2_config_month_string_selected:
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
                                cel = createText((j * float(i.width) / my_document.nb_day_usual_week) + float(i.xpos) -
                                                 float(my_document.pagex),
                                                 float(i.ypos) - float(my_document.pagey),
                                                 float(i.width) / my_document.nb_day_usual_week,
                                                 float(i.height), str(i.anname) + str(j))
                                if self.short_day_name is True and i.anname == "week_box" or \
                                   self.next_short_day_name is True and i.anname == "next_week_box" or \
                                   self.prev_short_day_name is True and i.anname == "prev_week_box":
                                    setText(str(name[0:3] + '.'), cel)
                                else:
                                    setText(str(name), cel)
                                setStyle(self.pStyleDate, cel)
                        # draw and fill all days_box
                        elif i.anname == "days_box" or i.anname == "next_days_box":
                            h = 0
                            # creer les box pour les jours du mois et les remplies
                            for j, week in enumerate(cal):
                                for day in week:
                                    cel = createText((h * float(i.width) / my_document.nb_day_usual_week) + float(i.xpos) - float(my_document.pagex),
                                                     (j * float(i.height) / my_document.nb_week) + float(i.ypos) - float(my_document.pagey),
                                                     float(i.width) / my_document.nb_day_usual_week,
                                                     float(i.height) / my_document.nb_week, str(i.anname) + str(h))
                                    if self.prev_day_name is 1 and day.month < month_variable + 1:
                                        setText(str(day.day), cel)
                                        setStyle(self.pStyleDate, cel)
                                    if self.next_day_name is 1 and day.month > month_variable + 1:
                                        setText(str(day.day), cel)
                                        setStyle(self.pStyleDate, cel)
                                    if day.month == month_variable + 1:
                                        setText(str(day.day), cel)
                                        setStyle(self.pStyleDate, cel)
                                    h += 1
                                h = 0
                        elif i.anname == "month_box" or i.anname == "next_month_box":
                            cel = createText(float(i.xpos) - float(my_document.pagex),
                                             float(i.ypos) - float(my_document.pagey),
                                             float(i.width),
                                             float(i.height), str(i.anname))
                            setText(localization[self.lang][0][month_variable], cel)
                            setStyle(self.pStyleDate, cel)
                        # draw and fill name_week_box
                        elif i.anname == "name_week_box" or i.anname == "next_name_week_box":
                            cel = createText(float(i.xpos) - float(my_document.pagex),
                                             float(i.ypos) - float(my_document.pagey),
                                             float(i.width),
                                             float(i.height), str(i.anname))
                            setText("#", cel)
                            setStyle(self.pStyleDate, cel)
                        # draw and fill all num_week_box
                        elif i.anname == "num_week_box" or i.anname == "next_num_week_box":
                            for j, week in enumerate(cal):
                                cel = createText(float(i.xpos) - float(my_document.pagex),
                                                 (j * float(i.height) / my_document.nb_week) + float(i.ypos) - float(my_document.pagey),
                                                 float(i.width),
                                                 float(i.height) / my_document.nb_week, str(i.anname))
                                # imprime le numéro de la semaine sur l'année
                                setText(str(datetime.date(self.year_var, week[0].month, week[0].day).isocalendar()[1]), cel)
                                setStyle(self.pStyleDate, cel)
                        else:
                            cel = createText(float(i.xpos) - float(my_document.pagex),
                                             float(i.ypos) - float(my_document.pagey),
                                             float(i.width),
                                             float(i.height), str(i.anname))
                            setText(str(1), cel)
                            setStyle(self.pStyleDate, cel)
                    else:
                        createImage(float(i.xpos) - float(my_document.pagex),
                                    float(i.ypos) - float(my_document.pagey),
                                    float(i.width),
                                    float(i.height), str(i.anname))
                progressSet(run)
                run += 1
            # delete first empty page
            deletePage(1)

        except:
            self.quit()
        try:
            self.quit()
        except:
            pass
        return

    def get_year(self):
        self.year_var = int(self.frame2_spinbox_year.get())

    def make_frames(self):
        # ELEMENT MIDDLE FRAME 1
        frame1_root = Frame(self.canvas_frame)

        frame1_frame_types = Frame(frame1_root)
        frame1_frame_types.grid(row=0, column=0, columnspan=1, sticky=W + E + N + S)
        Label(frame1_frame_types, text="Types").pack(padx=10, pady=10)
        self.frame1_listbox_types = tk.Listbox(frame1_frame_types, width=20, exportselection=0)
        self.frame1_listbox_types.insert(tk.END, "Day")
        self.frame1_listbox_types.insert(tk.END, "Week")
        self.frame1_listbox_types.insert(tk.END, "Month")
        self.frame1_listbox_types.insert(tk.END, "Year")
        self.frame1_listbox_types.bind('<<ListboxSelect>>', self.action_select_type)
        self.frame1_listbox_types.pack()

        frame1_frame_models = Frame(frame1_root)
        frame1_frame_models.grid(row=0, column=1, columnspan=1, sticky=W + E + N + S)
        Label(frame1_frame_models, text="Models").pack(padx=10, pady=10)
        self.frame1_listbox_models = tk.Listbox(frame1_frame_models, width=20, exportselection=0)
        self.frame1_listbox_models.bind('<<ListboxSelect>>', self.action_get_models)
        self.frame1_listbox_models.pack()

        frame1_frame_import = Frame(frame1_root)
        frame1_frame_import.grid(row=1, column=0, rowspan=1, columnspan=1, sticky=W + E + N + S, padx=15, pady=15)
        Label(frame1_frame_import, text="Models import").pack(ipady=5)
        self.frame1_button_import = Button(frame1_frame_import, text="import .sla", command=self.action_import_model)
        self.frame1_button_import.pack()

        frame1_frame_orientation = Frame(frame1_root)
        frame1_frame_orientation.grid(row=1, column=1, rowspan=1, columnspan=1, sticky=W + E + N + S, padx=15, pady=15)

        Label(frame1_frame_orientation, text="Size").pack(ipady=5)
        frame1_combobox_size = ttk.Combobox(frame1_frame_orientation, textvariable=self.size, width=15)

        frame1_combobox_size['values'] = size_document
        frame1_combobox_size.current(4)
        #frame1_combobox_size.bind("<<ComboboxSelected>>", self.action_select_size)
        frame1_combobox_size.pack(pady=5, anchor='w')

        frame1_frame_vide = Frame(frame1_root)
        frame1_frame_vide.grid(row=3, column=1, rowspan=3, columnspan=2, sticky=W + E + N + S)

        frame1_frame_preview = Frame(frame1_root)
        frame1_frame_preview.grid(row=0, column=2, rowspan=6, columnspan=1, padx=20, sticky=W + E + N + S)
        Label(frame1_frame_preview, text="Preview").pack(padx=10, pady=10)

        self.photo = PhotoImage(file="format/month.png")
        self.previewCanvas = Canvas(frame1_frame_preview, width=200, height=200)
        self.photo_img = self.previewCanvas.create_image(0, 0, anchor=NW, image=self.photo)
        self.previewCanvas.pack()

        # ELEMENT MIDDLE FRAME 2
        frame2_root = Frame(self.canvas_frame)

        frame2_list_language = Frame(frame2_root, bg='green')
        frame2_list_language.grid(row=0, rowspan=3, column=0, sticky=W + E + N + S)
        Label(frame2_list_language, text="Languages").pack(padx=10, pady=10)

        scrollbar_listbox_language = Scrollbar(frame2_list_language, orient=VERTICAL)
        self.frame2_listbox_language = tk.Listbox(frame2_list_language, yscrollcommand=scrollbar_listbox_language.set)
        scrollbar_listbox_language.config(command=self.frame2_listbox_language.yview)
        scrollbar_listbox_language.pack(anchor='n', side=RIGHT, ipady=63)  # place scrollbar near to the listbox

        keys = localization.keys()
        keys.sort()
        for i in keys:
            self.frame2_listbox_language.insert(END, i)
        self.frame2_listbox_language.bind('<<ListboxSelect>>', self.action_get_language)
        self.frame2_listbox_language.pack()

        self.frame2_button = Button(frame2_list_language, text="import ICS", command=self.action_import_ics, padx=30, pady=10)
        self.frame2_button.pack(pady=20)

        frame2_checkbox = Frame(frame2_root, bg='yellow')
        frame2_vide = Frame(frame2_root, bg = 'cyan')
        frame2_vide.grid(row=0, column=2, pady=20, sticky=W + N + E + S)

        frame2_label = Frame(frame2_root, bg='blue')
        frame2_label.grid(row=1, column=2, padx=10, sticky=W + N + E + S)
        frame2_checkbox.grid(row=1, column=3, sticky=W + N + E + S)

        Label(frame2_label, text="Show previous days:").pack(padx=4, pady=4, anchor='w')
        Label(frame2_label, text="Show next days:").pack(padx=4, pady=4, anchor='w')
        Label(frame2_label, text="Short day name:").pack(padx=4, pady=4, anchor='w')
        Label(frame2_label, text="Next short day name:").pack(padx=4, pady=4, anchor='w')
        Label(frame2_label, text="Prev short day name:").pack(padx=4, pady=4, anchor='w')
        Label(frame2_label, text='Week begins with:').pack(padx=4, pady=4, anchor='w')
        Label(frame2_label, text='Year:').pack(padx=4, pady=20, anchor='w')

        Checkbutton(frame2_checkbox, variable=self.checkoption_prev_day, command=self.get_prev_day).pack(padx=3, pady=3, anchor='w')  # command=self.cb)
        Checkbutton(frame2_checkbox, variable=self.checkoption_next_day, command=self.get_next_day).pack(padx=3, pady=3, anchor='w')  # command=self.cb)
        Checkbutton(frame2_checkbox, variable=self.checkoption_short_day, command=self.get_short_day).pack(padx=3, pady=3, anchor='w')
        Checkbutton(frame2_checkbox, variable=self.checkoption_next_short_day, command=self.get_next_short_day).pack(padx=3, pady=3, anchor='w')  # command=self.cb)
        Checkbutton(frame2_checkbox, variable=self.checkoption_prev_short_day, command=self.get_prev_short_day).pack(padx=3, pady=3, anchor='w')  # command=self.cb)

        Radiobutton(frame2_checkbox, text='Mon', variable=self.week_var, value=calendar.MONDAY).pack()
        Radiobutton(frame2_checkbox, text='Sun', variable=self.week_var, value=calendar.SUNDAY).pack()

        self.frame2_spinbox_year = Spinbox(frame2_checkbox, width=5, from_=0, to=2132, wrap=True,
                                           textvariable=self.year_var, command=self.get_year)
        self.frame2_spinbox_year.delete(0, 1600)
        self.frame2_spinbox_year.insert(0, self.year_var)
        self.frame2_spinbox_year.pack(padx=3, pady=6, anchor='w')

        frame2_preview = Frame(frame2_root, bg='red')
        frame2_preview.grid(row=0, rowspan=3, column=4, sticky=W + E + N + S)
        Label(frame2_preview, text="Month").pack(padx=10, pady=10)
        self.scrollbar_listbox_month = Scrollbar(frame2_preview, orient=VERTICAL)
        self.frame2_listbox_month = tk.Listbox(frame2_preview, selectmode='multiple', exportselection=0,
                                               yscrollcommand=self.scrollbar_listbox_month.set)
        self.frame2_listbox_month.bind('<<ListboxSelect>>', self.action_select_month)
        self.scrollbar_listbox_month.config(command=self.frame2_listbox_month.yview)
        self.scrollbar_listbox_month.pack(anchor='ne', side=RIGHT, ipady=62)  # place scrollbar near to the listbox
        self.frame2_listbox_month.pack()
        Button(frame2_preview, text="Select All", command=self.select_all_month).pack(padx=10, pady=10)
        Button(frame2_preview, text="Unselect All", command=self.unselect_all_month).pack(padx=5, pady=5)

        # ELEMENT MIDDLE FRAME 3
        frame3_root = Frame(self.canvas_frame)
        frame3_root.rowconfigure(1, weight=1)

        frame3_frame_list = Frame(frame3_root)
        frame3_frame_list.grid(row=0, column=0, rowspan=3, sticky=W + E + N + S)
        Label(frame3_frame_list, text="Elements").pack(padx=10, pady=10)
        self.frame3_listbox_font = tk.Listbox(frame3_frame_list, exportselection=0)
        self.frame3_listbox_font.bind('<<ListboxSelect>>')
        self.frame3_listbox_font.pack()
        Button(frame3_frame_list, text='Uniform Font', command=self.select_all_elements).pack(pady=20,
                                                                                              anchor='center')

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
        Label(frame3_frame_font_label, text="Color:").pack(padx=15, pady=18, anchor='nw')

        self.fontVar = StringVar()
        self.fontStyleVar = StringVar()
        frame3_combobox_font = ttk.Combobox(frame3_frame_font_combobox, textvariable=self.fontVar)
        try:
            frame3_combobox_font['values'] = scribus.getFontNames()
        except:
            frame3_combobox_font['values'] = ('Arial', 'Comic', 'Times New Roman')

        frame3_combobox_font.current(1)
        frame3_combobox_font.bind("<<ComboboxSelected>>", self.action_select_font)
        frame3_combobox_font.pack(pady=10, anchor='w')

        frame3_combobox_font_style = ttk.Combobox(frame3_frame_font_combobox, textvariable=self.fontStyleVar)
        try:
            frame3_combobox_font_style['values'] = scribus.getFontStyle()
        except:
            frame3_combobox_font_style['values'] = ('Bold', 'Italic')

        frame3_combobox_font_style.current(1)
        frame3_combobox_font_style.bind("<<ComboboxSelected>>", self.action_select_font)
        frame3_combobox_font_style.pack(pady=10, anchor='w')

        Spinbox(frame3_frame_font_combobox, from_=2, to=300).pack(pady=10, anchor='w')
        Button(frame3_frame_font_combobox, text='Font Color', command=self.action_get_color).pack(pady=10, anchor='center')

        self.frame_master_allframes = [frame1_root, frame2_root, frame3_root]

    def quit(self):
        self.destroy()
        self.parent.destroy()

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        # configuration variable globale
        self.parent = parent

        self.frame_master_allframes = []
        self.frame_master_last_page = 0
        self.frame_master_max_page = 3
        self.frame_master_current_page = 0
        self.frame1_config_model_name = ''
        self.frame1_config_modelpath = './models/'
        self.frame1_config_type_string_selected = ''
        self.frame1_config_type_index_selected = IntVar()
        self.frame1_listbox_types = tk.Listbox()
        self.model_index_selected = IntVar()
        self.checkoption_prev_day = IntVar()
        self.checkoption_next_day = IntVar()
        self.checkoption_short_day = IntVar()
        self.checkoption_next_short_day = IntVar()
        self.checkoption_prev_short_day = IntVar()
        self.frame2_config_language_string_selected = 'English'
        self.frame2_config_language_index_selected = 0
        self.frame2_config_month_index_selected = []
        self.frame2_config_month_string_selected = []
        self.frame2_config_file_i_c_s = ''

        self.now = datetime.datetime.now()
        self.year_var = StringVar()
        self.year_entry = Entry(self, textvariable=self.year_var, width=4)
        self.status_var = StringVar()
        self.status_label = Label(self, textvariable=self.status_var)
        self.status_var.set('Select Options and Values')
        self.type_var = IntVar()
        self.year_var = self.now.year
        self.months = []
        self.draw_sauce = True
        self.sep_months = '/'
        self.lang = 'English'
        self.week_var = IntVar ()
        self.first_day = calendar.SUNDAY
        self.short_day_name = BooleanVar()
        self.next_short_day_name = BooleanVar()
        self.prev_short_day_name = BooleanVar()
        self.prev_day_name = BooleanVar()
        self.next_day_name = BooleanVar()
        self.week_number = BooleanVar()

        self.p_style_date = "Date"  # paragraph styles
        self.p_style_weekday = "Weekday"
        self.p_style_month = "Month"
        self.p_style_week_no = "WeekNo"
        self.layer_img = 'Calendar image'
        self.layer_cal = 'Calendar'
        self.master_page = "Weekdays"

        self.size = StringVar()

        self.make_top()
        self.make_middle()
        self.make_bottom()

        self.make_frames()
        # bottom frame
        self.update()


def main():
    """ Application/Dialog loop with Scribus sauce around """
    # try:
    print('Running script...')
    try:
        progressReset()
    except:
        pass
    root = tk.Tk()
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

