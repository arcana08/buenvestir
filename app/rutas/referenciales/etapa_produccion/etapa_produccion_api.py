from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.etapa_produccion.Etapa_produccionDao import EproDao

eproapi = Blueprint('eproapi', __name__)

# Obtener todas las etapas de producción
@eproapi.route('/etapas', methods=['GET'])
def getEtapas():
    etapadao = EproDao()

    try:
        etapas = etapadao.getEtapasProduccion()

        return jsonify({
            'success': True,
            'data': etapas,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todas las etapas de producción: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Obtener una etapa de producción por ID
@eproapi.route('/etapas/<int:etapa_id>', methods=['GET'])
def getEtapa(etapa_id):
    etapadao = EproDao()

    try:
        etapa = etapadao.getEtapaProduccionById(etapa_id)

        if etapa:
            return jsonify({
                'success': True,
                'data': etapa,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la etapa con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener la etapa: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agregar una nueva etapa de producción
@eproapi.route('/etapas', methods=['POST'])
def addEtapa():
    data = request.get_json()
    etapadao = EproDao()

    campos_requeridos = ['nombre']

    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(data[campo].strip()) == 0:
            return jsonify({
                            'success': False,
                            'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
                            }), 400

    try:
        nombre = data['nombre'].upper()
        etapa_id = etapadao.guardarEtapaProduccion(nombre)
        if etapa_id is not None:
            return jsonify({
                'success': True,
                'data': {'id': etapa_id, 'nombre': nombre},
                'error': None
            }), 201
        else:
            return jsonify({ 'success': False, 'error': 'No se pudo guardar la etapa. Consulte con el administrador.' }), 500
    except Exception as e:
        app.logger.error(f"Error al agregar etapa: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Actualizar una etapa de producción
@eproapi.route('/etapas/<int:etapa_id>', methods=['PUT'])
def updateEtapa(etapa_id):
    data = request.get_json()
    etapadao = EproDao()

    campos_requeridos = ['nombre']

    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(data[campo].strip()) == 0:
            return jsonify({
                            'success': False,
                            'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
                            }), 400
    nombre = data['nombre']
    try:
        if etapadao.updateEtapaProduccion(etapa_id, nombre.upper()):
            return jsonify({
                'success': True,
                'data': {'id': etapa_id, 'nombre': nombre},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la etapa con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar etapa: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Eliminar una etapa de producción
@eproapi.route('/etapas/<int:etapa_id>', methods=['DELETE'])
def deleteEtapa(etapa_id):
    etapadao = EproDao()

    try:
        if etapadao.deleteEtapaProduccion(etapa_id):
            return jsonify({
                'success': True,
                'mensaje': f'Etapa con ID {etapa_id} eliminada correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la etapa con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar etapa: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500
