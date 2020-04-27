#!/usr/bin/env python3
# coding: utf-8
#
# $Id: tktest05b_tabs.py 1302 $
# SPDX-License-Identifier: BSD-2-Clause

# https://tkdocs.com/tutorial/morewidgets.html
# https://docs.python.org/3.1/library/tkinter.ttk.html

from tkinter import *
from tkinter import ttk

root = Tk()

#tabControl = ttk.Notebook(root, width=450, height=250)     
#tab1 = ttk.Frame(tabControl)            
#tabControl.add(tab1, text='Tab 1')    
#tabControl.pack(expand=1, fill="both")  

# tabs (notebook)
MonBook = ttk.Notebook(root, width=450, height=250, padding="3 3 3 3")
Book1 = ttk.Frame(MonBook)   # first page, which would get widgets gridded into it
Book2 = ttk.Frame(MonBook)   # second page
MonBook.add(Book1, text='One', state='normal')
MonBook.add(Book2, text='Two', state='normal')

#MonBook.pack(expand=1, fill="both")

# Canvas = zone de base pour dessiner
MonCanvas = Canvas(Book1, bg="white").pack(padx=5, pady=5) #, width=450, height=250

can1 = Canvas(Book2, width =123, height =125, bg ='white')
photo = PhotoImage(file='/usr/share/pixmaps/debian-logo.png')
can1.create_image(65, 65, image=photo)
#can1.create_image(65, 65, image=photo)
#can1.grid(row =0, column =2, rowspan =4, padx =10, pady =5)
can1.pack()

MonBook.pack(expand=1, fill="both")


print(MonBook.configure())
#print(MonCanvas.configure())

root.mainloop()

