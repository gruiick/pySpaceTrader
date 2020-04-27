#!/usr/bin/env python3
# coding: utf-8
#
# $Id: testcli_0.py 1302 $
# SPDX-License-Identifier: BSD-2-Clause

"""
some tests
"""

import collections

from pprint import pprint

import constants

goods = constants.GOODS
print(list(enumerate(goods.keys())))
print(list(goods.keys()))
print(len(list(goods.keys())))
print(collections.Counter(goods.keys()))

