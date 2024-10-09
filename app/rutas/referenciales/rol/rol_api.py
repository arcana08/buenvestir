from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.rol.RolDao import RolDao

rolapi = Blueprint('rolapi', __name__)

# Trae todos los roles
@rolapi.route('/roles', methods=['GET'])
def getRoles():
    roldao = RolDao()

    try:
        roles = roldao.getRoles()

        return jsonify({
            'success': True,
            'data': roles,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todos los roles: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@rolapi.route('/roles/<int:rol_id>', methods=['GET'])
def getRol(rol_id):
    roldao = RolDao()

    try:
        rol = roldao.getRolById(rol_id)

        if rol:
            return jsonify({
                'success': True,
                'data': rol,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el rol con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener rol: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega un nuevo rol
@rolapi.route('/roles', methods=['POST'])
def addRol():
    data = request.get_json()
    roldao = RolDao()

    campos_requeridos = ['nombre']

    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(data[campo].strip()) == 0:
            return jsonify({
                            'success': False,
                            'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
                            }), 400

    try:
        nombre = data['nombre'].upper()
        rol_id = roldao.guardarRol(nombre)
        if rol_id is not None:
            return jsonify({
                'success': True,
                'data': {'id': rol_id, 'nombre': nombre},
                'error': None
            }), 201
        else:
            return jsonify({ 'success': False, 'error': 'No se pudo guardar el rol. Consulte con el administrador.' }), 500
    except Exception as e:
        app.logger.error(f"Error al agregar rol: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@rolapi.route('/roles/<int:rol_id>', methods=['PUT'])
def updateRol(rol_id):
    data = request.get_json()
    roldao = RolDao()

    campos_requeridos = ['nombre']

    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(data[campo].strip()) == 0:
            return jsonify({
                            'success': False,
                            'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
                            }), 400
    nombre = data['nombre']
    try:
        if roldao.updateRol(rol_id, nombre.upper()):
            return jsonify({
                'success': True,
                'data': {'id': rol_id, 'nombre': nombre},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el rol con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar rol: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@rolapi.route('/roles/<int:rol_id>', methods=['DELETE'])
def deleteRol(rol_id):
    roldao = RolDao()

    try:
        if roldao.deleteRol(rol_id):
            return jsonify({
                'success': True,
                'mensaje': f'Rol con ID {rol_id} eliminado correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el rol con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar rol: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500
