#!/usr/bin/env python3
# coding: utf-8
#
# $Id: core.py 1560 $
# SPDX-License-Identifier: BSD-2-Clause

"""
    Core Classes & functions (not UI related):

    Captain class
    Planet class
    PriceSlip class
    Ship class

    generate universe
        generate captain and ship
        generate list of planets

    collision(target, object.bbox, radius=None)

    slip_list(Planet.price_slip)

    save game objects
    open previously saved  objects

    some debug (CLI)

"""

import collections
import math
import random
import shelve

from dataclasses import dataclass
from pprint import pprint

import constants


class BankAccount:
    """
    Quick & Dirty bank account log
    """
    def __init__(self):
        self.owner = ''
        self.homeworld = ''
        self.log = []


class Captain:
    """
    This is captain speaking
    """
    def __init__(self):
        self.name = 'Speaking'  # As in "This is Captain speaking...", got it?
        self.homeworld = ()
        self.location = ()
        self.destination = ()
        self.ship = ()
        # self.status = {'skills': '',
        #                'reputation': '',
        #                'record': '',
        #                }
        self.cash = constants.CASH

    @property
    def balance(self):
        # self.cash replace initial balance
        _lst = []
        liste_pods = [x for x in self.ship.cargo.keys() if self.ship.cargo[x]['value'] is not None]
        for idx in liste_pods:
            _lst.append(self.ship.cargo[idx]['value'])

        cargo_value = sum(_lst)
        balance = cargo_value + self.cash

        return balance


class Planet:
    """
    a planet : name
    position (x, y)
    governement = size, regime, techlevel, status
    visited/unknown (True/False)
    homeworld (True/False)
    boundingbox
    price slip (bordereau de prix)
    """
    def __init__(self):
        """ create a planet """
        self.name = random.choice(constants.NAME)
        self.__x = random.randint(constants.XMIN, constants.MAXWIDTH - 1)
        self.__y = random.randint(constants.YMIN, constants.MAXHEIGHT - 1)
        self.position = (self.__x, self.__y)

        self.system_size = random.choice(list(constants.SYSTEMSIZE.keys()))
        self.tech_level = random.choice(list(constants.TECHLEVEL.keys()))
        self.regim = random.choice(list(constants.REGIM.keys()))
        self.special = random.choice(list(constants.SPECIALRESOURCES.keys()))

        dice = random.randint(0, 100)
        if dice < 60:
            self.status = 'nopressure'
        else:
            self.status = random.choice(list(constants.STATUS.keys()))

        self.gov = (constants.SYSTEMSIZE[self.system_size],
                    constants.SPECIALRESOURCES[self.special],
                    constants.TECHLEVEL[self.tech_level],
                    constants.REGIM[self.regim],
                    constants.STATUS[self.status])

        self.homeworld = False
        self.visited = False
        self.bbox = [(self.__x - constants.BOX, self.__y - constants.BOX),
                     (self.__x + constants.BOX, self.__y + constants.BOX)]

        # bordereau des prix et stocks
        # self.price_slip = PriceSlip(self)
        self.price_slip = {}
        PriceSlip(self)

        self.fuel_price = self.price_slip['fuel'][1]  # by unit of ship.reservoir (T)


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


class Ship:
    """ a ship
        simplest for now
    """
    def __init__(self):
        # first ship is always a flea type
        self.__type = 'flea'
        self.model = constants.SHIPTYPES[self.__type]
        self.reservoir = self.model['fuel'] * constants.MAXPARSEC
        self.gadget = 'escapepod'
        # pods management
        self.cargo = {}
        for i in range(self.model['cargo']):
            self.cargo.update({i: {'type': None, 'value': None}})

@dataclass
class Transaction:
    """ a transaction of some sort
    used to store any buy/sell operation

    See dataclass
    https://docs.python.org/3.7/library/dataclasses.html
    """
    good_type: str
    good_price: float
    quantity: int = 0

    @property
    def total_value(self) -> float:
        return self.good_price * self.quantity


def calculate_profit_pod(location, destination):
    """ calculate net profit by good (for one pod) between location planet and destination planet

    return a list of list
    """
    _profit = []
    for key in destination.price_slip.keys():
        if location.price_slip[key] != 0 and destination.price_slip[key] != 0 and location.price_slip[key][1] != 0 and location.price_slip[key][2] != 0 :
            benefit = destination.price_slip[key][0] - location.price_slip[key][1]
            _profit.append([benefit])
        else:
            _profit.append([0])

    return _profit


def collision(target, objet, radius=None):
    """ is (x, y) inside objet.bbox? """
    # TODO: when creating Planet, radius should be bigger/doubled
    # FIXME octogonal bbox ?
    # bool Collision(int curseur_x,int curseur_y,AABB box)
    #  if (curseur_x >= box.x && curseur_x < box.x + box.w
    #      && curseur_y >= box.y && curseur_y < box.y + box.h)
    #  return true; else return false;
    (xt, yt) = target
    (x1, y1), (x2, y2) = objet.bbox

    if (x1 < xt < x2) and (y1 < yt < y2):
        center_h = int((x2 - x1) / 2) + x1
        center_v = int((y2 - y1) / 2) + y1
        center = (center_h, center_v)
        # print('center: ', center)
        # print('target: ', (xt, yt))
        # print((x1, y1), (x2, y2))
        return True
    else:
        return False


def create_planetes():
    """ create the planetes """
    planetes = []
    planetes.append(Planet())  # first one
    for i in range(0, constants.MAXPLANET):
        temp = Planet()
        for planete in planetes:
            # planete.name has to be uniq
            if not any(temp.name in planete.__dict__.values() for planete in planetes):
                # planetes should not be too close (-> radius)
                if not collision(temp.position, planete):
                    planetes.append(temp)

    # pick one, set to homeworld
    planete = random.choice(planetes)
    planete.homeworld = True
    planete.visited = True

    return planetes


def create_universe():
    """ create the whole universe and stuffz """
    # Universe is a large list, planets and others things are separated using
    # type() and isinstance(object, ClassInfo)
    univers = []
    captain = Captain()
    captain.ship = Ship()
    planetes = create_planetes()
    for planete in planetes:
        if planete.homeworld:
            captain.homeworld = planete
            captain.location = planete

    univers.append(captain)
    univers.extend(planetes)

    return univers


def load_game(fname=None):
    """ open the previously saved shelve and load the game data """
    # TODO use try/except
    poney = []
    if not fname:
        fname = 'savegame'
    with shelve.open(fname, 'r') as savefile:
        poney = savefile['univers']
        savefile.close()

    return poney


def print_universe(univers):
    """ print the current universe (debug purpose) """

    print('Debug Universe:')
    for truc in univers:
        if isinstance(truc, Planet):
            print('{} : {}'.format(truc.name, ' '.join(truc.gov)))  # __repr__?
            pprint(truc.__dict__)

        elif isinstance(truc, Captain):
            print('{} : {}, {}'.format(truc.name, truc.homeworld.name, truc.ship.model))  # __repr__?
            pprint(truc.__dict__)
            pprint(truc.ship.__dict__)


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


def inside_circle(point, centre, rayon):
    """ is the point inside the circle?

    centre = (x0, y0)
    point = (x1, y1)
    rayon: int (or float?)
    a = x0 - x1
    b = y0 - y1
    longueur = sqrt(b*b + a*a) (-> math.hypot((a, b))

    return True or False
    """
    x0, y0 = centre
    x1, y1 = point
    a = x0 - x1
    b = y0 - y1
    longueur = math.hypot(a, b)
    if longueur <= rayon:
        return True
    else:
        return False


def save_game(univers, fname=None):
    """ open a new empty shelve (or overwrite previous one)
        to write the game data
    """
    # TODO use try/except
    if not fname:
        fname = 'savegame'
    with shelve.open(fname, 'n') as savefile:
        savefile['univers'] = univers
        savefile.close()


def slip_list(slip):
    """ return a list of list made from slip(dict) elements 
        needed by PySimpleGUI using only lists
    """
    new_list = []

    for key in slip.keys():
        _interne = []
        _interne.append(key)
        _interne.extend(slip[key])
        new_list.append(list(_interne))

    # pprint(new_list)
    return new_list


if __name__ == '__main__':
    """ """
    toto = create_universe()
    print_universe(toto)
