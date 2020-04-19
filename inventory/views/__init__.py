
from flask import Blueprint

from inventory.views import index
from inventory.views import sailors
from inventory.views import boats
from inventory.views import voyages

blueprint = Blueprint('views', __name__)
index.views(blueprint)
sailors.views(blueprint)
boats.views(blueprint)
voyages.views(blueprint)

def init_app(app):
    app.register_blueprint(blueprint)
    app.add_url_rule('/', endpoint='index')
