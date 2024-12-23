from flask import Blueprint, render_template

prodmod = Blueprint('produccion', __name__, template_folder='templates')

@prodmod.route('/produccion-index')
def produccionIndex():
    return render_template('produccion-index.html')