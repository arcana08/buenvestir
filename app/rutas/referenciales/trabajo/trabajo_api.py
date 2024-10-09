from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.trabajo.TrabajoDao import TrabajoDao

traapi = Blueprint('traapi', __name__)

# Trae todos los trabajos
@traapi.route('/trabajos', methods=['GET'])
def getTrabajos():
    trabajodao = TrabajoDao()

    try:
        trabajos = trabajodao.getTrabajos()

        return jsonify({
            'success': True,
            'data': trabajos,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todos los trabajos: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@traapi.route('/trabajos/<int:trabajo_id>', methods=['GET'])
def getTrabajo(trabajo_id):
    trabajodao = TrabajoDao()

    try:
        trabajo = trabajodao.getTrabajoById(trabajo_id)

        if trabajo:
            return jsonify({
                'success': True,
                'data': trabajo,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el trabajo con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener trabajo: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega un nuevo trabajo
@traapi.route('/trabajos', methods=['POST'])
def addTrabajo():
    data = request.get_json()
    trabajodao = TrabajoDao()

    campos_requeridos = ['nombre']

    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(data[campo].strip()) == 0:
            return jsonify({
                            'success': False,
                            'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
                            }), 400

    try:
        nombre = data['nombre'].upper()
        trabajo_id = trabajodao.guardarTrabajo(nombre)
        if trabajo_id is not None:
            return jsonify({
                'success': True,
                'data': {'id': trabajo_id, 'nombre': nombre},
                'error': None
            }), 201
        else:
            return jsonify({ 'success': False, 'error': 'No se pudo guardar el trabajo. Consulte con el administrador.' }), 500
    except Exception as e:
        app.logger.error(f"Error al agregar trabajo: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@traapi.route('/trabajos/<int:trabajo_id>', methods=['PUT'])
def updateTrabajo(trabajo_id):
    data = request.get_json()
    trabajodao = TrabajoDao()

    campos_requeridos = ['nombre']

    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(data[campo].strip()) == 0:
            return jsonify({
                            'success': False,
                            'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
                            }), 400
    nombre = data['nombre']
    try:
        if trabajodao.updateTrabajo(trabajo_id, nombre.upper()):
            return jsonify({
                'success': True,
                'data': {'id': trabajo_id, 'nombre': nombre},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el trabajo con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar trabajo: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@traapi.route('/trabajos/<int:trabajo_id>', methods=['DELETE'])
def deleteTrabajo(trabajo_id):
    trabajodao = TrabajoDao()

    try:
        if trabajodao.deleteTrabajo(trabajo_id):
            return jsonify({
                'success': True,
                'mensaje': f'Trabajo con ID {trabajo_id} eliminado correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el trabajo con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar trabajo: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500
