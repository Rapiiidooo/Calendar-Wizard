from Tkinter import *

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

def add_item():
    """
    add the text in the Entry widget to the end of the listbox
    """
    listbox1.insert(tk.END, enter1.get())
def delete_item():
    """
    delete a selected line from the listbox
    """
    try:
        # get selected line index
        index = listbox1.curselection()[0]
        listbox1.delete(index)
    except IndexError:
        pass
 
def get_list(event):
    """
    function to read the listbox selection
    and put the result in an entry widget
    """
    # get selected line index
    index = listbox1.curselection()[0]
    # get the line's text
    seltext = listbox1.get(index)
    # delete previous text in enter1
    enter1.delete(0, 50)
    # now display the selected text
    enter1.insert(0, seltext)
def set_list(event):
    """
    insert an edited line from the entry widget
    back into the listbox
    """
    try:
        index = listbox1.curselection()[0]
        # delete old listbox line
        listbox1.delete(index)
    except IndexError:
        index = tk.END
    # insert edited item back into listbox1 at index
    listbox1.insert(index, enter1.get())
def sort_list():
    """
    function to sort listbox items case insensitive
    """
    temp_list = list(listbox1.get(0, tk.END))
    temp_list.sort(key=str.lower)
    # delete contents of present listbox
    listbox1.delete(0, tk.END)
    # load listbox with sorted data
    for item in temp_list:
        listbox1.insert(tk.END, item)
def save_list():
    """
    save the current listbox contents to a file
    """
    # get a list of listbox lines
    temp_list = list(listbox1.get(0, tk.END))
    # add a trailing newline char to each line
    temp_list = [chem + '\n' for chem in temp_list]
    # give the file a different name
    fout = open("chem_data2.txt", "w")
    fout.writelines(temp_list)
    fout.close()
 



root=Tk()
root.wm_geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))

myframe=Frame(root,relief=GROOVE,width=sizex,height=sizey,bd=1)
myframe.grid(row = 2, column=0)

myframe.place(x=0,y=0)
canvas=Canvas(myframe)



# create the listbox (note that size is in characters)
listbox1 = tk.Listbox(root, width=50, height=6)
listbox1.grid(row=0, column=0)
 
# create a vertical scrollbar to the right of the listbox
yscroll = tk.Scrollbar(command=listbox1.yview, orient=tk.VERTICAL)
yscroll.grid(row=0, column=1, sticky=tk.N+tk.S)
listbox1.configure(yscrollcommand=yscroll.set)




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
