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

# Image of calendar model
imageCalender = [
    "format/format-day.png",
    "format/format-week.png",
    "format/format-week-month.png",
    "format/format-month.png",
    "format/format-year.png"]

sizex = 650
sizey = 350
posx = 300
posy = 200

class ScCalendar:
    """ Parent class for all calendar types """

    def __init__(self, prev_day_name, next_day_name, short_day_name, lang, year, months=[], firstDay=calendar.SUNDAY, drawSauce=True, sepMonths='/'):
        """ Setup basic things """
        # params
        self.short_day_name = short_day_name
        self.prev_day_name = prev_day_name
        self.next_day_name = next_day_name
        self.drawSauce = drawSauce  # draw supplementary image?
        self.year = year
        self.months = months
        self.lang = lang
        # day order
        self.dayOrder = localization[self.lang][1]
        if firstDay == calendar.SUNDAY:
            dl = self.dayOrder[:6]
            dl.insert(0, self.dayOrder[6])
            self.dayOrder = dl
        self.mycal = calendar.Calendar(firstDay)

        self.layerImg = 'Calendar image'
        self.layerCal = 'Calendar'
        self.pStyleDate = "Date"  # paragraph styles
        self.pStyleWeekday = "Weekday"
        self.pStyleMonth = "Month"
        self.pStyleWeekNo = "WeekNo"
        self.masterPage = "Weekdays"
        self.sepMonths = sepMonths
        # settings
        self.firstPage = True  # create only 2nd 3rd ... pages. No 1st one.
        calendar.setfirstweekday(firstDay)
        progressTotal(len(months))

    def setup_doc_variables(self):
        """ Compute base metrics here. Page layout is bordered by margins and
        virtually divided by golden mean 'cut' in the bottom. The calendar is
        in the bottom part - top is occupied with empty image frame. """
        page = getPageSize()
        self.pagex = page[0]
        self.pagey = page[1]
        marg = getPageMargins()
        # See http://docs.scribus.net/index.php?lang=en&page=scripterapi-page#-getPageMargins
        self.margint = marg[0]
        self.marginl = marg[1]
        self.marginr = marg[2]
        self.marginb = marg[3]
        self.width = self.pagex - self.marginl - self.marginr
        self.height = self.pagey - self.margint - self.marginb

    def golden_mean(self, aSize):
        """ Taken from samples/golden-mean.py."""
        return aSize * ((sqrt(5) - 1) / 2)

    def apply_text_to_frame(self, aText, aFrame):
        """ Insert the text with style. """
        setText(aText, aFrame)
        setStyle(self.pStyleDate, aFrame)

    def create_calendar(self):
        """ Walk through months dict and call monthly sheet """
        if not newDocDialog():
            return 'Create a new document first, please'
        createParagraphStyle(name=self.pStyleDate, alignment=ALIGN_RIGHT)
        createParagraphStyle(name=self.pStyleWeekday, alignment=ALIGN_RIGHT)
        createParagraphStyle(name=self.pStyleMonth)
        createParagraphStyle(name=self.pStyleWeekNo, alignment=ALIGN_RIGHT)
        originalUnit = getUnit()
        setUnit(UNIT_POINTS)
        self.setup_doc_variables()
        if self.drawSauce:
            createLayer(self.layerImg)
        createLayer(self.layerCal)
        self.setup_master_page()
        run = 0
        for i in self.months:
            run += 1
            progressSet(run)
            cal = self.mycal.monthdatescalendar(self.year, i + 1)
            self.create_month_calendar(i, cal)
        setUnit(originalUnit)
        return None

    def create_layout(self):
        """ Create the page and optional bells and whistles around """
        self.create_page()
        if self.drawSauce:
            setActiveLayer(self.layerImg)
            self.create_image()
        setActiveLayer(self.layerCal)

    def create_page(self):
        """ Wrapper to the new page with layers """
        if self.firstPage:
            self.firstPage = False
            newPage(-1, self.masterPage)  # create a new page using the master_page
            deletePage(1)  # now it's safe to delete the first page
            gotoPage(1)
            return
        newPage(-1, self.masterPage)


class ScEventCalendar(ScCalendar):
    """ Parent class for event
        (horizontal event, vertical event) calendar types """

    def __init__(self, prev_day_name, next_day_name, short_day_name, year, months=[], firstDay=calendar.SUNDAY, drawSauce=True, sepMonths='/', lang='English'):
        ScCalendar.__init__(self, prev_day_name, next_day_name, short_day_name, year, months, firstDay, drawSauce, sepMonths, lang)

    def print_month(self, cal, month, week):
        """ Print the month name(s) """
        if week[6].day < 7:
            if week == cal[len(cal) - 1]:
                self.create_header(
                    localization[self.lang][0][month] + self.sepMonths + localization[self.lang][0][(month + 1) % 12])
            elif month - 1 not in self.months:
                self.create_header(
                    localization[self.lang][0][(month - 1) % 12] + self.sepMonths + localization[self.lang][0][month])
        else:
            self.create_header(localization[self.lang][0][month])

    def create_month_calendar(self, month, cal):
        """ Draw one week calendar per page """
        for week in cal:
            # Avoid duplicate week around the turn of the months:
            # Only include week:
            # * If it's not the first week in a month, or, if it is:
            # * If it starts on the first weekday
            # * If the month before it isn't included
            if (week != cal[0]) or (week[0].day == 1) or ((month - 1) not in self.months):
                self.create_layout()
                self.print_month(cal, month, week)
                self.print_week_no(week)

                for day in week:
                    self.print_day(day)


class ScHorizontalEventCalendar(ScEventCalendar):
    """ One day = one row calendar. I suggest LANDSCAPE orientation.\
        One week per page."""

    def __init__(self, prev_day_name, next_day_name, short_day_name, year, months=[], firstDay=calendar.SUNDAY, drawSauce=True, sepMonths='/', lang='English'):
        ScEventCalendar.__init__(self, prev_day_name, next_day_name, short_day_name, year, months, firstDay, drawSauce, sepMonths, lang)

    def setup_doc_variables(self):
        """ Compute base metrics here. Page layout is bordered by margins and
        virtually divided by golden mean 'cut' in the bottom. The calendar is
        in the bottom part - top is occupied with empty image frame. """
        # golden mean
        ScCalendar.setup_doc_variables(self)
        self.gmean = self.width - self.golden_mean(self.width) + self.marginl
        # calendar size = gmean
        # rows and cols
        self.rowSize = self.height / 8

    def print_week_no(self, week):
        """ Dummy for now
            (for this type of calendar - see ScVerticalEventCalendar) """
        return

    def print_day(self, j):
        """ Print a given day """
        cel = createText(self.gmean + self.marginl,
                         self.margint + (1 + (j.weekday() - calendar.firstweekday()) % 7) * self.rowSize,
                         self.width - self.gmean, self.rowSize)
        setText(str(j.day), cel)
        setStyle(self.pStyleDate, cel)

    def create_header(self, monthName):
        """ Draw calendar header: Month name """
        cel = createText(self.gmean + self.marginl, self.margint,
                         self.width - self.gmean, self.rowSize)
        setText(monthName, cel)
        setStyle(self.pStyleMonth, cel)

    def create_image(self):
        """ Wrapper for everytime-the-same image frame. """
        if self.drawSauce:
            createImage(self.marginl, self.margint, self.gmean, self.height)

    def setup_master_page(self):
        """ Create a master page (not used for this type of calendar """
        createMasterPage(self.masterPage)
        closeMasterPage()


class ScVerticalCalendar(ScCalendar):
    """ Parent class for vertical
        (classic, vertical event) calendar types """

    def __init__(self, prev_day_name, next_day_name, short_day_name, lang, year, months=[], first_day=calendar.SUNDAY, draw_sauce=True, sep_months='/'):
        ScCalendar.__init__(self, prev_day_name, next_day_name, short_day_name, lang, year, months, first_day, draw_sauce, sep_months)

    def setup_doc_variables(self):
        """ Compute base metrics here. Page layout is bordered by margins and
        virtually divided by golden mean 'cut' in the bottom. The calendar is
        in the bottom part - top is occupied with empty image frame. """
        # gloden mean
        ScCalendar.setup_doc_variables(self)
        self.gmean = self.height - self.golden_mean(self.height) + self.margint
        # calendar size
        self.cal_height = self.height - self.gmean + self.margint
        # rows and cols
        self.row_size = self.gmean / 8
        self.col_size = self.width / 7

    def setup_master_page(self):
        """ Draw invariant calendar header: Days of the week """
        createMasterPage(self.masterPage)
        editMasterPage(self.masterPage)
        setActiveLayer(self.layerCal)
        row_cnt = 0
        for j in self.dayOrder:  # days
            cel = createText(self.marginl + row_cnt * self.col_size,
                             self.cal_height + self.row_size,
                             self.col_size, self.row_size)
            if self.short_day_name is 1: #Si checkbox short day cochee alors jour raccourcis
                setText(j[:3] + ".", cel)
            else:
                setText(j, cel)
            setStyle(self.pStyleWeekday, cel)
            row_cnt += 1
        closeMasterPage()

    def create_header(self, monthName):
        """ Draw calendar header: Month name """
        header = createText(self.marginl, self.cal_height, self.width, self.row_size)
        setText(monthName, header)
        setStyle(self.pStyleMonth, header)

    def create_image(self):
        """ Wrapper for everytime-the-same image frame. """
        if self.drawSauce:
            createImage(self.marginl, self.margint,
                         self.width, self.cal_height - self.margint)


class ScClassicCalendar(ScVerticalCalendar):
    """ Calendar matrix creator itself. I suggest PORTRAIT orientation.
        One month per page."""

    def __init__(self, prev_day_name, next_day_name, short_day_name, lang, year, months=[], first_day=calendar.SUNDAY, draw_sauce=True, sep_months='/'):
        ScVerticalCalendar.__init__(self, prev_day_name, next_day_name, short_day_name, lang, year, months, first_day, draw_sauce, sep_months)

    def create_month_calendar(self, month, cal):
        """ Create a page and draw one month calendar on it """
        self.create_layout()
        self.create_header(localization[self.lang][0][month])
        row_cnt = 2

        # creer les box pour les jours du mois et les remplies
        for week in cal:
            col_cnt = 0
            for day in week:
                cel = createText(self.marginl + col_cnt * self.col_size,
                                 self.cal_height + row_cnt * self.row_size,
                                 self.col_size, self.row_size)
                col_cnt += 1
                if self.prev_day_name is 1 and day.month < month + 1:
                    setText(str(day.day), cel)
                    setStyle(self.pStyleDate, cel)
                if self.next_day_name is 1 and day.month > month + 1:
                    setText(str(day.day), cel)
                    setStyle(self.pStyleDate, cel)
                if day.month == month + 1:
                    setText(str(day.day), cel)
                    setStyle(self.pStyleDate, cel)
            row_cnt += 1


class ScVerticalEventCalendar(ScVerticalCalendar, ScEventCalendar):
    """ One day = one column calendar. I suggest LANDSCAPE orientation.\
        One week per page."""

    def __init__(self, prev_day_name, next_day_name, short_day_name, lang, year, months=[], first_day=calendar.SUNDAY, draw_sauce=True, sep_months='/'):
        ScVerticalCalendar.__init__(self, prev_day_name, next_day_name, short_day_name, lang, year, months, first_day, draw_sauce, sep_months)
        ScEventCalendar.__init__(self, prev_day_name, next_day_name, short_day_name, lang, year, months, first_day, draw_sauce, sep_months)

    def print_day(self, j):
        """ Print a given day """
        cel = createText(self.marginl + ((j.weekday() - calendar.firstweekday()) % 7) * self.col_size,
                         self.cal_height + self.row_size,
                         self.col_size / 5, self.row_size)
        setText(str(j.day), cel)
        setStyle(self.pStyleDate, cel)

    def print_week_no(self, week):
        """ Print the week number for the given week"""
        week_cel = createText(self.marginl, self.cal_height, self.width, self.row_size)
        # Week number: of this week's Thursday.
        # See http://docs.python.org/library/datetime.html#datetime.date.isocalendar
        # Note that week calculation isn't perfectly universal yet:
        # http://en.wikipedia.org/wiki/Week_number#Week_number
        setText(str(week[(calendar.THURSDAY - calendar.firstweekday()) % 7].isocalendar()[1]), week_cel)
        setStyle(self.pStyleWeekNo, week_cel)


class BoxObject:
    """ BoxObject represent some attribut from PAGEOBJECT from scribus file. """
    def __init__(self, xpos, ypos, width, height, anname, img=False):
        self.xpos = xpos
        self.ypos = ypos
        self.width = width
        self.height = height
        self.anname = anname
        self.img = img


class Document:
    """ Document contains all attribute useful about master page, margin, etc."""
    def __init__(self, path_file):
        self.path_file = path_file

        self.pagex = 0.0
        self.pagey = 0.0
        self.border_left = 0.0
        self.border_right = 0.0
        self.border_top = 0.0
        self.border_bottom = 0.0
        self.size = "A4"
        self.orientation = BooleanVar()

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
            self.orientation = balise.get("Orientation")
            self.border_left = balise.get("BORDERLEFT")
            self.border_right = balise.get("BORDERRIGHT")
            self.border_top = balise.get("BORDERTOP")
            self.border_bottom = balise.get("BORDERBOTTOM")
            self.size = str(balise.get("Size"))


class TkCalendar(tk.Frame):
    # update the current page of the wizard
    def update(self):
        #print(self.frame_master_current_page)  # show in terminal the number of the current page

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
                #print(spilted_elements)
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

    def action_finnish(self):
        try:
            self.year_var = self.frame2_spinbox_year.get()
            year = str(self.year_var)
            if len(year) != 4:
                raise ValueError
            self.year = int(year)
        except ValueError:
            self.status_var.set('Year must be in the "YYYY" format e.g. 2005.')
            return

        # create calendar (finally)
        if self.type_var.get() == 0:
            cal = ScClassicCalendar(self.prev_day_name, self.next_day_name, self.short_day_name, self.lang, self.year, self.frame2_config_month_string_selected, self.week_var.get(),
                                    self.sep_months)
        elif self.type_var.get() == 1:
            cal = ScHorizontalEventCalendar(self.prev_day_name, self.next_day_name, self.short_day_name, self.year, self.frame2_config_month_string_selected, self.week_var.get(),
                                            self.sep_months, self.lang)
        else:
            cal = ScVerticalEventCalendar(self.prev_day_name, self.next_day_name, self.short_day_name, self.year, self.frame2_config_month_string_selected, self.week_var.get(),
                                          self.sep_months, self.lang)
        tkMessageBox.showinfo("Action", "Creating Calendar... ")
        err = cal.create_calendar()
        if err is not None:
            self.status_var.set(err)
        else:
            self.quit()

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
        # [6:-4] meaning 6: model- et :-4 .sla
        model_name = self.frame1_config_model_name[6:-4]

        for i in imageCalender:
            if i[14:-4] == model_name:
                self.photo = PhotoImage(file=i)
                self.previewCanvas.itemconfigure(self.photo_img, image=self.photo, anchor=NW)
                self.previewCanvas.image = self.photo

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
        print(self.fontVar.get())

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
                    print(val)
                    #  Si on trouve un type de calendrier dans les KEYWORDS du document
                    #  on recupere ce modele pour l'afficher dans l'etape suivante
                    avail = re.findall(type_cal, val)
                    if avail:
                        available_models.append(model)
        #print available_models

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
        self.short_day_name = self.checkoption_short_day.get()

    def get_prev_day(self):
        self.prev_day_name = self.checkoption_prev_day.get()

    def get_next_day(self):
        self.next_day_name = self.checkoption_next_day.get()

    def get_week_number(self):
        self.week_number = self.checkoption_week_number.get()

    def setup_doc_variables(self):
        """ Compute base metrics here. Page layout is bordered by margins and
        virtually divided by golden mean 'cut' in the bottom. The calendar is
        in the bottom part - top is occupied with empty image frame. """

        self.dayOrder = localization[self.lang][1]

        self.layerImg = 'Calendar image'
        self.layerCal = 'Calendar'

        self.masterPage = "Weekdays"
        # settings
        self.firstPage = True  # create only 2nd 3rd ... pages. No 1st one.


        page = getPageSize()
        self.pagex = page[0]
        self.pagey = page[1]
        marg = getPageMargins()
        # See http://docs.scribus.net/index.php?lang=en&page=scripterapi-page#-getPageMargins
        self.margint = marg[0]
        self.marginl = marg[1]
        self.marginr = marg[2]
        self.marginb = marg[3]
        self.width = self.pagex - self.marginl - self.marginr
        self.height = self.pagey - self.margint - self.marginb

        self.gmean = self.height - self.golden_mean(self.height) + self.margint
        # calendar size
        self.cal_height = self.height - self.gmean + self.margint
        # rows and cols
        self.row_size = self.gmean / 8
        self.col_size = self.width / 7

    def create_layout(self):
        """ Create the page and optional bells and whistles around """
        self.create_page()
        #setActiveLayer(self.layerCal)

    def create_page(self):
        """ Wrapper to the new page with layers """
        if self.firstPage:
            self.firstPage = False
            newPage(-1)  # create a new page using the master_page
            deletePage(1)  # now it's safe to delete the first page
            gotoPage(1)
            return
        newPage(-1)

    def create_header(self, monthName):
        """ Draw calendar header: Month name """
        cel = createText(self.gmean + self.marginl, self.margint,
                         self.width - self.gmean, self.rowSize)
        setText(monthName, cel)
        setStyle(self.pStyleMonth, cel)

    def my_test(self):
        if self.frame1_config_model_name == '':
            self.frame1_config_model_name = 'test.sla'

        my_document = Document(self.frame1_config_modelpath + self.frame1_config_model_name)
        print my_document.size
        print my_document.border_left
        print my_document.border_right
        print my_document.border_top
        print my_document.border_bottom
        print my_document.orientation

        test = "PAPER_" + my_document.size

# reverif enumerate
        try:
            if not newDocument(eval(test),
                    (float(my_document.border_left), float(my_document.border_right),
                     float(my_document.border_top), float(my_document.border_bottom)),
                    int(my_document.orientation), 1, UNIT_POINTS, NOFACINGPAGES, FIRSTPAGELEFT, 1):
                print 'Create a new document first, please'
                return
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
            for i in my_document.box_container:
                if i.img is False:
                    cel = createText(float(i.xpos) - float(my_document.pagex),
                                     float(i.ypos) - float(my_document.pagey),
                                     float(i.width),
                                     float(i.height), str(i.anname))
                    setText(str(i.anname), cel)
                    setStyle(self.pStyleDate, cel)
                else:
                    createImage(float(i.xpos) - float(my_document.pagex),
                                float(i.ypos) - float(my_document.pagey),
                                float(i.width),
                                float(i.height), str(i.anname))

            #newPage(-1)
            #cel = createText(40, 40, 100, 100)
            #setText(str(1), cel)
            #setStyle(self.pStyleDate, cel)
            #img2 = createImage(140, 140, 100, 100)
        except:
            self.quit()
        try:
            self.quit()
        except:
            pass
        return

    def make_frames(self):
        # ELEMENT MIDDLE FRAME 1
        frame1_root = Frame(self.canvas_frame, padx=10, pady=10)

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
        frame1_frame_import.grid(row=1, column=0, rowspan=1, columnspan=1, sticky=W + E + N + S, padx=20, pady=20)
        Label(frame1_frame_import, text="Models import").pack(padx=10, pady=10)
        self.Frame1_button_import = Button(frame1_frame_import, text="import .sla", command=self.action_import_model)
        self.Frame1_button_import.pack()

        frame1_frame_orientation = Frame(frame1_root)
        frame1_frame_orientation.grid(row=1, column=1, rowspan=1, columnspan=1, sticky=W + E + N + S, padx=30, pady=30)

        Button(frame1_frame_orientation, text="MYTEST", command=self.my_test).pack(ipady=15)

        self.typeClRadio = Radiobutton(frame1_frame_orientation, text='Classic', variable=self.type_var, value=0).pack()
        self.typeEvRadio = Radiobutton(frame1_frame_orientation, text='Event (Horizontal)', variable=self.type_var,
                                       value=1).pack()
        self.typeVERadio = Radiobutton(frame1_frame_orientation, text='Event (Vertical)', variable=self.type_var,
                                       value=2).pack()

        frame1_frame_vide = Frame(frame1_root)
        frame1_frame_vide.grid(row=3, column=1, rowspan=3, columnspan=2, sticky=W + E + N + S)

        frame1_frame_preview = Frame(frame1_root)
        frame1_frame_preview.grid(row=0, column=2, rowspan=6, columnspan=1, padx=20, sticky=W + E + N + S)
        Label(frame1_frame_preview, text="Preview").pack(padx=10, pady=10)

        self.photo = PhotoImage(file=imageCalender[3])
        self.previewCanvas = Canvas(frame1_frame_preview, width=180, height=240)
        self.photo_img = self.previewCanvas.create_image(0, 0, anchor=NW, image=self.photo)
        self.previewCanvas.pack()

        # ELEMENT MIDDLE FRAME 2
        frame2_root = Frame(self.canvas_frame)

        frame2_list_language = Frame(frame2_root)
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

        frame2_checkbox = Frame(frame2_root)
        frame2_vide = Frame(frame2_root)
        frame2_vide.grid(row=0, column=2, pady=20, sticky=W + N + E + S)

        frame2_label = Frame(frame2_root)
        frame2_label.grid(row=1, column=2, padx=10, sticky=W + N + E + S)
        frame2_checkbox.grid(row=1, column=3, sticky=W + N + E + S)

        Label(frame2_label, text="Show previous days:").pack(padx=4, pady=4, anchor='w')
        Label(frame2_label, text="Show next days:").pack(padx=4, pady=4, anchor='w')
        Label(frame2_label, text="Short day name:").pack(padx=4, pady=4, anchor='w')
        Label(frame2_label, text="Number of week:").pack(padx=4, pady=4, anchor='w')
        Label(frame2_label, text='Week begins with:').pack(padx=4, pady=4, anchor='w')
        Label(frame2_label, text='Year:').pack(padx=4, pady=20, anchor='w')

        Checkbutton(frame2_checkbox, variable=self.checkoption_prev_day, command=self.get_prev_day).pack(padx=3, pady=3, anchor='w')  # command=self.cb)
        Checkbutton(frame2_checkbox, variable=self.checkoption_next_day, command=self.get_next_day).pack(padx=3, pady=3, anchor='w')  # command=self.cb)
        Checkbutton(frame2_checkbox, variable=self.checkoption_short_day, command=self.get_short_day).pack(padx=3, pady=3, anchor='w')
        Checkbutton(frame2_checkbox, variable=self.checkoption_week_number, command=self.get_week_number).pack(padx=3, pady=3, anchor='w')  # command=self.cb)

        Radiobutton(frame2_checkbox, text='Mon', variable=self.week_var, value=calendar.MONDAY).pack()
        Radiobutton(frame2_checkbox, text='Sun', variable=self.week_var, value=calendar.SUNDAY).pack()

        self.frame2_spinbox_year = Spinbox(frame2_checkbox, width=5, from_=1600, to=2132,
                                           textvariable=self.year_var)
        self.frame2_spinbox_year.delete(0, 1600)
        self.frame2_spinbox_year.insert(0, self.year_var)
        self.frame2_spinbox_year.pack(padx=3, pady=6, anchor='w')

        frame2_frame_import = Frame(frame2_root)
        frame2_frame_import.grid(row=2, column=2, columnspan=2, sticky=N + E + S + W)
        self.frame2_button = Button(frame2_frame_import, text="import ICS", command=self.action_import_ics, padx=30, pady=10)
        self.frame2_button.pack()

        frame2_preview = Frame(frame2_root)
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
        frame3_root = Frame(self.canvas_frame, padx=10, pady=10)
        frame3_root.rowconfigure(1, weight=1)

        frame3_frame_list = Frame(frame3_root)
        frame3_frame_list.grid(row=0, column=0, rowspan=3, sticky=W + E + N + S)
        Label(frame3_frame_list, text="Elements").pack(padx=20, pady=20)
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
        self.model_index_selected = IntVar()
        self.checkoption_prev_day = IntVar()
        self.checkoption_next_day = IntVar()
        self.checkoption_short_day = IntVar()
        self.checkoption_week_number = IntVar()
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
        self.first_day = calendar.SUNDAY
        self.draw_sauce = True
        self.sep_months = '/'
        self.lang = 'English'
        self.week_var = IntVar()
        self.short_day_name = BooleanVar()
        self.prev_day_name = BooleanVar ()
        self.next_day_name = BooleanVar ()
        self.week_number = BooleanVar()

        self.p_style_date = "Date"  # paragraph styles
        self.p_style_weekday = "Weekday"
        self.p_style_month = "Month"
        self.p_style_week_no = "WeekNo"
        self.layer_img = 'Calendar image'
        self.layer_cal = 'Calendar'
        self.master_page = "Weekdays"
        self.day_order = localization[self.lang][1]

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
    # progressReset()
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

