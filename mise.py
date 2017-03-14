from Tkinter import *
import Tkinter as tk  # gives tk namespace

def get_list(event):
    # get selected line index
    index = listbox1.curselection()[0]
    photo=PhotoImage(file=imageCalender[index])
    previewCanvas.itemconfigure(myimg,image=photo)
    previewCanvas.image = photo


fenetre=[]
current = 0
_max = 3
sizex = 400
sizey = 400
posx  = 100
posy  = 100

typeOfCalender=["bancaire","bureau","magnetique","mural","double-mural","poster"]
imageCalender=["format/calendrier-format-bancaire.png",
"format/calendrier-format-bureau.png",
"format/calendrier-format-magnetique.png",
"format/calendrier-format-mural.png",
"format/calendrier-format-mural-double.png",
"format/calendrier-format-poster.png"]

root = Tk()
root.wm_geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))
master=Frame(root)
master.rowconfigure(0, weight=1)
master.columnconfigure(0, weight=1)

# choix de model
menuFrame=Frame(master)
menuFrame.grid(row = 0) 
itemFrame=Frame(master)
itemFrame.grid(row = 1) 
configFrame=Frame(master)
configFrame.grid(row = 3) 

Frame0 = Frame(itemFrame, width=80, height=50, borderwidth=2, relief=GROOVE)
Frame0.grid(row = 0, column = 1, rowspan = 3) 
Label(Frame0, text="Models",bg="white").pack(padx=10, pady=10)
#Frame0.pack(side=LEFT, padx=30, pady=30)
listbox1 = tk.Listbox(Frame0)
for item in typeOfCalender:
    listbox1.insert(tk.END, item)

listbox1.bind('<ButtonRelease-1>', get_list)
listbox1.pack()
# choix de model

# bouton radio

# previe
Frame2 = Frame(itemFrame, width=80, height=50, borderwidth=2, relief=GROOVE)
Frame2.grid(row = 0, column = 2, rowspan = 6, columnspan = 3, sticky = W+E+N+S)        
photo=PhotoImage(file=imageCalender[0])
previewCanvas = Canvas(Frame2,width=400, height=200)
myimg=previewCanvas.create_image(0, 0, anchor=NW, image=photo)
previewCanvas.pack()
#rame2.pack(side=LEFT, padx=30, pady=30)
# preview
master.pack()

# bouton radio
Frame1 = Frame(configFrame, width=80, height=50, borderwidth=2, relief=GROOVE)
Frame1.grid(row = 0, column = 0)
value = StringVar() 
bouton1 = Radiobutton(Frame1, text="Mois", variable=value, value=1)
bouton2 = Radiobutton(Frame1, text="Annee", variable=value, value=2)
bouton3 = Radiobutton(Frame1, text="None", variable=value, value=3)
bouton1.pack()
bouton2.pack()
bouton3.pack()
master.pack()












root.mainloop()
