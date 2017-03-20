from tkinter import *
import tkinter as tk
import datetime

class MainApplication(tk.Frame):

    def _event_canvas(self, event):
    #    print(datetime.datetime.now())
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_mousewheel(self, event):
        tup = self.scrollbar_middle.get()
        if(tup[0] != 0 or tup[1] != 1):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")


    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        # configuration variable globale
        self.sizex = 400
        self.sizey = 300
        self.posx  = 100
        self.posy  = 100
        self.parent = parent

        # top frame
        self.top = Frame(self, bg='green', padx=20, pady = 20)
        self.top.grid(row = 0, column = 0)
        self.top_label = Label(self.top, text="top pane")
        self.top_label.pack()



        # middle
        self.middle = Frame(self, bg='blue', padx=20, pady = 20 )
        self.middle.grid(row=1, column=0)

        self.canvas = Canvas(self.middle, bg = 'orange')
        self.canvas.pack()

        self.canvas_frame = Frame(self.canvas, bg = 'black', padx=20, pady = 20)
        self.canvas_frame.bind("<Configure>", self._event_canvas)


        ########### ELEMENT MIDDLE        
        self.firstFrame = Frame(self.canvas_frame,bg = 'blue',padx=20, pady = 20)
     
        #     self.top_label2 = Label(self.firstFrame, text="top pane")
        #    self.top_label2.pack()
        for i in range(0,50):
            b2 = Button(self.firstFrame, text="test")
            b2.grid(row = i, column = 0)
        

        self.firstFrame.pack()
        ########### ELEMENT MIDDLE

        self.canvas_frame.pack()

        self.scrollbar_middle=Scrollbar(self.middle,orient = "vertical",command = self.canvas.yview)
        self.canvas.configure(yscrollcommand = self.scrollbar_middle.set)

        self.scrollbar_middle.pack(side="right", fill="y")
        self.canvas.pack(side="left")
        self.canvas.create_window((0,0),window=self.canvas_frame,anchor='nw')
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # bottom frame
        self.bottom = Frame(self, bg='red', padx=20, pady = 20)
        self.bottom.grid(row=2, column=0)
        self.bottom_bt=[Button(self.bottom, text = "prev"),Button(self.bottom, text = "next"),Button(self.bottom, text = "finish")]
        for i in range(0,3):
            self.bottom_bt[i].grid(row=0, column=i)
  
       
    
if __name__ == "__main__":
    root = tk.Tk()
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()