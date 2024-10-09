from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.deposito.DepositoDao import DepositoDao

depoapi = Blueprint('depoapi', __name__)

# Trae todos los datos
@depoapi.route('/depositos', methods=['GET'])
def getDepositos():
    depdao = DepositoDao()

    try:
        depositos = depdao.getDepositos()

        return jsonify({
            'success': True,
            'data': depositos,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todos los datos: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@depoapi.route('/depositos/<int:deposito_id>', methods=['GET'])
def getDeposito(deposito_id):
    depdao = DepositoDao()

    try:
        deposito = depdao.getDepositoById(deposito_id)

        if deposito:
            return jsonify({
                'success': True,
                'data': deposito,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el depósito con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener depósito: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega un nuevo depósito
@depoapi.route('/depositos', methods=['POST'])
def addDeposito():
    data = request.get_json()
    depdao = DepositoDao()

    campos_requeridos = ['descripcion']

    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(data[campo].strip()) == 0:
            return jsonify({
                            'success': False,
                            'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
                            }), 400

    try:
        descripcion = data['descripcion'].upper()
        deposito_id = depdao.guardarDeposito(descripcion)
        if deposito_id is not None:
            return jsonify({
                'success': True,
                'data': {'id': deposito_id, 'descripcion': descripcion},
                'error': None
            }), 201
        else:
            return jsonify({ 'success': False, 'error': 'No se pudo guardar el depósito. Consulte con el administrador.' }), 500
    except Exception as e:
        app.logger.error(f"Error al agregar depósito: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@depoapi.route('/depositos/<int:deposito_id>', methods=['PUT'])
def updateDeposito(deposito_id):
    data = request.get_json()
    depdao = DepositoDao()

    campos_requeridos = ['descripcion']

    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(data[campo].strip()) == 0:
            return jsonify({
                            'success': False,
                            'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
                            }), 400
    descripcion = data['descripcion']
    try:
        if depdao.updateDeposito(deposito_id, descripcion.upper()):
            return jsonify({
                'success': True,
                'data': {'id': deposito_id, 'descripcion': descripcion},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el depósito con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar depósito: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@depoapi.route('/depositos/<int:deposito_id>', methods=['DELETE'])
def deleteDeposito(deposito_id):
    depdao = DepositoDao()

    try:
        if depdao.deleteDeposito(deposito_id):
            return jsonify({
                'success': True,
                'mensaje': f'Depósito con ID {deposito_id} eliminado correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el depósito con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar depósito: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500
