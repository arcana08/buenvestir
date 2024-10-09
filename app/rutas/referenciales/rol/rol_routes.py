from flask import Blueprint, render_template

rolmod = Blueprint('rol', __name__, template_folder='templates')

@rolmod.route('/rol-index')
def rolIndex():
    return render_template('rol-index.html')