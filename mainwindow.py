#!/usr/bin/env python

"""
This file is part of VWCR
"""

__author__ = "Koert Loret"
__license__ = "GPLv3"

# standard libraries
import gtk
# non-standard libraries
# custom libraries

class MainWindow():
    """
    The main window of VWCR.
    From this window you can choose what kind of action you want to perform.
    """
    def __init__(self, vwcr):
        self.vwcr = vwcr
        self.result = "No result yet"
        
        # Create the window itself
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("destroy",  gtk.main_quit)
        self.window.maximize()
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.set_title("VWCR")
        
        # Create the buttons that all users can use
        # Close button
        closebutton = gtk.Button("Close")
        closebutton.connect("clicked", self.Stop)
        # Order button
        orderbutton = gtk.Button("Order")
        orderbutton.connect("clicked", self.Order)
        # Stock button
        stockbutton = gtk.Button("Stock")
        orderbutton.connect("clicked", self.Stock)
        # Report button
        reportbutton = gtk.Button("Report")
        reportbutton.connect("clicked", self.Report)
        # Create a box to hold the buttons, then add the buttons
        normalbox = gtk.HBox()
        normalbox.pack_start(orderbutton)
        normalbox.pack_start(stockbutton)
        normalbox.pack_start(reportbutton)
        normalbox.pack_start(closebutton)
        
        
        # Create the buttons that only privileged users can use
        # Create a box to hold the buttons, then add the buttons
        privilegedbox = gtk.HBox()
        
        # Create a box to hold both buttonboxes
        allbox = gtk.VBox()
        allbox.pack_start(normalbox)
        allbox.pack_start(privilegedbox)
        
        # Add allbox to the window, then display the window
        self.window.add(allbox)
        self.window.show_all()
        
        # Start the window
        gtk.main()
    
    def Stop(self, widget):
        self.result = "Close"
        self.Close()
    
    def Order(self, widget):
        self.result = "Order"
        self.Close()
        
    def Stock(self, widget):
        self.result = "Stock"
        self.Close()
        
    def Report(self, widget):
        self.result = "Report"
        self.Close()
        
    def Close(self):
        """
        Closes the window
        """
        self.window.destroy()
    
if __name__ == "__main__":
    print "You should be trying to run anything in here directly."