from flask import Blueprint, render_template

conmod = Blueprint('control_de_calidad', __name__, template_folder='templates')

@conmod.route('/control-index')
def controlIndex():
    return render_template('control-index.html')