#!/usr/bin/env python3
# coding: utf-8
#
# $Id: testcli_3.py 1303.v0.2-dev.1 $
# SPDX-License-Identifier: BSD-2-Clause

"""
some tests
"""

from dataclasses import dataclass
from pprint import pprint

import constants
import core

PODS = {0: {'type': 'food', 'value': 109},
        1: {'type': 'food', 'value': 109},
        2: {'type': 'food', 'value': 109},
        3: {'type': 'food', 'value': 109},
        4: {'type': 'food', 'value': 109},
        5: {'type': 'furs', 'value': 264},
        6: {'type': 'furs', 'value': 264},
        7: {'type': 'furs', 'value': 264},
        8: {'type': 'water', 'value': 34},
        9: {'type': 'water', 'value': 34}}

PODS2 = [[0, 'water', 46],
         [1, 'water', 46],
         [2, 'water', 46],
         [3, 'food', 123],
         [4, 'water', 46],
         [5, 'food', 123],
         [6, 'food', 123],
         [7, 'food', 123],
         [8, 'ore', 440],
         [9, 'ore', 440]]


nouvdic = {'food': {'value': 109, 'qty': 5, 'idx': [0, 1, 2, 3, 4]},
          'furs': {'value': 264, 'qty': 3, 'idx': [5, 6, 7]},
          'water': {'value': 34, 'qty': 2, 'idx': [8, 9]},
          }

from itertools import groupby

def key0(item):
    return (item[0], item[2])

def key1(item):
    return (item[1]['type'], item[1]['value'])

def convert(dic):
    iitem = sorted(dic.items(), key=key1)
    for k, group in groupby(iitem, key=key1):
        g = list(group)
        d = dict(g[0][1])
        d.update(qty=len(g), idx=sorted(x[0] for x in g))

        yield d

def sell_cargo(pods):
    """ FIXME use Transaction() """

    # ça marche pour transaction, mais il manque les indices des pods 
    # pour les vidanger...

    a = sorted(pods, key=lambda x: x[1])  # tri sur good_type
    for key, value in groupby(a, lambda x: [x[1], x[2]]):  # tri sur good_type, good_value
        idx = []
        valeurs = list(value)
        pprint(valeurs)
        for items in valeurs:
            idx.append(items[0])
        print(f'key: {key[0]}, {key[1]}, {list(valeurs)}')
        print(f'len: {len(list(valeurs))}')
        print(f'idx: {idx}')
        captain.account.log.append(core.Transaction(key[0], key[1], len(list(valeurs))))


if __name__ == '__main__':
    """ """
    captain = core.Captain()
    captain.ship = core.Ship()
    captain.account = core.BankAccount(captain.name, [])

    invoice = core.Transaction('fuel', 13.00, 2.00)
    inv2 = core.Transaction('fur', 7.00, 3)

    captain.account.log.append(invoice)
    captain.account.log.append(inv2)

    total = []
    for item in captain.account.log:
        total.append(item.total_value)
        print(item.total_value)

    print(f'Total: {sum(total)}')

    #print(list(convert(PODS)))

    sell_cargo(PODS2)

    pprint(captain)
    pprint(captain.account.log)
