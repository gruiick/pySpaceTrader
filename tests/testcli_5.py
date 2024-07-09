#!/usr/bin/env python3
# coding: utf-8
#
# $Id: testcli_3.py 1303.v0.2-dev.1 $
# SPDX-License-Identifier: BSD-2-Clause

"""
some tests
"""

# from dataclasses import dataclass
import random
from pprint import pprint
from itertools import groupby

import constants
import core


"""
ship: {
'model': {'model': 'wasp',
          'cargo': 35,
          'weapon': 3,
          'shield': 2,
          'shieldstrengh': 2,
          'gadget': 3,
          'crew': 7,
          'efficiency': 0.93,  # float: {:.2f}
          'hull': 300000,
          'tribbles': False,
          'price': hull * efficiency  # float: {:.2f}
          },
        }

[['model: mosquito'],
 ['cargo: 15'],
 ['weapon: 2'],
 ['shield: 1'],
 ['shieldstrengh: 1'],
 ['gadget: 1'],
 ['crew: 5'],
 ['efficiency: 0.86'],  # float: {:.2f}
 ['hull: 30000'],
 ['tribbles: False']
 ['price': 25800]  # float: {:.2f}
 ]
"""



if __name__ == '__main__':
    """ """

    planete = core.Planet(
        name=random.choice(constants.NAMES),
        x=random.randint(constants.XMIN, constants.MAXWIDTH - 1),
        y=random.randint(constants.YMIN, constants.MAXHEIGHT - 1),
        system_size=random.choice(list(constants.SYSTEMSIZE.keys())),
        tech_level=random.choice(list(constants.TECHLEVEL.keys())),
        regim=random.choice(list(constants.REGIM.keys())),
        special=random.choice(list(constants.SPECIALRESOURCES.keys())),
        status='nopressure',
        price_slip={},
        shipyard=[])

    planete.shipyard = core.populate_shipyard()

    pprint(planete)
    for item in planete.shipyard:
        # pprint(item.__dict__)
        print(item['model']['model'])
        pprint(item.display())
