from flask import Flask

app = Flask(__name__)

# Importar referenciales
from app.rutas.referenciales.ciudad.ciudad_routes import ciumod
from app.rutas.referenciales.pais.pais_routes import paimod
from app.rutas.referenciales.departamento.departamento_routes import depmod
from app.rutas.referenciales.barrio.barrio_routes import barmod
from app.rutas.referenciales.categoria.categoria_routes import catmod
from app.rutas.referenciales.deposito.deposito_routes import depomod
from app.rutas.referenciales.rol.rol_routes import rolmod
from app.rutas.referenciales.trabajo.trabajo_routes import tramod
from app.rutas.referenciales.etapa_produccion.etapa_produccion_routes import epromod
from app.rutas.referenciales.persona.persona_routes import permod
from app.rutas.referenciales.usuario.usuario_routes import usermod
from app.rutas.referenciales.funcionario.funcionario_routes import funmod
from app.rutas.referenciales.cliente.cliente_routes import climod
from app.rutas.referenciales.materia_prima.materia_prima_routes import matmod
from app.rutas.referenciales.producto.producto_routes import promod

# Lista de módulos referenciales
modulos_referenciales = [
    (ciumod, 'ciudad'),
    (paimod, 'pais'),
    (depmod, 'departamento'),
    (barmod, 'barrio'),
    (catmod, 'categoria'),
    (depomod, 'deposito'),
    (rolmod, 'rol'),
    (tramod, 'trabajo'),
    (epromod, 'etapa_produccion'),
    (permod, 'persona'),
    (usermod, 'usuario'),
    (funmod, 'funcionario'),
    (climod, 'cliente'),
    (matmod, 'materia_prima'),
    (promod, 'producto'),
]

# Registrar referenciales
modulo0 = '/referenciales'
for modulo, ruta in modulos_referenciales:
    app.register_blueprint(modulo, url_prefix=f'{modulo0}/{ruta}')

# Importar APIS
from app.rutas.referenciales.ciudad.ciudad_api import ciuapi
from app.rutas.referenciales.pais.pais_api import paiapi
from app.rutas.referenciales.departamento.departamento_api import depapi
from app.rutas.referenciales.barrio.barrio_api import barapi
from app.rutas.referenciales.categoria.categoria_api import catapi
from app.rutas.referenciales.deposito.deposito_api import depoapi
from app.rutas.referenciales.rol.rol_api import rolapi
from app.rutas.referenciales.trabajo.trabajo_api import traapi
from app.rutas.referenciales.etapa_produccion.etapa_produccion_api import eproapi
from app.rutas.referenciales.persona.persona_api import perapi
from app.rutas.referenciales.usuario.usuario_api import userapi
from app.rutas.referenciales.funcionario.funcionario_api import funapi
from app.rutas.referenciales.cliente.cliente_api import cliapi
from app.rutas.referenciales.materia_prima.materia_prima_api import matapi
from app.rutas.referenciales.producto.producto_api import proapi

# Lista de APIS
apis_v1 = [
    ciuapi,
    paiapi,
    depapi,
    barapi,
    catapi,
    depoapi,
    rolapi,
    traapi,
    eproapi,
    perapi,
    userapi,
    funapi,
    cliapi,
    matapi,
    proapi,
]

# Registrar APIS v1
version1 = '/api/v1'
for api in apis_v1:
    app.register_blueprint(api, url_prefix=version1)
