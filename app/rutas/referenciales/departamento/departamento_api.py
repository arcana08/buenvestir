from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.departamento.DepartamentoDao import DepartamentoDao

depapi = Blueprint('depapi', __name__)

# Trae todos los datos
@depapi.route('/departamentos', methods=['GET'])
def getDepartamentos():
    depdao = DepartamentoDao()

    try:
        departamentos = depdao.getDepartamentos()

        return jsonify({
            'success': True,
            'data': departamentos,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todos los datos: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@depapi.route('/departamentos/<int:departamento_id>', methods=['GET'])
def getDepartamento(departamento_id):
    depdao = DepartamentoDao()

    try:
        departamento = depdao.getDepartamentoById(departamento_id)

        if departamento:
            return jsonify({
                'success': True,
                'data': departamento,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el departamento con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener departamento: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega una nueva departamento
@depapi.route('/departamentos', methods=['POST'])
def addDepartamento():
    data = request.get_json()
    depdao = DepartamentoDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['descripcion','idpais']

    # Verificar si faltan campos o son vacíos
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(str(data[campo]).strip()) == 0:
            return jsonify({
                            'success': False,
                            'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
                            }), 400

    try:
        descripcion = data['descripcion'].upper()
        id_pais = data['idpais']
        departamento_id = depdao.guardarDepartamento(descripcion,id_pais)
        if departamento_id is not None:
            return jsonify({
                'success': True,
                'data': {'id': departamento_id, 'descripcion': descripcion},
                'error': None
            }), 201
        else:
            return jsonify({ 'success': False, 'error': 'No se pudo guardar el departamento. Consulte con el administrador.' }), 500
    except Exception as e:
        app.logger.error(f"Error al agregar departamento: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@depapi.route('/departamentos/<int:departamento_id>', methods=['PUT'])
def updateDepartamento(departamento_id):
    data = request.get_json()
    depdao = DepartamentoDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['descripcion','idpais']

    # Verificar si faltan campos o son vacíos
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(str(data[campo]).strip()) == 0:
            return jsonify({
                            'success': False,
                            'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
                            }), 400
    descripcion = data['descripcion']
    idpais = data['idpais']
    try:
        if depdao.updateDepartamento(departamento_id, descripcion.upper(),idpais):
            return jsonify({
                'success': True,
                'data': {'id': departamento_id, 'descripcion': descripcion, 'idpais':idpais},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el departamento con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar departamento: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@depapi.route('/departamentos/<int:departamento_id>', methods=['DELETE'])
def deleteDepartamento(departamento_id):
    depdao = DepartamentoDao()

    try:
        # Usar el retorno de eliminarDepartamento para determinar el éxito
        if depdao.deleteDepartamento(departamento_id):
            return jsonify({
                'success': True,
                'mensaje': f'Departamento con ID {departamento_id} eliminada correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el departamento con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar departamento: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500