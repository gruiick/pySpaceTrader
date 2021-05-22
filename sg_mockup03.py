#!/usr/bin/env python3
# coding: utf-8
#
# $Id: sg_mockup03.py 1530 $
# SPDX-License-Identifier: BSD-2-Clause

"""
même GUI que tk_mockup02, mais avec PySimpleGUI
python3 >= 3.7

"""

import PySimpleGUI as sg
import math

import constants
import cli_01

from pprint import pprint

# Globals
MAXW = constants.MAXWIDTH
MAXH = constants.MAXHEIGHT
MAXP = constants.MAXPARSEC
GOODS = constants.GOODS
MAX = 60

overview = ' '.join(constants.OVERVIEW)
msg_overview = '\n'.join(['pySpaceTrader', constants.VERSION, overview])

target = []             # items composing the 'target'
limite = []             # item composing the limit circle
clicked_position = ()   # keep temporary click position global

######################
## define GUI Elements
# Menu first
menu_def = [['&File',
                ['&New', '&Load', '&Save', 'E&xit']
            ],
            ['&Help', '&About'],
           ]

# Captain layout
captain_layout = sg.Frame(
    layout = [
        [sg.Text('display Captain infos', size=(30,2), key='-IN-CAPTAIN-')],
        [sg.Button('homeworld', key='-HOMEWORLD-')],
        [sg.Button('location', key='-LOCATION-')],
        [sg.Button('destination', key='-DESTINATION-')],
            ], title='Captain')

# info layout
info_layout = sg.Frame(
    layout = [
        [sg.Text('display planet infos', size=(30,5), key='-IN-PLANET-')],
             ], title='Info')

# actions layout
action_layout = sg.Frame(
    layout = [
        [sg.Button('set destination', key='-SETDEST-')],
        [sg.Button('refuel', key='-REFUEL-')],
        [sg.Button('next turn', key='-NEXT-TURN-')],
            ], title='Actions')

# first column's frame
navigation_layout = sg.Frame(
    layout=[
        [captain_layout],
        [info_layout],
        [action_layout],
            ], title='Navigation')

# one layout for each Tab
tab_galactic_map = [
    [sg.Graph(
        (MAXW, MAXH),
        (0, 0),
        (MAXW, MAXH),
        background_color='lightgrey',
        enable_events=True,
        key='-GRAPH-')],
    [sg.Text('Detected clic in X=, Y=', size=(30,1), key='-IN-CLIC-')],
                    ]

tab_trading = [
               [sg.Text('This is inside tab 2:')],
               [sg.Input(key='-IN-')], [sg.Button('update', key='Update')],
               [sg.Text('', size=(10,1), key='-OUTPUT-')],
              ]

# two columns
left_column = sg.Column([[navigation_layout]],
                        justification='left',
                        element_justification='left',
                        vertical_alignment='top')

right_column = sg.Column([
                        [sg.TabGroup(
                            [[
                            sg.Tab('Galactic Map', tab_galactic_map),
                            sg.Tab('Trading', tab_trading),
                            ]],
                        )],
                        ],
                        justification='right',
                        element_justification='right',
                        vertical_alignment='top')

# final layout
layout = [
    [sg.Menu(menu_def, tearoff=True)],
    [left_column, right_column],
         ]

# create window
window = sg.Window('mockup03', layout, auto_size_buttons=False)

# simplify call for map objects
graph = window['-GRAPH-']

############
## Functions

def new_game():
    """ nouveau jeu """
    global univers, planetes, captain
    # créer l'univers
    univers = cli_01.create_universe()
    # séparer la liste de planetes
    planetes = [x for x in univers if isinstance(x, cli_01.Planet)]
    # pprint(planetes)
    # séparer le capitaine (tant qu'à faire)
    toto = [x for x in univers if isinstance(x, cli_01.Captain)]
    captain = toto[0]
    # pprint(captain)
    draw_map()
    update_gui()


def draw_limite(position, rayon=None):
    """ erase and redraw the parsec limit
    position: positionnal tuple (x, y)
    rayon: int (or None)
    """
    if rayon is None:
        rayon = 5  # int(captain.ship.model['fuel'] * MAXP)
    # supprimer le cercle existant (if any)
    for item in limite:
        graph.delete_figure(item)
    limite.clear()
    limite.append(graph.draw_circle(position, rayon, line_color='red'))


def draw_target(position):
    """ erase and redraw the target
    position: positionnal tuple (x, y)
    """
    x, y = position
    for item in target:
        graph.delete_figure(item)
    target.clear()
    target.append(graph.draw_line((x, 0), (x, MAXH), color='blue'))
    target.append(graph.draw_line((0, y), (MAXW, y), color='blue'))


def draw_map(rayon=None):
    """ draw the Galactic Map
    rayon: int (or None)
    """
    graph.erase()

    for planete in planetes:
        x, y = planete.position
        if planete.homeworld:
            graph.draw_circle((x, y), 2, fill_color='blue', line_color='blue')
        elif planete.visited:
            graph.draw_circle((x, y), 2, fill_color='green', line_color='green')
        else:
            graph.draw_circle((x, y), 2, fill_color='red', line_color='red')
    # draw and update Captain location
    x, y = captain.location.position
    # trace fuel limit
    draw_limite((x, y), rayon=captain.ship.reservoir)
    if captain.destination:
        x, y = captain.destination.position
    draw_target((x, y))


def update_affiche(objet):
    """ update text in labels
    objet: Planet() or Captain()
    """
    if isinstance(objet, cli_01.Planet):
        description = ' '.join([objet.name, ':', str(objet.position), '\n', ' '.join(objet.gov)])
        window['-IN-PLANET-'].update(description)
    elif isinstance(objet, cli_01.Captain):
        description = ' '.join([objet.name, 'from', objet.homeworld.name, '\n', str(objet.balance)])
        window['-IN-CAPTAIN-'].update(description)


def update_gui():
    """ update GUI """
    update_affiche(captain)
    planete = captain.location
    update_affiche(planete)

    capacity = int(captain.ship.model['fuel'] * MAXP)
    if captain.ship.reservoir < capacity:
        window['-REFUEL-'].update(disabled=None)
    else:
        window['-REFUEL-'].update(disabled=True)

    if captain.destination:
        window['-SETDEST-'].update(disabled=False)
        window['-NEXT-TURN-'].update(disabled=False)
        # update trading tab
        # update_trading()
    else:
        window['-SETDEST-'].update(disabled=False)
        window['-NEXT-TURN-'].update(disabled=True)
        # update trading tab
        # update_trading()


def show_homeworld():
    """ set target on homeworld """
    for planete in planetes:
        if planete.homeworld:
            position = planete.position
            update_affiche(planete)
            draw_target(position)


def show_location():
    """ set target on actual captain.location """
    planete = captain.location
    position = planete.position
    update_affiche(planete)
    draw_target(position)


def get_distance(source, target):
    """ calculate distance between source and target
    source: positionnal tuple (x, y)
    target: positionnal tuple (x, y)
    return: positionnal tuple (x, y)
    """
    xa, ya = source
    xb, yb = target
    x = xb - xa
    y = yb - ya
    return int(math.hypot(x, y))

def save_as():
    """ save to a new file """
    fname = sg.popup_get_file('Save game to file',
                            save_as = True,
                            default_extension = '',
                            file_types = (('saved game(s)', '*.db'),
                                          ('all files', '*.*')),
                            ).replace('.db', '')
    # print(fname)
    cli_01.save_game(univers, fname=fname)


def set_destination():
    """ save clicked position into captain.destination """
    global captain, clicked_position
    try:
        distance = get_distance(captain.location.position, clicked_position.position)

        if distance is 0:
            sg.popup(f'Cannot set destination: Same as current location.')
        elif distance < captain.ship.reservoir:
            captain.destination = clicked_position
            # update_trading(destinationTradingInfo, captain.destination)
            # window['-SETDEST-'].update(disabled=False)
            window['-NEXT-TURN-'].update(disabled=False)
        elif distance > int(captain.ship.model['fuel'] * MAXP):
            sg.popup(f'Cannot set destination: too far.')
        else:
            sg.popup(f'Cannot set destination: Not enought fuel.')

    except AttributeError:
        sg.popup(f'Cannot set destination: Same as current location.')


def next_turn():
    """ step forward """
    # is there a destination set? ->AttributeError
    try:
        distance = get_distance(captain.location.position, captain.destination.position)

        if captain.ship.reservoir > 0:
            # calculate rayon loss
            rayon = captain.ship.reservoir - distance
            if rayon <= 0:
                captain.ship.reservoir = 0
                rayon = 0
            else:
                captain.ship.reservoir = rayon
            # update planete.visited to True
            captain.destination.visited = True
            # switch captain position
            captain.location = captain.destination
            captain.destination = None
            # print(captain.location.name)
            # update gui
            window['-SETDEST-'].update(disabled=False)
            window['-REFUEL-'].update(disabled=False)
            window['-NEXT-TURN-'].update(disabled=True)
            update_affiche(captain.location)
            #self.update_trading(self.locationTradingInfo, self.captain.location)
            #self.update_trading(self.destinationTradingInfo)
            draw_map(rayon=rayon)
            update_gui()

    except AttributeError:
        sg.popup(f'Set a destination first.')


def refuel():
    """ refuel the captain.ship according to captain.balance
    and planete.fuel_price
    """
    capacity = int(captain.ship.model['fuel'] * MAXP)
    # TODO: quantity available on planete ?
    if captain.ship.reservoir < capacity:
        deficit = capacity - captain.ship.reservoir
        price = deficit * captain.location.fuel_price
        # print(price)
        if price <= captain.balance:
            captain.balance = captain.balance - price
            captain.ship.reservoir = capacity  # or reservoir + deficit
            rayon = capacity
            # TODO: update (planete.price_slip[goods['fuel']][2]) - deficit)
            draw_limite(captain.location.position, rayon)
            update_affiche(captain)
            window['-REFUEL-'].update(disabled=True)
            # window['-NEXT-TURN-'].update(disabled=False)
            # update_board()
        else:
            sg.popup(f'Cannot buy fuel: not enought credit')
    else:
        sg.popup(f'Cannot buy fuel: full capacity')


def show_destination():
    """ set/draw target on destination """
    if captain.destination:
        planete = captain.destination
        position = planete.position
        update_affiche(planete)
        draw_target(position)
    else:
        sg.popup(f'Cannot show destination: None set.')


def on_click(position):
    """ redraw graph with new clicked position """
    global clicked_position
    for planete in planetes:
        if cli_01.collision(position, planete):
            position = planete.position
            clicked_position = planete
            update_affiche(planete)
            draw_target(position)

    x, y = position
    window['-IN-CLIC-'].update(value=f'Detected clic in X={x}, Y={y}')


def load_file():
    """ load saved game """
    global univers, planetes, captain
    fname = sg.popup_get_file('Saved game to open',
                            default_extension = '.db',
                            file_types = (('saved game(s)', '*.db'),
                                          ('all files', '*.*')),
                            ).replace('.db', '')
    # print(fname)
    univers = cli_01.load_game(fname=fname)
    planetes = [x for x in univers if isinstance(x, cli_01.Planet)]
    toto = [x for x in univers if isinstance(x, cli_01.Captain)]
    captain = toto[0]
    draw_map()
    update_gui()


# Event Loop
while True:
    event, values = window.read()
    print(event, values)

    if event == sg.WIN_CLOSED or event == 'Exit':
        break

    elif event == 'New':
        new_game()

    elif event == 'Update':
        # Update the "output" text element to be the value of "input" element
        window['-OUTPUT-'].update(values['-IN-'])

    elif event == 'Load':
        load_file()

    elif event == 'Save':
        # TODO: SaveAs vs 'Save to existing'
        save_as()

    elif event == '-GRAPH-':
        on_click(values['-GRAPH-'])

    elif event == '-HOMEWORLD-':
        show_homeworld()

    elif event == '-LOCATION-':
        show_location()

    elif event == '-DESTINATION-':
        show_destination()

    elif event == '-SETDEST-':
        set_destination()

    elif event == '-REFUEL-':
        refuel()

    elif event == '-NEXT-TURN-':
        next_turn()

    elif event == 'About':
        sg.popup(msg_overview)


window.close()
