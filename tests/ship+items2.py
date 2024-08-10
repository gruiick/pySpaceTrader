#!/usr/bin/env python3
# coding: utf-8
#
# $Id: ship+items2.py 1.develop.8 $
# SPDX-License-Identifier: BSD-2-Clause

""" experimentations around Ship() and Item() """

import random
from dataclasses import dataclass

from pprint import pprint

import constants
import core


if __name__ == "__main__":
    """ """
    #ship = Ship()
    ship = core.Ship('hornet')

    # test, buy or sell an xtrapod
    pulse = core.Weapon("beam", 20, 20)
    shield = core.Shield("energy", 15, 15)
    gadget = core.Gadget("autorepair", 50, 'autorepair')
    crew = core.Crew('nemo', 500)

    captain = core.Captain()
    captain.ship = ship

    ship.add_item(pulse)
    ship.add_item(shield)
    ship.remove_item(shield)  # pass, for now
    ship.add_item(gadget)
    ship.add_item(crew)

    print("\nShip & Captain:")
    print(f"Contents of {ship.model['model']}:")
    for item in ship.cargo:
        print(f'cargo; {item}')
    print(f'Capacity: {ship.capacity}')
    print(f'Pods: {ship.xtrapods}')

    pprint(captain)
    print(captain.show_skills)
    print(f"Pilot: {captain.skills['Pilot']}")
    print(captain.show_status)
    print(captain.ship['xtrapods'])
    print(captain.ship.weapons)


    print("\nUse of items:")
    for item in captain.ship.weapons:
        print(f"{item}, {captain.ship.weapons.index(item)}")
        captain.ship.use_item(captain.ship.weapons[captain.ship.weapons.index(item)])

    # if (x for x in captain.ship.weapons if isinstance(Weapon, x)):
    #     captain.ship.use_item(captain.ship.weapons)

    for item in captain.ship.shields:
        captain.ship.use_item(captain.ship.shields[captain.ship.shields.index(item)])
    # ship.use_item(shield)
    # ship.use_item(gadget)

