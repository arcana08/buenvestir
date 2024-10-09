from flask import Blueprint, render_template

tramod = Blueprint('trabajo', __name__, template_folder='templates')

@tramod.route('/trabajo-index')
def trabajoIndex():
    return render_template('trabajo-index.html')