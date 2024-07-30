#!/usr/bin/env python3
# coding: utf-8
#
# $Id: test_ship+items.py 1.develop.1 $
# SPDX-License-Identifier: BSD-2-Clause

""" experimentations around Ship() and Item() """

import constants
import core


class Item:
    """ les items sont dans constants.EQUIPEMENTS
        un parcours dedans pour les créer ?
    """
    def __init__(self, name, price):
        self.name = name
        self.price = price  # le prix dépends de la planète (PriceSlip)

    def __str__(self):
        return f"{self.name} ({self.price} Cr)"


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
        # capacity is sum of gadgets + weapons + shields + crew pods
        self.capacity = sum([self.model['weapon'],
                             self.model['shield'],
                             self.model['gadget'],
                             self.model['crew']])
        self.pods = []  # make it a list of objects

    def add_item(self, item):
        if self.capacity >= 1:
            self.pods.append(item)
            self.capacity -= 1
        else:
            print(f"Pas assez de place pour {item}")


    def use_item(self, item):
        if isinstance(item, Weapon):
            item.attack()
        elif isinstance(item, Shield):
            item.block()
        else:
            print(f"Vous ne pouvez pas utiliser un {item.name} de cette façon")


if __name__ == "__main__":
    """ """
    # déplacer, c'est au vaisseau de créer/remplir ses pods par défaut
    pulse = Weapon("Pulse laser", 20, 20)
    shield = Shield("Bouclier", 15, 15)
    gadget = Item("autorepair", 50)

    ship = Ship('firefly')
    #ship = Ship()

    ship.add_item(pulse)
    ship.add_item(shield)
    ship.add_item(gadget)

    print(f"Contenu du cargo du {ship.model}:")
    #for item in ship.cargo:
    #    print(item)
    print(f'Capacity: {ship.capacity}')
    for item in ship.pods:
        print(item)

    print("\nUtilisation des objets:")
    ship.use_item(pulse)
    ship.use_item(shield)
    ship.use_item(gadget)
