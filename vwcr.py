#!/usr/bin/env python

"""
VWCR - VoidWarranties Cash Register
As the name suggests, a cash register program written with VoidWarranties in mind.
"""

__title__ = "VWCR"
__version__ = "2.0"
__license__ = "GPLv3"
__author__ = "Koert Loret"
__email__ = "koert@dumsoft.be"

# standard libraries
# non-standard libraries
# custom libraries
import mainwindow

class VWCR():
    """
    The main program
    """
    def __init__(self):
        # Where is the database located?
        self.source = "MALMan"
        self.running = True
        self.StartMainWindow()

    def GetConfig(self):
        """mainwindow
        Reads the configuration file.
        """
        pass
    
    def StartMainWindow(self):
        while self.running:
            self.mainwindow = mainwindow.MainWindow(self)
            if self.mainwindow.result == "Close":
                # Break the loop and thus end the program
                self.running = False
            if self.mainwindow.result == "Order":
                # Open a window to take the order
                # Window not written yet
                pass
            if self.mainwindow.result == "Stock":
                # Open a window that shows the stock
                # Window not written yet
                pass
            if self.mainwindow.result == "Report":
                # Open a widow that shows the report
                # Window not written yet
                pass
            

if __name__ == "__main__":
    print "We have ignition!"
    vwcr = VWCR()   
