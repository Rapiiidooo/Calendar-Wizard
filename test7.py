# -*- coding: utf-8 -*-
from Tkinter import *
from tkFileDialog import *
from lxml import etree
from shutil import copyfile

import ttk
#Python 2.x Version
from tkColorChooser import askcolor              
#Python 3.x Version
#from tkinter.colorchooser import *
import Tkinter as tk
import sys
import calendar
import datetime
import re
import glob,os
try:
    import scribus
except ImportError:
    print('This Python script is written for the Scribus scripting interface.')


#Translation day/month
localization = {
'Catalan' :
    [['Gener', 'Febrer', 'Març', 'Abril', 'Maig',
      'Juny', 'Juliol', 'Agost', 'Setembre',
      'Octubre', 'Novembre', 'Desembre'],
     ['Dilluns', 'Dimarts', 'Dimecres', 'Dijous', 'Divendres', 'Dissabte', 'Diumenge']],
'Catalan-short' :
    [['Gener', 'Febrer', 'Març', 'Abril', 'Maig',
      'Juny', 'Juliol', 'Agost', 'Setembre',
      'Octubre', 'Novembre', 'Desembre'],
     ['Dl', 'Dm', 'Dc', 'Dj', 'Dv', 'Ds', 'Dg']],
# Catalan by "Cesc Morata" <atarom@gmail.com>
'Czech' :
    [['Leden', 'Únor', 'Březen', 'Duben', 'Květen',
        'Červen', 'Červenec', 'Srpen', 'Září',
        'Říjen', 'Listopad', 'Prosinec'],
     ['Pondělí','Úterý','Středa','Čtvrtek','Pátek','Sobota', 'Neděle']],
'Czech-short' :
    [['Leden', 'Únor', 'Březen', 'Duben', 'Květen',
        'Červen', 'Červenec', 'Srpen', 'Září',
        'Říjen', 'Listopad', 'Prosinec'],
     ['Po', 'Út', 'St', 'Čt', 'Pá', 'So', 'Ne']],
# Croatian by daweed
'Croatian' :
    [['Siječanj', 'Veljača', 'Ožujak', 'Travanj', 'Svibanj',
        'Lipanj', 'Srpanj', 'Kolovoz', 'Rujan',
        'Listopad', 'Studeni', 'Prosinac'],
     ['Ponedjeljak','Utorak','Srijeda','Četvrtak','Petak','Subota', 'Nedjelja']],

'Dutch' :
    [['Januari', 'Februari', 'Maart', 'April',
      'Mei', 'Juni', 'Juli', 'Augustus', 'September',
      'Oktober', 'November', 'December'],
     ['Maandag','Dinsdag','Woensdag','Donderdag','Vrijdag','Zaterdag', 'Zondag']],
# Dutch by "Christoph Schäfer" <christoph-schaefer@gmx.de>
'English' :
    [['January', 'February', 'March', 'April',
      'May', 'June', 'July', 'August', 'September',
      'October', 'November', 'December'],
     ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday', 'Sunday']],
'English-short' :
    [['January', 'February', 'March', 'April', 'May',
      'June', 'July', 'August', 'September', 'October',
      'November', 'December'],
     ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']],
'Finnish' :
    [['Tammikuu', 'Helmikuu', 'Maaliskuu', 'Huhtikuu',
      'Toukokuu', 'Kesäkuu', 'Heinäkuu', 'Elokuu', 'Syyskuu',
      'Lokakuu', 'Marraskuu', 'Joulukuu'],
     ['ma','ti','ke','to','pe','la', 'su']],
'French':
    [['Janvier', u'F\xe9vrier', 'Mars', 'Avril',
      'Mai', 'Juin', 'Juillet', u'Ao\xfbt', 'Septembre',
      'Octobre', 'Novembre', u'D\xe9cembre'],
     ['Lundi','Mardi','Mercredi','Jeudi','Vendredi','Samedi','Dimanche']],
'German' :
    [['Januar', 'Februar', u'M\xe4rz', 'April',
      'Mai', 'Juni', 'Juli', 'August', 'September',
      'Oktober', 'November', 'Dezember'],
     ['Montag','Dienstag','Mittwoch','Donnerstag','Freitag','Samstag','Sonntag']],
'German (Austrian)' :
    [[u'J\xe4nner', 'Feber', u'M\xe4rz', 'April',
      'Mai', 'Juni', 'Juli', 'August', 'September',
      'Oktober', 'November', 'Dezember'],
     ['Montag','Dienstag','Mittwoch','Donnerstag','Freitag','Samstag','Sonntag']],
# Hungarian by Gergely Szalay szalayg@gmail.com	      
'Hungarian' :
    [['Január', 'Február', 'Március', 'Április',
       'Május', 'Június', 'Július', 'Augusztus', 'Szeptember',
       'Október', 'November', 'December'],
    ['Hétfő','Kedd','Szerda','Csütörtök','Péntek','Szombat','Vasárnap']],
'Italian' :
    [['Gennaio', 'Febbraio', 'Marzo', 'Aprile',
       'Maggio', 'Giugno', 'Luglio', 'Agosto', 'Settembre',
       'Ottobre', 'Novembre', 'Dicembre'],
    [u'Luned\xec', u'Marted\xec', u'Mercoled\xec', u'Gioved\xec', u'Venerd\xec', 'Sabato', 'Domenica']],
# Norwegian by Joacim Thomassen joacim@net.homelinux.org
'Norwegian' :
    [['Januar', 'Februar','Mars', 'April','Mai', 'Juni','Juli', 'August','September', 'Oktober', 'November', 'Desember'],
     ['Mandag', 'Tirsdag','Onsdag', 'Torsdag','Fredag', 'Lørdag','Søndag']],
# Polish by "Łukasz [DeeJay1] Jernaś" <deejay1@nsj.srem.pl>
'Polish' :
    [['Styczeń', 'Luty', 'Marzec', 'Kwiecień', 'Maj',
      'Czerwiec', 'Lipiec', 'Sierpień', 'Wrzesień',
      'Październik', 'Listopad', 'Grudzień'],
     ['Poniedziałek', 'Wtorek', 'Środa', 'Czwartek', 'Piątek', 'Sobota', 'Niedziela']],
'Portuguese' :
    [['Janeiro', 'Fevereiro', u'Mar\xe7o', 'Abril',
      'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro',
      'Outubro', 'Novembro', 'Dezembro'],
     ['Segunda-feira', u'Ter\xe7a-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', u'S\xe1bado', 'Domingo']],
# Romanian by Costin Stroie <costinstroie@eridu.eu.org>
'Romanian' :
    [['Ianuarie', 'Februarie', 'Martie', 'Aprilie',
      'Mai', 'Iunie', 'Iulie', 'August', 'Septembrie',
      'Octombrie', 'Noiembrie', 'Decembrie'],
     ['Luni','Mar\xc8\x9bi','Miercuri','Joi','Vineri','S\xc3\xa2mb\xc4\x83t\xc4\x83', 'Duminic\xc4\x83']],
'Russian' :
    [['Январь', 'Февраль', 'Март', 'Апрель',
      'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь',
      'Октябрь', 'Ноябрь', 'Декабрь'],
     ['Понедельник','Вторник','Среда','Четверг','Пятница','Суббота', 'Воскресенье']],
'Slovak' :
    [['Január', 'Február', 'Marec', 'Apríl',
      'Máj', 'Jún', 'Júl', 'August', 'September',
      'Október', 'November', 'December'],
      ['Pondelok','Utorok','Streda','Štvrtok','Piatok','Sobota', 'Nedeľa']],
'Slovak-short' :
    [['Január', 'Február', 'Marec', 'Apríl',
      'Máj', 'Jún', 'Júl', 'August', 'September',
      'Október', 'November', 'December'],
      ['Po','Ut','St','Št','Pi','So', 'Ne']],
'Spanish' :
    [['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo',
      'Junio', 'Julio', 'Agosto', 'Septiembre',
      'Octubre', 'Noviembre', 'Diciembre'],
     ['Lunes', 'Martes', u'Mi\xe9rcoles', 'Jueves', 'Viernes', u'S\xe1bado', 'Domingo']],
'Swedish' :
    [['Januari', 'Februari','Mars', 'April','Maj', 'Juni','Juli', 'Augusti','September', 'Oktober', 'November', 'December'],
     ['Måndag', 'Tisdag','Onsdag', 'Torsdag','Fredag', 'Lördag','Söndag']]
}

#Image of calendar model
imageCalender = [
"format/calendrier-format-bureau.png",
"format/calendrier-format-magnetique.png",
"format/calendrier-format-mural.png",
"format/calendrier-format-mural-double.png",
"format/calendrier-format-poster.png"]

sizex = 650
sizey = 450
posx  = 100
posy  = 100



class MainApplication(tk.Frame):
	#update the current page of the wizard
    def update(self):
        print(self.FrameMaster_currentPage) #show in terminal the number of the current page
        self.FrameMaster_allframes[self.FrameMaster_lastPage].pack_forget() #remove the last current page

        #If element page
        if(self.FrameMaster_currentPage == 2 ):
            if(self.Frame1_config_modelname != ''):
                type_ele = re.compile('element=\'(.*)\'')
                tree = etree.parse(self.Frame1_config_modelpath+self.Frame1_config_modelname)
                keys = tree.getroot()
                for key in keys:
                    val=key.attrib['KEYWORDS']
                elements=re.findall(type_ele,val)
                spilted_elements=re.split(",",elements[0])
                print(spilted_elements) 
                self.Frame3_listbox_font.delete(0, END)
                for i in spilted_elements:
                    self.Frame3_listbox_font.insert(END, i)

        #if type page
        if(self.FrameMaster_currentPage <= 0):
            self.FrameMaster_currentPage = 0
            self.bottom_button[0].config(state=DISABLED)
            self.bottom_button[2].config(state=DISABLED)
        else:
            if(self.FrameMaster_currentPage >= self.FrameMaster_maxPage - 1):
                self.FrameMaster_currentPage = self.FrameMaster_maxPage - 1
                self.bottom_button[1].config(state=DISABLED)
                self.bottom_button[2].config(state=ACTIVE)
            else:
                self.bottom_button[1].config(state=ACTIVE)
                self.bottom_button[2].config(state=DISABLED)
                self.bottom_button[0].config(state=ACTIVE)
        
        self.FrameMaster_allframes[self.FrameMaster_currentPage].pack()
        self.FrameMaster_lastPage=self.FrameMaster_currentPage
        self.canvas.yview_moveto(0.0)
        self.scrollbar_middle.set(0.0, 1.0)

    #import file .sla
    def actionImportModel(self):
        print("Import model")
      	try:
        	filename = askopenfilename(title="Ouvrir votre document",filetypes = [('scrubus files','.sla'), ('all files','.*') ] )
        	#fichier = open(filename, "r")
        	copyfile(filename,self.Frame1_config_modelpath+os.path.basename(filename))
        	#content = fichier.read()
        	#fichier.close()	
        except:
        	print("No files imported.")

    #import an ICS file
    def actionImportICS(self):
        print("Import ics")
        try:
        	filename = askopenfilename(title="Ouvrir votre document",filetypes = [('ics files','.ics'), ('all files','.*') ] )
        	fichier = open(filename, "r")
        	self.Frame2_config_fileICS = fichier.read()
        	fichier.close()
        except:
			print("No files imported.")        	

    #goto next page
    def actionIncrement(self):
        self.FrameMaster_currentPage = self.FrameMaster_currentPage + 1
        self.update()

	#goto previous page
    def actionDecrement(self):
        self.FrameMaster_currentPage = self.FrameMaster_currentPage - 1
        self.update()

    #get all elements of the wizard inside a canvas.
    def actionCanvas(self, event):
        tup = self.scrollbar_middle.get()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        if(tup[0] == 0 and tup[1] == 1):
            self.canvas.yview_moveto(0.0)

    #define the scroll
    def actionMouseWeel(self, event):
        if(event.num == 5):
            event.delta = -120;
        elif(event.num == 4):
            event.delta = 120;
        print(datetime.datetime.now())
        tup = self.scrollbar_middle.get()
        if(tup[0] != 0 or tup[1] != 1):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        print(event.num)

    #update preview with the selected model
    def actionGetModels(self,event):
        # get selected line index
        self.Frame1_config_modelIndexSelected = self.Frame1_listbox_models.curselection()[0]
        print(self.Frame1_listbox_models.get(self.Frame1_config_modelIndexSelected))
        self.Frame1_config_modelname=self.Frame1_listbox_models.get(self.Frame1_config_modelIndexSelected)


        self.Frame1_listbox_models.get(self.Frame1_config_modelIndexSelected)
        self.photo=PhotoImage(file=imageCalender[self.Frame1_config_modelIndexSelected])
        self.previewCanvas.itemconfigure(self.myimg,image=self.photo)
        self.previewCanvas.image = self.photo

    #update the list of months with the right language
    def actionGetLanguage(self,event):
        # get selected line index
        try:
        	self.Frame2_config_languageIndexSelected = self.Frame2_listbox.curselection()[0]
        	if self.Frame2_config_languageIndexSelected == 0:
        	    return        
        	months=localization[self.Frame2_listbox.get(self.Frame2_config_languageIndexSelected)][0]	
        	self.Frame2_config_languageStringSelected=self.Frame2_listbox.get(self.Frame2_config_languageIndexSelected)

        	self.Frame2_listbox_month.delete(0, END)
        	for i in months:
        	    self.Frame2_listbox_month.insert(END, i)
       	except:
       		print("Language non reconnue")


    #get selected month
    def actionSelectMonth(self,event):
        self.Frame2_config_monthIndexSelected=self.Frame2_listbox_month.curselection()
        self.Frame2_config_monthStringSelected=[]
        for tous in self.Frame2_config_monthIndexSelected:
            self.Frame2_config_monthIndexSelected = tous
            self.Frame2_config_monthStringSelected.append(localization[self.Frame2_listbox.get(self.Frame2_config_languageIndexSelected)][0][tous])
        print(self.Frame2_config_monthStringSelected)
        
    #get color for button "Font Color"
    def actionGetColor(self):
        color = askcolor() 
        print color

    #define title label
    def makeTop(self):
        self.top = Frame(self)
        self.top.grid(row = 0, column = 0)
        self.top_label = Label(self.top, text="Calendar wizard 2")
        self.top_label.pack()

    #define the middle gridPane
    def makeMiddle(self):
        self.middle = Frame(self,width=600, height=350, padx=20, pady = 20 )
        self.middle.grid(row=1, column=0)

        self.canvas = Canvas(self.middle, width=600, height=350)
        self.canvas.pack()

        self.canvas_frame = Frame(self.canvas,width=600, height=350, padx=20, pady = 20)
        self.canvas_frame.pack()
        self.canvas_frame.bind("<Configure>", self.actionCanvas)

        self.scrollbar_middle=Scrollbar(self.middle,orient = "vertical",command = self.canvas.yview)
        self.canvas.configure(yscrollcommand = self.scrollbar_middle.set)

        self.scrollbar_middle.pack(side="right", fill="y")
        self.canvas.pack(side="left")
        self.canvas.create_window((0,0),window=self.canvas_frame,anchor='nw')
	if sys.platform == "Windows":
             self.canvas.bind_all("<MouseWheel>", self.actionMouseWeel)
	elif sys.platform == "Linux":
            self.canvas.bind_all("<Button-4>", self.actionMouseWeel)
            self.canvas.bind_all("<Button-5>", self.actionMouseWeel)


    #action when clicking on a Font button in Page 3
    def actionSelectFont(self, event):
        print(self.fontVar.get())
        

    def actionSelectType(self, event):
        self.Frame1_config_typeIndexSelected = self.Frame1_listbox_types.curselection()[0]
        if self.Frame1_config_typeIndexSelected ==0:
            return
        search_type=self.Frame1_listbox_types.get(self.Frame1_config_typeIndexSelected)
        self.Frame1_config_typeStirngSelected=search_type    
        #mon_type='year'
            
        type_cal=re.compile('type=\'.*' + search_type + '.*\'')

        # On cherche dans le repertoire avec les modeles

        available_models=[]

        # On parcours tous les documents qui se terminent par .sla dans le
        # repertoire qui contient les modeles
        for model in os.listdir(self.Frame1_config_modelpath):
            if model.endswith(".sla"):

        # On parse chaque modele pour voir quels sont les keywords definis
                tree = etree.parse(self.Frame1_config_modelpath+model)
                keys = tree.getroot()
                for key in keys:
                    val=key.attrib['KEYWORDS']

        # Si on trouve un type de calendrier dans les KEYWORDS du document
        # on recupere ce modele pour l'afficher dans l'etape suivante
                    avail=re.findall(type_cal,val)
                    if avail:
                        available_models.append(model)
        print available_models
        
        self.Frame1_listbox_models.delete(0, END)
        for i in available_models:
            self.Frame1_listbox_models.insert(END, i)


    #show button Previous, Next, and finnish
    def makeBottom(self):
        self.bottom = Frame(self)
        self.bottom.grid(row=2, column=0)
        self.bottom_button=[Button(self.bottom, text = "Previous", padx = 10, command=self.actionDecrement),Button(self.bottom, text = "Next", padx = 20, command = self.actionIncrement),Button(self.bottom, padx = 20, text = "Finnish")]
        for i in range(0,3):
            self.bottom_button[i].grid(padx = 10, row=0, column=i)


    def makeFrames(self):
        ########### ELEMENT MIDDLE FRAME 1
        Frame1_root = Frame(self.canvas_frame, padx=10, pady = 10)
        Frame1_frame_models = Frame(Frame1_root)
        Frame1_frame_models.grid(row = 0, column = 1, columnspan = 1,sticky = W+E+N+S, padx = 10) 
        Label(Frame1_frame_models, text="Models").pack(padx=10, pady=10)
        self.Frame1_listbox_models = tk.Listbox(Frame1_frame_models,exportselection=0)
        self.Frame1_listbox_models.bind('<<ListboxSelect>>', self.actionGetModels)
        self.Frame1_listbox_models.pack()


        Frame1_frame_types = Frame(Frame1_root)       
        Frame1_frame_types.grid(row = 0, column = 0,columnspan = 1,sticky = W+E+N+S, padx = 10) 
        Label(Frame1_frame_types, text="Types").pack(padx=10, pady=10)
        self.Frame1_listbox_types = tk.Listbox(Frame1_frame_types,width=20,exportselection=0)
        self.Frame1_listbox_types.insert(tk.END, "month")
        self.Frame1_listbox_types.insert(tk.END, "year")
        self.Frame1_listbox_types.insert(tk.END, "day")
        self.Frame1_listbox_types.insert(tk.END, "week")
        self.Frame1_listbox_types.bind('<<ListboxSelect>>', self.actionSelectType)
        self.Frame1_listbox_types.pack()


        Frame1_frame_import = Frame(Frame1_root)
        Frame1_frame_import.grid(row = 3, column = 0, rowspan = 1, columnspan = 1, sticky = W+E+N+S)
        Label(Frame1_frame_import, text="Models import").pack(padx=10, pady=10)
        self.Frame1_button_import=Button(Frame1_frame_import, text = "import .sla",command=self.actionImportModel)
        self.Frame1_button_import.pack()


        Frame1_frame_vide = Frame(Frame1_root)
        Frame1_frame_vide.grid(row = 3, column = 1, rowspan = 3, columnspan = 2, sticky = W+E+N+S)


        Frame1_frame_preview = Frame(Frame1_root)
        Frame1_frame_preview.grid(row = 0, column = 2, rowspan = 6, columnspan =1, padx = 20, sticky = W+E+N+S)
        Label(Frame1_frame_preview, text="Preview").pack(padx=10, pady=10)
        self.photo=PhotoImage(file=imageCalender[0])
        self.previewCanvas = Canvas(Frame1_frame_preview,width=150, height=220)
        self.myimg=self.previewCanvas.create_image(0, 0,anchor=NW, image=self.photo)
        self.previewCanvas.pack()



        ########### ELEMENT MIDDLE FRAME 2
        Frame2_root = Frame(self.canvas_frame, padx=10, pady = 10)
        Frame2_list = Frame(Frame2_root)
        Frame2_list.grid(row = 0, column = 0, rowspan = 5, columnspan = 2, sticky = W+E+N+S) 
        Label(Frame2_list, text="Languages").pack(padx=10, pady=10)
        self.Frame2_listbox = tk.Listbox(Frame2_list)
        keys = localization.keys()
        keys.sort()
        for i in keys:
            self.Frame2_listbox.insert(END, i)
        self.Frame2_listbox.bind('<<ListboxSelect>>', self.actionGetLanguage)
        self.Frame2_listbox.pack()
 
        Frame2_frame_import = Frame(Frame2_root)
        Frame2_frame_import.grid(row = 3, column = 2, rowspan = 4, columnspan = 1, sticky = W+E+N+S, padx=10, pady = 10)
        self.Frame2_button=Button(Frame2_frame_import, text = "import ICS",command=self.actionImportICS, padx=30)
        self.Frame2_button.pack()
        Frame2_option = Frame(Frame2_root)
        Frame2_option.grid(row = 3, column = 0, rowspan = 3, columnspan = 1, sticky = W+E+N+S)


        Frame2_checkbox1 = Checkbutton(Frame2_option, text="Number of week", variable=self.Frame2_config_checkoption1) #command=self.cb)
        Frame2_checkbox2 = Checkbutton(Frame2_option, text="Full day name", variable=self.Frame2_config_checkoption2) #command=self.cb)
        Frame2_checkbox3 = Checkbutton(Frame2_option, text="Previous day of current month", variable=self.Frame2_config_checkoption3) #command=self.cb)
        Frame2_checkbox4 = Checkbutton(Frame2_option, text="Next day of current month", variable=self.Frame2_config_checkoption4) #command=self.cb)
        Frame2_checkbox1.pack()
        Frame2_checkbox2.pack()
        Frame2_checkbox3.pack()
        Frame2_checkbox4.pack()




        Frame2_preview = Frame(Frame2_root)
        Frame2_preview.grid(row = 0, column = 2, rowspan = 3, columnspan = 2, sticky = W+E+N+S)
        Label(Frame2_preview, text="Month").pack(padx=10, pady=10)
        self.Frame2_listbox_month = tk.Listbox(Frame2_preview,selectmode='multiple',exportselection=0)
        self.Frame2_listbox_month.bind('<<ListboxSelect>>', self.actionSelectMonth)
        self.Frame2_listbox_month.pack()


        ########### ELEMENT MIDDLE FRAME 3
        Frame3_root = Frame(self.canvas_frame, padx=10, pady = 10)

        Frame3_frame_list = Frame(Frame3_root)
        Frame3_frame_list.grid(row = 0, column = 0, columnspan = 1,sticky = W+E+N+S) 
        Label(Frame3_frame_list, text="Elements").pack(padx=10, pady=10)
        self.Frame3_listbox_font = tk.Listbox(Frame3_frame_list,exportselection=0)
        self.Frame3_listbox_font.bind('<<ListboxSelect>>',)# self.get_list)
        self.Frame3_listbox_font.pack()


        Frame3_frame_font = Frame(Frame3_root)
        Frame3_frame_font.grid(row = 0, column = 1, rowspan = 1, columnspan = 1, sticky = W+E+N+S)  
        Label(Frame3_frame_font, text="Font").pack(padx=10, pady=10)
        self.fontVar = StringVar()
        self.Frame3_combobox_font = ttk.Combobox(Frame3_frame_font, textvariable=self.fontVar)
        try:
            self.Frame3_combobox_font['values'] = scribus.getFontNames()
        except :
            self.Frame3_combobox_font['values'] = ('Arial', 'Arial Bold', 'Arial Black')

        self.Frame3_combobox_font.current(1)
        self.Frame3_combobox_font.bind("<<ComboboxSelected>>", self.actionSelectFont)
        self.Frame3_combobox_font.pack()
        Frame3_spinbox = Spinbox(Frame3_frame_font, from_=2, to=100)
        Frame3_spinbox.pack()    
        Frame3_colorpicker=Button(Frame3_frame_font, text='Font Color', command=self.actionGetColor)
        Frame3_colorpicker.pack()
            
        
        self.FrameMaster_allframes = [Frame1_root, Frame2_root, Frame3_root]

    def initConfigure(self):
        self.FrameMaster_allframes=[]
        self.FrameMaster_lastPage = 0
        self.FrameMaster_maxPage = 3
        self.FrameMaster_currentPage = 0
        self.Frame1_config_modelname=''
        self.Frame1_config_modelpath='./models/'
        self.Frame1_config_typeStirngSelected=''
        self.Frame1_config_typeIndexSelected = IntVar()
        self.Frame1_config_modelIndexSelected = IntVar()
        self.Frame2_config_checkoption1 = IntVar()
        self.Frame2_config_checkoption2 = IntVar()
        self.Frame2_config_checkoption3 = IntVar()
        self.Frame2_config_checkoption4 = IntVar()
        self.Frame2_config_languageStringSelected = 'English'
        self.Frame2_config_languageIndexSelected = 0
        self.Frame2_config_monthIndexSelected = []  
        self.Frame2_config_monthStringSelected = []        
        self.Frame2_config_fileICS = ''

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        # configuration variable globale
        self.parent = parent
        self.initConfigure()
        self.makeTop()
        self.makeMiddle()
        self.makeBottom()
        
        self.makeFrames()
        # bottom frame
        
        self.update()
    
if __name__ == "__main__":
    root = tk.Tk()
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.wm_geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))
    root.mainloop()
