===================
python3 SpaceTrader
===================

.. meta::
    :date: 2018-12-19
    :status: work in progress
    :version: $Id: README.rst 1552.develop.3 $
    :licence: SPDX-License-Identifier: BSD-2-Clause


A little game inspired by `Space Trader <https://www.benjamin-schieder.de/androidspacetrader.html>`_, in python3/Tk, as a toy project.

Turn-based 'strategy' game. This is neither a python port nor a full copy of original(s) Space Trader.

``Space Trader is an Android strategy game in space by Benjamin Schieder. It is a port of the Palm Pilot game "Space Trader" by Pieter Spronck, which is inspired by David J. Webb’s PalmPilot game "SolarWars" (which in turn is based on Matt Lee’s game "DopeWars") and the 80’s classic 3D strategy game "Elite" (though it does not have Elite’s 3D flight mode).``


References
==========

* https://www.benjamin-schieder.de/androidspacetrader.html (Android version Homepage)

* https://github.com/blind-coder/SpaceTrader (Android Java source code)

* http://www.spronck.net/spacetrader/STFrames.html (Original SpaceTrader homepage and C source code)


Use and tests
=============

At the moment, you'll need:


.. code-block:: bash

    .
    ├── core.py
    ├── constants.py
    ├── sgui.py
    └── main.py


I try to use as less additionnal python3 modules as possible, but you will need these:

.. code-block:: python

    PySimpleGUI>=4.41.2
    python3 -m pip install PySimpleGUI


You may also need to install Tkinter:

.. code-block:: bash

    apt install python3-tk


To run (and test), simply:

.. code-block:: bash

    python3 main.py


Select Game -> New. Navigate through the Galactic Map, set a destination, then have a look at Trading Tab, if you want to earn some profit... (Select goods, Buy cargo, next turn, Sell cargo, repeat *ad nauseam*... And watch for your fuel!!)


Contributing
============

Disclaimer: This is a toy project, early work in progress... It may never be finished and it will differ from original games.

I am not a professional developer, but I am heager to learn. I needed something to work on my (poor) python skills.

That being said, you are *very welcome* to help, if you want to (See CONTRIBUTING.rst).


