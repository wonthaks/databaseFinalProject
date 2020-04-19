
from flask import Blueprint

from inventory.views import index
from inventory.views import staff
from inventory.views import items
from inventory.views import uses

blueprint = Blueprint('views', __name__)
index.views(blueprint)

staff.views(blueprint)
staff.history(blueprint)
staff.returnStaffItem(blueprint)

items.views(blueprint)
items.report(blueprint)
items.raiseStockCount(blueprint)
items.lowerStockCount(blueprint)
items.addItem(blueprint)

uses.views(blueprint)
uses.returnU(blueprint)
uses.returnI(blueprint)
uses.showOldest(blueprint)
uses.borrowItem(blueprint)

def init_app(app):
    app.register_blueprint(blueprint)
    app.add_url_rule('/', endpoint='index')
