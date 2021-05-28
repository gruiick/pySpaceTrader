#!/usr/bin/env python3
# coding: utf-8
#
# $Id: sg_mockup03.py 1550 $
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
COLORS = constants.COLORS

overview = ' '.join(constants.OVERVIEW)
msg_overview = '\n'.join(['pySpaceTrader', constants.VERSION, overview])

univers = []            # global container for game objects
target = []             # items composing the 'target'
limite = []             # item composing the limit circle
clicked_position = ()   # keep temporary click position global

######################
## define GUI Elements

# Theme
sg.theme('Default1')

# Menu
menu_layout = [['&Game',
                ['&New',
                 '&Load',
                 '&Save_as',
                 'E&xit']],
                ['Help',
                 '&About'],]

# Captain layout
captain_layout = sg.Frame(
    layout = [
        [sg.Text('display Captain info',
                 size=(25, 2),
                 key='-IN-CAPTAIN-')],
        [sg.Button('Homeworld',
                   key='-HOMEWORLD-')],
        [sg.Button('Location',
                   key='-LOCATION-')],
        [sg.Button('Destination',
                   key='-DESTINATION-')],
        ], title='Captain',
        element_justification='center')

# info layout
info_layout = sg.Frame(
    layout = [
        [sg.Text('display Planet info',
                 size=(25, 7),
                 key='-IN-PLANET-')],
        ], title='Planet')

# actions layout
action_layout = sg.Frame(
    layout = [
        [sg.Button('Set destination',
                   key='-SETDEST-')],
        [sg.Button('Refuel',
                   key='-REFUEL-')],
        [sg.Button('Next turn',
                   key='-NEXT-TURN-')],
        ], title='Actions',
        size=(25, 3),
        element_justification='center')

# first column's frame
navigation_layout = sg.Frame(
    layout=[
        [captain_layout],
        [info_layout],
        [action_layout],
        ], title='Navigation',
    element_justification='center')

# Galactic Map Tab
tab_galactic_map = [
    [sg.Graph(
        (MAXW, MAXH),
        (0, 0),
        (MAXW, MAXH),
        background_color=COLORS['background'],
        enable_events=True,
        key='-GRAPH-')],
    [sg.StatusBar('detected clic in X=, Y=',
             size=(30,1),
             key='-IN-CLIC-')],
    ]

# trading stuffs, before Tab
numrow = len(GOODS.keys())
location_layout = sg.Frame(
    layout=[[sg.Table(values=[['None', 0, 0, 0]],
                             headings=[' Items ', 'buy (Cr)', 'sell (Cr)', 'stock (Qty)'],
                             auto_size_columns=True,
                             display_row_numbers=False,
                             num_rows=numrow,
                             justification='center',
                             hide_vertical_scroll=True,
                             selected_row_colors=(COLORS['default'], 'white'),
                             key='-LOC-TABLE-',
                   )]],
    title='Current location:',
    key='-LOC-TITLE-',
    title_location=sg.TITLE_LOCATION_TOP_LEFT)

destination_layout = sg.Frame(
    layout=[[sg.Table(values=[['None', 0, 0, 0]],
                             headings=[' Items ', 'buy (Cr)', 'sell (Cr)', 'stock (Qty)'],
                             auto_size_columns=True,
                             display_row_numbers=False,
                             num_rows=numrow,
                             justification='center',
                             hide_vertical_scroll=True,
                             selected_row_colors=(COLORS['default'], 'white'),
                             key='-DEST-TABLE-',
                   )]],
    title='Destination:',
    key='-DEST-TITLE-',
    title_location=sg.TITLE_LOCATION_TOP_LEFT)

profit_layout = sg.Frame(
    layout=[[sg.Table(values=[[0]],
                      headings=['profit'],
                      auto_size_columns=True,
                      display_row_numbers=False,
                      num_rows=numrow,
                      justification='center',
                      hide_vertical_scroll=True,
                      selected_row_colors=(COLORS['default'], 'white'),
                      key='-PROFIT-TABLE-',
                      )]],
    title=None,)


# Captain Board
board_layout = sg.Frame(
    layout=[
            [sg.Text('Balance:', justification='left'),
            sg.Text('',
                     key='-IN-BD-BALANCE-',
                     size=(20, 1),
                     justification='right',
                     relief='sunken'),
            ],
            [sg.Text('Cargo:', justification='left'),
            sg.Text('',
                     key='-IN-BD-CARGO-',
                     size=(6, 1),
                     justification='right',
                     relief='sunken'),
            ],
            [sg.Text('Value:', justification='left'),
            sg.Text('',
                     key='-IN-BD-VALUE-',
                     size=(20, 1),
                     justification='right',
                     relief='sunken'),
            ],
            [sg.HorizontalSeparator(color=None, pad=(1, 1))],
            [sg.Text('Credit:', justification='left'),
            sg.Text('',
                     key='-IN-BD-CREDIT-',
                     size=(20, 1),
                     justification='right',
                     relief='sunken'),
            ],
            [sg.Text('Interests:', justification='left'),
            sg.Text('',
                     key='-IN-BD-INTERESTS-',
                     size=(20, 1),
                     justification='right',
                     relief='sunken'),
            ],
    ],
    title='Captain board',
    #size=(25, 15),
    element_justification='right')

cargo_layout = sg.Frame(
    layout=[[sg.Text('Goods:'),
             sg.Combo(values=[None],
                     default_value=None,
                     readonly=True,
                     enable_events=True,
                     key='-IN-GOODS-',
                     )],
            [sg.Text('Quantity:'),
             # ça devrait plutot être un sg.Spin
             # de 0 à max(avail.pods)|max(good[-1])
             sg.Combo(values=[None],
             default_value=None,
             readonly=True,
             enable_events=True,
             key='-IN-QTY-',
             )],
             [sg.Button('buy cargo',
                   key='-BUY-CARGO-',
                   disabled=True)],
             ],
    title='Cargo',)



# trading, 2 columns top + 2 columns bottom
trading_loc_col = sg.Column([[location_layout]],
                             justification='left',
                             element_justification='left',
                             vertical_alignment='top')

trading_profit_col = sg.Column([[profit_layout]],
                               justification='center',
                               element_justification='center',
                               vertical_alignment='bottom')

trading_dest_col = sg.Column([[destination_layout]],
                             justification='right',
                             element_justification='right',
                             vertical_alignment='top')

trading_cargo_col = sg.Column([[cargo_layout]],
                             justification='left',
                             element_justification='left',
                             vertical_alignment='top')

trading_board_col = sg.Column([[board_layout]],
                             justification='right',
                             element_justification='right',
                             vertical_alignment='top')

tab_trading = [
    [trading_loc_col,
     #sg.VerticalSeparator(color='red', pad=(1, 1)),
     trading_profit_col,
     trading_dest_col],

    [sg.HorizontalSeparator(color='red', pad=(1, 1))],

    [trading_cargo_col,
     sg.VerticalSeparator(color='red', pad=(1, 1)),
     trading_board_col],
    ]

tab_bank = [[sg.Text('Not yet implemented')]]

tab_shipyard = [[sg.Text('Not yet implemented')]]

tab_news = [[sg.Text('Not yet implemented')]]

# Main, two columns
main_left_col = sg.Column([[navigation_layout]],
                        justification='left',
                        element_justification='left',
                        vertical_alignment='top')

main_right_col = sg.Column(
    [[sg.TabGroup([
        [sg.Tab('Galactic Map', tab_galactic_map),
         sg.Tab('Trading', tab_trading),
         sg.Tab('Bank', tab_bank),
         sg.Tab('Shipyard', tab_shipyard),
         sg.Tab('News', tab_news),
        ]],
    )]],
    justification='right',
    element_justification='right',
    vertical_alignment='top')

# final layout assembly
final_layout = [[sg.Menu(menu_layout, tearoff=True)],
          [main_left_col, main_right_col],]

# create window
window = sg.Window('mockup03',
                   final_layout,
                   auto_size_buttons=False,
                   resizable=True)

# simplify call for map objects
graph = window['-GRAPH-']

############
## Functions

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


def new_game():
    """ new game """
    global univers, planetes, captain
    # create universe
    univers = cli_01.create_universe()
    # set planets apart
    planetes = [x for x in univers if isinstance(x, cli_01.Planet)]
    # pprint(planetes)
    # set Captain apart too
    toto = [x for x in univers if isinstance(x, cli_01.Captain)]
    captain = toto[0]
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
        if cli_01.collision(position, planete):
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
            update_board()
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
    if isinstance(objet, cli_01.Planet):
        description = ''.join([objet.name,
                               ' : ',
                               str(objet.position),
                               '\n',
                               '\n'.join(objet.gov)])
        window['-IN-PLANET-'].update(description)

    elif isinstance(objet, cli_01.Captain):
        description = ''.join([objet.name,
                               ' from ',
                               objet.homeworld.name,
                               '\n',
                               str(objet.balance)])
        window['-IN-CAPTAIN-'].update(description)


def update_cargo_goods(planet):
    """ update values in combo's goods Cargo frame """
    _key_list = []

    for key, value in planet.price_slip.items():
        # if no stock, don't bother adding to picklist
        if value[-1] != 0:
            _key_list.append(key)

    window['-IN-GOODS-'].update(values=_key_list)


def update_cargo_qty(good):
    """ update picklist in combo's quantity Cargo frame """
    # FIXME: total_pods -> avail_pods
    total_pods = captain.ship.model['cargo']
    _qty_max = captain.location.price_slip[good][-1]
    # _value_list = []
    if _qty_max < total_pods:
        _value_list = list(range(1, _qty_max + 1))
    else:
        _value_list = list(range(1, total_pods + 1))

    window['-IN-QTY-'].update(values=_value_list)


def update_board():
    """ update Captain board informations """
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
    """ update all GUI """
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
    update_board()


def update_profit(planet):
    """ update profit element """
    if planet is None:
        window['-PROFIT-TABLE-'].update(values=[[0]])
    else:
        valeurs = cli_01.calculate_profit_pod(captain.location, planet)
        print(valeurs)
        window['-PROFIT-TABLE-'].update(values=valeurs)


def update_trading(element, planet=None):
    """ update price slip in the Trading tab tables """
    if planet is None:
        element.update(values=[['None', 0, 0, 0]])
    else:
        price_list = cli_01.slip_list(planet.price_slip)
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
            if values['-IN-QTY-'] is None :
                window['-BUY-CARGO-'].update(disabled=True)
            else:
                window['-BUY-CARGO-'].update(disabled=False)

        elif event == 'About':
            sg.popup(msg_overview)

    window.close()
