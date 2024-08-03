#!/usr/bin/env python3
# coding: utf-8
#
# $Id: ship+items.py 1.develop.7 $
# SPDX-License-Identifier: BSD-2-Clause

""" experimentations around Ship() and Item() """

import random
from dataclasses import dataclass

from pprint import pprint

import constants


class Item:
    """ items are define in constants.EQUIPEMENTS
    """
    def __init__(self, name, price):
        self.name = name
        self.price = price  # price depends on planet{PriceSlip}

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.name}"


class Weapon(Item):
    def __init__(self, name, price, damage):
        super().__init__(name, price)
        self.damage = damage

    def attack(self):
        print(f"Attacking with {self.name} for {self.damage} points!")


class Shield(Item):
    def __init__(self, name, price, defense):
        super().__init__(name, price)
        self.defense = defense

    def block(self):
        print(f"Defending with {self.name} for {self.defense} points!")


class Gadget(Item):
    def __init__(self, name, price, fonction):
        super().__init__(name, price)
        self.fonction = fonction

    def action(self):
        print(f"Doing stuff with {self.name}...")


class Crew():
    def __init__(self, name, wage):
        self.name = name
        self.wage = wage
        self.skills = {'Pilot': random.randint(0, 10),
                       'Fighter': random.randint(0, 10),
                       'Trader': random.randint(0, 10),
                       'Engineer': random.randint(0, 10),
                       }

    # def __str__(self):
    #     return f"{self.name} ({self.wage} Cr)"

    def __repr__(self):
        return f"{self.name}"

    def __getitem__(self, key):
        """ make Ship subscriptable """
        return getattr(self, key)

    @property
    def show_skills(self):
        return f"{self.name}, {self.skills}"


class Captain(Crew):
    """
    This is captain speaking
    """
    def __init__(self):
        self.name = 'Speaking'  # As in "This is Captain speaking...", got it?
        super().__init__(self.name, None)

        self.homeworld = None
        self.location = None
        self.destination = None
        self.ship = None
        self.account = None

        self.status = {'Kills': 0,
                      'Reputation': '',
                      'Police Record': None,
                      'Difficulty': None,
                      }

    @property
    def show_status(self):
        return f"{self.name}, {self.status}"

    @property
    def balance(self):
        # self.cash replace initial balance
        _lst = []
        liste_pods = [x for x in self.ship.cargo.keys() if self.ship.cargo[x]['value'] is not None]
        for idx in liste_pods:
            _lst.append(self.ship.cargo[idx]['value'])

        cargo_value = sum(_lst)
        balance = cargo_value + self.account.cash

        return balance


class Ship:
    def __init__(self, modele=None):
        # default ship is always a flea
        if not modele:
            self.__type = 'flea'
        else:
            self.__type = modele

        self.model = constants.SHIPTYPES[self.__type]
        # FIXME quick & dirty price ship
        self.model['price'] = self.model['hull'] * self.model['efficiency']
        self.reservoir = self.model['efficiency'] * constants.MAXPARSEC
        # pods management
        self.cargo = {}
        for i in range(self.model['cargo']):
            self.cargo.update({i: {'type': None, 'value': None}})

        self.capacity_weapon = self.model['weapon']
        self.capacity_shield = self.model['shield']
        self.capacity_gadget = self.model['gadget']
        self.capacity_crew = self.model['crew']

        # créer des attributs/properties
        self.weapons = []
        self.shields = []
        self.gadgets = []
        self.crews = []
        self.xtrapods = [self.weapons, self.shields, self.gadgets, self.crews]

        # add equipment type by default key from constants (simpliest)
        for equipement_type in self.model.keys():
            # print(equipement_type)
            if equipement_type in constants.EQUIPEMENTS.keys():
                for k, v in constants.EQUIPEMENTS[equipement_type].items():
                    if self.model[equipement_type] == v:
                        if equipement_type == 'weapon':
                            if len(self.weapons) <= self.capacity_weapon:
                                self.weapons.append(Weapon(k, v, 20))
                                print(f'adding: {k}, {v}')
                        if equipement_type == 'shield':
                            if len(self.shields) <= self.capacity_shield:
                                self.shields.append(Shield(k, v, 20))
                                print(f'adding: {k}, {v}')
                        if equipement_type == 'gadget':
                            if len(self.gadgets) <= self.capacity_gadget:
                                self.gadgets.append(Gadget(k, v, 'escapepod'))
                                print(f'adding: {k}, {v}')
                        # by default, there's never a crew in a brand new ship
                        # you have to find and hire them

    def __str__(self):
        return f"{self.model[model]}: ({self.cargo}), ({self.xtrapods})"

    def __getitem__(self, key):
        """ make Ship subscriptable """
        return getattr(self, key)

    @property
    def capacity(self):
        """ capacity is sum of all xtrapods (gadgets + weapons + shields + crews) """
        return sum([self.capacity_weapon,
                    self.capacity_shield,
                    self.capacity_gadget,
                    self.capacity_crew])

    def add_item(self, item):
        if isinstance(item, Weapon):
            if len(self.weapons) < self.capacity_weapon:
                self.weapons.append(item)
            else:
                print(f"cannot add {item}, not enough weapon pods left.")
        elif isinstance(item, Shield):
            if len(self.shields) < self.capacity_shield:
                self.shields.append(item)
            else:
                print(f"cannot add {item}, not enough shield pods left.")
        elif isinstance(item, Gadget):
            if len(self.gadgets) < self.capacity_gadget:
                self.gadgets.append(item)
            else:
                print(f"cannot add {item}, not enough gadget pods left.")
        elif isinstance(item, Crew):
            if len(self.crews) < self.capacity_crew:
                self.crews.append(item)
            else:
                print(f"cannot hire {item}, not enough crew pods left.")

    def use_item(self, item):
        if isinstance(item, Weapon):
            item.attack()
        elif isinstance(item, Shield):
            item.block()
        elif isinstance(item, Gadget):
            item.action()
        else:
            print(f"You cannot use an {item} that way")

    def remove_item(self, item):
        pass

    def drop_item(self, item):
        pass



if __name__ == "__main__":
    """ """
    #ship = Ship()
    ship = Ship('hornet')

    # test, buy or sell an xtrapod
    pulse = Weapon("beam", 20, 20)
    shield = Shield("energy", 15, 15)
    gadget = Gadget("autorepair", 50, 'autorepair')
    crew = Crew('nemo', 500)

    captain = Captain()
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

