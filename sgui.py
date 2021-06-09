#!/usr/bin/env python3
# coding: utf-8
#
# $Id: sgui.py 1565 $
# SPDX-License-Identifier: BSD-2-Clause

"""
PySimpleGUI layout for pySpaceTrader
"""

import PySimpleGUI as sg

import constants

# Globals
MAXW = constants.MAXWIDTH
MAXH = constants.MAXHEIGHT
MAXP = constants.MAXPARSEC
GOODS = constants.GOODS
COLORS = constants.COLORS

# GUI Elements

# Theme
sg.theme('Default1')

# Menu
menu_layout = [['&Game',
                ['&New',
                 '&Load',
                 '&Save_as',
                 'E&xit']],
                ['Help',
                 '&About'],
                ]

# Captain layout
captain_layout = sg.Frame(
    layout=[[sg.Text('display Captain info',
                     size=(20, 1),
                     justification='left',
                     key='-IN-CAPTAIN-',
                     ),
            ],
            [sg.Text('Balance (Cr): ',
                     size=(12, 1),
                     justification='left',
                     ),
             sg.Text('',
                    key='-IN-BALANCE-',
                    size=(16, 1),
                    justification='right',
                    relief='sunken'),
            ],
            [sg.Text('Fuel (T): ',
                     size=(12, 1),
                     justification='left',
                     ),
             sg.Text('',
                    key='-IN-RESERVE-',
                    size=(16, 1),
                    justification='right',
                    relief='sunken'),
            ],
        ], title='Captain',
        element_justification='center')

# location btn
location_btn = sg.Frame(
    layout=[[sg.Button('Homeworld',
                   key='-HOMEWORLD-')],
        [sg.Button('Location',
                   key='-LOCATION-')],
        [sg.Button('Destination',
                   key='-DESTINATION-')],
        ],
        title='Locations',
        element_justification='center')

# action btn
action_btn = sg.Frame(
    layout=[[sg.Button('Set destination',
                       key='-SETDEST-')],
        [sg.Button('Refuel',
                   key='-REFUEL-')],
        [sg.Button('Next turn',
                   key='-NEXT-TURN-')],
        ],
        title='Actions',
        # size=(25, 3),
        element_justification='center')

btn_column = sg.Column([[location_btn, action_btn]],
                            justification='left',
                            element_justification='left',
                            vertical_alignment='top')

# info layout
info_layout = sg.Frame(
    layout=[[sg.Text('display Planet info',
                     size=(25, 7),
                     key='-IN-PLANET-')],
        ], title='Planet')


# first column's frame
navigation_layout = sg.Frame(
    layout=[
        [captain_layout],
        [btn_column],
        [info_layout],
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
             size=(30, 1),
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
                      ),
    ]],
    title='Current location:',
    key='-LOC-TITLE-',
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
                      ),
    ]],
    title=None,)

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
                      ),
    ]],
    title='Destination:',
    key='-DEST-TITLE-',
    title_location=sg.TITLE_LOCATION_TOP_LEFT)

# TODO: destination(s) in range
# combo list of planets within ship range
# same selector as galactic map, for -SETDEST-
planet_selector = sg.Frame(
    layout=[[sg.Combo(values=[None],
                      default_value=None,
                      readonly=True,
                      enable_events=True,
                      key = '-IN-PLNT-SELECTOR-',
                      )]
    ],
    title = 'Nearest(s) planet(s)',
    title_location=sg.TITLE_LOCATION_TOP_LEFT)

# Cargo Board
cargo_layout = sg.Frame(
    layout=[[sg.Text('Cash (Cr):',
                     justification='left'),
               sg.Text('',
                       key='-IN-BD-CASH-',
                       size=(16, 1),
                       justification='right',
                       relief='sunken'),
               sg.Text('Pod(s):',
                       justification='left'),
               sg.Text('',
                       key='-IN-BD-CARGO-',
                       size=(5, 1),
                       justification='right',
                       relief='sunken'),
               ],
               # TODO something with all pods, good type & value
               [sg.Text('[pod n°][type][value (Cr)]',
                        # size=(20, 1),
                        justification='center'),],
                [sg.Listbox(values=[],
                           default_values=None,
                           size=(20, 10),
                           no_scrollbar=False,
                           auto_size_text=True,
                           select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE,
                           enable_events=True,
                           key='-MANIFEST-',
                           ),
                ],
                [sg.Text('Cargo Value (Cr):', justification='left'),
                 sg.Text('',
                         key='-IN-BD-VALUE-',
                         size=(20, 1),
                         justification='right',
                         relief='sunken'),
                 ],
                 # [sg.HorizontalSeparator(color=None, pad=(1, 1))],
    ],
    title='Cargo manifest',
    # size=(25, 15),
    element_justification='left')

docks_layout = sg.Frame(
    layout=[[sg.Text('Goods:',
                     justification='left'),
             sg.Combo(values=[None],
                      default_value=None,
                      readonly=True,
                      enable_events=True,
                      key='-IN-GOODS-',),
             ],
            [sg.Text('Quantity:',
                     justification='left'),
             # ça devrait plutot être un sg.Spin ?
             # de 0 à max(avail.pods)|max(good[-1])
             sg.Combo(values=[None],
                      default_value=None,
                      readonly=True,
                      enable_events=True,
                      key='-IN-QTY-',),
             ],
             [sg.Text('Invoice (Cr):',
                      justification='left'),
             sg.Text('',
                     key='-IN-INVOICE-',
                     size=(16, 1),
                     justification='right',
                     relief='sunken'),
             ],
    ],
    title='Docks',
    element_justification='right')

docks_btn_layout = sg.Frame(
    layout=[[sg.Button('Buy',
                        key='-BUY-CARGO-',
                        disabled=True)],
            [sg.Button('Sell',
                       key='-SELL-')],
            [sg.Button('Dump',
                       key='-DUMP-')],
    ],
    title='Manage cargo:',
    size=(25, 3),
    element_justification='center')


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

trading_board_col = sg.Column([[docks_layout],
                               [docks_btn_layout]],
                             justification='right',
                             element_justification='right',
                             vertical_alignment='top')

tab_trading = [
    [planet_selector, trading_cargo_col,
     sg.VerticalSeparator(color='red', pad=(1, 1)),
     trading_board_col],

    [sg.HorizontalSeparator(color='red', pad=(1, 1))],

    [trading_loc_col,
     trading_profit_col,
     trading_dest_col],
    ]

# Bank layout
bank_board = sg.Frame(
    layout=[[sg.Text('Credit:',
                     justification='left'),
             sg.Text('',
                     key='-IN-BK-CREDIT-',
                     size=(20, 1),
                     justification='right',
                     relief='sunken'),
            ],
            [sg.Text('Interests:',
                      justification='left'),
              sg.Text('',
                      key='-IN-BK-INTERESTS-',
                      size=(20, 1),
                      justification='right',
                      relief='sunken'),
            ],
    ],
    title='Bank board',
    # size=(25, 15),
    element_justification='left')

# tab_bank = [[sg.Text('Not yet implemented')]]
tab_bank = [[sg.Text('Not yet implemented')],
            [bank_board]]

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
                [main_left_col, main_right_col], ]

# window creation take place in main.py
