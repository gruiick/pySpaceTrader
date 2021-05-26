=============================
python3 remake of SpaceTrader
=============================

:date: 2018-12-19
:status: draft
:version: $Id: README.rst 1543 $
:licence: SPDX-License-Identifier: BSD-2-Clause


http://www.spronck.net/spacetrader/STFrames.html

https://github.com/blind-coder/SpaceTrader

I need something to work on my poor python skills. And it may differ from original games.

disclaimer: This is a toy project, early work in progress... It may never be finished.

But you are very welcome to help, if you want to.

* Space Trader, python3/Tk, turn-based, based on:
    * https://www.benjamin-schieder.de/androidspacetrader.html
    * http://www.spronck.net/spacetrader/STFrames.html
    * https://github.com/blind-coder/SpaceTrader (java)
    * https://github.com/blind-coder/SpaceTrader/tree/master/SpaceTrader/src/main/res/drawable (png)
    * https://github.com/blind-coder/SpaceTrader/blob/master/SpaceTrader/src/main/java/de/anderdonau/spacetrader/Main.java

simple interface (Tk) <- TODO have a test of PySimpleGUI
    mockup: (with tabs)
        local cluster (short range) map?, circle = fuel capacity, full speed
        galactic map with grid (select local cluster)
        trading UI

generators (planets, geopolitical env, space routes, encounters, ...)
    Object : dict, tuple(s) (mutable/immutable)
geopolitic: (mutable/immutable ?)
    conflict = weapons bid++, stable = leisures, wealth (more drugs, games and robots), etc
routes:(mutable/immutable ?)
    concentration/quantity of ships (4 types: light, medium, high, swarm)

transaction management, earnings/losses, bank account
    money: galactic credits (Cr)
    goods:
        water
        food
        furs
        ore
        games
        firearms (potentially illegal)
        machines
        narcotics (mostly illegal)
        robots
        [fuel] (mandatory, for now)

ships : hull type (small, medium, large, xtralarge) 
        nb of cargo pod, 
        nb of attack/defense pod (laser, torpedo, shield), 
        nb of crew pod, 
            escape pod (x1 or 0)
            Hydrogen scoop: 0.5 parsec/turn (in case of empty fuel tank)

captain/player : reputation management (Wanted poster(s), bounty?, arrests, fines)
-> ships/shipyard, false identities

minimal spatial fights management (rolldice)


