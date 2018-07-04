#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from .. baseanalysis import BaseAnalyer


class kdj(BaseAnalyer):
    def __init__(self):
        pass

    def name(self):
        return "KDJ"

    def colnum_info(self):
        return (3, ("K", "D", "J"))
