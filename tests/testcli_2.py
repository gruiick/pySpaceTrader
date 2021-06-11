#!/usr/bin/env python3
# coding: utf-8
#
# $Id: testcli_2.py 1306 $
# SPDX-License-Identifier: BSD-2-Clause

"""
some tests
"""

import collections
import random
import math

from dataclasses import dataclass
from pprint import pprint

import constants

MIN_DISTANCE = 20


class PriceSlip:
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


@dataclass
class Planet:
    name: str
    x: int
    y: int
    system_size: int
    tech_level: int
    regim: int
    special: str
    status: str
    homeworld: bool = False
    visited: bool = False
    price_slip: {} = None

    @property
    def position(self):
        return (self.x, self.y)

    @property
    def gov(self):
        return (constants.SYSTEMSIZE[self.system_size],
                constants.SPECIALRESOURCES[self.special],
                constants.TECHLEVEL[self.tech_level],
                constants.REGIM[self.regim],
                constants.STATUS[self.status])

    @property
    def fuel_price(self):
        return self.price_slip['fuel'][1]

    def distance(self, other):
        return math.hypot((self.x - other.x), (self.y - other.y))


def make_planet():

    dice = random.randint(0, 100)
    if dice < 60:
        status = 'nopressure'
    else:
        status = random.choice(list(constants.STATUS.keys()))

    return Planet(
        name=random.choice(constants.NAMES),
        x=random.randint(constants.XMIN, constants.MAXWIDTH - 1),
        y=random.randint(constants.YMIN, constants.MAXHEIGHT - 1),
        system_size=random.choice(list(constants.SYSTEMSIZE.keys())),
        tech_level=random.choice(list(constants.TECHLEVEL.keys())),
        regim=random.choice(list(constants.REGIM.keys())),
        special=random.choice(list(constants.SPECIALRESOURCES.keys())),
        status=status,
        price_slip={},
        )


def make_universe(n_planets):
    planets = {}
    for i in range(n_planets):
        while True:
            planet = make_planet()
            if (
                    planet.name not in planets
                    and all(
                        planet.distance(p) >= MIN_DISTANCE
                        for p in planets.values()
                    )
            ):
                PriceSlip(planet)
                planets[planet.name] = planet

                break
    return list(planets.values())

univers = make_universe(constants.MAXPLANET)
pprint(univers)
for planete in univers:
    #print(f'{planete.name}, {planete.position}, {planete.gov}')
    pprint(planete.__dict__)
