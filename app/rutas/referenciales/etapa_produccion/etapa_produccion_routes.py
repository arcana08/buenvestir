from flask import Blueprint, render_template

epromod = Blueprint('etapa_produccion', __name__, template_folder='templates')

@epromod.route('/etapa_produccion-index')
def etapa_produccionIndex():
    return render_template('etapa_produccion-index.html')