# -*- coding: utf-8 -*-
from Tkinter import *
from tkFileDialog import *
from lxml import etree
from shutil import copyfile

import ttk
# Python 2.x Version
from tkColorChooser import askcolor
# Python 3.x Version
# from tkinter.colorchooser import *
import Tkinter as tk
import sys
import calendar
import datetime
import re
import glob, os
import calendar
from math import sqrt
from sys import exit

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
    "format/calendrier-format-bureau.png",
    "format/calendrier-format-magnetique.png",
    "format/calendrier-format-mural.png",
    "format/calendrier-format-mural-double.png",
    "format/calendrier-format-poster.png"]

sizex = 700
sizey = 500
posx = 300
posy = 200


class ScCalendar:
    """ Parent class for all calendar types """

    def __init__(self, year, months=[], firstDay=calendar.SUNDAY, drawSauce=True, sepMonths='/', lang='English'):
        """ Setup basic things """
        # params
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
            print(self.year)
            print(i + 1)
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

    def __init__(self, year, months=[], firstDay=calendar.SUNDAY, drawSauce=True, sepMonths='/', lang='English'):
        ScCalendar.__init__(self, year, months, firstDay, drawSauce, sepMonths, lang)

    def print_month(self, cal, month, week):
        """ Print the month name(s) """
        if week[6].day < 7:
            if (week == cal[len(cal) - 1]):
                self.create_header(
                    localization[self.lang][0][month] + self.sepMonths + localization[self.lang][0][(month + 1) % 12])
            elif ((month - 1) not in self.months):
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

    def __init__(self, year, months=[], firstDay=calendar.SUNDAY, drawSauce=True, sepMonths='/', lang='English'):
        ScEventCalendar.__init__(self, year, months, firstDay, drawSauce, sepMonths, lang)

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

    def __init__(self, year, months=[], first_day=calendar.SUNDAY, draw_sauce=True, sep_months='/', lang='English'):
        ScCalendar.__init__(self, year, months, first_day, draw_sauce, sep_months, lang)

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
            create_image(self.marginl, self.margint,
                         self.width, self.cal_height - self.margint)


class ScClassicCalendar(ScVerticalCalendar):
    """ Calendar matrix creator itself. I suggest PORTRAIT orientation.
        One month per page."""

    def __init__(self, year, months=[], first_day=calendar.SUNDAY, draw_sauce=True, sep_months='/', lang='English'):
        ScVerticalCalendar.__init__(self, year, months, first_day, draw_sauce, sep_months, lang)

    def create_month_calendar(self, month, cal):
        """ Create a page and draw one month calendar on it """
        self.create_layout()
        self.create_header(localization[self.lang][0][month])
        row_cnt = 2
        for week in cal:
            col_cnt = 0
            for day in week:
                cel = createText(self.marginl + col_cnt * self.col_size,
                                 self.cal_height + row_cnt * self.row_size,
                                 self.col_size, self.row_size)
                col_cnt += 1
                if day.month == month + 1:
                    setText(str(day.day), cel)
                    setStyle(self.pStyleDate, cel)
            row_cnt += 1


class ScVerticalEventCalendar(ScVerticalCalendar, ScEventCalendar):
    """ One day = one column calendar. I suggest LANDSCAPE orientation.\
        One week per page."""

    def __init__(self, year, months=[], first_day=calendar.SUNDAY, draw_sauce=True, sep_months='/', lang='English'):
        ScVerticalCalendar.__init__(self, year, months, first_day, draw_sauce, sep_months, lang)
        ScEventCalendar.__init__(self, year, months, first_day, draw_sauce, sep_months, lang)

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


class TkCalendar(tk.Frame):
    # update the current page of the wizard
    def update(self):
        print(self.frame_master_current_page)  # show in terminal the number of the current page
        self.frame_master_allframes[self.frame_master_last_page].pack_forget()  # remove the last current page

        # If page == 2
        if self.frame_master_current_page == 2:
            if self.frame1_config_modelname != '':
                type_ele = re.compile('element=\'(.*)\'')
                tree = etree.parse(self.frame1_config_modelpath + self.frame1_config_modelname)
                keys = tree.getroot()
                for key in keys:
                    val = key.attrib['KEYWORDS']
                elements = re.findall(type_ele, val)
                spilted_elements = re.split(",", elements[0])
                print(spilted_elements)
                self.Frame3_listbox_font.delete(0, END)
                for i in spilted_elements:
                    self.Frame3_listbox_font.insert(END, i)

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
        print("Import model")
        try:
            filename = askopenfilename(title="Ouvrir votre document",
                                       filetypes=[('scribus files', '.sla'), ('all files', '.*')])
            # fichier = open(filename, "r")
            copyfile(filename, self.frame1_config_modelpath + os.path.basename(filename))
        # content = fichier.read()
        # fichier.close()
        except:
            print("No files imported.")

    # import an ICS file
    def action_import_ics(self):
        print("Import ics")
        try:
            filename = askopenfilename(title="Ouvrir votre document",
                                       filetypes=[('ics files', '.ics'), ('all files', '.*')])
            fichier = open(filename, "r")
            self.frame2_config_file_i_c_s = fichier.read()
            fichier.close()
        except:
            print("No files imported.")

        # goto next page

    def action_increment(self):
        self.frame_master_current_page = self.frame_master_current_page + 1
        self.update()

    # goto previous page
    def action_decrement(self):
        self.frame_master_current_page = self.frame_master_current_page - 1
        self.update()

    def action_finnish(self):
        print("Finnish")
        # try:
        #   year = self.year_var.get().strip()
        #   if len(year) != 4:
        #       raise ValueError
        #   year = int(year, 10)
        # except ValueError:
        #   print('err')
        #   self.status_var.set('Year must be in the "YYYY" format e.g. 2005.')
        #   return
        self.year = 2017
        print(self.year)
        print(self.sep_months)
        print(self.lang)
        # months
        # if len(self.frame2_config_month_string_selected) == 0:
        # 	print('At least one month must be selected.')
        # 	self.status_var.set('At least one month must be selected.')
        # 	return

        print(self.frame2_config_month_string_selected)
        # # draw images etc.
        # if self.imageVar.get() == 0:
        #   draw = False
        # else:
        #   draw = True
        # create calendar (finally)
        if self.type_var.get() == 0:
            cal = ScClassicCalendar(self.year, self.frame2_config_month_string_selected, self.week_var.get(),
                                    self.sep_months, self.lang)
        elif self.type_var.get() == 1:
            cal = ScHorizontalEventCalendar(self.year, self.frame2_config_month_string_selected, self.week_var.get(),
                                            self.sep_months, self.lang)
        else:
            cal = ScVerticalEventCalendar(self.year, self.frame2_config_month_string_selected, self.week_var.get(),
                                          self.sep_months, self.lang)
        # self.master.withdraw()
        tkMessageBox.showinfo("test", "Debut creation... ")
        err = cal.create_calendar()
        print("create Calendar DONE")
        if err is not None:
            self.deiconify()
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
            event.delta = -120;
        elif event.num == 4:
            event.delta = 120;
        print(datetime.datetime.now())
        tup = self.scrollbar_middle.get()
        if tup[0] != 0 or tup[1] != 1:
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        print(event.num)

    # update preview with the selected model
    def action_get_models(self, event):
        # get selected line index
        self.frame1_config_model_index_selected = self.Frame1_listbox_models.curselection()[0]
        print(self.Frame1_listbox_models.get(self.frame1_config_model_index_selected))
        self.frame1_config_modelname = self.Frame1_listbox_models.get(self.frame1_config_model_index_selected)

        self.Frame1_listbox_models.get(self.frame1_config_model_index_selected)
        self.photo = PhotoImage(file=imageCalender[self.frame1_config_model_index_selected])
        self.previewCanvas.itemconfigure(self.myimg, image=self.photo)
        self.previewCanvas.image = self.photo

    # update the list of months with the right language
    def action_get_language(self, event):
        # get selected line index
        try:
            self.frame2_config_language_index_selected = self.Frame2_listbox.curselection()[0]
            if self.frame2_config_language_index_selected == 0:
                return
            months = localization[self.Frame2_listbox.get(self.frame2_config_language_index_selected)][0]
            self.frame2_config_language_string_selected = self.Frame2_listbox.get(
                self.frame2_config_language_index_selected)

            self.Frame2_listbox_month.delete(0, END)
            for i in months:
                self.Frame2_listbox_month.insert(END, i)
        except:
            print("Language non reconnue")

    # get selected month
    def action_select_month(self, event):
        self.frame2_config_month_index_selected = self.Frame2_listbox_month.curselection()
        self.frame2_config_month_string_selected = []
        for tous in self.frame2_config_month_index_selected:
            self.frame2_config_month_index_selected = tous
            # self.frame2_config_month_string_selected.append(localization[self.Frame2_listbox.get(self.frame2_config_language_index_selected)][0][tous])
            self.frame2_config_month_string_selected.append(int(tous))
        print(self.frame2_config_month_string_selected)

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
        self.middle = Frame(self, width=650, height=400, padx=20, pady=20)
        self.middle.grid(row=1, column=0)

        self.canvas = Canvas(self.middle, width=650, height=400)
        self.canvas.pack()

        self.canvas_frame = Frame(self.canvas, width=650, height=400, padx=20, pady=20)
        self.canvas_frame.pack()
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
        self.frame1_config_type_index_selected = self.Frame1_listbox_types.curselection()[0]
        if self.frame1_config_type_index_selected == 0:
            return
        search_type = self.Frame1_listbox_types.get(self.frame1_config_type_index_selected)
        self.frame1_config_type_stirng_selected = search_type
        # mon_type='year'

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
        print available_models

        self.Frame1_listbox_models.delete(0, END)
        for i in available_models:
            self.Frame1_listbox_models.insert(END, i)

    # show button Previous, Next, and finnish
    def make_bottom(self):
        self.bottom = Frame(self)
        self.bottom.grid(row=2, column=0)
        self.bottom_button = [Button(self.bottom, text="Previous", padx=10, command=self.action_decrement),
                              Button(self.bottom, text="Next", padx=20, command=self.action_increment),
                              Button(self.bottom, padx=20, text="Finnish", command=self.action_finnish),
                              Button(self.bottom, padx=20, text="Cancel", command=self.quit)]
        for i in range(0, 4):
            self.bottom_button[i].grid(padx=10, row=0, column=i)

    def make_frames(self):
        ########### ELEMENT MIDDLE FRAME 1
        frame1_root = Frame(self.canvas_frame, padx=10, pady=10)
        frame1_frame_models = Frame(frame1_root)
        frame1_frame_models.grid(row=0, column=1, columnspan=1, sticky=W + E + N + S, padx=10)
        Label(frame1_frame_models, text="Models").pack(padx=10, pady=10)
        self.Frame1_listbox_models = tk.Listbox(frame1_frame_models, exportselection=0)
        self.Frame1_listbox_models.bind('<<ListboxSelect>>', self.action_get_models)
        self.Frame1_listbox_models.pack()

        frame1_frame_types = Frame(frame1_root)
        frame1_frame_types.grid(row=0, column=0, columnspan=1, sticky=W + E + N + S, padx=10)
        Label(frame1_frame_types, text="Types").pack(padx=10, pady=10)
        self.Frame1_listbox_types = tk.Listbox(frame1_frame_types, width=20, exportselection=0)
        self.Frame1_listbox_types.insert(tk.END, "month")
        self.Frame1_listbox_types.insert(tk.END, "year")
        self.Frame1_listbox_types.insert(tk.END, "day")
        self.Frame1_listbox_types.insert(tk.END, "week")
        self.Frame1_listbox_types.bind('<<ListboxSelect>>', self.action_select_type)
        self.Frame1_listbox_types.pack()

        frame1_frame_import = Frame(frame1_root)
        frame1_frame_import.grid(row=3, column=0, rowspan=1, columnspan=1, sticky=W + E + N + S)
        Label(frame1_frame_import, text="Models import").pack(padx=10, pady=10)
        self.Frame1_button_import = Button(frame1_frame_import, text="import .sla", command=self.action_import_model)
        self.Frame1_button_import.pack()

        self.typeClRadio = Radiobutton(frame1_frame_import, text='Classic', variable=self.type_var, value=0).pack()
        self.typeEvRadio = Radiobutton(frame1_frame_import, text='Event (Horizontal)', variable=self.type_var,
                                       value=1).pack()
        self.typeVERadio = Radiobutton(frame1_frame_import, text='Event (Vertical)', variable=self.type_var,
                                       value=2).pack()

        frame1_frame_vide = Frame(frame1_root)
        frame1_frame_vide.grid(row=3, column=1, rowspan=3, columnspan=2, sticky=W + E + N + S)

        frame1_frame_preview = Frame(frame1_root)
        frame1_frame_preview.grid(row=0, column=2, rowspan=6, columnspan=1, padx=20, sticky=W + E + N + S)
        Label(frame1_frame_preview, text="Preview").pack(padx=10, pady=10)
        self.photo = PhotoImage(file=imageCalender[0])
        self.previewCanvas = Canvas(frame1_frame_preview, width=150, height=220)
        self.myimg = self.previewCanvas.create_image(0, 0, anchor=NW, image=self.photo)
        self.previewCanvas.pack()

        ########### ELEMENT MIDDLE FRAME 2
        frame2_root = Frame(self.canvas_frame, padx=10, pady=10)
        frame2_list = Frame(frame2_root)
        frame2_list.grid(row=0, column=0, rowspan=5, columnspan=2, sticky=W + E + N + S)
        Label(frame2_list, text="Languages").pack(padx=10, pady=10)
        self.Frame2_listbox = tk.Listbox(frame2_list)
        keys = localization.keys()
        keys.sort()
        for i in keys:
            self.Frame2_listbox.insert(END, i)
        self.Frame2_listbox.bind('<<ListboxSelect>>', self.action_get_language)
        self.Frame2_listbox.pack()
        frame2_frame_import = Frame(frame2_root)
        frame2_frame_import.grid(row=3, column=2, rowspan=4, columnspan=1, sticky=W + E + N + S, padx=10, pady=10)
        self.Frame2_button = Button(frame2_frame_import, text="import ICS", command=self.action_import_ics, padx=30)
        self.Frame2_button.pack()
        frame2_option = Frame(frame2_root)
        frame2_option.grid(row=3, column=0, rowspan=3, columnspan=1, sticky=W + E + N + S)

        frame2_checkbox1 = Checkbutton(frame2_option, text="Number of week",
                                       variable=self.frame2_config_checkoption1)  # command=self.cb)
        frame2_checkbox2 = Checkbutton(frame2_option, text="Full day name",
                                       variable=self.frame2_config_checkoption2)  # command=self.cb)
        frame2_checkbox3 = Checkbutton(frame2_option, text="Previous day of current month",
                                       variable=self.frame2_config_checkoption3)  # command=self.cb)
        frame2_checkbox4 = Checkbutton(frame2_option, text="Next day of current month",
                                       variable=self.frame2_config_checkoption4)  # command=self.cb)
        frame2_checkbox1.pack()
        frame2_checkbox2.pack()
        frame2_checkbox3.pack()
        frame2_checkbox4.pack()

        Label(frame2_option, text='Week begins with:').pack()
        Radiobutton(frame2_option, text='Mon', variable=self.week_var, value=calendar.MONDAY).pack()
        Radiobutton(frame2_option, text='Sun', variable=self.week_var, value=calendar.SUNDAY).pack()

        frame2_preview = Frame(frame2_root)
        frame2_preview.grid(row=0, column=2, rowspan=3, columnspan=2, sticky=W + E + N + S)
        Label(frame2_preview, text="Month").pack(padx=10, pady=10)
        self.Frame2_listbox_month = tk.Listbox(frame2_preview, selectmode='multiple', exportselection=0)
        self.Frame2_listbox_month.bind('<<ListboxSelect>>', self.action_select_month)
        self.Frame2_listbox_month.pack()

        ########### ELEMENT MIDDLE FRAME 3
        frame3_root = Frame(self.canvas_frame, padx=10, pady=10)

        frame3_frame_list = Frame(frame3_root)
        frame3_frame_list.grid(row=0, column=0, columnspan=1, sticky=W + E + N + S)
        Label(frame3_frame_list, text="Elements").pack(padx=10, pady=10)
        self.Frame3_listbox_font = tk.Listbox(frame3_frame_list, exportselection=0)
        self.Frame3_listbox_font.bind('<<ListboxSelect>>', )  # self.get_list)
        self.Frame3_listbox_font.pack()

        frame3_frame_font = Frame(frame3_root)
        frame3_frame_font.grid(row=0, column=1, rowspan=1, columnspan=1, sticky=W + E + N + S)
        Label(frame3_frame_font, text="Font").pack(padx=10, pady=10)
        self.fontVar = StringVar()
        self.Frame3_combobox_font = ttk.Combobox(frame3_frame_font, textvariable=self.fontVar)
        try:
            self.Frame3_combobox_font['values'] = scribus.getFontNames()
        except:
            self.Frame3_combobox_font['values'] = ('Arial', 'Arial Bold', 'Arial Black')

        self.Frame3_combobox_font.current(1)
        self.Frame3_combobox_font.bind("<<ComboboxSelected>>", self.action_select_font)
        self.Frame3_combobox_font.pack()
        frame3_spinbox = Spinbox(frame3_frame_font, from_=2, to=100)
        frame3_spinbox.pack()
        frame3_colorpicker = Button(frame3_frame_font, text='Font Color', command=self.action_get_color)
        frame3_colorpicker.pack()

        self.frame_master_allframes = [frame1_root, frame2_root, frame3_root]

    # def create_calendar(self):
    # 	""" Walk through months dict and call monthly sheet """
    # 	print("create_calendar ...")
    # 	if not newDocDialog():
    # 		print("Create a new document first, please")
    # 		return
    # 	createParagraphStyle(name=self.p_style_date, alignment=ALIGN_RIGHT)
    # 	createParagraphStyle(name=self.p_style_weekday, alignment=ALIGN_RIGHT)
    # 	createParagraphStyle(name=self.p_style_month)
    # 	createParagraphStyle(name=self.p_style_week_no, alignment=ALIGN_RIGHT)
    # 	originalUnit = getUnit()
    # 	setUnit(UNIT_POINTS)
    # 	self.setupDocVariables()
    # 	if self.draw_sauce:
    # 		createLayer(self.layer_img)
    # 	createLayer(self.layer_cal)
    # 	self.setup_master_page()
    # 	run = 0
    # 	for i in self.frame2_config_month_string_selected:
    # 		run += 1
    # 		progressSet(run)
    # 		cal = self.mycal.monthdatescalendar(self.year, i + 1)
    # 		self.create_month_calendar(i, cal)
    # 	setUnit(originalUnit)
    # 	return None

    # def setupDocVariables(self):
    # 	""" Compute base metrics here. Page layout is bordered by margins and
    # 	virtually divided by golden mean 'cut' in the bottom. The calendar is
    # 	in the bottom part - top is occupied with empty image frame. """
    # 	page = getPageSize()
    # 	self.pagex = page[0]
    # 	self.pagey = page[1]
    # 	marg = getPageMargins()
    # 	# See http://docs.scribus.net/index.php?lang=en&page=scripterapi-page#-getPageMargins
    # 	self.margint = marg[0]
    # 	self.marginl = marg[1]
    # 	self.marginr = marg[2]
    # 	self.marginb = marg[3]
    # 	self.width = self.pagex - self.marginl - self.marginr
    # 	self.height = self.pagey - self.margint - self.marginb

    # def golden_mean(self, aSize):
    # 	""" Taken from samples/golden-mean.py."""
    # 	return aSize * ((sqrt(5) - 1)/2)

    def quit(self):
        self.destroy()
        self.parent.destroy()

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        # configuration variable globale
        self.parent = parent
        self.init_configure()

        self.frame_master_allframes = []
        self.frame_master_last_page = 0
        self.frame_master_max_page = 3
        self.frame_master_current_page = 0
        self.frame1_config_modelname = ''
        self.frame1_config_modelpath = './models/'
        self.frame1_config_type_stirng_selected = ''
        self.frame1_config_type_index_selected = IntVar()
        self.frame1_config_model_index_selected = IntVar()
        self.frame2_config_checkoption1 = IntVar()
        self.frame2_config_checkoption2 = IntVar()
        self.frame2_config_checkoption3 = IntVar()
        self.frame2_config_checkoption4 = IntVar()
        self.frame2_config_language_string_selected = 'English'
        self.frame2_config_language_index_selected = 0
        self.frame2_config_month_index_selected = []
        self.frame2_config_month_string_selected = []
        self.frame2_config_file_i_c_s = ''

        self.year_var = StringVar()
        self.year_entry = Entry(self, textvariable=self.year_var, width=4)
        self.status_var = StringVar()
        self.status_label = Label(self, textvariable=self.status_var)
        self.status_var.set('Select Options and Values')
        self.type_var = IntVar()
        self.year_var = set(str(datetime.date(1, 1, 1).today().year))
        self.year = 0
        self.months = []
        self.first_day = calendar.SUNDAY
        self.draw_sauce = True
        self.sep_months = '/'
        self.lang = 'English'
        self.week_var = IntVar()

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
    app = TkCalendar(root).pack(side="top", fill="both", expand=True)

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

