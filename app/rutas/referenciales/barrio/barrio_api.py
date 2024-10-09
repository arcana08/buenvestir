from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.barrio.BarrioDao import BarrioDao

barapi = Blueprint('barapi', __name__)

# Trae todas los barrios
@barapi.route('/barrios', methods=['GET'])
def getBarrios():
    bardao = BarrioDao()

    try:
        barrios = bardao.getBarrios()

        return jsonify({
            'success': True,
            'data': barrios,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todos los barrios: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@barapi.route('/barrios/<int:barrio_id>', methods=['GET'])
def getBarrio(barrio_id):
    bardao = BarrioDao()

    try:
        barrio = bardao.getBarrioById(barrio_id)

        if barrio:
            return jsonify({
                'success': True,
                'data': barrio,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró elbarrio con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener barrio: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega una nueva barrio
@barapi.route('/barrios', methods=['POST'])
def addBarrio():
    data = request.get_json()
    bardao = BarrioDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['descripcion','ciudad']

    # Verificar si faltan campos o son vacíos
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(str(data[campo]).strip()) == 0:
            return jsonify({
                            'success': False,
                            'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
                            }), 400

    try:
        descripcion = data['descripcion'].upper()
        ciudad_id = data['ciudad']
        barrio_id = bardao.guardarBarrio(descripcion,ciudad_id)
        if barrio_id is not None:
            return jsonify({
                'success': True,
                'data': {'id': barrio_id, 'descripcion': descripcion, 'ciudad': ciudad_id},
                'error': None
            }), 201
        else:
            return jsonify({ 'success': False, 'error': 'No se pudo guardar el barrio. Consulte con el administrador.' }), 500
    except Exception as e:
        app.logger.error(f"Error al agregar barrio: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@barapi.route('/barrios/<int:barrio_id>', methods=['PUT'])
def updateBarrio(barrio_id):
    data = request.get_json()
    bardao = BarrioDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['descripcion','ciudad']

    # Verificar si faltan campos o son vacíos
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(str(data[campo]).strip()) == 0:
            return jsonify({
                            'success': False,
                            'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
                            }), 400
    descripcion = data['descripcion']
    ciudad_id = data['ciudad']
    try:
        if bardao.updateBarrio(barrio_id, descripcion.upper(),ciudad_id):
            return jsonify({
                'success': True,
                'data': {'id': barrio_id, 'descripcion': descripcion,'ciudad': ciudad_id},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el barrio con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar barrio: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@barapi.route('/barrios/<int:barrio_id>', methods=['DELETE'])
def deleteBarrio(barrio_id):
    bardao = BarrioDao()

    try:
        # Usar el retorno de eliminarBarrio para determinar el éxito
        if bardao.deleteBarrio(barrio_id):
            return jsonify({
                'success': True,
                'mensaje': f'Barrio con ID {barrio_id} eliminada correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el barrio con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar barrio: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500