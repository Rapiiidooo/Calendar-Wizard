from Tkinter import *
import Tkinter as tk
import datetime

typeOfCalender=["bancaire","bureau","magnetique","mural","double-mural","poster"]
imageCalender=["format/calendrier-format-bancaire.png",
"format/calendrier-format-bureau.png",
"format/calendrier-format-magnetique.png",
"format/calendrier-format-mural.png",
"format/calendrier-format-mural-double.png",
"format/calendrier-format-poster.png"]

sizex = 500
sizey = 400
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

    def get_list(self,event):
        # get selected line index
        index = self.Frame1_listbox.curselection()[0]
        self.photo=PhotoImage(file=imageCalender[index])
        self.previewCanvas.itemconfigure(self.myimg,image=self.photo)
        self.previewCanvas.image = self.photo

    def make_top(self):
        self.top = Frame(self, bg='green')
        self.top.grid(row = 0, column = 0)
        self.top_label = Label(self.top, text="First page")
        self.top_label.pack()

    def make_middle(self):
        self.middle = Frame(self, bg='blue', padx=20, pady = 20 )
        self.middle.grid(row=1, column=0)

        self.canvas = Canvas(self.middle, bg = 'orange')
        self.canvas.pack()

        self.canvas_frame = Frame(self.canvas, bg = 'black', padx=20, pady = 20)
        self.canvas_frame.pack()
        self.canvas_frame.bind("<Configure>", self._event_canvas)

        self.scrollbar_middle=Scrollbar(self.middle,orient = "vertical",command = self.canvas.yview)
        self.canvas.configure(yscrollcommand = self.scrollbar_middle.set)

        self.scrollbar_middle.pack(side="right", fill="y")
        self.canvas.pack(side="left")
        self.canvas.create_window((0,0),window=self.canvas_frame,anchor='nw')
        #self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)

    def make_bottom(self):
        self.bottom = Frame(self, bg='red')
        self.bottom.grid(row=2, column=0)
        self.bottom_button=[Button(self.bottom, text = "prev",command=self.decrement),Button(self.bottom, text = "next",command=self.increment),Button(self.bottom, text = "finish")]
        for i in range(0,3):
            self.bottom_button[i].grid(row=0, column=i)

    def make_frames(self):
        frame3 = Frame(self.canvas_frame, bg = 'black', padx=20, pady = 20)
        for i in range(0, 20):
            tmp = Button(frame3, text="osef")
            tmp.grid(row=i, column=0)


        ########### ELEMENT MIDDLE FRAME 1
        frame2 = Frame(self.canvas_frame,bg = 'violet',padx=20, pady = 20)
        Frame1_list = Frame(frame2, bg="blue")
        Frame1_list.grid(row = 0, column = 0, rowspan = 3, columnspan = 2, sticky = W+E+N+S) 
        Label(Frame1_list, text="Models",bg="blue").pack(padx=10, pady=10)
        self.Frame1_listbox = tk.Listbox(Frame1_list)
        for item in typeOfCalender:
            self.Frame1_listbox.insert(tk.END, item)
        self.Frame1_listbox.bind('<<ListboxSelect>>', self.get_list)
        self.Frame1_listbox.pack()

        Frame1_radio = Frame(frame2,bg="red")
        Frame1_radio.grid(row = 3, column = 0, rowspan = 3, columnspan = 1, sticky = W+E+N+S)
        value = StringVar() 
        button_radio1 = Radiobutton(Frame1_radio, text="Mois", bg="red",variable=value, value=1)
        button_radio2 = Radiobutton(Frame1_radio, text="Annee",bg="red", variable=value, value=2)
        button_radio1.pack()
        button_radio2.pack()

        Frame1_vide = Frame(frame2, bg="yellow")
        Frame1_vide.grid(row = 3, column = 1, rowspan = 3, columnspan = 2, sticky = W+E+N+S)

        Frame1_preview = Frame(frame2, bg="green")
        Frame1_preview.grid(row = 0, column = 2, rowspan = 6, columnspan = 3, sticky = W+E+N+S)
        Label(Frame1_preview, text="Preview",bg="green").pack(padx=10, pady=10)
        self.photo=PhotoImage(file=imageCalender[0])
        self.previewCanvas = Canvas(Frame1_preview,bg="green",width=self.photo.width(), height=self.photo.height())
        self.myimg=self.previewCanvas.create_image(0, 0, anchor=NW, image=self.photo)
        self.previewCanvas.pack()
      
        ########### ELEMENT MIDDLE FRAME 1




        frame1 = Frame(self.canvas_frame, bg = 'yellow', padx=20, pady = 20)
        lab3 = Label(frame1, text="Parametre")
        lab3.pack()
        Frame2_checkbutton = Frame(frame1, bg="blue")
        Frame2_checkbutton.grid(row = 0, column = 0, rowspan = 3, columnspan = 2, sticky = W+E+N+S) 

        self.var1 = IntVar()
        self.var2 = IntVar()
        self.var3 = IntVar()
        self.var4 = IntVar()
        c1 = Checkbutton(frame1, text="Numero de jour", variable=self.var1) #command=self.cb)
        c2 = Checkbutton(frame1, text="Nom de jour entier", variable=self.var2) #command=self.cb)
        c3 = Checkbutton(frame1, text="Afficher mois suivant", variable=self.var3) #command=self.cb)
        c4 = Checkbutton(frame1, text="Afficher mois precedent", variable=self.var4) #command=self.cb)

        c1.pack()
        c2.pack()
        c3.pack()
        c4.pack()

        s = Spinbox(frame1, from_=2, to=100)
        s.pack()

        
        self.frames = [frame1, frame2, frame3]

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        # configuration variable globale
        self.window_width = 500
        self.window_height = 400
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
