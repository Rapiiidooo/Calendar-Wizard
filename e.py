from tkinter import *

frames=[]
current = 0
_max = 3
sizex = 800
sizey = 600
posx  = 100
posy  = 100

def incr():
	global current
	current = current + 1
	update()

def decr():
	global current
	current = current - 1
	update()

def update():
	global current
	if(current <= 0):
		current = 0
		bt1.config(state=DISABLED)
		bt3.config(state=DISABLED)
	else:
		if(current >= _max - 1):
			current = _max - 1
			bt2.config(state=DISABLED)
			bt3.config(state=ACTIVE)
		else:
			bt2.config(state=ACTIVE)
			bt3.config(state=DISABLED)
			bt1.config(state=ACTIVE)

	if(update.last != -1):
		frames[update.last].grid_forget()
	frames[current].grid(row = 1, column=0)
	update.last = current


def myfunction(event):
    canvas.configure(scrollregion=canvas.bbox("all"),width=sizex-20,height=sizey-5)





root=Tk()
root.wm_geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))

myframe=Frame(root,relief=GROOVE,width=sizex,height=sizey,bd=1)
myframe.grid(row = 2, column=0)

myframe.place(x=0,y=0)
canvas=Canvas(myframe)


frame=Frame(canvas)
myscrollbar=Scrollbar(myframe,orient="vertical",command=canvas.yview)
canvas.configure(yscrollcommand=myscrollbar.set)

myscrollbar.pack(side="right",fill="y")
canvas.pack(side="left")
canvas.create_window((0,0),window=frame,anchor='nw')
frame.bind("<Configure>",myfunction)

bt1 = Button(frame, text="prev", command=decr)
bt1.grid(row = 0, column=0)
bt2 = Button(frame, text="suiv", command=incr)
bt2.grid(row = 0, column=1)
bt3 = Button(frame, text="finish")
bt3.grid(row = 0, column=2)
frames.extend([Frame(frame,bg='black', padx=20, pady = 20), Frame(frame, bg='green', padx=20, pady = 20), Frame(frame,bg='red', padx=20, pady = 20)])

ButtonImage = PhotoImage(file='img.png')

taCanvas = Canvas(frames[0])
taCanvas.create_image(300/2,231/2,image=ButtonImage)
taCanvas.pack()
for i in range(0,50):
	b2 = Button(frames[1], text="test")
	b2.grid(row = i, column = 0)

b2 = Button(frames[2], text="test")
b2.grid(row = 0, column = 0)

update.last = -1
update()

def _on_mousewheel(event):
	tup = myscrollbar.get()
	if(tup[0] != 0 or tup[1] != 1):
		canvas.yview_scroll(int(-1*(event.delta/120)), "units")

canvas.bind_all("<MouseWheel>", _on_mousewheel)   

root.mainloop()