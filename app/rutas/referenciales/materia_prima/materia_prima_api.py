from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.materia_prima.Materia_primaDao import Materia_primaDao

matapi = Blueprint('matapi', __name__)

# Trae todas las materia_primas
@matapi.route('/materia_primas', methods=['GET'])
def getMateria_primas():
    perdao = Materia_primaDao()

    try:
        materia_primas = perdao.getMateria_primas()
        
        return jsonify({
            'success': True,
            'data': materia_primas,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todas las materia_primas: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@matapi.route('/materia_primas/<int:materia_prima_id>', methods=['GET'])
def getMateria_prima(materia_prima_id):
    perdao = Materia_primaDao()

    try:
        materia_prima = perdao.getMateria_primaById(materia_prima_id)
        
        if materia_prima:
            return jsonify({
                'success': True,
                'data': materia_prima,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la materia_prima con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener materia_prima: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega una nueva materia_prima
@matapi.route('/materia_primas', methods=['POST'])
def addMateria_prima():
    data = request.get_json()
    perdao = Materia_primaDao()
    
    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['nombre', 'color', 'umedida', 'cantidad', 'categoria']

    # Verificar si faltan campos o son vacíos
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(str(data[campo]).strip()) == 0:
            return jsonify({
                            'success': False,
                            'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
                            }), 400

    try:
        nombre = data['nombre'].upper()
        color = data['color'].upper()
        umedida = data['umedida']
        cantidad = data['cantidad']
        categoria = data['categoria']

        materia_prima_id = perdao.guardarMateria_prima(nombre, color, umedida, cantidad, categoria)
        if materia_prima_id is not None:
            return jsonify({
                'success': True,
                'data': {
                    'id': materia_prima_id,
                    'nombre': nombre,
                    'color': color,
                    'umedida': umedida,
                    'cantidad': cantidad,
                    'categoria': categoria
                    
                },
                'error': None
            }), 201
        else:
            return jsonify({'success': False, 'error': 'No se pudo guardar la materia_prima. Consulte con el administrador.'}), 500
    except Exception as e:
        app.logger.error(f"Error al agregar materia_prima: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@matapi.route('/materia_primas/<int:materia_prima_id>', methods=['PUT'])
def updateMateria_prima(materia_prima_id):
    data = request.get_json()
    perdao = Materia_primaDao()
    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['nombre', 'color', 'umedida', 'cantidad', 'categoria']

    # Verificar si faltan campos o son vacíos
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(str(data[campo]).strip()) == 0:
            return jsonify({
                            'success': False,
                            'error': f'El campo {campo} {data} es obligatorio y no puede estar vacío.'
                            }), 400

    nombre = data['nombre'].upper()
    color = data['color'].upper()
    umedida = data['umedida']
    cantidad = data['cantidad']
    categoria = data['categoria']

    try:
        if perdao.updateMateria_prima(materia_prima_id, nombre, color, umedida, cantidad, categoria):
            return jsonify({
                'success': True,
                'data': {
                    'id': materia_prima_id,
                    'nombre': nombre,
                    'color': color,
                    'umedida': umedida,
                    'cantidad': cantidad,
                    'categoria': categoria
                },
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la materia_prima con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar materia_prima: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@matapi.route('/materia_primas/<int:materia_prima_id>', methods=['DELETE'])
def deleteMateria_prima(materia_prima_id):
    perdao = Materia_primaDao()

    try:
        if perdao.deleteMateria_prima(materia_prima_id):
            return jsonify({
                'success': True,
                'mensaje': f'Materia_prima con ID {materia_prima_id} eliminada correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la materia_prima con el ID proporcionado o no se pudo eliminar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al eliminar materia_prima: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500
