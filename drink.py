#! /usr/bin/env python

"""
This file is part of VWCR
"""

__author__ = "Koert Loret"
__license__ = "GPLv3"

# standard libraries
# non-standard libraries
# custom libraries
import gtk

class Drink():
    """
    Describes a drink or snack
    """

    def __init__(self):
        self.name = ""
        self.price = ""
        self.barcode = ""
        self.category = ""
        self.owner = "" # bad name, I should come up with something different
        self.stock = 0
        self.minimum = 0
 
