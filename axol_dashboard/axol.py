#! /usr/bin/env python
#-----------------------------------------#
# Written by Kelcey Damage, 2013

# Imports
#-----------------------------------------------------------------------#
from Tkinter import *
print TkVersion
from sys import exit
import urllib2
import json

def gather_data():
	response = urllib2.urlopen('http://10.100.10.63/api/readonly/dashboard')

	return json.loads(response.read())


def data(data):
	n = 1
	for i in data:
		Label(frame,text=i,justify=LEFT).grid(row=n,column=0,sticky=W)
		Label(frame,justify='left',text=str(data[i]['cpu'])).grid(row=n,column=1,sticky=W)
		Label(frame,text=str(data[i]['cpu'])).grid(row=n,column=2,sticky=W)
		n += 1

def myfunction(event):
    canvas.configure(scrollregion=canvas.bbox("all"),height=200,width=760)

response = gather_data()

root=Tk()
sizex = 800
sizey = 600
posx  = 100
posy  = 100
root.wm_geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))

myframe=Frame(root,relief=GROOVE,height=100,bd=1)
myframe.place(x=10,y=10)

canvas=Canvas(myframe)
frame=Frame(canvas)
myscrollbar=Scrollbar(myframe,orient="vertical",command=canvas.yview)
canvas.configure(yscrollcommand=myscrollbar.set)

myscrollbar.pack(side="right",fill="y")
canvas.pack(side="left", fill='x')
canvas.create_window((0,0),window=frame,anchor='nw')
frame.bind("<Configure>",myfunction)
data(response['response']['value'])
root.mainloop()

