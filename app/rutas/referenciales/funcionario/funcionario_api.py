from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.funcionario.FuncionarioDao import FuncionarioDao

# Crear blueprint para funcionarios
funapi = Blueprint('funapi', __name__)

# Obtener todos los funcionarios
@funapi.route('/funcionarios', methods=['GET'])
def getFuncionarios():
    funcionariodao = FuncionarioDao()

    try:
        funcionarios = funcionariodao.getFuncionarios()
        return jsonify({
            'success': True,
            'data': funcionarios,
            'error': None
        }), 200
    except Exception as e:
        app.logger.error(f"Error al obtener todos los funcionarios: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Obtener un funcionario por ID
@funapi.route('/funcionarios/<int:funcionario_id>', methods=['GET'])
def getFuncionario(funcionario_id):
    funcionariodao = FuncionarioDao()

    try:
        funcionario = funcionariodao.getFuncionarioById(funcionario_id)
        if funcionario:
            return jsonify({
                'success': True,
                'data': funcionario,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el funcionario con el ID proporcionado.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al obtener funcionario: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agregar un nuevo funcionario
@funapi.route('/funcionarios', methods=['POST'])
def addFuncionario():
    data = request.get_json()
    funcionariodao = FuncionarioDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['idpersona', 'idtrabajo']

    for campo in campos_requeridos:
        if campo not in data or data[campo] is None:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio.'
            }), 400

    try:
        idpersona = data['idpersona']
        idtrabajo = data['idtrabajo']

        funcionario_id = funcionariodao.guardarFuncionario(idpersona, idtrabajo)
        if funcionario_id:
            return jsonify({
                'success': True,
                'data': {
                    'idfuncionario': funcionario_id,
                    'idpersona': idpersona,
                    'idtrabajo': idtrabajo
                },
                'error': None
            }), 201
        else:
            return jsonify({'success': False, 'error': 'No se pudo guardar el funcionario. Consulte con el administrador.'}), 500
    except Exception as e:
        app.logger.error(f"Error al agregar funcionario: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Actualizar un funcionario
@funapi.route('/funcionarios/<int:funcionario_id>', methods=['PUT'])
def updateFuncionario(funcionario_id):
    data = request.get_json()
    funcionariodao = FuncionarioDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = [ 'idtrabajo']
    print(data)
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio.'
            }), 400

    try:
        
        idtrabajo = data['idtrabajo']

        if funcionariodao.updateFuncionario(funcionario_id,  idtrabajo):
            return jsonify({
                'success': True,
                'data': {
                    'idfuncionario': funcionario_id,
                    'idtrabajo': idtrabajo
                },
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el funcionario con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar funcionario: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Eliminar un funcionario
@funapi.route('/funcionarios/<int:funcionario_id>', methods=['DELETE'])
def deleteFuncionario(funcionario_id):
    funcionariodao = FuncionarioDao()

    try:
        if funcionariodao.deleteFuncionario(funcionario_id):
            return jsonify({
                'success': True,
                'mensaje': f'Funcionario con ID {funcionario_id} eliminado correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el funcionario con el ID proporcionado o no se pudo eliminar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al eliminar funcionario: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500
