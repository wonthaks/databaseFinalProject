from collections import namedtuple

from flask import g
from flask import escape
from flask import render_template
from flask import request

from inventory.db import get_db, execute
from inventory.validate import validate_field, render_errors
from inventory.validate import NAME_RE, INT_RE, DATE_RE

def staff(conn):
    return execute(conn, "SELECT s.staffID as 'Staff ID', s.name as 'Name', s.age as 'Age', s.department as 'Department', s.address as 'Address', s.phoneNum as 'Phone Number' FROM Staff AS s")
def getTotalPrice(conn):
    staffID = request.args.get('staffID')
    return execute(conn, "SELECT SUM(i.price) as totalPrice FROM Staff as s INNER JOIN Uses as u ON s.staffID = u.staffID INNER JOIN Items as i ON u.itemID = i.itemID WHERE s.staffID = "+staffID+" AND u.dateReturned IS NULL GROUP BY s.staffID")
def getStaffInfo(conn):
    staffID = request.args.get('staffID')
    return execute(conn, "SELECT s.staffID, s.name, s.department FROM Staff as s INNER JOIN Uses as u ON s.staffID = u.staffID INNER JOIN Items as i ON u.itemID = i.itemID WHERE s.staffID = "+staffID+" GROUP BY s.staffID")
def getHistory(conn):
    staffID = request.args.get('staffID')
    return execute(conn, "SELECT i.itemID as 'Item ID', i.type as 'Item Type', u.dateBorrowed as 'Date borrowed', u.dateReturned as 'Date returned' FROM ITEMS as i INNER JOIN Uses as u ON i.itemID = u.itemID INNER JOIN Staff as s ON u.staffID = s.staffID WHERE s.staffID = "+staffID+" ORDER BY u.dateReturned IS NULL DESC, u.dateBorrowed DESC")
def returnItem(conn):
    itemID = request.args.get('itemID')
    staffID = request.args.get('staffID')
    dateBorrowed = request.args.get('dateBorrowed')
    execute(conn, "UPDATE Uses SET dateReturned = DATE('now') WHERE Uses.itemID = "+itemID+" AND Uses.staffID = "+staffID+" AND DATE(Uses.dateBorrowed) = ?", [dateBorrowed])
    execute(conn, "UPDATE Items SET borrowedNum = (Items.borrowedNum - 1) WHERE Items.itemID = "+itemID+"")

def views(bp):
    @bp.route("/staff/show")
    def _staff():
        with get_db() as conn:
            rows = staff(conn)
        return render_template("staffPage.html", name="staff", rows=rows)

def history(bp):
    @bp.route("/staff/itemHistory")
    def _getHistory():
        with get_db() as conn:
            if getTotalPrice(conn) != []:
                totalPriceInfo = getTotalPrice(conn)[0]['totalPrice']
            else:
                totalPriceInfo = 0
            staffInfo = getStaffInfo(conn)[0]
            rows = getHistory(conn)
        return render_template("staffHistory.html", name="history", rows=rows, staffID=staffInfo['staffID'], staffName=staffInfo['name'], department=staffInfo['department'], totalPriceInfo = totalPriceInfo)

def returnStaffItem(bp):
    @bp.route("/staff/return")
    def _returnItem():
        with get_db() as conn:
            returnItem(conn)
            if getTotalPrice(conn) != []:
                totalPriceInfo = getTotalPrice(conn)[0]['totalPrice']
            else:
                totalPriceInfo = 0
            staffInfo = getStaffInfo(conn)[0]
            rows = getHistory(conn)
        return render_template("staffHistory.html", type="report", rows=rows, staffID=staffInfo['staffID'], staffName=staffInfo['name'], department=staffInfo['department'], totalPriceInfo = totalPriceInfo)
