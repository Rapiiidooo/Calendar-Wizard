from tkinter import *

frames=[]
current = 0
_max = 3

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

root = Tk()

top = Label(text="top pane")
top.grid(row = 0, column=0)

vert = Frame()
vert.grid(row = 2, column=0)

bt1 = Button(vert, text="prev", command=decr)
bt1.grid(row = 0, column=0)

bt2 = Button(vert, text="suiv", command=incr)
bt2.grid(row = 0, column=1)

bt3 = Button(vert, text="finish")
bt3.grid(row = 0, column=2)

frames.extend([Frame(bg='black', padx=20, pady = 20), Frame( bg='green', padx=20, pady = 20), Frame(bg='red', padx=20, pady = 20)])

bt = Button(frames[0], text="test")
bt.grid(row = 0, column = 0)

b2 = Button(frames[1], text="test2")
b2.grid(row = 0, column = 0)

b2 = Button(frames[2], text="test3")
b2.grid(row = 0, column = 0)
for i in range(0, 20):
	b3 = Button(frames[2], text="test3", bg='green')
	b3.grid(row = i, column = 0)
update.last = -1
update()

root.mainloop()
