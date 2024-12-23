from flask import Blueprint, request, jsonify, current_app as app
from app.dao.gestionar_costos.costos.CostosDao import CostoDao

cosapi = Blueprint('cosapi', __name__)

# Trae todas los costos
@cosapi.route('/costos', methods=['GET'])
def getCostos():
    cosdao = CostoDao()

    try:
        costos = cosdao.getCostos()

        return jsonify({
            'success': True,
            'data': costos,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todos los costos: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@cosapi.route('/costos/<int:costo_id>', methods=['GET'])
def getCosto(costo_id):
    cosdao = CostoDao()

    try:
        costo = cosdao.getCostoById(costo_id)

        if costo:
            return jsonify({
                'success': True,
                'data': costo,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró elcosto con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener costo: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@cosapi.route('/costos/<int:costo_id>/detalles', methods=['GET'])
def getCostoDetalles(costo_id):
    cosdao = CostoDao()

    try:
        detalles = cosdao.getDetallesByCostoId(costo_id)

        if detalles:
            return jsonify({
                'success': True,
                'data': detalles,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontraron detalles para el costo con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener detalles del costo: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega una nueva costo
@cosapi.route('/costos', methods=['POST'])
def addCosto():
    data = request.get_json()
    cosdao = CostoDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['producto_id', 'detalles']
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
        if 'dco_cantidad' in detalle and 'idmateria_prima' in detalle:
            try:
                dco_cantidad = float(detalle['dco_cantidad'])
                idmateria_prima = int(detalle['idmateria_prima'])
                detalles_procesados.append((dco_cantidad, idmateria_prima))
            except ValueError:
                return jsonify({
                    'success': False,
                    'error': 'Los valores de dco_cantidad deben ser numéricos y idmateria_prima debe ser un entero.'
                }), 400
        else:
            return jsonify({
                'success': False,
                'error': 'Cada objeto en detalles debe contener dco_cantidad e idmateria_prima.'
            }), 400

    try:
        # Convertir producto_id a entero y llamar al método guardarCosto en el DAO
        producto_id = int(data['producto_id'])
        costo_id = cosdao.guardarCosto(producto_id, detalles_procesados)

        if costo_id is not None:
            return jsonify({
                'success': True,
                'data': {
                    'id': costo_id,
                    'producto_id': producto_id,
                    'detalles': detalles
                },
                'error': None
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo guardar el costo. Consulte con el administrador.'
            }), 500
    except Exception as e:
        app.logger.exception("Error al agregar costo")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

                
@cosapi.route('/costos/<int:costo_id>', methods=['PUT'])
def updateCosto(costo_id):
    data = request.get_json()
    cosdao = CostoDao()

    # Validar campos requeridos
    campos_requeridos = ['producto_id', 'detalles']
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or not str(data[campo]).strip():
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400

    # Validar que detalles sea una lista válida
    detalles = data['detalles']
    if not isinstance(detalles, list) or not all(isinstance(d, dict) for d in detalles):
        return jsonify({
            'success': False,
            'error': 'El campo detalles debe ser una lista de objetos con dco_cantidad e idmateria_prima.'
        }), 400

    # Procesar detalles
    detalles_procesados = []
    for detalle in detalles:
        if 'dco_cantidad' in detalle and 'idmateria_prima' in detalle:
            try:
                dco_cantidad = float(detalle['dco_cantidad'])
                idmateria_prima = int(detalle['idmateria_prima'])
                detalles_procesados.append((dco_cantidad, idmateria_prima))
            except ValueError:
                return jsonify({
                    'success': False,
                    'error': 'Los valores de dco_cantidad deben ser numéricos y idmateria_prima debe ser un entero.'
                }), 400
        else:
            return jsonify({
                'success': False,
                'error': 'Cada objeto en detalles debe contener dco_cantidad e idmateria_prima.'
            }), 400

    try:
        # Actualizar costo y detalles
        producto_id = int(data['producto_id'])
        actualizado = cosdao.actualizarCosto(costo_id, producto_id, detalles_procesados)

        if actualizado:
            return jsonify({
                'success': True,
                'data': {
                    'id': costo_id,
                    'producto_id': producto_id,
                    'detalles': detalles
                },
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo actualizar el costo. Consulte con el administrador.'
            }), 500

    except Exception as e:
        app.logger.exception("Error al actualizar costo")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@cosapi.route('/costos/<int:costo_id>', methods=['DELETE'])
def deleteCosto(costo_id):
    cosdao = CostoDao()

    try:
        # Usar el retorno de eliminarCosto para determinar el éxito
        if cosdao.deleteCosto(costo_id):
            return jsonify({
                'success': True,
                'mensaje': f'Costo con ID {costo_id} eliminada correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el costo con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar costo: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500