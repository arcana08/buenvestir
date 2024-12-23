from flask import Blueprint, request, jsonify, current_app as app
from werkzeug.security import generate_password_hash
from app.dao.referenciales.usuario.UsuarioDao import UsuarioDao

# Crear blueprint para usuarios
userapi = Blueprint('userapi', __name__)

# Obtener todos los usuarios
@userapi.route('/usuarios', methods=['GET'])
def getUsuarios():
    userdao = UsuarioDao()

    try:
        usuarios = userdao.getUsuarios()
        return jsonify({
            'success': True,
            'data': usuarios,
            'error': None
        }), 200
    except Exception as e:
        app.logger.error(f"Error al obtener todos los usuarios: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Obtener un usuario por ID
@userapi.route('/usuarios/<int:usuario_id>', methods=['GET'])
def getUsuario(usuario_id):
    userdao = UsuarioDao()

    try:
        usuario = userdao.getUsuarioById(usuario_id)
        if usuario:
            return jsonify({
                'success': True,
                'data': usuario,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el usuario con el ID proporcionado.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al obtener usuario: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agregar un nuevo usuario
# Agregar un nuevo usuario
@userapi.route('/usuarios', methods=['POST'])
def addUsuario():
    data = request.get_json()
    userdao = UsuarioDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['usu_nombre', 'usu_clave', 'usu_estado', 'idpersona', 'idrol']
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(str(data[campo]).strip()) == 0:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400

    try:
        usu_nombre = data['usu_nombre'].upper()
        usu_clave = generate_password_hash(data['usu_clave'])  # Hashear contraseña
        usu_estado = data['usu_estado']
        idpersona = data['idpersona']
        idrol = data['idrol']

        usuario_id = userdao.guardarUsuario(usu_nombre, usu_clave, usu_estado, idpersona, idrol)
        if usuario_id:
            return jsonify({
                'success': True,
                'data': {
                    'id': usuario_id,
                    'usu_nombre': usu_nombre,
                    'usu_estado': usu_estado,
                    'idpersona': idpersona,
                    'idrol': idrol
                },
                'error': None
            }), 201
        else:
            return jsonify({'success': False, 'error': 'No se pudo guardar el usuario. Consulte con el administrador.'}), 500
    except Exception as e:
        app.logger.error(f"Error al agregar usuario: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Actualizar un usuario
@userapi.route('/usuarios/<int:usuario_id>', methods=['PUT'])
def updateUsuario(usuario_id):
    data = request.get_json()
    userdao = UsuarioDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['usu_nombre', 'usu_clave', 'usu_estado', 'idrol']
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(str(data[campo]).strip()) == 0:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400

    try:
        usu_nombre = data['usu_nombre'].upper()
        usu_clave = generate_password_hash(data['usu_clave'])  # Hashear contraseña
        usu_estado = data['usu_estado']
        idrol = data['idrol']

        if userdao.updateUsuario(usuario_id, usu_nombre, usu_clave, usu_estado, idrol):
            return jsonify({
                'success': True,
                'data': {
                    'id': usuario_id,
                    'usu_nombre': usu_nombre,
                    'usu_estado': usu_estado,
                    'idrol': idrol
                },
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el usuario con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar usuario: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Eliminar un usuario
@userapi.route('/usuarios/<int:usuario_id>', methods=['DELETE'])
def deleteUsuario(usuario_id):
    userdao = UsuarioDao()

    try:
        if userdao.deleteUsuario(usuario_id):
            return jsonify({
                'success': True,
                'mensaje': f'Usuario con ID {usuario_id} eliminado correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el usuario con el ID proporcionado o no se pudo eliminar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al eliminar usuario: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500
