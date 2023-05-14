from flask import Blueprint
registry = Blueprint('registry', __name__)


@registry.route('/ixox')
def timeline():
    return f"You requested ixox\n"
    pass

@registry.route('/images')
def images():
    return "OK"
