from flask import Blueprint, render_template

cosmod = Blueprint('costo', __name__, template_folder='templates')

@cosmod.route('/costo-index')
def costoIndex():
    return render_template('costo-index.html')