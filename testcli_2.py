#!/usr/bin/env python3
# coding: utf-8
#
# $Id: testcli_2.py 1304 $
# SPDX-License-Identifier: BSD-2-Clause

"""
some tests
"""

import collections
import dataclasses
import random
import math

from pprint import pprint

import constants

MIN_DISTANCE = 20

@dataclasses.dataclass
class Planet:
    name: str
    x: int
    y: int
    system_size: str
    tech_level: str
    regim: str
    special: str
    status: str
    homeworld: bool
    visited: bool

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
        homeworld=False,
        visited=False,
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
                planets[planet.name] = planet
                break
    return list(planets.values())

univers = make_universe(constants.MAXPLANET)
pprint(univers)
for planete in univers:
    print(f'{planete.name}, {planete.position}, {planete.gov}')
