from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.cliente.ClienteDao import ClienteDao

# Crear blueprint para clientes
cliapi = Blueprint('cliapi', __name__)

# Obtener todos los clientes
@cliapi.route('/clientes', methods=['GET'])
def getClientes():
    clientedao = ClienteDao()

    try:
        clientes = clientedao.getClientes()
        return jsonify({
            'success': True,
            'data': clientes,
            'error': None
        }), 200
    except Exception as e:
        app.logger.error(f"Error al obtener todos los clientes: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Obtener un cliente por ID
@cliapi.route('/clientes/<int:cliente_id>', methods=['GET'])
def getCliente(cliente_id):
    clientedao = ClienteDao()

    try:
        cliente = clientedao.getClienteById(cliente_id)
        if cliente:
            return jsonify({
                'success': True,
                'data': cliente,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el cliente con el ID proporcionado.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al obtener cliente: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agregar un nuevo cliente
@cliapi.route('/clientes', methods=['POST'])
def addCliente():
    data = request.get_json()
    clientedao = ClienteDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['idpersona']

    for campo in campos_requeridos:
        if campo not in data or data[campo] is None:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio.'
            }), 400

    try:
        idpersona = data['idpersona']
        
        cliente_id = clientedao.guardarCliente(idpersona,)
        if cliente_id:
            return jsonify({
                'success': True,
                'data': {
                    'idcliente': cliente_id,
                    'idpersona': idpersona
                },
                'error': None
            }), 201
        else:
            return jsonify({'success': False, 'error': 'No se pudo guardar el cliente. Consulte con el administrador.'}), 500
    except Exception as e:
        app.logger.error(f"Error al agregar cliente: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Actualizar un cliente
@cliapi.route('/clientes/<int:cliente_id>', methods=['PUT'])
def updateCliente(cliente_id):
    data = request.get_json()
    clientedao = ClienteDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = [ 'idpersona']
    print(data)
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio.'
            }), 400

    try:
        
        idpersona = data['idpersona']

        if clientedao.updateCliente(cliente_id,  idpersona):
            return jsonify({
                'success': True,
                'data': {
                    'idcliente': cliente_id,
                    'idpersona': idpersona
                },
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el cliente con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar cliente: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Eliminar un cliente
@cliapi.route('/clientes/<int:cliente_id>', methods=['DELETE'])
def deleteCliente(cliente_id):
    clientedao = ClienteDao()

    try:
        if clientedao.deleteCliente(cliente_id):
            return jsonify({
                'success': True,
                'mensaje': f'Cliente con ID {cliente_id} eliminado correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el cliente con el ID proporcionado o no se pudo eliminar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al eliminar cliente: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500
