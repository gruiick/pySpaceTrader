#!/usr/bin/env python3
# coding:utf-8

# $Id: tktest06a_array.py 1302 $
# SPDX-License-Identifier: BSD-2-Clause

import tkinter as tk
from tkinter import ttk

root = tk.Tk()

height = 5
width = 5
for i in range(height): #Rows
    for j in range(width): #Columns
        entrée = str((i, j))
        b = tk.Canvas(root)
        lbl = ttk.Label(b, text=entrée)
        cell = ttk.Entry(b, text='')
        lbl.grid(row=i, column=j, sticky='ew')
        cell.grid(row=i, column=j + 1, sticky='ew')
        b.grid(row=i, column=j, sticky='ew')

tk.mainloop()
