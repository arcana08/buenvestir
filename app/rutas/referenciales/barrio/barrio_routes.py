from flask import Blueprint, render_template

barmod = Blueprint('barrio', __name__, template_folder='templates')

@barmod.route('/barrio-index')
def barrioIndex():
    return render_template('barrio-index.html')