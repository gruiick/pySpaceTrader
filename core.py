#!/usr/bin/env python3
# coding: utf-8
#
# $Id: core.py 1565.develop.12 $
# SPDX-License-Identifier: BSD-2-Clause

"""
    Core Classes & functions (not UI related):

    Captain class
    Planet class
    PriceSlip class
    Ship class
    BankAccount class
    Transaction class

    generate universe
        generate captain and ship
        generate list of planets

    slip_list(Planet.price_slip)

    get_distance between positions
    inside_circle (ex-collision code)

    save game objects
    open previously saved objects

    some debug (CLI)

"""

import collections
import math
import random
import shelve

from dataclasses import dataclass
from pprint import pprint

import constants


@dataclass
class BankAccount:
    """
    Quick & Dirty bank account log

    TODO logging Transaction() should modify cash value
    FIXME do not store more than 5 to 10 Transaction() history?
          or store all history but only display 5~10 lasts?
    """
    owner: str
    log: []
    cash: float = constants.CASH
    # debt

    def display(self):
        """ display account log for GUI
        return a list of list
        """
        new_list = []

        for trans in self.log:
            interne = []
            # apply a 2 decimals float format
            interne.extend([f'{trans.good_type}',
                            f'{trans.good_value:.2f}',
                            f'{trans.quantity:.2f}',
                            f'{trans.sign}',
                            f'{trans.total_value:.2f}'])
            new_list.append(list(interne))
        return new_list


class Crew():
    def __init__(self, name, wage):
        self.name = name
        self.wage = wage
        self.skills = {'Pilot': random.randint(0, 10),
                       'Fighter': random.randint(0, 10),
                       'Trader': random.randint(0, 10),
                       'Engineer': random.randint(0, 10),
                       }

    def __str__(self):
        return f"{self.name} ({self.wage} Cr)"

    def __repr__(self):
        return f"{self.name}"

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


@dataclass
class Planet:
    name: str
    x: int
    y: int
    system_size: int
    tech_level: int
    regim: int
    special: str
    status: str = 'nopressure'
    homeworld: bool = False
    visited: bool = False
    moon: bool = False
    price_slip: {} = None
    shipyard: [] = None

    def __init__(self):
        """ initialize Planet object with random stuff """
        dice = random.randint(0, 100)

        self.name = random.choice(constants.NAMES)
        self.x = random.randint(constants.XMIN, constants.MAXWIDTH - 1)
        self.y = random.randint(constants.YMIN, constants.MAXHEIGHT - 1)
        self.system_size = random.choice(list(constants.SYSTEMSIZE.keys()))
        self.tech_level = random.choice(list(constants.TECHLEVEL.keys()))
        self.regim = random.choice(list(constants.REGIM.keys()))
        self.special = random.choice(list(constants.SPECIALRESOURCES.keys()))
        self.price_slip = {}
        self.shipyard = []
        if dice >= 60:
            self.status = random.choice(list(constants.STATUS.keys()))
        if 42 <= dice <= 61:
            self.moon = True

    @property
    def position(self):
        return self.x, self.y

    @property
    def gov(self):
        # temporary display solution
        if self.moon:
            moon_status = "has moon(s)"
        else:
            moon_status = "no moon"

        return (constants.SYSTEMSIZE[self.system_size],
                constants.SPECIALRESOURCES[self.special],
                constants.TECHLEVEL[self.tech_level],
                constants.REGIM[self.regim],
                constants.STATUS[self.status],
                moon_status)

    def distance(self, other):
        return math.hypot((self.x - other.x), (self.y - other.y))

    @property
    def ships(self):
        """ return None or nb of ships available, for display """
        if self.shipyard is not None:
            if self.tech_level > 5:
                return len(self.shipyard)
        else:
            return None


@dataclass
class Point:
    """ needed for Planet.distance() purpose """
    x: int
    y: int

    @property
    def position(self):
        return self.x, self.y


class PriceSlip:  # pour le plaisir de mettre slip dans un nom de Class
    """ for each good, calculate prices and update planete.price_slip

    dict object {good: [buying price, selling price, stock],}
    """
    # TODO: need love, and proper redo
    # maybe @classmethod?
    # need a refresh function for stock and prices
    # depending on TradeItem modificators

    def __init__(self, planet):  # planet=planete
        """ """
        self.planet = planet
        self.goods = constants.GOODS
        # pourquoi un namedtuple déjà ?
        TradeItem = collections.namedtuple('TradeItem',
                                           ['name',
                                            'tp',  # Tech level needed for production
                                            'tu',  # Tech level needed to use
                                            'ttp',  # Tech level which produces this item the most
                                            'plt',  # Medium price at lowest tech level
                                            'pi',  # Price increase per tech level
                                            'var',  # Max percentage above or below calculated price
                                            'dps',  # Price increases considerably when this event occurs
                                            'cr',  # When this resource is available, this item is cheap
                                            'er',  # When this resource is available, this item is expensive
                                            'mintp',  # Minimum price to buy/sell in orbit
                                            'maxtp',  # Maximum price to buy/sell in orbit
                                            'ro'  # Roundoff price for trade in orbit
                                            ])

        for good in list(self.goods.keys()):
            self.tradeitem = TradeItem(good,
                                       self.goods[good]['tp'],
                                       self.goods[good]['tu'],
                                       self.goods[good]['ttp'],
                                       self.goods[good]['plt'],
                                       self.goods[good]['pi'],
                                       self.goods[good]['var'],
                                       self.goods[good]['dps'],
                                       self.goods[good]['cr'],
                                       self.goods[good]['er'],
                                       self.goods[good]['mintp'],
                                       self.goods[good]['maxtp'],
                                       self.goods[good]['ro'],
                                       )
            # print(self.tradeitem)
            # relire sam&max
            self.planet.price_slip.update({good: self.calculate_prices(good)})

    def buying_price(self):
        """ calculate initial buying price of a good, on a planet """
        buy_price = self.standard_init_price()
        # Special status and resources price adaptation
        if self.planet.status in [self.tradeitem.dps]:
            buy_price = (buy_price * 5) / 3

        elif self.planet.special in [self.tradeitem.cr]:
            buy_price = (buy_price * 3) / 4

        elif self.planet.special in [self.tradeitem.er]:
            buy_price = (buy_price * 4) / 3

        # randomize a bit
        moins = random.randrange(self.tradeitem.var)
        plus = random.randrange(self.tradeitem.var)
        buy_price = buy_price - moins + plus

        # price can't be negative
        if buy_price < 0:
            buy_price = 0

        return int(buy_price)

    def calculate_prices(self, good=None):
        """ calculate initial prices (and stocks) of a good, on a planet """

        stock = self.calculate_init_stock(good)
        buy = self.buying_price()

        if stock == 0:
            sell = 0
            buy = buy + (buy * 0.5)

        elif stock < 500:
            # mild bug: stock, without selling price
            sell = self.selling_price()
        elif stock >= 500:
            # higher production, lower prices
            sell = self.selling_price() / 2
            buy = buy - (buy * 0.5)

        return [buy, sell, stock]

    def calculate_init_stock(self, good=None):
        """ calculate initial stock of a good """
        # random quantity * systemsize * techlevel (hence, it can be zero)
        size = self.planet.system_size
        level = self.planet.tech_level
        stock = random.randrange(0, 25) * (size + 1) * level

        # SPECIALRESOURCES add 50% production
        if self.planet.special in [self.tradeitem.cr]:
            stock = stock + (stock * 0.5)

        # TODO enhancement: difficulty levels should affect fuel stocks
        if good in ['fuel']:
            stock = stock * 10

        return int(stock)

    def selling_price(self):
        """ calculate initial selling price of a good, on a planet """
        # If a system can't produce something, its price is zero.
        _good = self.tradeitem
        if self.planet.tech_level < _good.tp and _good.name not in 'fuel':
            sell_price = 0
        else:
            sell_price = self.standard_init_price()
            # raise a bit, randomized
            sell_price = sell_price + random.randrange(self.tradeitem.var)

        return int(sell_price)

    def standard_init_price(self):
        """ calculate standard price of a good, on a planet """
        # If a system can't use something, its price is zero.
        _good = self.tradeitem
        if self.planet.tech_level < _good.tu and _good.name not in 'fuel':
            base_price = 0
        else:
            base_price = _good.plt + (self.planet.tech_level * _good.pi)
            # if good is highly requested, increase the price
            if self.planet.status in [_good.dps]:
                base_price = base_price + (base_price * 0.5)
            # large system: high production decreases prices
            base_price = (base_price * (100 - self.planet.system_size)) / 100

        # price can't be negative
        if base_price < 0:
            base_price = 0

        return int(base_price)


class Item:
    """ items are define in constants.EQUIPEMENTS
    """
    def __init__(self, name, price):
        self.name = name # constants.EQUIPEMENTS[name] ?
        self.price = price  # price depends on planet{PriceSlip}

    def __str__(self):
        return f"{self.name} ({self.price} Cr)"

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


class Ship:
    """ a ship
        simplest for now
    """
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

        # cargo pods management
        self.cargo = {}
        for i in range(self.model['cargo']):
            self.cargo.update({i: {'type': None, 'value': None}})

        # special pods (extra pods)
        self.capacity_weapon = self.model['weapon']
        self.capacity_shield = self.model['shield']
        self.capacity_gadget = self.model['gadget']
        self.capacity_crew = self.model['crew']

        self.weapons = []
        self.shields = []
        self.gadgets = []
        self.crews = []
        self.xtrapods = [self.weapons, self.shields, self.gadgets, self.crews]  # @property?

        # by default, add equipment type using key from constants (simpliest)
        for equipement_type in self.model.keys():
            if equipement_type in constants.EQUIPEMENTS.keys():
                for k, v in constants.EQUIPEMENTS[equipement_type].items():
                    if self.model[equipement_type] == v:
                        if equipement_type == 'weapon':
                            if len(self.weapons) <= self.capacity_weapon:
                                self.weapons.append(Weapon(k, v, 20))
                        if equipement_type == 'shield':
                            if len(self.shields) <= self.capacity_shield:
                                self.shields.append(Shield(k, v, 20))
                        if equipement_type == 'gadget':
                            if len(self.gadgets) <= self.capacity_gadget:
                                self.gadgets.append(Gadget(k, v, 'escapepod'))
                        # by default, there's never a crew in a brand new ship
                        # you have to find and hire them

    def __getitem__(self, key):
        """ make Ship subscriptable """
        return getattr(self, key)

    def unload_cargo(self, idx):
        """ unload one pod at a time """
        self.cargo.update({idx: {'type': None, 'value': None}})

    def display(self):
        """ display ship specifications for SimpleGUI
        return a list of list
        """
        new_list = []
        for key, value in self.model.items():
            interne = []
            # print some values in {:.2f} format
            if key in ['price', 'efficiency']:
                interne.extend([f'{value:.2f}'])
            else:
                interne.extend([f'{value}'])
            new_list.append(list(interne))
        return new_list

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


@dataclass
class Transaction:
    """ a transaction of some sort
    used to store any buy/sell operation
    """
    sign: str  # +/-
    good_type: str
    good_value: float
    quantity: int = 0

    @property
    def total_value(self) -> float:
        return self.good_value * self.quantity


def calculate_profit_pod(location, destination):
    """ calculate net profit by good (for one pod) between location planet and destination planet

    return a list of list, with a 2 decimals float format
    """
    _profit = []
    for key in destination.price_slip.keys():
        if location.price_slip[key] != 0 and destination.price_slip[key] != 0 and location.price_slip[key][1] != 0 and location.price_slip[key][2] != 0:
            benefit = destination.price_slip[key][0] - location.price_slip[key][1]
            _profit.append([f'{benefit:.2f}'])
        else:
            _profit.append([f'0.00'])

    return _profit


def create_planetes():
    """ create all the planetes
    return a list
    """
    planetes = {}
    for i in range(constants.MAXPLANET):
        while True:
            planete = Planet()
            # planets must not be too close to each other
            if (planete.name not in planetes and all(planete.distance(p) >= constants.MIN_DISTANCE for p in planetes.values())):
                PriceSlip(planete)  # attach a PriceSlip to planet object
                planetes[planete.name] = planete

                break

    # pick one, set to homeworld
    planete = random.choice(list(planetes.values()))
    planete.homeworld = True
    planete.visited = True
    planete.moon = True

    return list(planetes.values())


def create_universe():
    """ create the whole universe and stuffz """
    # Universe is a large list, planets and others things are separated using
    # type() and isinstance(object, ClassInfo)
    univers = []
    captain = Captain()
    captain.ship = Ship()
    captain.account = BankAccount(captain.name, [])
    planetes = create_planetes()
    for planete in planetes:
        if planete.homeworld:
            captain.homeworld = planete
            captain.location = planete
        if planete.tech_level > 5:
            planete.shipyard = populate_shipyard()

    univers.append(captain)
    univers.extend(planetes)

    return univers


def populate_shipyard():
    """ initialize a Planet().ship_yard with random Ship()
    """
    dice = random.randint(0, 5)
    inliste = []
    # exclude escapepod and non-boughtable ships
    ship_types = list(constants.SHIPTYPES.keys())[1:11]
    for _ in range(dice):
        ship = Ship(modele=random.choice(ship_types))
        inliste.append(ship)

    return inliste


def print_universe(univers):
    """ print the current universe (debug purpose) """

    print('Debug Universe:')
    # a whatever Point()
    bidule = Point(2, 3)
    pprint(bidule.__dict__)

    # a whatever Transaction()
    machin = Transaction('-', 'fuel', 8.5, 10)
    pprint(machin.__dict__)
    print(f'Total= {machin.total_value}')

    for truc in univers:
        if isinstance(truc, Planet):
            print(f'{truc.name}: {" ".join(truc.gov)}')
            pprint(truc.__dict__)
            for item in truc.shipyard:
                pprint(item.__dict__)

        elif isinstance(truc, Captain):
            print(f'{truc.name}, {truc.homeworld.name}, {truc.ship.model}')
            pprint(truc.ship.__dict__)
            pprint(truc.__dict__)
            print(f'Distance: {truc.homeworld.distance(bidule):.2f}\n')
            print(f'{truc.account.display()}')


def load_file(fname):
    """ open the previously saved shelve and load the game data """
    # FIXME use try/except may not work here, go upstairs
    poney = []
    print(f"{fname}")
    with shelve.open(fname, 'r') as loadfile:
        poney = loadfile['univers']
        loadfile.close()
    return poney


def save_file(univers, fname):
    """ open a new empty shelve (or overwrite previous one)
        to write the game data
    """
    # TODO use try/except
    print(f"{fname}")
    with shelve.open(fname, 'c') as savefile:
        savefile['univers'] = univers
        savefile.close()


def slip_list(slip):
    """ return a list of list made from slip(dict) elements
        needed by PySimpleGUI using only lists
        TODO make it a PriceSlip method()
    """
    new_list = []

    for key in slip.keys():
        interne = []
        interne.append(key)
        # apply a 2 decimals float format
        interne.extend([f'{slip[key][0]:.2f}', f'{slip[key][1]:.2f}', f'{slip[key][2]:.2f}'])
        new_list.append(list(interne))

    return new_list


if __name__ == '__main__':
    """ """
    toto = create_universe()
    print_universe(toto)
