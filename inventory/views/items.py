from collections import namedtuple

from flask import render_template
from flask import request
from flask import escape

from inventory.db import get_db, execute

def items(conn):
    return execute(conn, "SELECT i.itemID as ID, i.type as TYPE, i.manufacturer as MANUFACTURER FROM Items AS i")
def getItemInformation(conn):
    id = request.args.get('itemID')
    return execute(conn, "SELECT i.itemID, i.type, i.manufacturer, i.stockNum, i.borrowedNum, i.price, i.price * i.stockNum as totalPrice FROM Items as i WHERE i.itemID = " +id+"")
def itemsReport(conn):
    id = request.args.get('itemID')
    return execute(conn, "SELECT s.staffID as 'Staff ID', s.name as 'Staff Name', u.dateBorrowed as 'Date borrowed', u.dateReturned as 'Date returned' FROM ITEMS as i INNER JOIN Uses as u ON i.itemID = u.itemID INNER JOIN Staff as s ON u.staffID = s.staffID WHERE i.itemID = "+id+" ORDER BY u.dateReturned IS NULL DESC, u.dateBorrowed DESC")
def increaseCount(conn):
    id = request.args.get('itemID')
    execute(conn, "UPDATE Items SET stockNum = (Items.stockNum + 1) WHERE Items.itemID = "+id+"")
    return True
def decreaseCount(conn):
    id = request.args.get('itemID')
    stockNum = request.args.get('stockNum')
    borrowedNum = request.args.get('borrowedNum')

    if borrowedNum >= stockNum:
        return False
    else:
        execute(conn, "UPDATE Items SET stockNum = (Items.stockNum - 1) WHERE Items.itemID = "+id+"")
        return True
def addItemToInventory(conn):
    type = request.args.get('itemType')
    price = request.args.get('itemPrice')
    stockNum = request.args.get('itemStockNum')
    manu = request.args.get('itemManufacturer')
    execute(conn, "INSERT INTO Items (stockNum, borrowedNum, price, manufacturer, type) VALUES (?, 0, ?, ?, ?)", [stockNum, price, manu, type])
    return True

def views(bp):
    @bp.route("/items/show")
    def _items():
        with get_db() as conn:
            rows = items(conn)
        return render_template("itemsPage.html", name="items", rows=rows)

def report(bp):
    @bp.route("/items/report")
    def _report():
        with get_db() as conn:
            rows = itemsReport(conn)
            itemInfo = getItemInformation(conn)[0]
        return render_template("reportPage.html", type="report", rows=rows, itemType=itemInfo['type'], id=itemInfo['itemID'], manu=itemInfo['manufacturer'],
        stockN=itemInfo['stockNum'], borrowedN=itemInfo['borrowedNum'], price=itemInfo['price'], totalP=itemInfo['totalPrice'])

def raiseStockCount(bp):
    @bp.route("/items/increaseItemCount")
    def _raiseStockCount():
        with get_db() as conn:
            success = increaseCount(conn)
            rows = itemsReport(conn)
            itemInfo = getItemInformation(conn)[0]
        return render_template("reportPageAfterRaise.html", name="items", rows=rows, success=success, itemType=itemInfo['type'], id=itemInfo['itemID'], manu=itemInfo['manufacturer'],
        stockN=itemInfo['stockNum'], borrowedN=itemInfo['borrowedNum'], price=itemInfo['price'], totalP=itemInfo['totalPrice'])

def lowerStockCount(bp):
    @bp.route("/items/decreaseItemCount")
    def _lowerStockCount():
        with get_db() as conn:
            success = decreaseCount(conn)
            rows = itemsReport(conn)
            itemInfo = getItemInformation(conn)[0]
        return render_template("reportPageAfterLower.html", name="items", rows=rows, success=success, itemType=itemInfo['type'], id=itemInfo['itemID'], manu=itemInfo['manufacturer'],
        stockN=itemInfo['stockNum'], borrowedN=itemInfo['borrowedNum'], price=itemInfo['price'], totalP=itemInfo['totalPrice'])

def addItem(bp):
    @bp.route("/items/addItem")
    def _addItem():
        with get_db() as conn:
            success = addItemToInventory(conn)
            rows = items(conn)
        return render_template("itemsPageAfterAdd.html", name="items", rows=rows, success=success)
