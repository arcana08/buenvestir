from flask import Blueprint, render_template

funmod = Blueprint('funcionario', __name__, template_folder='templates')

@funmod.route('/funcionario-index')
def funcionarioIndex():
    return render_template('funcionario-index.html')