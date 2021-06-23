#!/usr/bin/env python3
# coding: utf-8
#
# $Id: sgui.py 1566.v0.2-dev.1 $
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

# Common UI

# Captain layout
captain_layout = sg.Frame(
    layout=[[sg.Text('display Captain info',
                     size=(20, 1),
                     justification='left',
                     key='-IN-CAPTAIN-',
                     ),
            ],
            [sg.Text('Cash (Cr):',
                     size=(12, 1),
                     justification='left'),
            sg.Text('',
                    key='-IN-BD-CASH-',
                    size=(16, 1),
                    justification='right',
                    relief='sunken'),
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
    layout=[
        # [sg.Button('Set destination',
        #               key='-SETDEST-',
        #               disabled=True)],
        [sg.Button('Refuel',
                   key='-REFUEL-')],
        [sg.Button('Next turn',
                   key='-NEXT-TURN-')],
        ],
        title='Actions',
        # size=(25, 3),
        vertical_alignment='center',
        element_justification='center')

btn_column = sg.Column([[location_btn, action_btn]],
                            justification='left',
                            element_justification='left',
                            vertical_alignment='top')

# info layout
info_layout = sg.Frame(
    layout=[
        [sg.Text('display Planet info',
                     size=(25, 7),
                     key='-IN-PLANET-')],
        [sg.Text('',
                 size=(25, 1),
                 key='-IN-DSTCE-')],
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

# Trading tab layouts
numrow = len(GOODS.keys())

location_layout = sg.Frame(
    layout=[[sg.Table(values=[['None', 0, 0, 0]],
                      headings=[' Items ', 'buy (Cr)', 'sell (Cr)', 'stock (Qty)'],
                      auto_size_columns=True,
                      col_widths=[15, 15, 15, 15],
                      display_row_numbers=False,
                      num_rows=numrow,
                      justification='right',
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
                      col_widths=[15],
                      display_row_numbers=False,
                      num_rows=numrow,
                      justification='right',
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
                      col_widths=[15, 15, 15, 15],
                      display_row_numbers=False,
                      num_rows=numrow,
                      justification='right',
                      hide_vertical_scroll=True,
                      selected_row_colors=(COLORS['default'], 'white'),
                      key='-DEST-TABLE-',
                      ),
    ]],
    title='Destination:',
    key='-DEST-TITLE-',
    title_location=sg.TITLE_LOCATION_TOP_LEFT)

# combo list of planets within ship range
planet_selector = sg.Frame(
    layout=[[sg.Combo(values=[None],
                      default_value=None,
                      size=(13, 1),
                      readonly=True,
                      enable_events=True,
                      key='-IN-PLNT-SELECTOR-',
                      )]
    ],
    title='Nearest(s) planet(s)',
    title_location=sg.TITLE_LOCATION_TOP_LEFT)

# Cargo Board
cargo_manifest = sg.Column(
    [
        [sg.Text('[pod n°][type][value (Cr)]',
                 # size=(20, 1),
                 justification='right'), ],
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
    ],
    justification='left',
    element_justification='center',
    vertical_alignment='top',
    )

cargo_btns = sg.Column(
    [
        [sg.Text('Pod(s):',
                 justification='left'),
         sg.Text('',
                key='-IN-BD-CARGO-',
                size=(5, 1),
                justification='right',
                relief='sunken'),
        ],
        [sg.Button('Sell',
                   key='-SELL-')],
        [sg.Button('Sell All',
                   key='-SELL-ALL-')],
        [sg.Button('Dump',
                   key='-DUMP-')],
    ],
    justification='right',
    element_justification='center',
    vertical_alignment='center',
    )

cargo_layout = sg.Frame(
    layout=[
               # [sg.HorizontalSeparator(color='red', pad=(1, 1))],
               [cargo_manifest,
               # sg.VerticalSeparator(color='red', pad=(1, 1)),
               cargo_btns],
               # [sg.HorizontalSeparator(color='red', pad=(1, 1))],
               [sg.Text('Cargo Value (Cr):',
                        justification='left'),
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
             [sg.Button('Buy',
                        key='-BUY-CARGO-',
                        disabled=True)
             ],
    ],
    title='Docks',
    element_justification='right')

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

trading_board_col = sg.Column([[planet_selector],
                               [docks_layout],
                               ],
                             justification='right',
                             element_justification='right',
                             vertical_alignment='top')

tab_trading = [
    [trading_board_col,
     # sg.VerticalSeparator(color='red', pad=(1, 1)),
     trading_cargo_col],

    # [sg.HorizontalSeparator(color='red', pad=(1, 1))],

    [trading_loc_col,
     trading_profit_col,
     trading_dest_col],
    ]

# Bank tab layouts
bank_table = sg.Frame(
    layout=[[sg.Table(values=[['None', 0, 0, '', 0]],
                      headings=[' Items ', 'Value (Cr)', 'Quantity', '+/-', 'Total (Cr)'],
                      auto_size_columns=True,
                      col_widths=[15, 15, 15, 3, 15],
                      display_row_numbers=False,
                      # num_rows=numrow,
                      justification='right',
                      hide_vertical_scroll=False,
                      selected_row_colors=(COLORS['default'], 'white'),
                      key='-BANK-TABLE-',
                      ),
    ]],
    title='Invoice log',
    title_location=sg.TITLE_LOCATION_TOP_LEFT)

loan_board = sg.Frame(
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
    title='Loan board',
    # size=(25, 15),
    element_justification='left')

# tab_bank = [[sg.Text('Not yet implemented')]]
tab_bank = [[bank_table],
            [loan_board]]

# Shipyard tab layouts
# FIXME gadgets, weapons, shields and crew will be lists -> "ship details msg box"?
captain_ship = sg.Frame(
    layout=[[sg.Text('Pods:',
                     justification='left'),
             sg.Text('',
                     key='-CPTN-SHIP-PODS-',
                     size=(6, 1),
                     justification='right',
                     relief='sunken'),
             ],
            [
             sg.Text('Weapons:',
                     justification='left'),
             sg.Text('',
                     key='-CPTN-SHIP-WPNS-',
                     size=(6, 1),
                     justification='right',
                     relief='sunken'),
            ],
            [sg.Text('Shields:',
                     justification='left'),
             sg.Text('',
                     key='-CPTN-SHIP-SHLDS-',
                     size=(6, 1),
                     justification='right',
                     relief='sunken'),
            ],
            [sg.Text('Gadgets:',
                     justification='left'),
             sg.Text('',
                     key='-CPTN-SHIP-GDGT-',
                     size=(6, 1),
                     justification='right',
                     relief='sunken'),
            ],
            [sg.Text('Crew:',
                     justification='left'),
             sg.Text('',
                     key='-CPTN-SHIP-CREW-',
                     size=(6, 1),
                     justification='right',
                     relief='sunken'),
            ],
            [sg.Text('Hull:',
                     justification='left'),
             sg.Text('',
                     key='-CPTN-SHIP-HULL-',
                     size=(6, 1),
                     justification='right',
                     relief='sunken'),
            ],
    ],
    title='Ship:',
    key='-CPTN-SHIP-MODEL-',
    element_justification='right',
    )

# Weapons block
weapons_clmn = sg.Column([
    [sg.Text('Weapons:',
             justification='left')],
    [sg.Text('Pulse laser',
             size=(14, 1),
             justification='left',
             relief='sunken')],
    [sg.Text('Beam laser',
             size=(14, 1),
            justification='left',
            relief='sunken')],
    [sg.Text('Military laser',
             size=(14, 1),
            justification='left',
            relief='sunken')]],
    justification='right',
    # element_justification='right',
    vertical_alignment='top')

# Shields block
shield_clmn = sg.Column([
    [sg.Text('Shields:',
             justification='left')],
    [sg.Text('Energy shield',
             size=(16, 1),
            justification='left',
            relief='sunken')],
    [sg.Text('Reflective shield',
             size=(16, 1),
             justification='left',
             relief='sunken')],
    ],
    justification='left',
    # element_justification='left',
    vertical_alignment='top')

# Gadgets block
gadget_clmn = sg.Column([
    [sg.Text('Gadgets:',
             justification='left')],
    [sg.Text('Auto-Repair System',
             size=(18, 1),
             justification='left',
             relief='sunken')],
    [sg.Text('Navigating System',
             size=(18, 1),
             justification='left',
             relief='sunken')],
    [sg.Text('Targeting System',
             size=(18, 1),
             justification='left',
             relief='sunken')],
    [sg.Text('Cloaking System',
             size=(18, 1),
             justification='left',
             relief='sunken')],
    [sg.Text('Escape Pod',
             size=(18, 1),
             justification='left',
             relief='sunken')],
    ],
    justification='right',
    # element_justification='right',
    vertical_alignment='top')

# Equipement Store
equipement_store = sg.Frame(
    layout=[[gadget_clmn,
            weapons_clmn,
            shield_clmn],

            [sg.Text('Extra Cargo Pod(s):',
                     justification='left'),
             sg.Slider(range=(1, 5),
                       default_value=1,
                       resolution=1,
                       orientation='horizontal',
                       disable_number_display=True,
                       relief='sunken',
                       enable_events=True,
                       #size=(5,1),
                       ),
            ],
    ],
    title='Equipements: Not yet implemented',
    element_justification='right',
    )

shipyard = sg.Frame(
    layout=[[sg.Table(values=[['None', 0, 0, 0, 0, 0, 0, 0, 0, None, 0]],
                      headings=['Model',
                                'Pod(s)',
                                'Weapon(s)',
                                'Shield(s)',
                                'Shield strengh',
                                'Gadget',
                                'Crew quarter(s)',
                                'Efficiency',
                                'Hull',
                                'Tribbles',
                                'Price (Cr)'],
                      auto_size_columns=True,
                      col_widths=[15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15],
                      display_row_numbers=False,
                      num_rows=numrow,
                      justification='right',
                      hide_vertical_scroll=True,
                      enable_events=True,
                      selected_row_colors=(COLORS['default'], 'white'),
                      key='-SHIP-TABLE-',
                      ), ],
            [sg.Button('Buy',
                       key='-BUY-SHIP-',
                       disabled=True)]
    ],
    title='',
    element_justification='center',
    )

# tab_shipyard
tab_shipyard = [[captain_ship, equipement_store],
                [shipyard]]


# News tab layouts
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
