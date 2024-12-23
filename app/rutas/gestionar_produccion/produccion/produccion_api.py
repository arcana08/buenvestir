from flask import Blueprint, request, jsonify, current_app as app
from app.dao.gestionar_produccion.produccion.ProduccionDao import ProduccionDao

prodapi = Blueprint('prodapi', __name__)

# Trae todas los producciones
@prodapi.route('/producciones', methods=['GET'])
def getProducciones():
    proddao = ProduccionDao()

    try:
        producciones = proddao.getProducciones()

        return jsonify({
            'success': True,
            'data': producciones,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todos los producciones: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@prodapi.route('/producciones/<int:produccion_id>', methods=['GET'])
def getProduccion(produccion_id):
    proddao = ProduccionDao()

    try:
        produccion = proddao.getProduccionById(produccion_id)
        print(produccion_id)
        if produccion:
            return jsonify({
                'success': True,
                'data': produccion,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el produccion con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener produccion: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@prodapi.route('/producciones/<int:produccion_id>/detalles', methods=['GET'])
def getCostoDetalles(produccion_id):
    proddao = ProduccionDao()

    try:
        detalles = proddao.getDetallesByProduccionId(produccion_id)

        if detalles:
            return jsonify({
                'success': True,
                'data': detalles,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontraron detalles para la orden con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener detalles de la orden: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500
@prodapi.route('/produccionesmp', methods=['PUT'])
def updateProduccionesMP():
    produccionDao = ProduccionDao()
    try:
        # Obtener los datos del cuerpo de la solicitud
        data = request.get_json()
        if 'detalles' not in data:
            return jsonify({
                'success': False,
                'error': 'El formato del cuerpo de la solicitud es incorrecto.'
            }), 400
        detalles = data['detalles']
        # Llamar al método del DAO
        success = produccionDao.updateMateriasPrimas(detalles)
        if success:
            return jsonify({
                'success': True,
                'message': 'Las materias primas fueron actualizadas correctamente.'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudieron actualizar las materias primas.'
            }), 500

    except Exception as e:
        app.logger.error(f"Error al actualizar materias primas: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500
        
@prodapi.route('/produccionesfin', methods=['PUT'])
def gestionarProduccion():
    data = request.json
    idproduccion = data.get('idproduccion')
    accion = data.get('accion')
    print (idproduccion)
    print (accion)
    if not idproduccion or not accion:
        return jsonify({
            'success': False,
            'error': 'Datos incompletos.'
        }), 400

    try:
        proddao = ProduccionDao()
        
        if accion == 'finalizar':
            resultado = proddao.finalizarProduccion(idproduccion)
        elif accion == 'mejorar':
            resultado = proddao.mejorarProduccion(idproduccion)
        elif accion == 'rechazar':
            resultado = proddao.rechazarProduccion(idproduccion)
        elif accion == 'procesar':
            resultado = proddao.procesarProduccion(idproduccion)
        else:
            return jsonify({
                'success': False,
                'error': 'Acción no válida.'
            }), 400

        if resultado:
            return jsonify({
                'success': True,
                'message': f'Producción {accion} con éxito.'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': f'No se pudo {accion} la producción.'
            }), 500

    except Exception as e:
        app.logger.error(f"Error al gestionar producción: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno.'
        }), 500
# Agrega una nueva produccion
@prodapi.route('/producciones', methods=['POST'])
def addProduccion():
    data = request.get_json()
    proddao = ProduccionDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['cliente_id', 'detalles']
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or not str(data[campo]).strip():
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400

    # Validar que detalles sea una lista de diccionarios
    detalles = data['detalles']
    if not isinstance(detalles, list) or not all(isinstance(d, dict) for d in detalles):
        return jsonify({
            'success': False,
            'error': 'El campo detalles debe ser una lista de objetos con dco_cantidad e idmateria_prima.'
        }), 400

    # Procesar detalles para asegurar que cada objeto tenga los campos requeridos
    detalles_procesados = []
    for detalle in detalles:
        if 'idcosto' in detalle :
            try:
                idcosto = int(detalle['idcosto'])
                detalles_procesados.append((idcosto))
            except ValueError:
                return jsonify({
                    'success': False,
                    'error': 'Error al cargar las prendas.'
                }), 400
        else:
            return jsonify({
                'success': False,
                'error': 'No puede crear una orden de produccion sin seleccionar al menos una prenda.'
            }), 400

    try:
        # Convertir producto_id a entero y llamar al método guardarProduccion en el DAO
        cliente_id = int(data['cliente_id'])
        produccion_id = proddao.guardarProduccion(cliente_id, detalles_procesados)

        if produccion_id is not None:
            return jsonify({
                'success': True,
                'data': {
                    'id': produccion_id,
                    'cliente_id': cliente_id,
                    'detalles': detalles
                },
                'error': None
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo guardar la Orden. Consulte con el administrador.'
            }), 500
    except Exception as e:
        app.logger.exception("Error al agregar produccion")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

                
@prodapi.route('/producciones/<int:produccion_id>', methods=['PUT'])
def updateProduccion(produccion_id):
    data = request.get_json()
    proddao = ProduccionDao()

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
        if proddao.updateProduccion(produccion_id, descripcion.upper(),ciudad_id):
            return jsonify({
                'success': True,
                'data': {'id': produccion_id, 'descripcion': descripcion,'ciudad': ciudad_id},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el produccion con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar produccion: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@prodapi.route('/producciones/<int:produccion_id>', methods=['DELETE'])
def deleteProduccion(produccion_id):
    proddao = ProduccionDao()

    try:
        # Usar el retorno de eliminarProduccion para determinar el éxito
        if proddao.deleteProduccion(produccion_id):
            return jsonify({
                'success': True,
                'mensaje': f'Produccion con ID {produccion_id} eliminada correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el produccion con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar produccion: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500