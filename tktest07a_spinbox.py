#!/usr/bin/env python3
# coding: utf-8
#
# $Id: tktest07a_spinbox.py 1099 $
# SPDX-License-Identifier: BSD-2-Clause

"""
tests around spinbox
http://effbot.org/tkinterbook/spinbox.htm
"""

import tkinter as tk

import constants

racine0=tk.Tk()
retour0=tk.StringVar()
retour1=tk.IntVar()
retour0.set(37.2)
spin0=tk.Spinbox(racine0, from_=35, to=43, increment=.2, width=4)
spin0.config(textvariable=retour0, font="courrier 10", justify="center")
spin0.pack()

spin1=tk.Spinbox(racine0, width=4)
ships = constants.SHIPTYPES
MAX = ships['flea']['cargo']
# testz = (0, MAX, 1)
spin1.config(textvariable=retour1, from_=0, to=MAX, increment=1, font="courrier 10", justify="center")
spin1.pack()

models = constants.SHIPTYPES.keys()
spin2=tk.Spinbox(racine0, values=list(models), increment=1)
spin2.pack()

racine0.mainloop()

#print(retour0.get())
