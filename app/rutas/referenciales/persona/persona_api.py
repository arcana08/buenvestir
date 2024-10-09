from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.persona.PersonaDao import PersonaDao

perapi = Blueprint('perapi', __name__)

# Trae todas las personas
@perapi.route('/personas', methods=['GET'])
def getPersonas():
    perdao = PersonaDao()

    try:
        personas = perdao.getPersonas()
        
        return jsonify({
            'success': True,
            'data': personas,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todas las personas: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@perapi.route('/personas/<int:persona_id>', methods=['GET'])
def getPersona(persona_id):
    perdao = PersonaDao()

    try:
        persona = perdao.getPersonaById(persona_id)
        if 'per_fechanac' in persona and persona['per_fechanac']:
            # Formatear la fecha de nacimiento al formato 'YYYY-MM-DD'
            persona['per_fechanac'] = persona['per_fechanac'].strftime('%Y-%m-%d')
        if persona:
            return jsonify({
                'success': True,
                'data': persona,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la persona con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener persona: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega una nueva persona
@perapi.route('/personas', methods=['POST'])
def addPersona():
    data = request.get_json()
    perdao = PersonaDao()
    
    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['nombre', 'apellido', 'ci', 'fechanac', 'telefono', 'barrio']

    # Verificar si faltan campos o son vacíos
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(str(data[campo]).strip()) == 0:
            return jsonify({
                            'success': False,
                            'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
                            }), 400

    try:
        nombre = data['nombre'].upper()
        apellido = data['apellido'].upper()
        ci = data['ci']
        fechanac = data['fechanac']
        telefono = data['telefono']
        idbarrio = data['barrio']

        persona_id = perdao.guardarPersona(nombre, apellido, ci, fechanac, telefono, idbarrio)
        if persona_id is not None:
            return jsonify({
                'success': True,
                'data': {
                    'id': persona_id,
                    'nombre': nombre,
                    'apellido': apellido,
                    'ci': ci,
                    'fechanac': fechanac,
                    'telefono': telefono,
                    'barrio': idbarrio
                },
                'error': None
            }), 201
        else:
            return jsonify({'success': False, 'error': 'No se pudo guardar la persona. Consulte con el administrador.'}), 500
    except Exception as e:
        app.logger.error(f"Error al agregar persona: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@perapi.route('/personas/<int:persona_id>', methods=['PUT'])
def updatePersona(persona_id):
    data = request.get_json()
    perdao = PersonaDao()
    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['nombre', 'apellido', 'ci', 'fechanac', 'telefono', 'barrio']

    # Verificar si faltan campos o son vacíos
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(str(data[campo]).strip()) == 0:
            return jsonify({
                            'success': False,
                            'error': f'El campo {campo} {data} es obligatorio y no puede estar vacío.'
                            }), 400

    nombre = data['nombre']
    apellido = data['apellido']
    ci = data['ci']
    fechanac = data['fechanac']
    telefono = data['telefono']
    idbarrio = data['barrio']

    try:
        if perdao.updatePersona(persona_id, nombre.upper(), apellido.upper(), ci, fechanac, telefono, idbarrio):
            return jsonify({
                'success': True,
                'data': {
                    'id': persona_id,
                    'nombre': nombre,
                    'apellido': apellido,
                    'ci': ci,
                    'fechanac': fechanac,
                    'telefono': telefono,
                    'barrio': idbarrio
                },
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la persona con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar persona: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@perapi.route('/personas/<int:persona_id>', methods=['DELETE'])
def deletePersona(persona_id):
    perdao = PersonaDao()

    try:
        if perdao.deletePersona(persona_id):
            return jsonify({
                'success': True,
                'mensaje': f'Persona con ID {persona_id} eliminada correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la persona con el ID proporcionado o no se pudo eliminar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al eliminar persona: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500
