=============================
python3 remake of SpaceTrader
=============================

:date: 2018-12-19
:modified: 2020-03-31
:status: draft
:version: $Id: README.rst 1289 $
:licence: SPDX-License-Identifier: BSD-2-Clause


http://www.spronck.net/spacetrader/STFrames.html

https://github.com/blind-coder/SpaceTrader

I need something to work on my poor python skills. And it may differ from original games.

disclaimer: early work in progress... It may never be finished.

* Space Trader, python3/Tk, turn-based, basé sur :
    * https://www.benjamin-schieder.de/androidspacetrader.html
    * http://www.spronck.net/spacetrader/STFrames.html
    * https://github.com/blind-coder/SpaceTrader (java)
    * https://github.com/blind-coder/SpaceTrader/tree/master/SpaceTrader/src/main/res/drawable (png)
    * https://github.com/blind-coder/SpaceTrader/blob/master/SpaceTrader/src/main/java/de/anderdonau/spacetrader/Main.java

interface simple (Tk)
    mockup: (with onglets)
        local cluster (short range) map, circle = fuel capacity, full speed
        galactic map with grid (select local cluster)

générateurs (planètes, situation géopolitique, routes, encounters, ...)
    Objet : dict, tuple(s) (mutable/immutable)
geopolitic: (mutable/immutable ?)
    conflit = demande d'arme++, stable = loisirs, richesses (conso++ de drugs, games et robots), etc
routes:(mutable/immutable ?)
    concentration/quantité de vaisseaux (4 différentes: light, medium, high, swarm)

gestion de transactions, profits/pertes, compte en banque
    money: galactic credits (GCr)
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

vaisseaux : hull type (small, medium, large, xtralarge) 
            nb de pod cargo, 
            nb de pod attack/defense (laser, torpedo, shield), 
            nb de pod crew, 
            escape pod (x1 ou 0)
            Hydrogen scoop: 0.5 parsec/turn (in case of empty fuel tank)

capitaine/joueur (player) : gestion de réputation (avis de recherche, primes?, arrestations, amendes)

gestion de combats spatiaux (rolldice)

