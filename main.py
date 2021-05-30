#!/usr/bin/env python3
# coding: utf-8
#
# $Id: main.py 1557 $
# SPDX-License-Identifier: BSD-2-Clause

"""
même GUI que tk_mockup02, mais avec PySimpleGUI
python3 >= 3.7

"""

import PySimpleGUI as sg
import math

import constants
import core
import sgui

# from pprint import pprint

# Globals
MAXW = constants.MAXWIDTH
MAXH = constants.MAXHEIGHT
MAXP = constants.MAXPARSEC
GOODS = constants.GOODS
# MAX = 60
COLORS = constants.COLORS

overview = ' '.join(constants.OVERVIEW)
msg_overview = '\n'.join(['pySpaceTrader', constants.VERSION, overview])

univers = []            # global container for game objects
target = []             # items composing the 'target'
limite = []             # item composing the limit circle
clicked_position = ()   # keep temporary click position global

# define GUI, using sgui.py layout
# create window
window = sg.Window('pySpaceTrader',
                   sgui.final_layout,
                   auto_size_buttons=False,
                   resizable=True)

# simplify call for map objects
graph = window['-GRAPH-']


def buy_cargo(facture):
    """ load into cargo pods whats in the incoming invoice """

    good_type, good_price, qty, cargo_value = facture

    _none_cargo = [x for x in captain.ship.cargo.keys() if captain.ship.cargo[x]['type'] is None]
    available_cargo = len(_none_cargo)
    print(f'pod(s): {_none_cargo}')
    print(f'avail: {available_cargo}')

    if qty > available_cargo:
        sg.popup_error('Cannot buy that quantity, not enought cargo space!')
    else:
        for index in range(0, qty):
            captain.ship.cargo[index]['type'] = good_type
            captain.ship.cargo[index]['value'] = good_price
            available_cargo -= 1
            captain.location.price_slip[good_type][-1] -= 1
        captain.balance -= cargo_value
        update_trading(window['-LOC-TABLE-'], captain.location)
        update_captain_board()
        update_cargo_board(captain.location)

    # TODO log invoice in bank account


def draw_limite(position, rayon=None):
    """ erase and redraw the parsec limit
    position: positionnal tuple (x, y)
    rayon: int (or None)
    """
    if rayon is None:
        rayon = int(captain.ship.model['fuel'] * MAXP)
    for item in limite:
        # supprimer le cercle existant (if any)
        graph.delete_figure(item)
    limite.clear()
    limite.append(graph.draw_circle(position, rayon, line_color=COLORS['limit']))


def draw_map(rayon=None):
    """ draw the Galactic Map
    rayon: int (or None)
    """
    graph.erase()

    for planete in planetes:
        x, y = planete.position
        if planete.homeworld:
            graph.draw_circle((x, y),
                              2,
                              fill_color=COLORS['homeworld'],
                              line_color=COLORS['homeworld'])
        elif planete.visited:
            graph.draw_circle((x, y),
                              2,
                              fill_color=COLORS['visited'],
                              line_color=COLORS['visited'])
        else:
            graph.draw_circle((x, y),
                              2,
                              fill_color=COLORS['default'],
                              line_color=COLORS['default'])
    # draw and update Captain location
    x, y = captain.location.position
    # trace fuel limit
    draw_limite((x, y), rayon=captain.ship.reservoir)
    if captain.destination:
        x, y = captain.destination.position
    draw_target((x, y))


def draw_target(position):
    """ erase and redraw the target
    position: positionnal tuple (x, y)
    """
    x, y = position
    for item in target:
        graph.delete_figure(item)
    target.clear()
    target.append(graph.draw_line((x, 0),
                                  (x, MAXH),
                                  color=COLORS['target']))
    target.append(graph.draw_line((0, y),
                                  (MAXW, y),
                                  color=COLORS['target']))


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


def load_file():
    """ load saved game """
    global univers, planetes, captain
    fname = sg.popup_get_file('Saved game to open',
                              default_extension='.db',
                              file_types=(('saved game(s)', '*.db'),
                                          ('all files', '*.*')),
                              ).replace('.db', '')
    # print(fname)
    univers = core.load_game(fname=fname)
    planetes = [x for x in univers if isinstance(x, core.Planet)]
    _toto = [x for x in univers if isinstance(x, core.Captain)]
    captain = _toto[0]
    draw_map()
    update_gui()


def new_game():
    """ new game """
    global univers, planetes, captain
    # create universe
    univers = core.create_universe()
    # set planets apart
    planetes = [x for x in univers if isinstance(x, core.Planet)]
    # pprint(planetes)
    # set Captain apart too
    _toto = [x for x in univers if isinstance(x, core.Captain)]
    captain = _toto[0]
    # pprint(captain.__dict__)
    draw_map()
    update_gui()


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
            draw_map(rayon=rayon)
            update_gui()

    except AttributeError:
        sg.popup(f'Set a destination first.')


def on_click(position):
    """ redraw graph with new clicked position """
    global clicked_position
    for planete in planetes:
        if core.collision(position, planete):
            position = planete.position
            clicked_position = planete
            update_affiche(planete)
            draw_target(position)

    x, y = position
    window['-IN-CLIC-'].update(value=f'Detected clic in X={x}, Y={y}')


def refuel():
    """ refuel the captain.ship according to captain.balance, ship.reservoir
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
            update_captain_board()
        else:
            sg.popup(f'Cannot buy fuel: not enought credit')
    else:
        sg.popup(f'Cannot buy fuel: full capacity')


def save():
    """ save into the previously open/selected file """
    pass


def save_as():
    """ save to a new file """
    fname = sg.popup_get_file('Save game to file',
                              save_as=True,
                              default_extension='',
                              file_types=(('saved game(s)', '*.db'),
                                          ('all files', '*.*')),
                              ).replace('.db', '')
    # print(fname)
    core.save_game(univers, fname=fname)


def set_destination():
    """ save clicked position into captain.destination """
    global captain, clicked_position
    try:
        distance = get_distance(captain.location.position, clicked_position.position)

        if distance == 0:
            sg.popup(f'Cannot set destination: Same as current location.')

        elif distance < captain.ship.reservoir:
            captain.destination = clicked_position
            # update Trading tab
            window['-DEST-TITLE-'].update(value=f'Destination: {captain.destination.name}')
            update_trading(window['-DEST-TABLE-'], captain.destination)
            update_profit(captain.destination)
            # allow next_turn()
            window['-NEXT-TURN-'].update(disabled=False)

        elif distance > int(captain.ship.model['fuel'] * MAXP):
            sg.popup(f'Cannot set destination: Too far.')
        else:
            sg.popup(f'Cannot set destination: Not enought fuel.')

    except AttributeError:
        sg.popup(f'Cannot set destination: Same as current location.')


def show_destination():
    """ set/draw target on destination """
    if captain.destination:
        planete = captain.destination
        update_affiche(planete)
        draw_target(planete.position)
    else:
        sg.popup(f'Cannot show destination: None set.')


def show_homeworld():
    """ set target on homeworld """
    for planete in planetes:
        if planete.homeworld:
            update_affiche(planete)
            draw_target(planete.position)


def show_location():
    """ set target on actual captain.location """
    planete = captain.location
    update_affiche(planete)
    draw_target(planete.position)


def update_affiche(objet):
    """ update text in labels
    objet: Planet() or Captain()
    """
    if isinstance(objet, core.Planet):
        description = ''.join([objet.name,
                               ' : ',
                               str(objet.position),
                               '\n',
                               '\n'.join(objet.gov)])
        window['-IN-PLANET-'].update(description)

    elif isinstance(objet, core.Captain):
        description = ''.join([objet.name,
                               ' from ',
                               objet.homeworld.name,
                               '\n',
                               str(objet.balance)])
        window['-IN-CAPTAIN-'].update(description)


def update_cargo_board(planet):
    """ clear values in Cargo frame's elements """
    update_cargo_goods(planet)
    update_cargo_qty(good=None)
    window['-IN-INVOICE-'].update(value='')


def update_cargo_goods(planet):
    """ update values in combo's goods Cargo frame """
    _key_list = []

    for key, value in planet.price_slip.items():
        # if no stock, don't bother adding to picklist
        if value[-1] != 0:
            _key_list.append(key)

    window['-IN-GOODS-'].update(values=_key_list)


def update_cargo_qty(good=None):
    """ update picklist in combo's quantity Cargo frame """
    # FIXME: clear=False, instead of good=None
    # redo this algo
    _none_cargo = [x for x in captain.ship.cargo.keys() if captain.ship.cargo[x]['type'] is None]
    avail_pods = len(_none_cargo)

    if good is not None:
        _qty_max = captain.location.price_slip[good][-1]
        # _value_list = []
        if _qty_max < avail_pods:
            _value_list = list(range(1, _qty_max + 1))
        else:
            _value_list = list(range(1, avail_pods + 1))

    else:
        if avail_pods != 0:
            _value_list = list(range(1, avail_pods + 1))
        else:
            _value_list = ''

    window['-IN-QTY-'].update(values=_value_list)


def update_captain_board():
    """ update Captain board informations GUI element """
    pods = 0
    tpods = len(captain.ship.cargo)
    overall = 0
    for key in captain.ship.cargo.keys():
        if captain.ship.cargo[key]['type']:
            pods += 1
            overall += captain.ship.cargo[key]['value']

    window['-IN-BD-BALANCE-'].update(captain.balance)
    window['-IN-BD-CARGO-'].update('/'.join([str(pods), str(tpods)]))
    window['-IN-BD-VALUE-'].update(int(overall))


def update_gui():
    """ update all GUI elements """
    update_affiche(captain)
    update_affiche(captain.location)

    capacity = int(captain.ship.model['fuel'] * MAXP)
    if captain.ship.reservoir < capacity:
        window['-REFUEL-'].update(disabled=False)
    else:
        window['-REFUEL-'].update(disabled=True)

    if captain.destination:
        window['-SETDEST-'].update(disabled=True)
        window['-NEXT-TURN-'].update(disabled=False)
        window['-DEST-TITLE-'].update(value=f'Destination: {captain.destination.name}')
        update_trading(window['-DEST-TABLE-'], captain.destination)
    else:
        window['-SETDEST-'].update(disabled=False)
        # window['-REFUEL-'].update(disabled=False)
        window['-NEXT-TURN-'].update(disabled=True)
        # clear trading tab -DEST-TABLE-
        window['-DEST-TITLE-'].update(value='Destination:')
        update_trading(window['-DEST-TABLE-'])

    window['-LOC-TITLE-'].update(value=f'Current location: {captain.location.name}')
    update_trading(window['-LOC-TABLE-'], captain.location)
    update_cargo_goods(captain.location)
    update_captain_board()


def update_invoice(good_type, qty):
    """ calculate the invoice, update the relevant GUI elements

    return a tuple(good_type, good_price, qty, cargo_value)
    """
    good_price = captain.location.price_slip[good_type][1]
    cargo_value = good_price * qty

    invoice = (good_type, good_price, qty, cargo_value)

    if cargo_value > captain.balance:
        window['-IN-INVOICE-'].update(value=cargo_value, text_color='red')
        window['-BUY-CARGO-'].update(disabled=True)
    else:
        window['-IN-INVOICE-'].update(value=cargo_value)
        window['-BUY-CARGO-'].update(disabled=False)

    return invoice


def update_profit(planet):
    """ update profit GUI element """
    if planet is None:
        window['-PROFIT-TABLE-'].update(values=[[0]])
    else:
        valeurs = core.calculate_profit_pod(captain.location, planet)
        window['-PROFIT-TABLE-'].update(values=valeurs)


def update_trading(element, planet=None):
    """ update price slip in the Trading tab tables """
    if planet is None:
        element.update(values=[['None', 0, 0, 0]])
    else:
        price_list = core.slip_list(planet.price_slip)
        element.update(values=price_list)


if __name__ == '__main__':
    # Event Loop
    while True:
        event, values = window.read()
        # debug:
        print(event, values)

        if event == sg.WIN_CLOSED or event == 'Exit':
            break

        elif event == 'New':
            new_game()

        elif event == 'Load':
            load_file()

        elif event == 'Save_as':
            # TODO: SaveAs vs 'Save to existing'
            # if not fname -> Save_as
            # else save in fname
            save_as()

        elif event == '-GRAPH-':
            if not univers:
                sg.popup_error('No game loaded!')
            else:
                on_click(values['-GRAPH-'])

        elif event == '-HOMEWORLD-':
            if not univers:
                sg.popup_error('No game loaded!')
            else:
                show_homeworld()

        elif event == '-LOCATION-':
            if not univers:
                sg.popup_error('No game loaded!')
            else:
                show_location()

        elif event == '-DESTINATION-':
            if not univers:
                sg.popup_error('No game loaded!')
            else:
                show_destination()

        elif event == '-SETDEST-':
            if not univers:
                sg.popup_error('No game loaded!')
            else:
                set_destination()

        elif event == '-REFUEL-':
            if not univers:
                sg.popup_error('No game loaded!')
            else:
                refuel()

        elif event == '-NEXT-TURN-':
            if not univers:
                sg.popup_error('No game loaded!')
            else:
                next_turn()

        elif event == '-IN-GOODS-':
            update_cargo_qty(values['-IN-GOODS-'])

        elif event == '-IN-QTY-':
            if values['-IN-QTY-'] is None:
                window['-BUY-CARGO-'].update(disabled=True)
            else:
                invoice = update_invoice(values['-IN-GOODS-'], values['-IN-QTY-'])

        elif event == '-BUY-CARGO-':
            buy_cargo(invoice)

        elif event == 'About':
            sg.popup(msg_overview)

    window.close()
