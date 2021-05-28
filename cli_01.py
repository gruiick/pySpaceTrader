#!/usr/bin/env python3
# coding: utf-8
#
# $Id: cli_01.py 1550 $
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
import random
import shelve

from pprint import pprint

import constants


class Captain:
    """
    This is captain speaking
    """
    def __init__(self):
        self.name = 'Speaking'  # As in "This is Captain speaking..."
        self.homeworld = ()
        self.location = ()
        self.destination = ()
        self.ship = ()
        # self.status = {'skills': '',
        #                'reputation': '',
        #                'record': '',
        #                }
        self.balance = 15000


class Planet:
    """
    une planète : nom
    position (x, y)
    gouvernement = taille, régime, techlevel, status
    visitée/inconnue (True/False)
    homeworld (True/False)
    boundingbox
    bordereau de prix (price slip)
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

        self.fuel_price = self.price_slip['fuel'][1]  # by unit of ship.reservoir


class PriceSlip:  # pour le plaisir de mettre slip dans un nom de Class
    """ for each good, calculate prices and update planete.price_slip 

    dict object {good: [buying price, selling price, stock],}
    """
    # TODO: refaire plus propre, beaucul plus propre
    # les calculs originaux dans le init ou @classmethod ?
    # les updates en .function()

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
            self.planet.price_slip.update({good: self.calculate_prices()})

    def buying_price(self):
        """ calculate initial buying price of a good, on a planet """
        buy_price = self.standard_price()
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

    def calculate_prices(self):
        """ calculate initial prices (and stocks) of a good, on a planet """

        # FIXME it should be stock first, then price
        # bug: selling price without stock!
        # enhancement: if no stock, buying price is higher
        buy = self.buying_price()
        sell = self.selling_price()
        if sell == 0:
            stock = 0
        else:
            stock = self.calculate_stock()

        return [buy, sell, stock]

    def calculate_stock(self):
        """ calculate initial stock of a good """
        # random quantity * systemsize * techlevel (hence, it can be zero)
        size = self.planet.system_size
        level = self.planet.tech_level
        stock = random.randrange(0, 25) * (size + 1) * level

        # SPECIALRESOURCES add 50% production
        if self.planet.special in [self.tradeitem.cr]:
            stock = stock + (stock * 0.5)

        return int(stock)

    def selling_price(self):
        """ calculate initial selling price of a good, on a planet """
        # If a system can't produce something, its price is zero.
        coin = self.tradeitem
        if self.planet.tech_level < coin.tp and coin.name not in 'fuel':
            sell_price = 0
        else:
            sell_price = self.standard_price()
            # raise a bit, randomized
            sell_price = sell_price + random.randrange(self.tradeitem.var)

        return int(sell_price)

    def standard_price(self):
        """ calculate standard price of a good, on a planet """
        # If a system can't use something, its price is zero.
        trade = self.tradeitem
        if self.planet.tech_level < trade.tu and trade.name not in 'fuel':
            base_price = 0
        else:
            base_price = trade.plt + (self.planet.tech_level * trade.pi)
            # if good is highly requested, increase the price
            if self.planet.status in [trade.dps]:
                base_price = base_price + (base_price * 0.5)
            # large system: high production decreases prices
            base_price = (base_price * (100 - self.planet.system_size)) / 100

        # price can't be negative
        if base_price < 0:
            base_price = 0

        return int(base_price)


class Ship:
    """ a ship """
    def __init__(self):
        # first ship is always a flea type
        self.__type = 'flea'
        self.model = constants.SHIPTYPES[self.__type]
        self.reservoir = self.model['fuel'] * constants.MAXPARSEC
        self.gadget = 'escapepod'
        # gestion des pods ?
        self.cargo = {}
        for i in range(self.model['cargo']):
            self.cargo.update({i: {'type': None, 'value': None}})
        #print(len(self.cargo))


def collision(target, objet, radius=None):
    """ is (x, y) inside objet.bbox? """
    # TODO: when creating Planet, radius should be bigger/doubled
    # TODO/FIXME octogonal bbox ?
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


def slip_list(slip):
    """ return a list of list made from slip(dict) elements """
    new_list = []

    for key in slip.keys():
        _interne = []
        _interne.append(key)
        _interne.extend(slip[key])
        new_list.append(list(_interne))

    pprint(new_list)
    return new_list


def calculate_profit_pod(location, destination):
    """ calculate net profit by good (for one pod) between location planet and destination planet 

    return a list of list
    """
    _profit = []
    for key in destination.price_slip.keys():
        if location.price_slip[key] != 0 and destination.price_slip[key] != 0 and location.price_slip[key][2] != 0 :
            benefit = destination.price_slip[key][0] - location.price_slip[key][1]
            _profit.append([benefit])
        else:
            _profit.append([0])

    return _profit


def create_planetes():
    """ create the planetes """
    planetes = []
    planetes.append(Planet())  # first one
    for i in range(0, constants.MAXPLANET):
        temp = Planet()
        for planete in planetes:
            # planete.name has to be uniq
            if not any(temp.name in planete.__dict__.values() for planete in planetes):
                # planetes should not be too close
                if not collision(temp.position, planete):
                    planetes.append(temp)

    # pick one, set to homeworld
    planete = random.choice(planetes)
    planete.homeworld = True
    planete.visited = True

    return planetes


def create_universe():
    """ create the whole universe and stuffz """
    # L'univers est une grande liste, on différencie les planetes et le 
    # reste avec type() et isinstance(object, ClassInfo)
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
            print('{} : {}'.format(truc.name, ' '.join(truc.gov)))  # __repr__ ?
            pprint(truc.__dict__)

        elif isinstance(truc, Captain):
            print('{} : {}, {}'.format(truc.name, truc.homeworld.name, truc.ship.model))  # __repr__ ?
            pprint(truc.__dict__)
            pprint(truc.ship.__dict__)


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


if __name__ == '__main__':
    """ """
    toto = create_universe()
    print_universe(toto)
