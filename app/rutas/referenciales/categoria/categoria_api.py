from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.categoria.CategoriaDao import CategoriaDao

catapi = Blueprint('catapi', __name__)

# Trae todos los datos
@catapi.route('/categorias', methods=['GET'])
def getCategorias():
    catdao = CategoriaDao()

    try:
        categorias = catdao.getCategorias()

        return jsonify({
            'success': True,
            'data': categorias,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todos los datos: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@catapi.route('/categorias/<int:categoria_id>', methods=['GET'])
def getCategoria(categoria_id):
    catdao = CategoriaDao()

    try:
        categoria = catdao.getCategoriaById(categoria_id)

        if categoria:
            return jsonify({
                'success': True,
                'data': categoria,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la categoria con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener categoria: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega una nueva categoria
@catapi.route('/categorias', methods=['POST'])
def addCategoria():
    data = request.get_json()
    catdao = CategoriaDao()

    campos_requeridos = ['descripcion']

    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(data[campo].strip()) == 0:
            return jsonify({
                            'success': False,
                            'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
                            }), 400

    try:
        descripcion = data['descripcion'].upper()
        categoria_id = catdao.guardarCategoria(descripcion)
        if categoria_id is not None:
            return jsonify({
                'success': True,
                'data': {'id': categoria_id, 'descripcion': descripcion},
                'error': None
            }), 201
        else:
            return jsonify({ 'success': False, 'error': 'No se pudo guardar la categoria. Consulte con el administrador.' }), 500
    except Exception as e:
        app.logger.error(f"Error al agregar categoria: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@catapi.route('/categorias/<int:categoria_id>', methods=['PUT'])
def updateCategoria(categoria_id):
    data = request.get_json()
    catdao = CategoriaDao()

    campos_requeridos = ['descripcion']

    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(data[campo].strip()) == 0:
            return jsonify({
                            'success': False,
                            'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
                            }), 400
    descripcion = data['descripcion']
    try:
        if catdao.updateCategoria(categoria_id, descripcion.upper()):
            return jsonify({
                'success': True,
                'data': {'id': categoria_id, 'descripcion': descripcion},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la categoria con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar categoria: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@catapi.route('/categorias/<int:categoria_id>', methods=['DELETE'])
def deleteCategoria(categoria_id):
    catdao = CategoriaDao()

    try:
        if catdao.deleteCategoria(categoria_id):
            return jsonify({
                'success': True,
                'mensaje': f'Categoria con ID {categoria_id} eliminada correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la categoria con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar categoria: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500
