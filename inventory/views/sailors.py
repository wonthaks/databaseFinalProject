from collections import namedtuple

from flask import g
from flask import escape
from flask import render_template
from flask import request

from inventory.db import get_db, execute
from inventory.validate import validate_field, render_errors
from inventory.validate import NAME_RE, INT_RE, DATE_RE


def views(bp):

    @bp.route("/sailors")
    def _get_all_sailors():
        return 'not implemented'
