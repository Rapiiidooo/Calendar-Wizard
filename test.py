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
    last = -1
    list_frames=[]
    
    def update(self):
        print(datetime.datetime.now())
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
        if(self.last != -1):
            self.list_frames[self.last].grid_forget()
        self.list_frames[self.current].grid(row = 1, column=0)
        self.last=self.current

    def increment(self):
	    self.current
	    self.current = self.current + 1
	    self.update()

    def decrement(self):
	    self.current
	    self.current = self.current - 1
	    self.update()

    def _event_canvas(self, event):
    #    print(datetime.datetime.now())
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_mousewheel(self, event):
        print(datetime.datetime.now())
        tup = self.scrollbar_middle.get()
        if(tup[0] != 0 or tup[1] != 1):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def get_list(self,event):
        # get selected line index
        index = self.Frame1_listbox.curselection()[0]
        self.photo=PhotoImage(file=imageCalender[index])
        self.previewCanvas.itemconfigure(self.myimg,image=self.photo)
        self.previewCanvas.image = self.photo

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        # configuration variable globale
        self.window_width = 500
        self.window_height = 400
        self.parent = parent

        # top frame
        self.top = Frame(self, bg='green')
        self.top.grid(row = 0, column = 0)
        self.top_label = Label(self.top, text="First page")
        self.top_label.pack()



        # middle
        self.middle = Frame(self, bg='blue', padx=20, pady = 20 )
        self.middle.grid(row=1, column=0)

        self.canvas = Canvas(self.middle, bg = 'orange')
        self.canvas.pack()

        self.canvas_frame = Frame(self.canvas, bg = 'black', padx=20, pady = 20)
        self.canvas_frame.bind("<Configure>", self._event_canvas)


        ########### ELEMENT MIDDLE FRAME 1
        self.Frame1_master = Frame(self.canvas_frame,bg = 'violet',padx=20, pady = 20)
        Frame1_list = Frame(self.Frame1_master, bg="blue")
        Frame1_list.grid(row = 0, column = 0, rowspan = 3, columnspan = 2, sticky = W+E+N+S) 
        Label(Frame1_list, text="Models",bg="blue").pack(padx=10, pady=10)
        self.Frame1_listbox = tk.Listbox(Frame1_list)
        for item in typeOfCalender:
            self.Frame1_listbox.insert(tk.END, item)
        self.Frame1_listbox.bind('<<ListboxSelect>>', self.get_list)
        self.Frame1_listbox.pack()


        Frame1_radio = Frame(self.Frame1_master,bg="red")
        Frame1_radio.grid(row = 3, column = 0, rowspan = 3, columnspan = 1, sticky = W+E+N+S)
        value = StringVar() 
        button_radio1 = Radiobutton(Frame1_radio, text="Mois", bg="red",variable=value, value=1)
        button_radio2 = Radiobutton(Frame1_radio, text="Annee",bg="red", variable=value, value=2)
        button_radio1.pack()
        button_radio2.pack()

        Frame1_vide = Frame(self.Frame1_master, bg="yellow")
        Frame1_vide.grid(row = 3, column = 1, rowspan = 3, columnspan = 2, sticky = W+E+N+S)

        Frame1_preview = Frame(self.Frame1_master, bg="green")
        Frame1_preview.grid(row = 0, column = 2, rowspan = 6, columnspan = 3, sticky = W+E+N+S)
        Label(Frame1_preview, text="Preview",bg="green").pack(padx=10, pady=10)
        self.photo=PhotoImage(file=imageCalender[0])
        self.previewCanvas = Canvas(Frame1_preview,bg="green",width=self.photo.width(), height=self.photo.height())
        self.myimg=self.previewCanvas.create_image(0, 0, anchor=NW, image=self.photo)
        self.previewCanvas.pack()
        self.Frame1_master.pack()
      
        ########### ELEMENT MIDDLE FRAME 1



        ########### ELEMENT MIDDLE FRAME 2

        self.Frame2_master = Frame(bg = 'white',padx=20, pady = 20)
        Label(self.Frame2_master, text="page 2",bg="blue").pack(padx=10, pady=10)
   
        ########### ELEMENT MIDDLE FRAME 2

        ########### ELEMENT MIDDLE FRAME 3

        self.Frame3_master = Frame(bg = 'green',padx=20, pady = 20)
        Label(self.Frame3_master, text="page 3",bg="blue").pack(padx=10, pady=10)
   
        ########### ELEMENT MIDDLE FRAME 3



        self.list_frames.extend([self.Frame1_master,self.Frame2_master,self.Frame3_master])




        self.canvas_frame.pack()

        self.scrollbar_middle=Scrollbar(self.middle,orient = "vertical",command = self.canvas.yview)
        self.canvas.configure(yscrollcommand = self.scrollbar_middle.set)

        self.scrollbar_middle.pack(side="right", fill="y")
        self.canvas.pack(side="left")
        self.canvas.create_window((0,0),window=self.canvas_frame,anchor='nw')
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # bottom frame
        self.bottom = Frame(self, bg='red')
        self.bottom.grid(row=2, column=0)
        self.bottom_button=[Button(self.bottom, text = "prev",command=self.decrement),Button(self.bottom, text = "next",command=self.increment),Button(self.bottom, text = "finish")]
        for i in range(0,3):
            self.bottom_button[i].grid(row=0, column=i)
  
       
        self.update()
    
if __name__ == "__main__":
    root = tk.Tk()
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.wm_geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))
    root.mainloop()
