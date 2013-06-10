#!/usr/bin/env python
# coding=UTF8

import pygtk
pygtk.require("2.0")
import gtk
import threading
import requests
import config
import nixies

class Drink():
    """ Definition of a consumption, usually but not always a drink """
    def __init__(self, id="", name="", barcode="", price=0, type="", user=""):
        self.id = id
        self.name = name
        self.barcode = barcode
        self.price = price
        self.type = type
        self.user = user

#############
# API HOOKS #
#############
def request(method, uri, data=None, params=None):
    function = getattr(requests, method)
    return function(config['serveradress'] + uri, auth=(config['api_user'], config['api_password']), verify=config['certificate'], data=data, params=params)

def GetStockList():
    response = request('get', 'api/stock')
    stock = response.json()
    # the next line sorts the stocklist by category first, name second
    stock = sorted(stock, key=lambda field: "%s %s" % (field['category'], field['name']))
    StockList = [ Drink(
            id = int(stockitem['id']),
            name = stockitem['name'],
            price = float(stockitem['price']),
            type = stockitem['category']
        ) for stockitem in stock ]
    return StockList

def GetUserList():
    response = request('get', 'api/user')
    return response.json()
    
def Authenticate(user_id, password):
    url = 'api/user/' + str(user_id)
    values = {'password': password}
    response= request('get', url, params=values)
    return response.text
    
def RegisterPurchase(item, user_id=None):
    values = {'item_id' : item.id }
    if user_id:
        values['user_id'] = user_id
    response = request('post', 'api/purchase', data=values)
    
###############
# WINDOW CLASSES #
###############
class PauseFunction(threading.Thread):
    def run(self):
        while MainWindow.BuyerWindow.get_visible():
            pass
        if MainWindow.Buyer <> ("NoUserSelected",  "SoFar"):
            MainWindow.CurrentDrink.user = MainWindow.Buyer


class VWCR():
    """ The main window of VWCR """
    def Close(self,  widget):
        gtk.main_quit()

    def AccountPay(self,  widget):
        user_account_balance = Authenticate(self.SelectedUser[0], self.BuyerPass.get_text())
        if user_account_balance != 'False':
            if self.CurrentDrink.price <= float(user_account_balance):
                self.BuyerWindow.set_title("Betaald")
                MainWindow.Buyer = MainWindow.SelectedUser
                RegisterPurchase(self.CurrentDrink, MainWindow.Buyer[0])
                MainWindow.Buyer = ("NoUserSelected",  "SoFar")
                MainWindow.SelectedUser = ("NoUserSelected",  "SoFar")
                self.hide_buyer(widget)
            else:
                self.BuyerWindow.set_title("onvoldoende krediet")
        else:
            self.BuyerWindow.set_title("Gebruiker en paswoord komen niet overeen")

    def AuthenticateBuyer(self):
        self.Buyer = ("NoUserSelected",  "SoFar")
        self.MainWindow.hide()
        self.BuyerWindow.show_all()
        pause = PauseFunction()
        pause.start()

    def ReturnResult(self,  widget,  Answer):
        self.ConfirmWindow.hide()
        if Answer == "cancel":
            self.MainWindow.show()
        if Answer == "account":
            self.AuthenticateBuyer()
        if Answer == "cash":
            self.CurrentDrink.user = "Cash"
            RegisterPurchase(self.CurrentDrink)
            self.MainWindow.show()
        
    def SellDrink(self, widget, Item):
        self.CurrentDrink = Item
        self.MainWindow.hide()
        confirmtitle = Item.name + " ---------- " + str(Item.price) + " Euro"
        nixies.price(Item.price)
        self.ConfirmWindow.set_title(confirmtitle)
        self.ConfirmWindow.show_all()

    def hide_stock(self,  widget):
        self.StockWindow.hide()
        self.MainWindow.show()

    def hide_buyer(self,  widget):
        self.treeselection.unselect_all()
        self.BuyerPass.set_text("")
        self.BuyerWindow.hide()
        self.MainWindow.show()

    def ClickBuyerRow(self,  widget,  data=None):
        self.treeselection = self.BuyerView.get_selection()
        self.treeselection.set_mode(gtk.SELECTION_SINGLE)
        (model, iter) = self.treeselection.get_selected()
        id = model.get_value(iter, 0)
        name = model.get_value(iter, 1)
        user = [id,  name]
        self.SelectedUser = user

    def __init__(self):
        self.CurrentDrink = Drink()
        self.Buyer = ("NoUserSelected", "SoFar")
        # buyer window
        ### User List
        self.SelectedUser = ["NoUserSelected", "so far"]
        self.BuyerList = gtk.ScrolledWindow()
        self.BuyerList.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.BuyerRawList = gtk.ListStore(str, str)
        for user in GetUserList():
            self.BuyerRawList.append([user["id"], user["name"]])
        self.BuyerView = gtk.TreeView(self.BuyerRawList)
        selectedrow = self.BuyerView.get_selection()
        selectedrow.connect('changed', self.ClickBuyerRow)
        cell = gtk.CellRendererText()
        col = gtk.TreeViewColumn("id",  cell,  text=0)
        self.BuyerView.append_column(col)
        cell = gtk.CellRendererText()
        col = gtk.TreeViewColumn("naam",  cell,  text=1)
        self.BuyerView.append_column(col)
        self.BuyerList.add(self.BuyerView)
        ### Buttons and password field
        self.BuyerPassLabel = gtk.Label("Password")
        self.BuyerPass = gtk.Entry()
        self.BuyerPass.set_visibility(False)
        self.BuyerPay = gtk.Button("Betalen")
        self.BuyerPay.connect("clicked",  self.AccountPay)
        self.BuyerCancel = gtk.Button("Annuleren")
        self.BuyerCancel.connect("clicked",  self.hide_buyer)
        self.BuyerButtons = gtk.HBox()
        self.BuyerButtons.pack_start(self.BuyerPassLabel)
        self.BuyerButtons.pack_start(self.BuyerPass)
        self.BuyerButtons.pack_start(self.BuyerPay)
        self.BuyerButtons.pack_start(self.BuyerCancel)
        ### Buyer Window
        self.BuyerLayout = gtk.VBox()
        self.BuyerLayout.pack_start(self.BuyerList)
        self.BuyerLayout.pack_start(self.BuyerButtons)
        self.BuyerWindow = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.BuyerWindow.maximize()
        self.BuyerWindow.set_title("Identificatie")
        self.BuyerWindow.add(self.BuyerLayout)
    
        # order confirmation window
        self.ConfirmWindow = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.ButtonBox = gtk.HBox()
        self.Cash = gtk.Button("Cash")
        self.Cash.connect("clicked",  self.ReturnResult,  "cash")
        self.ButtonBox .pack_start(self.Cash)
        self.Account = gtk.Button("Rekening")
        self.Account.connect("clicked",  self.ReturnResult,  "account")
        self.ButtonBox.pack_start(self.Account)
        #self.ButtonBox.pack_start(self.Account)
        self.Cancel = gtk.Button("Annuleren")
        self.Cancel.connect("clicked",  self.ReturnResult,  "cancel")
        self.ButtonBox.pack_start(self.Cancel)
        self.ConfirmWindow.add(self.ButtonBox)
        self.ConfirmWindow.maximize()
        
        # main window
        self.MainWindow = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.MainWindow.connect("destroy",  self.Close)
        self.MainWindow.maximize()
        self.MainWindow.set_position(gtk.WIN_POS_CENTER)
        self.Title = "VWCR"
        self.MainWindow.set_title(self.Title)

        # The DrinkButtons
        self.StockList = GetStockList()
        self.OrderButtonRows = gtk.VBox()
        counter = len(self.StockList)
        rows = (counter/5) + 2
        i = 1
        while (rows > i):
            templist = []
            j = 1
            OrderButtonRow = gtk.HBox()
            while (j<6):
                listindex = (j + ((i-1)*5)) - 1
                try:
                     templist.append(self.StockList[int(listindex)])
                except:
                    blankdrink = Drink()
                    blankdrink.name = ""
                    templist.append(blankdrink)
                j = j + 1
            for item in templist:
                # we can't center multiline button labels, so we'll include spacers on both lines and set the font to monospace
                self.drinkbutton = gtk.Button("")
                if item.name:
                    if len(item.name) < 6:
                        namespacer = ((6 - len(item.name)) / 2 ) * ' '
                        pricespacer = ''
                    else:
                        namespacer = ''
                        pricespacer = (len(item.name) / 2 - 3) * ' '
                    label = namespacer + item.name + '\n' + pricespacer + '€ %.2f' % item.price
                else:
                    label = ""
                self.drinkbutton.child.set_markup('<span face="monospace">' + label + '</span>')
                colormap = self.drinkbutton.get_colormap()
                color = colormap.alloc_color("#F2F2A7")
                if item.type == "alcoholic drink":
                    color = colormap.alloc_color("#1BE0D6")
                elif item.type == "non-alcoholic drink":
                    color = colormap.alloc_color("#76F59E")
                elif item.type == "food":
                    color = colormap.alloc_color("#F2F2A7")
                style = self.drinkbutton.get_style().copy()
                style.bg[gtk.STATE_NORMAL] = color
                self.drinkbutton.set_style(style)
                self.drinkbutton.connect("clicked",  self.SellDrink, item)
                OrderButtonRow.pack_start(self.drinkbutton)
            self.OrderButtonRows.pack_start(OrderButtonRow)
            i = i + 1

        self.WindowLayout = gtk.VBox()
        self.WindowLayout.pack_start(self.OrderButtonRows)
        hseparator = gtk.HSeparator()
        self.WindowLayout.pack_start(hseparator, expand=False,  padding=3)
        self.WindowLayout.pack_start(self.ButtonBox)
        self.MainWindow.add(self.WindowLayout)
        self.MainWindow.show_all()
        
    def main(self):
        gtk.main()
    
#########
# START #
#########
if __name__ == "__main__":
    gtk.gdk.threads_init()
    MainWindow = VWCR()
    gtk.gdk.threads_enter()
    MainWindow.main()
    gtk.gdk.threads_leave()

