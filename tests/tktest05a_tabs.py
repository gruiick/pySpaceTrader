#!/usr/bin/env python3
# coding: utf-8
#
# $Id: tktest05a_tabs.py 1303 $
# SPDX-License-Identifier: BSD-2-Clause

# https://tkdocs.com/tutorial/morewidgets.html
# https://docs.python.org/3.1/library/tkinter.ttk.html

from tkinter import *
from tkinter import ttk

root = Tk()
root.title('test05')

tabControl = ttk.Notebook(root, width=450, height=250)     
tab1 = ttk.Frame(tabControl)            
tabControl.add(tab1, text='Tab 1')    
tabControl.pack(expand=1, fill="both")  

root.monty = ttk.LabelFrame(tab1, text=' Monty Python ')
root.monty.grid(column=1, row=1, padx=8, pady=4)        


root.mainloop()
