#!/usr/bin/env python3
# coding: utf-8
#
# $Id: tk_mockup01.py 1303 $
# SPDX-License-Identifier: BSD-2-Clause

"""
premier essai : une pauv' fenêtre avec des menus
    http://tkinter.fdex.eu/doc/popdial.html
    https://docs.python.org/3.1/library/tkinter.ttk.html

"""

import tkinter as tk
import tkinter.messagebox as tkmsg
import tkinter.filedialog as tkfd
from tkinter import ttk
import random

import constants


MAXW = constants.MAXWIDTH
MAXH = constants.MAXHEIGHT
MAXP = constants.MAXPARSEC


def box_alert():
    tkmsg.showwarning('Alert!', 'Bravo!')


def box_open():
    tkfd.askopenfilename(defaultextension='.db')


def box_save():
    tkfd.asksaveasfilename(defaultextension='.db')


def box_help():
    tkmsg.showinfo('Help', 'You have to click everywhere.')


def box_about():
    tkmsg.showinfo('About', 'pySpaceTrader v0.1')


def box_error():
    tkmsg.showerror('Error', 'This is an error.')


def cercle(x, y, r, color='black'):
    """tracé d'un cercle de centre (x,y) et de rayon r"""
    MonCanvas.create_oval(x - r, y - r, x + r, y + r, outline=color)


def figure_1():
    """dessiner une cible"""
    # Effacer d'abord tout dessin préexistant :
    # MonCanvas.delete(tk.ALL)
    # tracer les deux lignes (vert. et horiz.) :
    MonCanvas.create_line(MAXW / 2, 0, MAXW / 2, MAXH, fill='blue')
    MonCanvas.create_line(0, MAXH / 2, MAXW, MAXH / 2, fill='blue')
    # tracer plusieurs cercles concentriques :
    rayon = 15
    while rayon < MAXW / 2:
        if rayon == MAXP:
            cercle(MAXW / 2, MAXH / 2, rayon, color='red')
        else:
            cercle(MAXW / 2, MAXH / 2, rayon)
        rayon += 15
    # MonCanvas.pack()


def etoile():
    """dessiner un rond au hasard"""
    x, y = random.randint(0, MAXW), random.randint(0, MAXH)
    cercle(x, y, 2, 'red')


def pointeur(event):
    """modifie chaine avec la position du curseur"""
    texte = 'Detected clic in X=' + str(event.x) + ', Y=' + str(event.y)
    chaine.configure(text=texte)


# la fenetre principale
Mafenetre = tk.Tk()
Mafenetre.title('test01')

# tabs (notebook)
MonBook = ttk.Notebook(Mafenetre, padding='3 3 5 5')  # , width=450, height=250
Book1 = ttk.Frame(MonBook)  # first page, which would get widgets gridded into it
Book2 = ttk.Frame(MonBook)  # second page
MonBook.add(Book1, text='Local Map', state='normal')
MonBook.add(Book2, text='Galactic Map', state='normal')

# Canvas = zone de base pour dessiner
MonCanvas = tk.Canvas(Book1, width=MAXW, height=MAXH - 2, bg='white')
MonCanvas.bind('<Button-1>', pointeur)
MonCanvas.pack(padx=2, pady=2)

b1 = tk.Button(Mafenetre, text='target', command=figure_1)
b1.pack(fill=tk.X, side=tk.LEFT, padx=2, pady=2)

b2 = tk.Button(Mafenetre, text='star', command=etoile)
b2.pack(fill=tk.X, side=tk.LEFT, padx=2, pady=2)

chaine = tk.Label(Book1)
chaine.pack(padx=2, pady=2)

can1 = tk.Canvas(Book2, width=123, height=125, bg='white')
photo = tk.PhotoImage(file='/usr/share/pixmaps/debian-logo.png')
can1.create_image(65, 65, image=photo)
can1.pack(side=tk.LEFT, padx=2, pady=2)

MonBook.pack(expand=True, fill=tk.BOTH)

# barre de menus
menubar = tk.Menu(Mafenetre)

# menu Fichier
menufile = tk.Menu(menubar, tearoff=0)
menufile.add_command(label='New', command=figure_1)
menufile.add_command(label='Open', command=box_open)
menufile.add_command(label='Save', command=box_save)
menufile.add_separator()
menufile.add_command(label='Quit', command=Mafenetre.quit)
menubar.add_cascade(label='File', menu=menufile)

# menu Commerce
menutrade = tk.Menu(menubar, tearoff=0)
menutrade.add_command(label='Buy', command=box_alert)
menutrade.add_command(label='Sell', command=box_alert)
menutrade.add_command(label='Yard', command=box_alert)
#   show spaceship state
#   bouton acheter vaisseau/équipement
#   bouton vendre vaisseau/équipement
menutrade.add_command(label='Bank', command=box_error)
#   bouton Crédit
#   bouton Assurance
menubar.add_cascade(label='Trade', menu=menutrade)

# menu Tableau de service
# Status du commandant
# Quête
# Vaisseau
# Cargo spécial

# menu Cartes
# Information du système
#   bouton News
# Carte galactique => tabs
# Carte courte portée => tabs

# menu Aide
menuhelp = tk.Menu(menubar, tearoff=0)
menuhelp.add_command(label='Help', command=box_help)
menuhelp.add_command(label='About', command=box_about)
menubar.add_cascade(label='Help', menu=menuhelp)

Mafenetre.config(menu=menubar)

# boucle d'attente
Mafenetre.mainloop()
