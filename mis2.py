from tkinter import *
import tkinter as tk  # gives tk namespace
sizex = 400
sizey = 300
posx  = 100
posy  = 100

typeOfCalender=["bancaire","bureau","magnetique","mural","double-mural","poster"]
imageCalender=["format/calendrier-format-bancaire.png",
"format/calendrier-format-bureau.png",
"format/calendrier-format-magnetique.png",
"format/calendrier-format-mural.png",
"format/calendrier-format-mural-double.png",
"format/calendrier-format-poster.png"]

class Application(Frame):
    _max = 3
    current = 0
    last = -1
    
    def update(self):
        if(self.current <= 0):
            self.current = 0
            self.bt1.config(state=DISABLED)
            self.bt3.config(state=DISABLED)
        else:
            if(self.current >= _max - 1):
                self.current = _max - 1
                self.bt2.config(state=DISABLED)
                self.bt3.config(state=ACTIVE)
            else:
                self.bt2.config(state=ACTIVE)
                self.bt3.config(state=DISABLED)
                self.bt1.config(state=ACTIVE)
        if(self.last != -1):
            self.frames[self.last].grid_forget()
        tmp= self.frames[self.current]
#	    tmp.grid(row = 1, column=0)
        self.last=self.current

    def increment(self):
	    self.current
	    self.current = self.current + 1
	    self.update()

    def decrement(self):
	    self.current
	    self.current = self.current - 1
	    self.update()

    def get_list(self,event):
        # get selected line index
        index = self.listbox1.curselection()[0]
        self.photo=PhotoImage(file=imageCalender[index])
        self.previewCanvas.itemconfigure(self.myimg,image=self.photo)
        self.previewCanvas.image = self.photo

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.master.title("CalanderWizard :for")



        self.frames=[]
       




        for r in range(6):
            self.master.rowconfigure(r, weight=1)    
        self.master.columnconfigure(0, weight=1)
        self.bt1=Button(master, text="Precedent",command=decrement.self)
        self.bt1.grid(row=6,column=0,sticky=E+W)
        self.master.columnconfigure(1, weight=1)
        self.bt2=Button(master, text="Suivant",command=self.increment)
        self.bt2.grid(row=6,column=1,sticky=E+W)        
        self.master.columnconfigure(2, weight=3)
        self.bt3=Button(master, text="Termine")
        self.bt3.grid(row=6,column=2,sticky=E+W)        
        Frame1 = Frame(master, bg="blue")
        Frame1.grid(row = 0, column = 0, rowspan = 3, columnspan = 2, sticky = W+E+N+S) 
        Label(Frame1, text="Models",bg="blue").pack(padx=10, pady=10)
        self.listbox1 = tk.Listbox(Frame1)
        for item in typeOfCalender:
            self.listbox1.insert(tk.END, item)
        self.listbox1.bind('<<ListboxSelect>>', self.get_list)
        self.listbox1.pack()


        Frame2 = Frame(master, bg="red")
        Frame2.grid(row = 3, column = 0, rowspan = 3, columnspan = 1, sticky = W+E+N+S)
        value = StringVar() 
        bouton1 = Radiobutton(Frame2, text="Mois", bg="red",variable=value, value=1)
        bouton2 = Radiobutton(Frame2, text="Annee",bg="red", variable=value, value=2)
        bouton1.pack()
        bouton2.pack()
        
        Frame22 = Frame(master, bg="yellow")
        Frame22.grid(row = 3, column = 1, rowspan = 3, columnspan = 2, sticky = W+E+N+S)
        Frame3 = Frame(master, bg="green")
        Frame3.grid(row = 0, column = 2, rowspan = 6, columnspan = 3, sticky = W+E+N+S)
        Label(Frame3, text="Preview",bg="green").pack(padx=10, pady=10)
        self.photo=PhotoImage(file=imageCalender[0])
        self.previewCanvas = Canvas(Frame3,bg="green",width=self.photo.width(), height=self.photo.height())
        self.myimg=self.previewCanvas.create_image(0, 0, anchor=NW, image=self.photo)
        self.previewCanvas.pack()
        

        master2 = Frame(self.frames, bg="yellow")
        master1 = Frame(self.frames, bg="orange")
        
<<<<<<< HEAD
        self.frames.extend([master,master2])
=======
        self.frames.extend([master1,master2])
>>>>>>> 8026a45235939da7faec1e6dc01749d0ed945c12
        self.update()



root = Tk()
root.wm_geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))
app = Application(master=root)
app.mainloop()
