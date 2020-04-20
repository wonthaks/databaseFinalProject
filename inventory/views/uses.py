
from collections import namedtuple

from flask import render_template
from flask import request
from flask import escape

from datetime import datetime
from inventory.db import get_db, execute

def returnItem(conn):
    itemID = request.args.get('itemID')
    staffID = request.args.get('staffID')
    dateBorrowed = request.args.get('dateBorrowed')
    execute(conn, "UPDATE Uses SET dateReturned = DATE('now') WHERE Uses.itemID = "+itemID+" AND Uses.staffID = "+staffID+" AND DATE(Uses.dateBorrowed) = ?", [dateBorrowed])
    execute(conn, "UPDATE Items SET borrowedNum = (Items.borrowedNum - 1) WHERE Items.itemID = "+itemID+"")
def itemsReport(conn):
    id = request.args.get('itemID')
    return execute(conn, "SELECT s.staffID as 'Staff ID', u.dateBorrowed as 'Date borrowed', u.dateReturned as 'Date returned' FROM ITEMS as i INNER JOIN Uses as u ON i.itemID = u.itemID INNER JOIN Staff as s ON u.staffID = s.staffID WHERE i.itemID = "+id+" ORDER BY u.dateReturned IS NULL DESC, u.dateBorrowed DESC")
def getItemInformation(conn):
    id = request.args.get('itemID')
    return execute(conn, "SELECT i.itemID, i.type, i.manufacturer, i.stockNum, i.borrowedNum, i.price, i.price * i.stockNum as totalPrice FROM Items as i WHERE i.itemID = "+id+"")
def uses(conn):
    return execute(conn, "SELECT u.itemID as 'Item ID', i.type as 'Item Type', u.staffID as 'Staff ID', s.name as 'Staff Name', u.dateBorrowed as 'Date borrowed', u.dateReturned as 'Date returned' FROM Items as i INNER JOIN Uses AS u ON i.itemID = u.itemID INNER JOIN Staff as s ON u.staffID = s.staffID ORDER BY u.dateReturned IS NULL DESC, u.dateBorrowed DESC")
def getOldestCount(conn):
    amount = request.args.get('amount-to-show')
    return execute(conn, "SELECT i.itemID as 'Item ID', i.type as 'Item Type', COUNT(i.itemID) as 'Total Uses' FROM Items as i INNER JOIN Uses as u ON i.itemID = u.itemID WHERE u.dateReturned IS NOT NULL GROUP BY i.itemID ORDER BY COUNT(i.itemID) ASC LIMIT "+amount+"")
def getOldestUses(conn):
    amount = request.args.get('amount-to-show')
    return execute(conn, "SELECT i.itemID as 'Item ID', i.type as 'Item Type', MAX(u.dateBorrowed) as 'Most Recent Date Used' FROM Items as i INNER JOIN Uses as u ON i.itemID = u.itemID WHERE u.dateReturned IS NOT NULL GROUP BY i.itemID ORDER BY MAX(u.dateBorrowed) ASC LIMIT "+amount+"")

def borrowItemToday(conn):
    staffID = request.args.get('staffID')
    itemID = request.args.get('itemID')

    foundItem = execute(conn, "SELECT * FROM Items WHERE Items.itemID = "+itemID+"")
    foundStaff = execute(conn, "SELECT * FROM Staff WHERE Staff.staffID = "+staffID+"")

    if foundItem == [] or foundStaff == []:
        return False
    else:
        if foundItem[0]['borrowedNum'] >= foundItem[0]['stockNum']:
            return False
        else:
            execute(conn, "INSERT INTO Uses (itemID, staffID, dateBorrowed, dateReturned) VALUES (?, ?, DATE('now'), NULL)", [itemID, staffID])
            execute(conn, "UPDATE Items SET borrowedNum = (Items.borrowedNum + 1) WHERE Items.itemID = "+itemID+"")
            return True

def views(bp):
    @bp.route("/uses/show")
    def _uses():
        with get_db() as conn:
            rows = uses(conn)
        return render_template("usesPage.html", name="uses", rows=rows)

def returnU(bp):
    @bp.route("/uses/returnUses")
    def _returnU():
        with get_db() as conn:
            returnItem(conn)
            rows = uses(conn)
        return render_template("usesPage.html", type="report", rows=rows)

def returnI(bp):
    @bp.route("/uses/return")
    def _returnI():
        with get_db() as conn:
            returnItem(conn)
            rows = itemsReport(conn)
            itemInfo = getItemInformation(conn)[0]
        return render_template("reportPage.html", type="report", rows=rows, itemType=itemInfo['type'], id=itemInfo['itemID'], manu=itemInfo['manufacturer'],
        stockN=itemInfo['stockNum'], borrowedN=itemInfo['borrowedNum'], price=itemInfo['price'], totalP=itemInfo['totalPrice'])

def showOldestItemsCount(bp):
    @bp.route("/uses/showOldestCount")
    def _showOldestCount():
        with get_db() as conn:
            rows = getOldestCount(conn)
        return render_template("usesCount.html", name="showOldestCount", rows=rows)

def showOldestItemsUses(bp):
    @bp.route("/uses/showOldestUsed")
    def _showOldestUses():
        with get_db() as conn:
            rows = getOldestUses(conn)
        return render_template("usesHistory.html", name="showOldestUsed", rows=rows)

def borrowItem(bp):
    @bp.route("/uses/borrowItem")
    def _borrowItem():
        with get_db() as conn:
            success = borrowItemToday(conn)
        return render_template("afterIndex.html", name="index", success=success)
