#!/usr/bin/env python3
# coding: utf-8
#
# $Id: main.py 1570 $
# SPDX-License-Identifier: BSD-2-Clause

"""
même GUI que tk_mockup02, mais avec PySimpleGUI
python3 >= 3.7

"""

import PySimpleGUI as sg

import constants
import core
import sgui

# from pprint import pprint

# Globals
MAXW = constants.MAXWIDTH
MAXH = constants.MAXHEIGHT
MAXP = constants.MAXPARSEC
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

    # unpack incoming invoice
    good_type = facture.good_type
    good_price = facture.good_price
    qty = facture.quantity
    cargo_value = facture.total_value

    # TODO if cargo_value is > captain.cash, propose a loan
    # and start computing interests (bank account)

    _none_cargo = [x for x in captain.ship.cargo.keys() if captain.ship.cargo[x]['type'] is None]
    available_cargo = len(_none_cargo)
    # print(f'pod(s): {_none_cargo}')
    # print(f'avail: {available_cargo}')

    if qty > available_cargo:
        sg.popup_error(f'Cannot buy, not enought cargo space!')
    else:
        for index in range(_none_cargo[0], _none_cargo[0] + qty):
            captain.ship.cargo[index]['type'] = good_type
            captain.ship.cargo[index]['value'] = good_price
            available_cargo -= 1
            captain.location.price_slip[good_type][2] -= 1
        captain.cash -= cargo_value
        update_trading(window['-LOC-TABLE-'], captain.location)
        update_cargo_board()
        update_docks_board(captain.location)

    # TODO log invoice into bank account


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
    """ compute next turn """
    try:
        distance = core.get_distance(captain.location.position, captain.destination.position)

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
            # update gui
            draw_map(rayon=rayon)
            update_gui()

    # if there is no destination set ->AttributeError
    except AttributeError:
        sg.popup(f'Set a destination first.')


def on_click(position):
    """ redraw graph with new clicked position """
    global clicked_position
    for planete in planetes:
        #if core.collision(position, planete):
        if core.inside_circle(position, planete.position, radius=5):
            position = planete.position
            clicked_position = planete
            update_affiche(planete)
            draw_target(position)

    x, y = position
    window['-IN-CLIC-'].update(value=f'Detected clic in X={x}, Y={y}')


def refuel():
    """ refuel the captain.ship according to captain.cash,
    captain.ship.reservoir and planete.fuel_price
    """
    capacity = int(captain.ship.model['fuel'] * MAXP)
    quantity = captain.location.price_slip['fuel'][2]
    fuel_price = captain.location.price_slip['fuel'][1]
    reserve = captain.ship.reservoir

    if reserve < capacity:
        fuel_deficit = capacity - reserve

        if fuel_deficit > quantity:
            fuel_deficit = quantity

        fuel_invoice = fuel_deficit * fuel_price
        print(f'fuel: {fuel_deficit}T')
        print(f'fuel price: {fuel_invoice} Cr')

        if fuel_invoice <= captain.cash:
            captain.cash = captain.cash - fuel_invoice
            _refuel = reserve + fuel_deficit
            captain.ship.reservoir = _refuel
            rayon = _refuel
            captain.location.price_slip['fuel'][2] -= fuel_deficit
            draw_limite(captain.location.position, rayon)
            update_trading(window['-LOC-TABLE-'], captain.location)
            update_affiche(captain)
            update_cargo_board()
            window['-REFUEL-'].update(disabled=True)

        else:
            # FIXME/TODO: how much can I buy?
            # and buy only that much or else 'not enought Cr'
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


def sell_cargo(pods, dump=False):
    """ sell (or dump) good from list of pods """

    # TODO use Transaction(), but separate by good_type to log
    # into bankaccount
    for elements in pods:
        _index, _good_type, _good_value = elements

        captain.location.price_slip[_good_type][2] += 1
        # TODO update planet(prices)
        captain.ship.cargo[_index]['type'] = None
        captain.ship.cargo[_index]['value'] = None

        if not dump:
            captain.cash += captain.location.price_slip[_good_type][0]

    update_trading(window['-LOC-TABLE-'], captain.location)
    update_cargo_board()
    update_affiche(captain)


def set_map_destination():
    """ save clicked position into captain.destination """
    global captain, clicked_position
    try:
        distance = core.get_distance(captain.location.position, clicked_position.position)

        if distance == 0:
            sg.popup(f'Cannot set destination: Same as current location.')

        elif distance < captain.ship.reservoir:
            captain.destination = clicked_position
            # update Trading tab
            window['-IN-PLNT-SELECTOR-'].update(value=captain.destination.name)
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


def set_trade_destination(planet):
    """ save trade destination into captain.destination """
    captain.destination = planet
    window['-DEST-TITLE-'].update(value=f'Destination: {captain.destination.name}')
    update_trading(window['-DEST-TABLE-'], captain.destination)
    update_profit(captain.destination)
    window['-NEXT-TURN-'].update(disabled=False)


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
        _description = ''.join([objet.name,
                               ' : ',
                               str(objet.position),
                               '\n',
                               '\n'.join(objet.gov)])
        window['-IN-PLANET-'].update(_description)

    elif isinstance(objet, core.Captain):
        _description = ''.join([objet.name,
                               ' from ',
                               objet.homeworld.name,
                               ])
        window['-IN-CAPTAIN-'].update(_description)
        _balance = objet.balance
        window['-IN-BALANCE-'].update(value=f'{_balance}')
        _reserve = objet.ship.reservoir
        window['-IN-RESERVE-'].update(value=f'{_reserve}')


def update_buy_goods(planet):
    """ update values in combo's goods Cargo frame """
    _key_list = []

    for key, value in planet.price_slip.items():
        # if no stock, don't bother adding to picklist
        if value[2] != 0:
            _key_list.append(key)

    window['-IN-GOODS-'].update(values=_key_list)


def update_buy_qty(good=None):
    """ update picklist in combo's quantity Cargo frame """
    # FIXME: clear=False, instead of good=None
    # redo this algo
    _none_cargo = [x for x in captain.ship.cargo.keys() if captain.ship.cargo[x]['type'] is None]
    avail_pods = len(_none_cargo)

    if good is not None:
        _qty_max = captain.location.price_slip[good][2]
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


def update_cargo_board():
    """ update Cargo board informations GUI element """
    pods = 0
    tbl_pod = []
    total_pods = len(captain.ship.cargo)
    total_value = 0
    for key in captain.ship.cargo.keys():
        if captain.ship.cargo[key]['type']:
            pods += 1
            total_value += captain.ship.cargo[key]['value']
            tbl_pod.append([key,
                            captain.ship.cargo[key]['type'],
                            captain.ship.cargo[key]['value']])

    window['-IN-BD-CASH-'].update(captain.cash)
    window['-IN-BD-CARGO-'].update('/'.join([str(pods),
                                             str(total_pods)]))
    window['-IN-BD-VALUE-'].update(int(total_value))
    window['-MANIFEST-'].update(values=tbl_pod)

    if pods == total_pods:
        window['-BUY-CARGO-'].update(disabled=True)


def update_docks_board(planet):
    """ clear values in Docks frame's elements """
    update_buy_goods(planet)
    update_buy_qty(good=None)
    window['-IN-INVOICE-'].update(value='')


def update_gui():
    """ update all GUI elements """

    update_affiche(captain)
    update_affiche(captain.location)

    capacity = int(captain.ship.model['fuel'] * MAXP)
    if captain.ship.reservoir < capacity:
        window['-REFUEL-'].update(disabled=False)
    else:
        window['-REFUEL-'].update(disabled=True)

    selectable_planets = update_planet_selector()
    if selectable_planets:
        lst_selectable_names = []
        for planete in selectable_planets:
            lst_selectable_names.append(planete.name)

        window['-IN-PLNT-SELECTOR-'].update(values=lst_selectable_names)

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
        update_profit()

    window['-LOC-TITLE-'].update(value=f'Current location: {captain.location.name}')
    update_trading(window['-LOC-TABLE-'], captain.location)
    update_buy_goods(captain.location)
    update_cargo_board()


def update_invoice(good_type, qty):
    """ calculate the invoice, update the relevant GUI elements

    return a core.Transaction() object
    """
    good_price = captain.location.price_slip[good_type][1]
    # cargo_value = good_price * qty
    invoice = core.Transaction(good_type, good_price, qty)
    cargo_value = invoice.total_value

    if cargo_value > captain.cash:
        window['-IN-INVOICE-'].update(value=cargo_value, text_color='red')
        window['-BUY-CARGO-'].update(disabled=True)
    else:
        window['-IN-INVOICE-'].update(value=cargo_value, text_color='black')
        window['-BUY-CARGO-'].update(disabled=False)

    print(f'{invoice}')
    return invoice


def update_planet_selector():
    """ update the planet combo selector """
    # do NOT add captain.location.position to the list

    _nearest_planets = []
    for planete in planetes:
        if core.inside_circle(planete.position, captain.location.position, radius=captain.ship.reservoir):
            if planete is not captain.location:
                _nearest_planets.append(planete)

    return _nearest_planets


def update_profit(planet=None):
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
                sg.popup_error(f'No game loaded!')
            else:
                on_click(values['-GRAPH-'])

        elif event == '-HOMEWORLD-':
            if not univers:
                sg.popup_error(f'No game loaded!')
            else:
                show_homeworld()

        elif event == '-LOCATION-':
            if not univers:
                sg.popup_error(f'No game loaded!')
            else:
                show_location()

        elif event == '-DESTINATION-':
            if not univers:
                sg.popup_error(f'No game loaded!')
            else:
                show_destination()

        elif event == '-SETDEST-':
            if not univers:
                sg.popup_error(f'No game loaded!')
            else:
                set_map_destination()

        elif event == '-IN-PLNT-SELECTOR-':
            name_planet = values['-IN-PLNT-SELECTOR-']
            for planete in planetes:
                if name_planet == planete.name:
                    set_trade_destination(planete)

        elif event == '-REFUEL-':
            if not univers:
                sg.popup_error(f'No game loaded!')
            else:
                refuel()

        elif event == '-NEXT-TURN-':
            if not univers:
                sg.popup_error(f'No game loaded!')
            else:
                next_turn()

        elif event == '-IN-GOODS-':
            update_buy_qty(values['-IN-GOODS-'])
            window['-IN-INVOICE-'].update(value='', text_color='black')

        elif event == '-IN-QTY-':
            if values['-IN-QTY-'] is None:
                window['-BUY-CARGO-'].update(disabled=True)
            else:
                invoice = update_invoice(values['-IN-GOODS-'], values['-IN-QTY-'])

        elif event == '-BUY-CARGO-':
            buy_cargo(invoice)

        elif event == '-SELL-':
            sell_cargo(values['-MANIFEST-'])

        elif event == '-DUMP-':
            sell_cargo(values['-MANIFEST-'], dump=True)

        elif event == 'About':
            sg.popup(f'{msg_overview}')

    window.close()
