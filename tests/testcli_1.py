#!/usr/bin/env python3
# coding: utf-8
#
# $Id: testcli_1.py 1303 $
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

    def distance(self, other):
        return math.hypot((self.x - other.x), (self.y - other.y))


def make_planet():
    return Planet(
        name=random.choice(constants.NAMES),
        x=random.randint(constants.XMIN, constants.MAXWIDTH - 1),
        y=random.randint(constants.YMIN, constants.MAXHEIGHT - 1),
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
    return planets

univers = make_universe(constants.MAXPLANET)
pprint(univers)
