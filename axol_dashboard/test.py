from Tkinter import *

class MyApp:
  def __init__(self, parent, data):

    self.myParent = parent

    self.myContainer1 = Frame(parent)
    self.myContainer1.pack()

    self.top_frame = Frame(self.myContainer1)
    self.top_frame.pack(side=TOP,
      fill=BOTH,
      expand=YES,
      )

    self.left_frame = Frame(self.top_frame, background="red",
      borderwidth=5,  relief=RIDGE,
      height=250,
      width=50,
      )
    self.left_frame.pack(side=LEFT,
      fill=BOTH,
      expand=YES,
      )

    self.right_frame = Frame(self.top_frame, background="tan",
      borderwidth=5,  relief=RIDGE,
      width=250,
      )
    self.right_frame.pack(side=RIGHT,
      fill=BOTH,
      expand=YES,
      )

    self.label_1 = Label(self.right_frame, background='gray',
    	width=200, text=data
    	)
    self.label_1.pack()

def callback(value):
	methods = {
		'new': None,
		'open': None,
		'exit': exit,
		'about': None
		}
	print "called the callback! %s" % value

	if value in methods:
		methods[value]()

root = Tk()

menu = Menu(root)
root.config(menu=menu)

filemenu = Menu(menu)
menu.add_cascade(label='File', menu=filemenu)
filemenu.add_command(label='New', command=lambda: callback('new'))
filemenu.add_command(label='Open', command=lambda: callback('open'))
filemenu.add_separator()
filemenu.add_command(label='Exit', command=lambda: callback('exit'))

helpmenu = Menu(menu)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About...", command=lambda: callback('about'))

toolbar = Frame(root)
b = Button(toolbar, text="new", width=6, command=callback)
b.pack(side=LEFT, padx=2, pady=2)

b = Button(toolbar, text="open", width=6, command=callback)
b.pack(side=LEFT, padx=2, pady=2)

toolbar.pack(side=TOP, fill=X)
status = Label(root, text="", bd=1, relief=SUNKEN, anchor=W)
status.pack(side=BOTTOM, fill=X)

canvas = Canvas(root)
scrollbar_1 = Scrollbar(root, orient='vertical', command=canvas.yview)
scrollbar_1.pack(side=RIGHT, fill=Y)
canvas.configure(yscrollcommand=scrollbar_1.set)
canvas.pack()

#c_frame = Frame(canvas, background='blue')

