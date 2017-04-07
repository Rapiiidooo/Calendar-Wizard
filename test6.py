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
except ImportError,err:
    print 'This Python script is written for the Scribus scripting interface.'

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

typeOfCalender = {
#'French' :
    'bancaire', 'bureau', 'magnetique', 'mural', 'double-mural', 'poster'
}

imageCalender = [
"format/calendrier-format-bancaire.png",
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
    # page variable
    maxPage = 3
    current = 0
    last = 0
    list_frames=[]
    
    def update(self):
        print(self.current)
        self.frames[self.last].pack_forget()
        
        if(self.current <= 0):
            self.current = 0
            self.bottom_button[0].config(state=DISABLED)
            self.bottom_button[2].config(state=DISABLED)
        else:
            if(self.current >= self.maxPage - 1):
                self.current = self.maxPage - 1
                self.bottom_button[1].config(state=DISABLED)
                self.bottom_button[2].config(state=ACTIVE)
            else:
                self.bottom_button[1].config(state=ACTIVE)
                self.bottom_button[2].config(state=DISABLED)
                self.bottom_button[0].config(state=ACTIVE)
        # if(self.last != -1):
        #     self.list_frames[self.last].grid_forget()
        # self.list_frames[self.current].grid(row = 1, column=0)
        
        self.frames[self.current].pack()
        self.last=self.current
        self.canvas.yview_moveto(0.0)
        self.scrollbar_middle.set(0.0, 1.0)

    def importAction(self):#import marche
        print("import")
        models_path='./models/'
        filename = askopenfilename(title="Ouvrir votre document",filetypes = [('scrubus files','.sla'), ('all files','.*') ] )
        #fichier = open(filename, "r")
        copyfile(filename,models_path+os.path.basename(filename))
        #content = fichier.read()
        #fichier.close()        

    def importActionICS(self):
        print("import ics")
        filename = askopenfilename(title="Ouvrir votre document",filetypes = [('ics files','.ics'), ('all files','.*') ] )
        fichier = open(filename, "r")
        content = fichier.read()
        fichier.close()        

    def increment(self):

        self.current = self.current + 1
        self.update()

    def decrement(self):
        self.current = self.current - 1
        self.update()

    def _event_canvas(self, event):
        tup = self.scrollbar_middle.get()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        if(tup[0] == 0 and tup[1] == 1):
            self.canvas.yview_moveto(0.0)

    def _on_mousewheel(self, event):
        if(event.num == 5):
            event.delta = -120;
        elif(event.num == 4):
            event.delta = 120;
        print(datetime.datetime.now())
        tup = self.scrollbar_middle.get()
        if(tup[0] != 0 or tup[1] != 1):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        print(event.num)

    def get_list2(self,event):
        # get selected line index
        index = self.Frame1_listbox.curselection()[0]
        self.photo=PhotoImage(file=imageCalender[index])
        self.previewCanvas.itemconfigure(self.myimg,image=self.photo)
        self.previewCanvas.image = self.photo

    def get_langage(self,event):
        # get selected line index
        self.index = self.Frame2_listbox.curselection()[0]
        months=localization[self.Frame2_listbox.get(self.index)][0]	
    
        self.Frame2_listboxMonth.delete(0, END)
        for i in months:
            self.Frame2_listboxMonth.insert(END, i)


    def select_month(self,event):
        index2 = self.Frame2_listboxMonth.curselection()[0]
        print(localization[self.Frame2_listbox.get(self.index)][0][index2])

    def getColor(self):
        color = askcolor() 
        print color


    def make_top(self):
        self.top = Frame(self, bg='green')
        self.top.grid(row = 0, column = 0)
        self.top_label = Label(self.top, text="Calendar wizard 2")
        self.top_label.pack()

    def make_middle(self):
        self.middle = Frame(self, bg='blue',width=600, height=350, padx=20, pady = 20 )
        self.middle.grid(row=1, column=0)

        self.canvas = Canvas(self.middle, width=600, height=350,bg = 'orange')
        self.canvas.pack()

        self.canvas_frame = Frame(self.canvas,width=600, height=350, bg = 'black', padx=20, pady = 20)
        self.canvas_frame.pack()
        self.canvas_frame.bind("<Configure>", self._event_canvas)

        self.scrollbar_middle=Scrollbar(self.middle,orient = "vertical",command = self.canvas.yview)
        self.canvas.configure(yscrollcommand = self.scrollbar_middle.set)

        self.scrollbar_middle.pack(side="right", fill="y")
        self.canvas.pack(side="left")
        self.canvas.create_window((0,0),window=self.canvas_frame,anchor='nw')
	if sys.platform == "Windows":
             self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
	elif sys.platform == "Linux":
            self.canvas.bind_all("<Button-4>", self._on_mousewheel)
            self.canvas.bind_all("<Button-5>", self._on_mousewheel)

    def make_bottom(self):
        self.bottom = Frame(self, bg='red')
        self.bottom.grid(row=2, column=0)
        self.bottom_button=[Button(self.bottom, text = "prev",command=self.decrement),Button(self.bottom, text = "next",command=self.increment),Button(self.bottom, text = "finish")]
        for i in range(0,3):
            self.bottom_button[i].grid(row=0, column=i)
    def selectFont(self, event):
        print(self.fontVar.get())




    def selectType(self, event):
        index = self.Frame1_listbox2.curselection()[0]
        if index==0:
            return
        mon_type=self.Frame1_listbox2.get(index)
        if mon_type==0:
            return

       #mon_type='year'
        models_path='./models/'
            
        type_cal=re.compile('type=\'.*' + mon_type + '.*\'')

        # On cherche dans le repertoire avec les modeles

        available_models=[]

        # On parcours tous les documents qui se terminent par .sla dans le
        # repertoire qui contient les modeles
        for model in os.listdir(models_path):
            if model.endswith(".sla"):

        # On parse chaque modele pour voir quels sont les keywords definis
                tree = etree.parse(models_path+model)
                keys = tree.getroot()
                for key in keys:
                    val=key.attrib['KEYWORDS']

        # Si on trouve un type de calendrier dans les KEYWORDS du document
        # on recupere ce modele pour l'afficher dans l'etape suivante
                    avail=re.findall(type_cal,val)
                    if avail:
                        available_models.append(model)
        print available_models

        self.Frame1_listbox.delete(0, END)
        for i in available_models:
            self.Frame1_listbox.insert(END, i)






    def make_frames(self):
        frame3 = Frame(self.canvas_frame, bg = 'black', padx=20, pady = 20)

        Frame3_list2 = Frame(frame3, bg="blue")
        Frame3_list2.grid(row = 0, column = 0, columnspan = 1,sticky = W+E+N+S) 
        Label(Frame3_list2, text="Elements",bg="blue").pack(padx=10, pady=10)
        self.Frame3_listbox = tk.Listbox(Frame3_list2,exportselection=0)
        self.Frame3_listbox.insert(tk.END,"Days string")
        self.Frame3_listbox.insert(tk.END,"Weeks string")
        self.Frame3_listbox.insert(tk.END,"Months string")
        self.Frame3_listbox.insert(tk.END,"Years string")
        self.Frame3_listbox.insert(tk.END,"Days number")
        self.Frame3_listbox.insert(tk.END,"Weeks number")
        self.Frame3_listbox.insert(tk.END,"Months number")
        self.Frame3_listbox.insert(tk.END,"Years number")
        self.Frame3_listbox.bind('<<ListboxSelect>>',)# self.get_list)
        self.Frame3_listbox.pack()


        Frame3_list = Frame(frame3, bg="blue")
        Frame3_list.grid(row = 0, column = 1, rowspan = 1, columnspan = 1, sticky = W+E+N+S)  
        Label(Frame3_list, text="Font",bg="blue").pack(padx=10, pady=10)
        self.fontVar = StringVar()
        self.Frame3_combo = ttk.Combobox(Frame3_list, textvariable=self.fontVar)
        try:
            self.Frame3_combo['values'] = scribus.getFontNames()
        except :
            self.Frame3_combo['values'] = ('Arial', 'Arial Bold', 'Arial Black')

        self.Frame3_combo.current(1)
        self.Frame3_combo.bind("<<ComboboxSelected>>",self.selectFont)
        self.Frame3_combo.pack()
        Frame3_size = Frame(frame3, bg="blue")
        Frame3_size.grid(row = 1, column = 0, rowspan = 1, columnspan = 1, sticky = W+E+N+S)  
        Frame3_spinbox = Spinbox(Frame3_list, from_=2, to=100)
        Frame3_spinbox.pack()    
        Frame3_colorpicker=Button(Frame3_list,text='Font Color', command=self.getColor)
        Frame3_colorpicker.pack()
        Frame3_list.grid(row = 0, column = 1, rowspan = 1, columnspan = 2, sticky = W+E+N+S)  
        Label(Frame3_list, text="Font",bg="blue").pack()








        ########### ELEMENT MIDDLE FRAME 1
        frame2 = Frame(self.canvas_frame,bg = 'violet',padx=20, pady = 20)
        Frame2_list = Frame(frame2, bg="blue")
        Frame2_list.grid(row = 0, column = 0, rowspan = 5, columnspan = 2, sticky = W+E+N+S) 
        Label(Frame2_list, text="Languages",bg="blue").pack(padx=10, pady=10)
        self.Frame2_listbox = tk.Listbox(Frame2_list)
        keys = localization.keys()
        keys.sort()
        for i in keys:
            self.Frame2_listbox.insert(END, i)
        self.Frame2_listbox.bind('<<ListboxSelect>>', self.get_langage)
        self.Frame2_listbox.pack()
 
        Frame2_import = Frame(frame2,bg="red")
        Frame2_import.grid(row = 3, column = 2, rowspan = 4, columnspan = 1, sticky = W+E+N+S)
        self.Frame2_button=Button(Frame2_import, text = "import ICS",command=self.importActionICS)
        self.Frame2_button.pack()
        Frame2_option = Frame(frame2,bg="yellow")
        Frame2_option.grid(row = 3, column = 0, rowspan = 3, columnspan = 1, sticky = W+E+N+S)
        #self.Frame2_button2=Button(Frame2_option, text = "import ICS",command=self.importAction)
        #self.Frame2_button2.pack()

        self.var1 = IntVar()
        self.var2 = IntVar()
        self.var3 = IntVar()
        self.var4 = IntVar()
        Frame2_checkbox1 = Checkbutton(Frame2_option, text="Numero de jour", variable=self.var1) #command=self.cb)
        Frame2_checkbox2 = Checkbutton(Frame2_option, text="Nom de jour entier", variable=self.var2) #command=self.cb)
        Frame2_checkbox3 = Checkbutton(Frame2_option, text="Afficher mois suivant", variable=self.var3) #command=self.cb)
        Frame2_checkbox4 = Checkbutton(Frame2_option, text="Afficher mois precedent", variable=self.var4) #command=self.cb)

        Frame2_checkbox1.pack()
        Frame2_checkbox2.pack()
        Frame2_checkbox3.pack()
        Frame2_checkbox4.pack()




        Frame2_preview = Frame(frame2, bg="green")
        Frame2_preview.grid(row = 0, column = 2, rowspan = 3, columnspan = 1, sticky = W+E+N+S)
        Label(Frame2_preview, text="Month",bg="green").pack(padx=10, pady=10)
        self.Frame2_listboxMonth = tk.Listbox(Frame2_preview,selectmode='multiple',exportselection=0)
        self.Frame2_listboxMonth.bind('<<ListboxSelect>>', self.select_month)
        self.Frame2_listboxMonth.pack()


      
        ########### ELEMENT MIDDLE FRAME 1


        frame1 = Frame(self.canvas_frame,bg = 'violet',padx=20, pady = 20)
        Frame1_list = Frame(frame1, bg="blue")
        Frame1_list.grid(row = 0, column = 1, columnspan = 1,sticky = W+E+N+S) 
        Label(Frame1_list, text="Models",bg="blue").pack(padx=10, pady=10)
        self.Frame1_listbox = tk.Listbox(Frame1_list,exportselection=0)
        self.Frame1_listbox.bind('<<ListboxSelect>>', self.get_list2)
        self.Frame1_listbox.pack()

        Frame1_list2 = Frame(frame1, bg="red",width=20)       
        Frame1_list2.grid(row = 0, column = 0,columnspan = 1,sticky = W+E+N+S) 
        Label(Frame1_list2, text="Types",bg="red").pack(padx=10, pady=10)
        self.Frame1_listbox2 = tk.Listbox(Frame1_list2,width=20,exportselection=0)
        self.Frame1_listbox2.insert(tk.END, "month")
        self.Frame1_listbox2.insert(tk.END, "year")
        self.Frame1_listbox2.insert(tk.END, "day")
        self.Frame1_listbox2.insert(tk.END, "week")
        self.Frame1_listbox2.bind('<<ListboxSelect>>', self.selectType)
        self.Frame1_listbox2.pack()

        Frame1_import = Frame(frame1,bg="red")
        Frame1_import.grid(row = 3, column = 0, rowspan = 3, columnspan = 1, sticky = W+E+N+S)
        self.Frame1_button=Button(Frame1_import, text = "import style",command=self.importAction)
        self.Frame1_button.pack()


        Frame1_vide = Frame(frame1, bg="blue")
        Frame1_vide.grid(row = 3, column = 1, rowspan = 3, columnspan = 2, sticky = W+E+N+S)

        Frame1_preview = Frame(frame1, bg="green")

        Frame1_preview.grid(row = 0, column = 2, rowspan = 6, columnspan =1, sticky = W+E+N+S)
        Label(Frame1_preview, text="Preview",bg="green").pack(padx=10, pady=10)
        self.photo=PhotoImage(file=imageCalender[0])
        self.previewCanvas = Canvas(Frame1_preview,bg="green",width=200, height=100)
        self.myimg=self.previewCanvas.create_image(0, 0, anchor=NW, image=self.photo)
        self.previewCanvas.pack()
 

        
        
        self.frames = [frame1, frame2, frame3]

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        # configuration variable globale
        self.parent = parent

        self.make_top()
        self.make_middle()
        self.make_bottom()
        
        self.make_frames()
        # bottom frame
        
        self.update()
    
if __name__ == "__main__":
    root = tk.Tk()
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.wm_geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))
    root.mainloop()
