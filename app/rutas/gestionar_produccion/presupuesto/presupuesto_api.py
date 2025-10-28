from flask import Blueprint, request, jsonify, current_app as app
from app.dao.gestionar_produccion.presupuesto.presupuestoDao import PresupuestoDao

presuapi = Blueprint('presuapi', __name__)
 
 # Trae todas los presupuestos
@presuapi.route('/presupuestos', methods=['GET'])
def getPresupuestos():
    proddao = PresupuestoDao()
    try:
        presupuestos = proddao.getPresupuestos()
        # Ajusta los nombres para la vista
        for p in presupuestos:
            p['estado'] = p.get('pre_estado')
            p['fecha'] = p.get('fecha_alta')
        return jsonify({
            'success': True,
            'data': presupuestos,
            'error': None
        }), 200
    except Exception as e:
        app.logger.error(f"Error al obtener todos los presupuestos: {e}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@presuapi.route('/presupuestos/<int:presupuesto_id>', methods=['GET'])
def getPresupuesto(presupuesto_id):
    proddao = PresupuestoDao()
    try:
        presupuesto = proddao.getPresupuestoById(presupuesto_id)
        app.logger.debug(f"getPresupuesto id={presupuesto_id}")
        if presupuesto:
            # Renombra para la vista
            presupuesto['estado'] = presupuesto.get('pre_estado')
            presupuesto['fecha'] = presupuesto.get('fecha_alta')
            presupuesto['fecha_solicitud'] = presupuesto.get('fecha_solicitud')
            presupuesto['fecha_estado'] = presupuesto.get('fecha_estado')
            presupuesto['total'] = presupuesto.get('total')
            return jsonify({
                'success': True,
                'data': presupuesto,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el presupuesto con el ID proporcionado.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al obtener presupuesto: {e}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@presuapi.route('/presupuestos/<int:presupuesto_id>/detalles', methods=['GET'])
def getCostoDetalles(presupuesto_id):
    proddao = PresupuestoDao()

    try:
        detalles = proddao.getDetallesByPresupuestoId(presupuesto_id)

        # Devolver lista vacía si no hay detalles (200). Cambiar a 404 sólo si lo prefieres.
        return jsonify({
            'success': True,
            'data': detalles or [],
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener detalles del presupuesto: {e}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500
@presuapi.route('/presupuestosmp', methods=['PUT'])
def updatePresupuestosMP():
    presupuestoDao = PresupuestoDao()
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
        success = presupuestoDao.updateMateriasPrimas(detalles)
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
        app.logger.error(f"Error al actualizar materias primas: {e}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@presuapi.route('/presupuestosfin', methods=['PUT'])
def gestionarPresupuesto():
    data = request.json
    idpresupuesto = data.get('idpresupuesto')
    accion = data.get('accion')
    app.logger.debug(f"gestionarPresupuesto id={idpresupuesto} accion={accion}")
    if not idpresupuesto or not accion:
        return jsonify({
            'success': False,
            'error': 'Datos incompletos.'
        }), 400

    try:
        proddao = PresupuestoDao()

        if accion == 'finalizar':
            resultado = proddao.finalizarPresupuesto(idpresupuesto)
        elif accion == 'mejorar':
            resultado = proddao.mejorarPresupuesto(idpresupuesto)
        elif accion == 'rechazar':
            resultado = proddao.rechazarPresupuesto(idpresupuesto)
        elif accion == 'procesar':
            resultado = proddao.procesarPresupuesto(idpresupuesto)
        else:
            return jsonify({
                'success': False,
                'error': 'Acción no válida.'
            }), 400

        if resultado:
            return jsonify({
                'success': True,
                'message': f'Presupuesto {accion} con éxito.'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': f'No se pudo {accion} el presupuesto.'
            }), 500

    except Exception as e:
        app.logger.error(f"Error al gestionar presupuesto: {e}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno.'
        }), 500
# Agrega una nueva produccion
@presuapi.route('/presupuestos', methods=['POST'])
def addPresupuesto():
    data = request.get_json()
    proddao = PresupuestoDao()

    campos_requeridos = ['cliente_id', 'detalles', 'total']
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or str(data[campo]).strip() == '':
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400

    detalles = data['detalles']
    if not isinstance(detalles, list) or not all(isinstance(d, dict) for d in detalles):
        return jsonify({
            'success': False,
            'error': 'El campo detalles debe ser una lista de objetos con idcosto.'
        }), 400

    detalles_procesados = []
    for detalle in detalles:
        if 'idcosto' in detalle:
            try:
                idcosto = int(detalle['idcosto'])
                detalles_procesados.append(idcosto)
            except ValueError:
                return jsonify({
                    'success': False,
                    'error': 'Error en el formato de idcosto en detalles.'
                }), 400
        else:
            return jsonify({
                'success': False,
                'error': 'Cada detalle debe incluir idcosto.'
            }), 400

    try:
        cliente_id = int(data['cliente_id'])
        total = float(data['total'])
        presupuesto_id = proddao.guardarPresupuesto(cliente_id, detalles_procesados, total)

        if presupuesto_id is not None:
            return jsonify({
                'success': True,
                'data': {
                    'id': presupuesto_id,
                    'cliente_id': cliente_id,
                    'detalles': detalles,
                    'total': total
                },
                'error': None
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo guardar el presupuesto. Consulte con el administrador.'
            }), 500
    except Exception as e:
        app.logger.exception("Error al agregar presupuesto")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@presuapi.route('/presupuestos/<int:presupuesto_id>', methods=['PUT'])
def updatePresupuesto(presupuesto_id):
    data = request.get_json()
    proddao = PresupuestoDao()

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
        if proddao.updatePresupuesto(presupuesto_id, descripcion.upper(),ciudad_id):
            return jsonify({
                'success': True,
                'data': {'id': presupuesto_id, 'descripcion': descripcion,'ciudad': ciudad_id},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el presupuesto con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar presupuesto: {e}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@presuapi.route('/presupuestos/<int:presupuesto_id>', methods=['DELETE'])
def deletePresupuesto(presupuesto_id):
    proddao = PresupuestoDao()

    try:
        # Usar el retorno de eliminarPresupuesto para determinar el éxito
        if proddao.deletePresupuesto(presupuesto_id):
            return jsonify({
                'success': True,
                'message': f'Presupuesto con ID {presupuesto_id} eliminado correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el presupuesto con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar presupuesto: {e}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@presuapi.route('/presupuestos/<int:presupuesto_id>/aprobar', methods=['POST'])
def aprobar_presupuesto(presupuesto_id):
    dao = PresupuestoDao()
    result = dao.aprobarPresupuesto(presupuesto_id)
    if result['success']:
        return jsonify({'success': True, 'message': 'Presupuesto aprobado y enviado a producción.'})
    else:
        return jsonify({'success': False, 'error': result['error']}), 400

@presuapi.route('/presupuestos/<int:presupuesto_id>/anular', methods=['POST'])
def anular_presupuesto(presupuesto_id):
    dao = PresupuestoDao()
    result = dao.anularPresupuesto(presupuesto_id)
    if result['success']:
        return jsonify({'success': True, 'message': 'Presupuesto anulado.'})
    else:
        return jsonify({'success': False, 'error': result['error']}), 400