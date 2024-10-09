from flask import Blueprint, render_template

usermod = Blueprint('usuario', __name__, template_folder='templates')

@usermod.route('/usuario-index')
def usuarioIndex():
    return render_template('usuario-index.html')