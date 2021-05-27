#!/usr/bin/env python3
# coding: utf-8
#
# $Id: tk_mockup02.py 1544 $
# SPDX-License-Identifier: BSD-2-Clause

"""
deuxième essai : même fenêtre avec ses menus, mais Class
    http://tkinter.fdex.eu/doc/popdial.html
    https://docs.python.org/3.1/library/tkinter.ttk.html
    http://www.jchr.be/python/tkinter.htm
    http://tkinter.fdex.eu/doc/gp.html (pack() to grid())
    http://tkinter.fdex.eu/index.html

TODO: séparer UI et logique de jeu

"""

import tkinter as tk
import tkinter.messagebox as tkmsg
import tkinter.filedialog as tkfd
from tkinter import ttk
import math

import constants
import cli_01

MAXW = constants.MAXWIDTH
MAXH = constants.MAXHEIGHT
MAXP = constants.MAXPARSEC
GOODS = constants.GOODS
MAX = 60


class Application(tk.Tk):
    """ gère la GUI """
    def __init__(self):
        tk.Tk.__init__(self)  # constructeur de la classe parente
        self.title('mockup02')

        self.univers = []  # the whole universe
        self.captain = ()  # Captain Speaking
        self.planetes = []  # list of planetes
        self.target = []  # items composing the 'target'
        self.limite = []  # item composing the limit circle
        self.clicked_position = ()  # keep temporary click position global

        self.colgauch = tk.Frame(self, bd=2)  # sa taille est fixée par self.affiche_?
        self.info_title = tk.LabelFrame(self.colgauch, text='Info', width=14, labelanchor=tk.NW)
        self.captain_title = tk.LabelFrame(self.colgauch, text='Captain', width=14, labelanchor=tk.NW)
        self.action_title = tk.LabelFrame(self.colgauch, text='Actions', labelanchor=tk.NW)
        # boutons
        self.bnew = tk.Button(self.action_title, text='new', height=1, command=self.new_game)  # devra disparaitre (->menu)
        self.bhworld = tk.Button(self.captain_title, text='homeworld', height=1, command=self.show_homeworld)
        self.bturn = tk.Button(self.action_title, text='next turn', height=1, state='disabled', command=self.next_turn)
        self.bsetdest = tk.Button(self.action_title, text='set destination', height=1, command=self.set_destination)
        self.blocat = tk.Button(self.captain_title, text='location', height=1, command=self.show_location)
        self.bfuel = tk.Button(self.action_title, text='refuel', height=1, state='disabled', command=self.refuel)
        self.bdest = tk.Button(self.captain_title, text='destination', height=1, state='disabled', command=self.show_destination)
        # zone(s) de texte
        self.affiche_planet_info = tk.Label(self.info_title, wraplength=100, width=14, anchor=tk.NW, justify=tk.LEFT)
        self.affiche_captain_info = tk.Label(self.captain_title, wraplength=100, width=14, anchor=tk.NW, justify=tk.LEFT)

        self.coldroit = tk.LabelFrame(self)  # sa taille est fixée par self.CanvasGalacticMap
        # onglets (notebook)
        self.Onglets = ttk.Notebook(self.coldroit, padding='3 3 5 5')  # , width=450, height=250
        self.OngletGalacticMap = ttk.Frame(self.Onglets)  # first page, which would get widgets gridded into it
        self.OngletTrading = ttk.Frame(self.Onglets)  # second page
        self.Onglets.add(self.OngletGalacticMap, text='Galactic Map', state='normal')
        self.Onglets.add(self.OngletTrading, text='Trading info', state='normal')

        # Galactic Canvas = zone de base pour dessiner
        self.CanvasGalacticMap = tk.Canvas(self.OngletGalacticMap, width=MAXW, height=MAXH - 2, bg='white')
        self.CanvasGalacticMap.bind('<Button-1>', self.on_click)
        # zone(s) de texte curseur
        self.chaineGalacticMap = tk.Label(self.OngletGalacticMap)  # (x, y) du curseur

        # Trading Frame = zone de base pour les tableaux
        self.framegTradingInfo = tk.LabelFrame(self.OngletTrading, text='Current location prices', width=14, labelanchor=tk.NW)
        self.locationTradingInfo = SimpleTable(self.framegTradingInfo, 12, 5, actif=True)
        # headers
        self.locationTradingInfo.set(0, 0, 'Item')
        self.locationTradingInfo.set(0, 1, 'Buy')
        self.locationTradingInfo.set(0, 2, 'Sell')
        self.locationTradingInfo.set(0, 3, 'Stocks')
        self.locationTradingInfo.set(0, 4, 'Cargo')
        # framecentre (Frame) pour selecteur de cargo
        self.framecTradingInfo = tk.Frame(self.OngletTrading, width=14)
        #
        self.framedTradingInfo = tk.LabelFrame(self.OngletTrading, text='Destination prices', width=14, labelanchor=tk.NE)
        self.destinationTradingInfo = SimpleTable(self.framedTradingInfo, 12, 4)
        # headers
        self.destinationTradingInfo.set(0, 0, 'Item')
        self.destinationTradingInfo.set(0, 1, 'Buy')
        self.destinationTradingInfo.set(0, 2, 'Sell')
        self.destinationTradingInfo.set(0, 3, 'Stocks')
        # self.destinationTradingInfo.set(0, 4, 'Cargo')
        # framesud (LabelFrame) pour afficher captain.balance, état des pods
        self.framesTradingInfo = tk.LabelFrame(self.OngletTrading, text='Captain board', width=28, labelanchor=tk.NW)
        self.board = SimpleTable(self.framesTradingInfo, 4, 4)
        # headers
        self.board.set(0,0, 'Balance: ')
        self.board.set(1,0, '')
        self.board.set(2,0, 'Credit: ')
        self.board.set(3,0, 'Interests: ')
        self.board.set(0,2, 'Cargo: ')
        self.board.set(1,2, 'Value: ')
        self.board.set(2,2, '')
        self.board.set(3,2, '')
        self.bbuy = tk.Button(self.framesTradingInfo, text='buy', height=1, state='disabled', command=self.buy_cargo)

        ########################
        # Gestionnaire de grille
        ########################
        # self.rowconfigure(0, weight=1)
        # self.columnconfigure(0, weight=1)
        # self.columnconfigure(1, weight=3)
        self.grid_bbox(0, 0, 19, 19)
        self.colgauch.grid(row=0, column=0, rowspan=20, sticky='enw')

        self.captain_title.columnconfigure(0, weight=1)
        self.captain_title.grid(row=1, column=0, sticky='ew', pady=2, ipady=2)
        self.affiche_captain_info.grid(row=0, column=0, rowspan=8, sticky='ew', pady=5, ipady=2)
        self.bhworld.grid(row=9, column=0, sticky='news')
        self.blocat.grid(row=10, column=0, sticky='news')
        self.bdest.grid(row=11, column=0, sticky='news')

        self.info_title.grid(row=9, column=0, sticky='ew', pady=2, ipady=2)
        self.affiche_planet_info.grid(row=0, column=0, rowspan=10, sticky='ew', pady=5, ipady=5)

        self.action_title.columnconfigure(0, weight=1)
        self.action_title.grid(row=20, column=0, sticky='ew', pady=2, padx=2)
        self.bnew.grid(row=0, column=0, sticky='news')
        self.bsetdest.grid(row=2, column=0, sticky='news')
        self.bfuel.grid(row=3, column=0, sticky='news')
        self.bturn.grid(row=4, column=0, sticky='news')

        self.coldroit.grid(row=0, column=1, rowspan=19, sticky='n')
        self.Onglets.grid(row=0, column=1)  # , columnspan=18, rowspan=19)
        self.CanvasGalacticMap.grid(in_=self.OngletGalacticMap, padx=2, pady=2, sticky='news')
        self.chaineGalacticMap.grid(in_=self.OngletGalacticMap, padx=2, pady=2, sticky='s')
        # slip location
        self.framegTradingInfo.grid(in_=self.OngletTrading, row=0, column=0, padx=2, pady=2, sticky='new')
        self.locationTradingInfo.grid(in_=self.framegTradingInfo, row=0, column=0, padx=2, pady=2, sticky='news')
        # caser les boutons buy/sell ici ? (column=1, sticky='n')
        self.framecTradingInfo.grid(in_=self.OngletTrading, row=0, column=1, padx=2, pady=2, sticky='ews')
        # slip destination
        self.framedTradingInfo.grid(in_=self.OngletTrading, row=0, column=2, padx=2, pady=2, sticky='new')
        self.destinationTradingInfo.grid(in_=self.framedTradingInfo, row=0, column=0, padx=2, pady=2, sticky='news')
        # afficher cargo pods et current captain.balance (row=2, sticky='ew')
        self.framesTradingInfo.grid(in_=self.OngletTrading, row=2, column=0, columnspan=3, padx=2, pady=2, sticky='ew')
        self.board.grid(in_=self.framesTradingInfo, row=0, column=0, padx=2, pady=2, sticky='ew')
        self.bbuy.grid(in_=self.framesTradingInfo, row=0, column=1, padx=2, pady=2, sticky='ew')

        # barre de menus
        self.menubar = tk.Menu(self)
        # menu Fichier
        self.menufile = tk.Menu(self.menubar, tearoff=0)
        self.menufile.add_command(label='New', command=self.new_game)
        self.menufile.add_command(label='Open', command=self.box_open)
        self.menufile.add_command(label='Save', command=self.box_save)
        self.menufile.add_separator()
        self.menufile.add_command(label='Quit', command=self.quit)
        self.menubar.add_cascade(label='File', menu=self.menufile)
        # menu Aide
        self.menuhelp = tk.Menu(self.menubar, tearoff=0)
        self.menuhelp.add_command(label='Help', command=self.box_help)
        self.menuhelp.add_command(label='About', command=self.box_about)
        self.menubar.add_cascade(label='Help', menu=self.menuhelp)
        # assemble menubar
        self.config(menu=self.menubar)

    def box_about(self):
        # TODO: revoir fonts et largeur de la box
        overview = ' '.join(constants.OVERVIEW)
        msg = '\n'.join(['pySpaceTrader v0.1', overview])
        tkmsg.showinfo('About', msg)

    def box_alert(self, msg=None):
        """ Alert, with optional message """
        if msg is None:
            tkmsg.showwarning('Alert', 'Bravo!')
        else:
            tkmsg.showwarning('Alert', msg)

    def box_error(self, msg=None):
        """ Error, with optional message """
        if msg is None:
            tkmsg.showerror('Error', 'This is an error.')
        else:
            tkmsg.showerror('Error', msg)

    def box_help(self):
        tkmsg.showinfo('Help', 'You have to click everywhere.')

    def box_info(self, msg=None):
        """ Info, with optional message """
        if msg is None:
            tkmsg.showinfo('Info', 'not much to show')
        else:
            tkmsg.showinfo('Info', msg)

    def box_open(self):
        """ load saved game """
        # strip extension '.db' from filename
        fname = tkfd.askopenfilename(filetypes=(("saved game(s)", "*.db"),
                                                ("all files", "*.*"))).replace('.db', '')
        self.univers = cli_01.load_game(fname=fname)
        self.planetes = [x for x in self.univers if isinstance(x, cli_01.Planet)]
        toto = [x for x in self.univers if isinstance(x, cli_01.Captain)]
        self.captain = toto[0]
        self.draw_map()
        self.update_gui()

    def box_save(self):
        """ save game """
        # strip extension '.db' from filename
        fname = tkfd.asksaveasfilename(defaultextension='',
                                       filetypes=(("saved game(s)", "*.db"),
                                                  ("all files", "*.*"))).replace('.db', '')
        cli_01.save_game(self.univers, fname=fname)

    def buy_cargo(self):
        """ buy good and update ship.cargo, captain.balance """
        # interact with spinboxes ?! interact with tab.location
        # ['water', 'furs', 'food', 'ore', 'games', 'firearms', 'medecine', 'machines', 'narcotics', 'robots', 'fuel']
        pass

    def draw_limite(self, x, y, rayon=None):
        """ erase and redraw the parsec limit """
        canv = self.CanvasGalacticMap
        if rayon is None:
            rayon = int(self.captain.ship.model['fuel'] * MAXP)
        # print(rayon)
        # supprimer le cercle existant (if any)
        for item in self.limite:
            canv.delete(item)
        self.limite.clear()
        # (re)tracer le cercle rouge
        self.limite.append(cercle(canv, x, y, rayon, color='red'))

    def draw_map(self, rayon=None):
        """ dessine la galactic map """
        # Effacer tout dessin préexistant :
        canv = self.CanvasGalacticMap
        canv.delete(tk.ALL)
        try:
            for planete in self.planetes:
                x, y = planete.position
                if planete.homeworld:
                    cercle(canv, x, y, 2, 'blue', fill='blue')
                elif planete.visited:
                    cercle(canv, x, y, 2, 'green', fill='green')
                else:
                    cercle(canv, x, y, 2, 'red', fill='red')
            # draw and update captain location
            x, y = self.captain.location.position
            # tracer limite fuel :
            self.draw_limite(x, y, rayon=self.captain.ship.reservoir)
            if self.captain.destination:
                x, y = self.captain.destination.position
            # tracer la target
            self.draw_target(x, y)

        except:
            print("planetes[] was not an array")
            print(type(self.planetes))

    def draw_target(self, x, y):
        """ erase and redraw the target """
        # supprimer les items existants (if any)
        canv = self.CanvasGalacticMap
        for item in self.target:
            canv.delete(item)
        self.target.clear()
        # tracer les deux lignes (vert. et horiz.) :
        self.target.append(canv.create_line(x, 0, x, MAXH, fill='blue'))
        self.target.append(canv.create_line(0, y, MAXW, y, fill='blue'))

    def get_distance(self, source, target):
        """ calculate distance between source and target """
        xa, ya = source
        xb, yb = target
        x = xb - xa
        y = yb - ya
        return int(math.hypot(x, y))

    def new_game(self):
        """ nouveau jeu """
        # créer l'univers
        self.univers = cli_01.create_universe()
        # séparer la liste de planetes
        self.planetes = [x for x in self.univers if isinstance(x, cli_01.Planet)]
        # séparer le capitaine (tant qu'à faire)
        toto = [x for x in self.univers if isinstance(x, cli_01.Captain)]
        self.captain = toto[0]
        # print(type(self.captain))
        self.draw_map()
        self.update_gui()

    def next_turn(self):
        """ step forward """
        # is there a destination set? ->AttributeError
        try:
            distance = self.get_distance(self.captain.location.position, self.captain.destination.position)

            if self.captain.ship.reservoir > 0:
                # calculate rayon loss
                rayon = self.captain.ship.reservoir - distance
                if rayon <= 0:
                    self.captain.ship.reservoir = 0
                    rayon = 0
                else:
                    self.captain.ship.reservoir = rayon
                # update planete.visited to True
                self.captain.destination.visited = True
                # switch captain position
                self.captain.location = self.captain.destination
                self.captain.destination = None
                # print(self.captain.location.name)
                # update gui
                #self.bdest.configure(state='disabled')
                #self.update_affiche(self.captain.location)
                #self.update_trading(self.locationTradingInfo, self.captain.location)
                #self.update_trading(self.destinationTradingInfo)
                self.draw_map(rayon=rayon)
                self.update_gui()

        except AttributeError:
            self.box_alert(msg='Set a destination first.')

    def on_click(self, event):
        """ modifie chaine avec la position du curseur, 
            if planete, sauve planete dans clicked_position
        """
        # self.affiche.configure(text=str(self.colgauch.grid_info()))
        position = (event.x, event.y)
        for planete in self.planetes:
            if cli_01.collision(position, planete):
                (x, y) = planete.position
                self.clicked_position = planete
                self.update_affiche(planete)
                self.draw_target(x, y)

        texte = 'Detected clic in X=' + str(event.x) + ', Y=' + str(event.y)
        self.chaineGalacticMap.configure(text=texte)

    def refuel(self):
        """ refuel the captain.ship according to captain.balance and planete.fuel_price """
        capacity = int(self.captain.ship.model['fuel'] * MAXP)
        # TODO: quantity available on planete ?
        if self.captain.ship.reservoir < capacity:
            deficit = capacity - self.captain.ship.reservoir
            price = deficit * self.captain.location.fuel_price
            # print(price)
            if price <= self.captain.balance:
                self.captain.balance = self.captain.balance - price
                self.captain.ship.reservoir = capacity  # or reservoir + deficit
                rayon = capacity
                # TODO: update (planete.price_slip[goods['fuel']][2]) - deficit)
                x, y = self.captain.location.position
                self.draw_limite(x, y, rayon)
                self.update_affiche(self.captain)
                self.bfuel.configure(state='disabled')
                self.update_board()
            else:
                self.box_error(msg='Cannot buy fuel: not enought credit')
        else:
            self.box_info(msg='Cannot buy fuel: full capacity')

    def set_destination(self):
        """ save clicked position into captain.destination """
        try:
            distance = self.get_distance(self.captain.location.position, self.clicked_position.position)

            if distance is 0:
                self.box_error(msg='Cannot set destination: Same as current location.')
            elif distance < self.captain.ship.reservoir:
                self.captain.destination = self.clicked_position
                self.update_trading(self.destinationTradingInfo, self.captain.destination)
                self.bdest.configure(state='normal')
                self.bturn.configure(state='normal')
            elif distance > int(self.captain.ship.model['fuel'] * MAXP):
                self.box_error(msg='Cannot set destination: too far.')
            else:
                self.box_error(msg='Cannot set destination: Not enought fuel.')

        except AttributeError:
            self.box_error(msg='Cannot set destination: Same as current location.')

    def show_destination(self):
        """ set target on destination """
        planete = self.captain.destination
        x, y = planete.position
        self.update_affiche(planete)
        self.draw_target(x, y)

    def show_homeworld(self):
        """ set target on homeworld """
        for planete in self.planetes:
            if planete.homeworld:
                x, y = planete.position
                self.update_affiche(planete)
                self.draw_target(x, y)

    def show_location(self):
        """ set target on actual captain.location """
        planete = self.captain.location
        x, y = planete.position
        self.update_affiche(planete)
        self.draw_target(x, y)

    def update_affiche(self, objet):
        """ update text of affiche.Label """
        if isinstance(objet, cli_01.Planet):
            description = ' '.join([objet.name, ':', str(objet.position),
                                    '\n', ' '.join(objet.gov)])
            self.affiche_planet_info.configure(text=description)

        elif isinstance(objet, cli_01.Captain):
            description = ' '.join([objet.name, 'from', objet.homeworld.name,
                                    '\n', str(objet.balance)])
            self.affiche_captain_info.configure(text=description)

    def update_board(self):
        """ update info in board tabler """
        # headers & formula
        # self.board.set(0,0, 'Balance: ')
        # self.board.set(1,0, '')
        # self.board.set(2,0, 'Credit: ')
        # self.board.set(3,0, 'Interests: ')
        # self.board.set(0,2, 'Cargo: ')  # nb of occupied pods / total pods
        # self.board.set(1,2, 'Value: ')  # overall value of cargo
        # self.board.set(2,2, '')
        # self.board.set(3,2, '')
        pods = 0
        tpods = len(self.captain.ship.cargo)
        overall = 0
        for key in self.captain.ship.cargo.keys():
            if self.captain.ship.cargo[key]['type']:
                pods += 1
                overall += self.captain.ship.cargo[key]['value']
        self.board.set(0,1, self.captain.balance)
        self.board.set(2,1, 0)
        self.board.set(3,1, 0)
        #self.board.set(0,3, int(pods))
        self.board.set(0,3, '/'.join([str(pods), str(tpods)]))
        self.board.set(1,3, int(overall))

    def update_gui(self):
        """ mets à jour la GUI (hors map) """

        self.update_affiche(self.captain)
        planete = self.captain.location
        self.update_affiche(planete)

        capacity = int(self.captain.ship.model['fuel'] * MAXP)
        if self.captain.ship.reservoir < capacity:
            self.bfuel.configure(state='normal')
        else:
            self.bfuel.configure(state='disabled')

        # update trading tab.destination
        if self.captain.destination:
            self.bdest.configure(state='normal')
            self.bturn.configure(state='normal')
            self.update_trading(self.destinationTradingInfo, self.captain.destination)
        else:
            self.bdest.configure(state='disabled')
            self.bturn.configure(state='disabled')
            self.update_trading(self.destinationTradingInfo)

        # update trading tab.location
        self.update_trading(self.locationTradingInfo, planete)
        self.update_spinboxes(self.locationTradingInfo, status=True)

        self.update_board()

    def update_spinboxes(self, table, status=False):
        """ update the 'cargo' part of the table """
        goods = list(GOODS.keys())
        height = table.rows
        # height(0, x) is the header, that's one row to avoid 
        # hence (height - 1) and (i + 1)
        for i in range(height - 1):
            to = len(self.captain.ship.cargo)
            tv = None
            if status:
                state = 'normal'
            else:
                state = 'disabled'
            table.spinset(i + 1, 4, to=to, tv=tv, state=state)

    def update_trading(self, table, planet=None):
        """ update price slip in the table """
        if planet is None:
            table.clear()
        else:
            goods = list(GOODS.keys())
            height = table.rows
            # height(0, x) is the header, that's one row to avoid 
            # hence (height - 1) and (i + 1)
            for i in range(height - 1):
                table.set(i + 1, 0, goods[i])
                table.set(i + 1, 1, planet.price_slip[goods[i]][0])
                table.set(i + 1, 2, planet.price_slip[goods[i]][1])
                table.set(i + 1, 3, planet.price_slip[goods[i]][2])


class SimpleTable(tk.Frame):
    """ generate a tabular frame of labels (rows, columns) """
    def __init__(self, parent, rows=2, columns=2, actif=False):
        # use black background so it "peeks through" to 
        # form grid lines
        tk.Frame.__init__(self, parent, background='black')
        self._widgets = []
        self.rows = rows
        self.columns = columns

        for row in range(self.rows):
            current_row = []
            for column in range(self.columns):
                if row > 0 and column == self.columns - 1 and actif:
                    #print('toto')
                    spinbox = tk.Spinbox(self, from_=0, to=10, increment=1, width=4)
                    spinbox.config(justify="center", state='disabled')
                    spinbox.grid(row=row, column=column, sticky='news', padx=1, pady=1)
                    current_row.append(spinbox)
                else:
                    label = tk.Label(self, text='', borderwidth=0, width=8)
                    label.grid(row=row, column=column, sticky='news', padx=1, pady=1)
                    current_row.append(label)
            self._widgets.append(current_row)

        for column in range(self.columns):
            self.grid_columnconfigure(column, weight=1)

    def clear(self):
        """ empty all cells, except headers, on demand """
        # headers are in row 0 -> (rows - 1, i + 1)
        for i in range(self.rows - 1):
            for j in range(self.columns):
                self.set(i + 1, j, '')

    def set(self, row, column, value):
        """ set the content of a cell (row, column, value) """
        widget = self._widgets[row][column]
        widget.configure(text=value)

    def spinset(self, row, column, to=None, tv=None, state=None):
        """ set the config of a spinbox (row, column, **kwargs) 
            to = max value (default to len(self.captain.ship.cargo))
            tv = textvariable value
            state = 'normal'/'disabled'
        """
        widget = self._widgets[row][column]
        if to:
            widget.configure(to=to)
        if tv:
            widget.configure(textvariable=tv)
        if state:
            widget.configure(state=state)

    # TODO: spinget, pour récupérer valeur et état(s)
    # gérer l'interdépendance entre spinbox (+1 sur une = ('to' - 1) sur toutes les autres)

    @property  # pour en caser une
    def size(self):
        """ return current size """
        return (self.rows, self.columns)


def cercle(canv, x, y, r, color='black', fill=None):
    """tracé d'un cercle de centre (x,y) et de rayon r"""
    return canv.create_oval(x - r, y - r, x + r, y + r, outline=color, fill=fill)


if __name__ == '__main__':
    app = Application()
    # boucle d'attente
    app.mainloop()
