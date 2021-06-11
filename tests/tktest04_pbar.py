#!/usr/bin/env python3
# coding: utf-8
#
# $Id: tktest04_pbar.py 1303 $
# SPDX-License-Identifier: BSD-2-Clause

# https://tkdocs.com/tutorial/morewidgets.html
# https://docs.python.org/3.1/library/tkinter.ttk.html

from tkinter import *
from tkinter import ttk
import time
root = Tk()

p = ttk.Progressbar(root, orient=HORIZONTAL, length=200, mode='indeterminate')

# marche pas, comprends pas

root.mainloop()

