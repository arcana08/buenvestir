from flask import Blueprint, render_template

presmod = Blueprint('presupuesto', __name__, template_folder='templates')

@presmod.route('/presupuesto-index')
def presupuestoIndex():
    return render_template('presupuesto-index.html')