from flask import Blueprint, render_template

catmod = Blueprint('categoria', __name__, template_folder='templates')

@catmod.route('/categoria-index')
def categoriaIndex():
    return render_template('categoria-index.html')