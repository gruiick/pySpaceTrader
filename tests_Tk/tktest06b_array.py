#!/usr/bin/env python3
# coding:utf-8

# $Id: tktest06b_array.py 1302 $
# SPDX-License-Identifier: BSD-2-Clause
# original author: noobien from openclassrooms.com
 
import tkinter as tk
 
# fenêtre principale
w = tk.Tk()
 
# le tableau à afficher : [0, 0, 0, 0, 0]
tableau = [0 for i in range(5)]
 
# les 2 couleurs à utiliser
couleurs = {0: "white", 1: "blue"}
 
# dimensions du canevas
can_width = 250
can_height = 50
 
# taille d'une "case"
size = 50
 
# création canevas
can = tk.Canvas(w, width=can_width, height=can_height)
can.grid()
 
def afficher(t):
    """
    Fonction d'affichage du tableau ; 1 élément = 1 case
    La couleur de la "case" dépend de l'état de l'élement correspondant, 0 ou 1
    """
    for i in range(len(t)):
        can.create_rectangle(i * size,
                             0,
                             i * size + size,
                             size,
                             fill = couleurs[tableau[i]])
 
def modifierTableau(evt):
    """
    Fonction appelée lors d'un clic gauche sur le canevas
    Déterminer la correspondance entre la position horizontale
    de la souris et l'élément correspondant du tableau :
    evt.x est la position en x de la souris
    Pour simplifier j'ai pris un tableau à une dimension ;
    si on utilise un tableau 2d (échecs, dames, tic tac toe, etc)
    il faudra s'occuper aussi de evt.y ... """
    pos_x = int(evt.x / size)
 
    # inverser la valeur de l'élément cliqué
    if tableau[pos_x] == 0:
        tableau[pos_x] = 1
    else:
        tableau[pos_x] = 0
 
    # ré-afficher le tableau
    afficher(tableau)
 
#-----------------------------------------------------
# programme
afficher(tableau)
# binding de la fonction modifierTableau sur le canevas
can.bind("<Button-1>", modifierTableau)
# boucle principale
w.mainloop()
