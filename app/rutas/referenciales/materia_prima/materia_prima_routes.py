from flask import Blueprint, render_template

matmod = Blueprint('materia_prima', __name__, template_folder='templates')

@matmod.route('/materia_prima-index')
def materia_primaIndex():
    return render_template('materia_prima-index.html')