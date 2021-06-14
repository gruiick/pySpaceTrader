#!/usr/bin/env python3
# coding: utf-8
#
# $Id: testcli_3.py 1303.v0.2-dev.1 $
# SPDX-License-Identifier: BSD-2-Clause

"""
some tests
"""

from dataclasses import dataclass
from pprint import pprint

import constants

@dataclass
class BankAccount:
    """
    Quick & Dirty bank account log
    """
    owner: str
    log: []
    cash: float = constants.CASH

@dataclass
class Captain:
    """
    This is captain speaking
    """
    name: str = 'Speaking'
    # homeworld: () = None
    # location: () = None
    # destination: () = None
    # ship: () = None
    account: () = None
    # cash: float = constants.CASH

    @property
    def balance(self):
        # self.cash replace initial balance
        _lst = []
        liste_pods = [x for x in self.ship.cargo.keys() if self.ship.cargo[x]['value'] is not None]
        for idx in liste_pods:
            _lst.append(self.ship.cargo[idx]['value'])

        cargo_value = sum(_lst)
        balance = cargo_value + self.account.cash

        return balance


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

if __name__ == '__main__':
    """ """
    captain = Captain()
    captain.account = BankAccount(captain.name, [])

    invoice = Transaction('fuel', 13.00, 12.00)
    inv2 = Transaction('fur', 7.00, 10)

    captain.account.log.append(invoice)
    captain.account.log.append(inv2)

    pprint(captain)
    pprint(captain.account.log)
    for item in captain.account.log:
        print(item.total_value)


