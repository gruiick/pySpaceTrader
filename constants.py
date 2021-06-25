#!/usr/bin/env python3
# coding: utf-8
#
# $Id: constants.py 1546.v0.2-dev.1 $
# SPDX-License-Identifier: BSD-2-Clause

"""
    Game constants, to be imported

    Lots from https://github.com/blind-coder/SpaceTrader/blob/master/SpaceTrader/src/main/java/de/anderdonau/spacetrader/Main.java
"""

VERSION = "v0.3"

# width, x = 640, height, y = 480 (Tk)
GRIDMIN = -100
GRIDMAX = 100
XMIN = 0
MAXWIDTH = 680
YMIN = 0
MAXHEIGHT = 480
MAXPARSEC = 120  # must be dividable by 15
CASH = 215000
MAXPLANET = 120
MIN_DISTANCE = 12

COLORS = {'default': 'brown',
          'limit': 'red',
          'homeworld': 'blue',
          'visited': 'green',
          'target': 'grey',
          'selected': 'brown',
          'background': 'lightgrey'}

OVERVIEW = ["Space Trader is a complex game, in which the player's aim",
            "is to amass enough money to be able to buy a moon to retire",
            "to. The player starts out with a small space ship, armed",
            "with one simple laser, and 1000 credits in cash. The safest",
            "and easiest way to earn money is to trade goods between",
            "neighbouring solar systems. If the player chooses the goods",
            "to trade wisely, it isn't too difficult to sell them with",
            "a profit. There are other ways to get rich, though. You",
            "might become a bounty hunter and hunt down pirates. It is",
            "also possible to become a pirate yourself and rob honest",
            "traders of their cargo. Beware, though: pirating is a way",
            "to get rich quickly, but the police force will go after you."]

NAMES = ['Acamar', 'Adahn', 'Aldea', 'Andevian', 'Antedi', 'Balosnee',
         'Baratas', 'Bob', 'Brax', 'Bretel', 'Calondia', 'Campor', 'Capelle',
         'Carzon', 'Castor', 'Cestus', 'Cheron', 'Courteney', 'Daled',
         'Damast', 'Davlos', 'Deneb', 'Deneva', 'Devidia', 'Draylon',
         'Drema', 'Endor', 'Esmee', 'Exo', 'Ferris', 'Festen', 'Fourmi',
         'Frolix', 'Gemulon', 'Guinifer', 'Hades', 'Hamlet', 'Helena',
         'Hulst', 'Iodine', 'Iralius', 'Janus', 'Japori', 'Jarada',
         'Jason', 'Kaylon', 'Khefka', 'Kira', 'Klaatu', 'Klaestron',
         'Korma', 'Kravat', 'Krios', 'Laertes', 'Largo', 'Lave', 'Ligon',
         'Lowry', 'Magrat', 'Malcoria', 'Melina', 'Mentar', 'Merik',
         'Mintaka', 'Montor', 'Mordan', 'Myrthe', 'Nelvana', 'Nix',
         'Nyle', 'Odet', 'Og', 'Omega', 'Omphalos', 'Orias', 'Othello',
         'Parade', 'Penthara', 'Picard', 'Pollux', 'Quator', 'Rakhar',
         'Ran', 'Regulas', 'Relva', 'Rhymus', 'Rochani', 'Rubicum',
         'Rutia', 'Sarpeidon', 'Sefalla', 'Seltrice', 'Sigma', 'Sol',
         'Somari', 'Stakoron', 'Styris', 'Talani', 'Tamus', 'Tantalos',
         'Tanuga', 'Tarchannen', 'Terosa', 'Thera', 'Titan', 'Torin',
         'Triacus', 'Turkana', 'Tyrus', 'Umberlee', 'Utopia', 'Vadera',
         'Vagra', 'Vandor', 'Ventax', 'Xenon', 'Xerxes', 'Yew', 'Yojimbo',
         'Zalkon', 'Zuul']

REGIM = {1: 'dictatorship',  # Ore and Weapons in demand
         2: 'monarchy',  # Ore, Furs and Narcotics in demand
         3: 'democracy'}  # Uneventful
# feodalism, imperium

TECHLEVEL = {0: 'Pre-agricultural',
             1: 'Agricultural',
             2: 'Medieval',
             3: 'Renaissance',
             4: 'Early Industrial',
             5: 'Industrial',
             6: 'Post-industrial',
             7: 'Hi-tech'}

SYSTEMSIZE = {0: 'Tiny',
              1: 'Small',
              2: 'Medium',
              3: 'Large',
              4: 'Huge'}

SPECIALRESOURCES = {'nothing': 'Nothing special',  # Uneventful
                    'mineralrich': 'Mineral rich',  # produce Ore
                    'mineralpoor': 'Mineral poor',  # Ore in demand
                    'desert': 'Desert',  # Water in demand
                    'lotsofwater': 'Sweetwater oceans',  # produce Water
                    'soilrich': 'Rich soil',  # produce Food
                    'soilpoor': 'Poor soil',  # Food in demand
                    'faunarich': 'Rich fauna',  # produce Fur
                    'lifepoor': 'Lifeless',  # Water and Food in demand
                    'weirdmushrooms': 'Weird mushrooms',  # produce Narcotics
                    'lotsofherbs': 'Special herbs',  # produce Narcotics
                    'artistic': 'Artistic populace',  # Narcotics in demand
                    'warlike': 'Warlike populace'}  # Weapons in demand

STATUS = {'nopressure': 'under no particular pressure',  # Uneventful
          'war': 'at war',  # Ore and Weapons in demand
          'plague': 'ravaged by a plague',  # Medicine in demand
          'drought': 'suffering from a drought',  # Water in demand
          'boredom': 'suffering from extreme boredom',  # Games and Narcotics in demand
          'cold': 'suffering from a cold spell',  # Furs in demand
          'cropfailure': 'suffering from a crop failure',  # Food in demand
          'lackofworkers': 'lacking enough workers'}  # Machinery and Robots in demand

"""
class TradeItem/Goods:
Tradeitem("Water", 0, 0, 2, 30, +3, 4, GameState.DROUGHT, GameState.LOTSOFWATER, GameState.DESERT, 30, 50, 1)
    key: name;
    tp: techProduction          // Tech level needed for production
    tu: techUsage               // Tech level needed to use
    ttp: techTopProduction      // Tech level which produces this item the most
    plt: priceLowTech           // Medium price at lowest tech level
    pi: priceInc                // Price increase per tech level
    var: variance               // Max percentage above or below calculated price
    dps: doublePriceStatus      // Price increases considerably when this event occurs
    cr: cheapResource           // When this resource is available, this trade item is cheap
    er: expensiveResource       // When this resource is available, this trade item is expensive
    mintp: minTradePrice        // Minimum price to buy/sell in orbit
    maxtp: maxTradePrice        // Maximum price to buy/sell in orbit
    ro: roundOff                // Roundoff price for trade in orbit
"""
GOODS = {'water': {'tp': 0, 'tu': 0, 'ttp': 2, 'plt': 30, 'pi': +3, 'var': 4, 'dps': 'drought', 'cr': 'lotsofwater', 'er': 'desert', 'mintp': 30, 'maxtp': 50, 'ro': 1},
         'furs': {'tp': 0, 'tu': 0, 'ttp': 0, 'plt': 250, 'pi': +10, 'var': 10, 'dps': 'cold', 'cr': 'faunarich', 'er': 'lifepoor', 'mintp': 230, 'maxtp': 280, 'ro': 5},
         'food': {'tp': 1, 'tu': 0, 'ttp': 1, 'plt': 100, 'pi': +5, 'var': 5, 'dps': 'cropfailure', 'cr': 'soilrich', 'er': 'soilpoor', 'mintp': 90, 'maxtp': 160, 'ro': 5},
         'ore': {'tp': 2, 'tu': 2, 'ttp': 3, 'plt': 350, 'pi': +20, 'var': 10, 'dps': 'war', 'cr': 'mineralrich', 'er': 'mineralpoor', 'mintp': 350, 'maxtp': 420, 'ro': 10},
         'games': {'tp': 3, 'tu': 1, 'ttp': 6, 'plt': 250, 'pi': -10, 'var': 5, 'dps': 'boredom', 'cr': 'artistic', 'er': None, 'mintp': 160, 'maxtp': 270, 'ro': 5},
         'firearms': {'tp': 3, 'tu': 1, 'ttp': 5, 'plt': 1250, 'pi': -75, 'var': 100, 'dps': 'war', 'cr': 'warlike', 'er': None, 'mintp': 600, 'maxtp': 1100, 'ro': 25},
         'medicines': {'tp': 4, 'tu': 1, 'ttp': 6, 'plt': 650, 'pi': -20, 'var': 10, 'dps': 'plague', 'cr': 'lotsofherbs', 'er': None, 'mintp': 400, 'maxtp': 700, 'ro': 25},
         'machines': {'tp': 4, 'tu': 3, 'ttp': 5, 'plt': 900, 'pi': -30, 'var': 5, 'dps': 'lackofworkers', 'cr': None, 'er': None, 'mintp': 600, 'maxtp': 800, 'ro': 25},
         'narcotics': {'tp': 5, 'tu': 0, 'ttp': 5, 'plt': 3500, 'pi': -125, 'var': 150, 'dps': 'boredom', 'cr': 'weirdmushrooms', 'er': None, 'mintp': 2000, 'maxtp': 3000, 'ro': 50},
         'robots': {'tp': 6, 'tu': 4, 'ttp': 7, 'plt': 5000, 'pi': -150, 'var': 100, 'dps': 'lackofworkers', 'cr': None, 'er': None, 'mintp': 3500, 'maxtp': 5000, 'ro': 100},
         'fuel': {'tp': 4, 'tu': 0, 'ttp': 7, 'plt': 17, 'pi': -1, 'var': 15, 'dps': 'war', 'cr': 'warlike', 'er': None, 'mintp': 17, 'maxtp': 5000, 'ro': 1},
         }

SHIPTYPES = {'escapepod': {'model': 'escapepod', 'cargo': 0, 'weapon': 0, 'shield': 0, 'shieldstrengh': 0, 'gadget': 0, 'crew': 0, 'efficiency': 1, 'hull': 500, 'tribbles': False},
             'flea': {'model': 'flea', 'cargo': 10, 'weapon': 1, 'shield': 0, 'shieldstrengh': 0, 'gadget': 1, 'crew': 0, 'efficiency': 1, 'hull': 2000, 'tribbles': False},
             'gnat': {'model': 'gnat', 'cargo': 15, 'weapon': 1, 'shield': 1, 'shieldstrengh': 1, 'gadget': 1, 'crew': 1, 'efficiency': 0.93, 'hull': 10000, 'tribbles': False},
             'firefly': {'model': 'firefly', 'cargo': 20, 'weapon': 1, 'shield': 1, 'shieldstrengh': 1, 'gadget': 1, 'crew': 2, 'efficiency': 1.15, 'hull': 25000, 'tribbles': False},
             'mosquito': {'model': 'mosquito', 'cargo': 15, 'weapon': 2, 'shield': 1, 'shieldstrengh': 1, 'gadget': 1, 'crew': 5, 'efficiency': 0.86, 'hull': 30000, 'tribbles': False},
             'bumblebee': {'model': 'bumblebee', 'cargo': 25, 'weapon': 1, 'shield': 2, 'shieldstrengh': 2, 'gadget': 2, 'crew': 5, 'efficiency': 1, 'hull': 60000, 'tribbles': False},
             'beetle': {'model': 'beetle', 'cargo': 50, 'weapon': 0, 'shield': 1, 'shieldstrengh': 1, 'gadget': 3, 'crew': 5, 'efficiency': 0.93, 'hull': 80000, 'tribbles': False},
             'hornet': {'model': 'hornet', 'cargo': 20, 'weapon': 3, 'shield': 2, 'shieldstrengh': 1, 'gadget': 2, 'crew': 5, 'efficiency': 1.06, 'hull': 100000, 'tribbles': False},
             'grasshopper': {'model': 'grasshopper', 'cargo': 30, 'weapon': 2, 'shield': 2, 'shieldstrengh': 3, 'gadget': 3, 'crew': 6, 'efficiency': 1, 'hull': 150000, 'tribbles': False},
             'termite': {'model': 'termite', 'cargo': 60, 'weapon': 1, 'shield': 3, 'shieldstrengh': 2, 'gadget': 3, 'crew': 7, 'efficiency': 0.86, 'hull': 225000, 'tribbles': False},
             'wasp': {'model': 'wasp', 'cargo': 35, 'weapon': 3, 'shield': 2, 'shieldstrengh': 2, 'gadget': 3, 'crew': 7, 'efficiency': 0.93, 'hull': 300000, 'tribbles': False},
             'spacemonster': {'model': 'spacemonster', 'cargo': 0, 'weapon': 3, 'shield': 0, 'shieldstrengh': 0, 'gadget': 1, 'crew': 0, 'efficiency': 0.5, 'hull': 500000, 'tribbles': False},
             # these have special purpose and cannot be bought
             'dragonfly': {'model': 'dragonfly', 'cargo': 0, 'weapon': 2, 'shield': 3, 'shieldstrengh': 2, 'gadget': 1, 'crew': 1, 'efficiency': 0.53, 'hull': 500000, 'tribbles': False},
             'mantis': {'model': 'mantis', 'cargo': 0, 'weapon': 3, 'shield': 1, 'shieldstrengh': 3, 'gadget': 1, 'crew': 1, 'efficiency': 0.53, 'hull': 500000, 'tribbles': False},
             'scarab': {'model': 'scarab', 'cargo': 20, 'weapon': 2, 'shield': 0, 'shieldstrengh': 0, 'gadget': 2, 'crew': 1, 'efficiency': 0.53, 'hull': 500000, 'tribbles': False},
             'bottle': {'model': 'bottle', 'cargo': 0, 'weapon': 0, 'shield': 0, 'shieldstrengh': 0, 'gadget': 1, 'crew': 1, 'efficiency': 0.53, 'hull': 100, 'tribbles': False},
             }

EQUIPEMENTS = {'weapons': {'pulse': 1, 'beam': 2, 'military': 3},
               'shields': {'energy': 1, 'reflective': 2},
               'gadgets': {'autorepair': 1,
                           'navigating': 1,
                           'targeting': 1,
                           'cloacking': 1,
                           'escape': 1},
               'cargopod': 5}

MERCENARYNAMES = ['Jameson', 'Alyssa', 'Armatur', 'Bentos', 'C2U2',
                  'ChTi', 'Crystal', 'Dane', 'Deirdre', 'Doc', 'Draco',
                  'Iranda', 'Jeremiah', 'Jujubal', 'Kirk', 'Krydon', 'Luis',
                  'Mercedez', 'Milete', 'Muri-L', 'Mystyc', 'Nandi',
                  'Orestes', 'Pancho', 'PS37', 'Quarck', 'Solo', 'Sosumi',
                  'Uma', 'Wesley', 'Wonton', 'Yorvick', 'Zeethibal']


if __name__ == '__main__':
    print('this file is to be imported')
