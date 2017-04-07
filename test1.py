from Tkinter import *
import Tkinter as tk  # gives tk namespace
import ttk
from tkColorChooser import askcolor


def getColor():
        color = askcolor() 
        print color

def make_frames(self):
    self.wm_geometry("%dx%d+%d+%d" % (400, 400, 0, 0))
    Label(self, text="Font",bg="blue").pack(padx=10, pady=10)
    
    p0 = PanedWindow(self, orient=HORIZONTAL)
    p1 = PanedWindow(self, orient=HORIZONTAL)
    p2 = PanedWindow(self, orient=HORIZONTAL)
    p3 = PanedWindow(self, orient=HORIZONTAL)
    p4 = PanedWindow(self, orient=HORIZONTAL)

    combo1 = ttk.Combobox(p1, width=10);
    combo2 = ttk.Combobox(p2, width=10);
    combo3 = ttk.Combobox(p3, width=10);
    combo4 = ttk.Combobox(p4, width=10);

    combo1['values'] = ('Arial', 'Arial Bold', 'Arial Black')
    combo1.current(1)
    combo1.bind("<<ComboboxSelected>>")

    combo2['values'] = ('Arial', 'Arial Bold', 'Arial Black')
    combo2.current(1)
    combo2.bind("<<ComboboxSelected>>")

    combo3['values'] = ('Arial', 'Arial Bold', 'Arial Black')
    combo3.current(1)
    combo3.bind("<<ComboboxSelected>>")

    combo4['values'] = ('Arial', 'Arial Bold', 'Arial Black')
    combo4.current(1)
    combo4.bind("<<ComboboxSelected>>")

    spb1 = Spinbox(p1, from_=2, to=100, width=3)
    spb2 = Spinbox(p2, from_=2, to=100, width=3)
    spb3 = Spinbox(p3, from_=2, to=100, width=3)
    spb4 = Spinbox(p4, from_=2, to=100, width=3)

    colorpickerbtn1 = Button(p1,text='Font Color', command=getColor)
    colorpickerbtn2 = Button(p2,text='Font Color', command=getColor)
    colorpickerbtn3 = Button(p3,text='Font Color', command=getColor)
    colorpickerbtn4 = Button(p4,text='Font Color', command=getColor)

    Label(self, text="Year").pack()
    p1.add(combo1)
    p1.add(spb1)
    p1.add(colorpickerbtn1)
    p1.pack()

    Label(self, text="Month").pack()
    p2.add(combo2)
    p2.add(spb2)
    p2.add(colorpickerbtn2)
    p2.pack()

    Label(self, text="Week").pack()
    p3.add(combo3)
    p3.add(spb3)
    p3.add(colorpickerbtn3)
    p3.pack()

    Label(self, text="Day").pack()
    p4.add(combo4)
    p4.add(spb4)
    p4.add(colorpickerbtn4)
    p4.pack()

    #spinbox.place(relx=1, x=1, y=1, anchor=NE)


    # frame3 = Frame(self.canvas_frame, bg = 'black', padx=20, pady = 20)
    # Frame3_list = Frame(frame3, bg="blue")
    # Frame3_list.grid(row = 0, column = 0, rowspan = 1, columnspan = 2, sticky = W+E+N+S)  
    # Label(Frame3_list, text="Font",bg="blue").pack(padx=10, pady=10)
    # self.fontVar = StringVar()
    # self.Frame3_combo = ttk.Combobox(Frame3_list, textvariable=self.fontVar)
    # self.Frame3_combo['values'] = ('Arial', 'Arial Bold', 'Arial Black')
    # self.Frame3_combo.current(1)
    # self.Frame3_combo.bind("<<ComboboxSelected>>",self.selectFont)
    # self.Frame3_combo.pack()
    # Frame3_spinbox2 = Spinbox(Frame3_list, from_=8, to=100, width=3)
    # Frame3_spinbox2.pack()
    # #Frame3_spinbox2.place(relx=1, x=1, y=1, anchor=NE)

    # Frame3_size = Frame(frame3, bg="blue")
    # Frame3_size.grid(row = 1, column = 0, rowspan = 1, columnspan = 3, sticky = W+E+N+S)  
    # Frame3_spinbox = Spinbox(Frame3_size, from_=2, to=100)
    # Frame3_spinbox.pack()
    # Frame3_colorpicker=Button(Frame3_size,text='Font Color', command=self.getColor)
    # Frame3_colorpicker.pack()
 


fenetre = Tk()

make_frames(fenetre)

fenetre.mainloop()

