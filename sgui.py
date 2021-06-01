#!/usr/bin/env python3
# coding: utf-8
#
# $Id: sgui.py 1560 $
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
                     size=(25, 1),
                     key='-IN-CAPTAIN-',
                     ),
            ],
            [sg.Text('Balance: ',
                     size=(25, 1),
                     key='-IN-BALANCE-',
                     justification='left',
                     ),
            ],
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
    layout=[[sg.Text('display Planet info',
                     size=(25, 7),
                     key='-IN-PLANET-')],
        ], title='Planet')

# actions layout
action_layout = sg.Frame(
    layout=[[sg.Button('Set destination',
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

# Cargo Board
cargo_layout = sg.Frame(
    layout=[[sg.Text('Cash (Cr):',
                     justification='left'),
               sg.Text('',
                       key='-IN-BD-CASH-',
                       size=(20, 1),
                       justification='right',
                       relief='sunken'),
               sg.Text('Pod(s):',
                       justification='left'),
               sg.Text('',
                       key='-IN-BD-CARGO-',
                       size=(6, 1),
                       justification='right',
                       relief='sunken'),
               ],
               # TODO something with all pods, good type & value
               [sg.Text('[pod][type][value (Cr)]',
                        # size=(20, 1),
                        justification='right'),],
                [sg.Listbox(values=[],
                           default_values=None,
                           size=(20, 10),
                           no_scrollbar=True,
                           auto_size_text=True,
                           select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE,
                           enable_events=True,
                           key='-MANIFEST-',
                           ),
               # TODO: size should be (20, total_pods)
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
    element_justification='right')

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
                     size=(6, 1),
                     justification='right',
                     relief='sunken'),
             ],
             [sg.Button('Buy',
                        key='-BUY-CARGO-',
                        disabled=True)],
    ],
    title='Docks',)


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

trading_cargo_col = sg.Column([[docks_layout]],
                             justification='left',
                             element_justification='left',
                             vertical_alignment='top')

trading_board_col = sg.Column([[cargo_layout]],
                             justification='right',
                             element_justification='right',
                             vertical_alignment='top')

tab_trading = [
    [trading_loc_col,
     # sg.VerticalSeparator(color='red', pad=(1, 1)),
     trading_profit_col,
     trading_dest_col],

    [sg.HorizontalSeparator(color='red', pad=(1, 1))],

    [trading_cargo_col,
     sg.VerticalSeparator(color='red', pad=(1, 1)),
     trading_board_col],
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
