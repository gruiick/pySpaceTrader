=============================
python3 remake of SpaceTrader
=============================

:date: 2018-12-19
:status: draft
:version: $Id: README.rst 1547 $
:licence: SPDX-License-Identifier: BSD-2-Clause


A little remake of Space Trader, with python3/Tk, as a toy project.

Turn-based strategy/trading small game.

References
==========

* https://www.benjamin-schieder.de/androidspacetrader.html

* http://www.spronck.net/spacetrader/STFrames.html

* https://github.com/blind-coder/SpaceTrader

Contributing
============

I am not a professional developer, but I am heager to learn. I need something to work on my (poor) python skills.

disclaimer: This is a toy project, early work in progress... It may never be finished and it may differ from original games.

But you are very welcome to help, if you want to (See CONTRIBUTING.rst).


Use and tests
=============

At the moment, you'll need:


.. code-block:: bash

    .
    ├── core.py
    ├── constants.py
    └── main.py


I try to use as less additionnal python3 modules as possible, but you will need these:

.. code-block:: python

    PySimpleGUI>=4.41.2


To run (and test), simply:

.. code-block:: bash

    python3 main.py


Select Game, New. Navigate through the Galactic Map, set a destination, then have a look at Trading Tab, if you want to earn some profit... (Buy cargo, next turn, Sell cargo, repeat *ad nauseam*)

