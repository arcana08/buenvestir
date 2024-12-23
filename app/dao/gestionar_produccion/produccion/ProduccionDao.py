# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class ProduccionDao:

    def getProducciones(self):

        produccionesQL = """
        SELECT op.idorden_produccion,  p.per_nombre,  p.per_apellido, p.per_ci, e.eta_nombre 
        FROM  orden_produccion op, clientes c,personas p, etapas_producciones e
        where op.idcliente=c.idcliente and c.idpersona=p.idpersona and op.estado=e.idetapa_produccion
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(produccionesQL)
            producciones = cur.fetchall() # trae datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{
            'idorden_produccion': produccion[0],
            'per_nombre': produccion[1],
            'per_apellido': produccion[2],
            'per_ci': produccion[3],
            'eta_nombre': produccion[4]
            } for produccion in producciones]

        except Exception as e:
            app.logger.error(f"Error al obtener todos los producciones: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getProduccionById(self, id):

        produccionesQL = """
        SELECT op.idorden_produccion, op.idcliente, p.per_nombre,  p.per_apellido, p.per_ci,op.estado, e.eta_nombre 
        FROM  orden_produccion op, clientes c,personas p, etapas_producciones e
        where op.idcliente=c.idcliente and c.idpersona=p.idpersona and op.estado=e.idetapa_produccion 
        and op.idorden_produccion=%s 
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(produccionesQL, (id,))
            costoEncontrada = cur.fetchone() # Obtener una sola fila
            if costoEncontrada:
                print (costoEncontrada) 
                return {
                        'idorden_produccion': costoEncontrada[0],
                        'idcliente': costoEncontrada[1],
                        'per_nombre': costoEncontrada[2],
                        'per_apellido': costoEncontrada[3],
                        'per_ci': costoEncontrada[4],
                        'estado': costoEncontrada[5],
                        'eta_nombre': costoEncontrada[6]
                        
                    }  # Retornar los datos de la produccion
            else:
                print('erro de consulta')
                return None # Retornar None si no se encuentra la produccion
        except Exception as e:
            app.logger.error(f"Error al obtener produccion: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()
    def getDetallesByProduccionId(self, produccion_id):
        detallesSQL = """
        SELECT dp.idcosto, p.pro_nombre, p.pro_color
        FROM detalle_produccion dp
        JOIN costos c ON dp.idcosto = c.idcosto 
        join productos p on c.idproducto = p.idproducto 
        WHERE dp.idorden_produccion = %s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(detallesSQL, (produccion_id,))
            detalles = cur.fetchall()
            return [
                {
                    'idcosto': row[0],
                    'pro_nombre': row[1],
                    'pro_color': row[2]
                }
                for row in detalles
            ]
        except Exception as e:
            app.logger.error(f"Error al obtener detalles del costo: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()
    
    def guardarProduccion(self, cliente_id, detalles):
        insertProduccionesQL = """
        INSERT INTO orden_produccion(idcliente,estado) VALUES (%s,2) RETURNING idorden_produccion
        """
        insertCostodetSQL = """
        INSERT INTO detalle_produccion( idorden_produccion, idcosto) VALUES (%s, %s)
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            # Inserta en producciones y obtiene el idcosto
            cur.execute(insertProduccionesQL, (cliente_id,))
            orden_produccion_id = cur.fetchone()[0]  # Obtiene el id de la inserción en producciones
            app.logger.info(f"Detalles a insertar: {detalles}")
            # Inserta cada detalle en detalle_producciones
            for detalle in detalles:
                idcosto = detalle
                cur.execute(insertCostodetSQL, ( orden_produccion_id, idcosto ))

            # Confirmar todas las inserciones
            con.commit()
            
        except Exception as e:
            app.logger.error(f"Error al insertar detalle de produccion para cliente {cliente_id}: {str(e)}")
            con.rollback()  # Retrocede si hubo error
            return False

        finally:
            cur.close()
            con.close()

        return True


    def procesarProduccion(self, id):
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            # Verificar si la producción está en estado pendiente
            cur.execute("SELECT estado FROM orden_produccion WHERE idorden_produccion = %s", (id,))
            estado = cur.fetchone()

            if not estado:
                raise ValueError("Orden de producción no encontrada.")

            if estado[0] == 2:  # Estado pendiente producción
                # Obtener costos asociados a la orden de producción
                cur.execute("SELECT idcosto FROM detalle_produccion WHERE idorden_produccion = %s", (id,))
                costos = cur.fetchall()

                if not costos:
                    raise ValueError("No se encontraron costos asociados a la orden de producción.")

                for costo in costos:
                    idcosto = costo[0]

                    # Obtener materias primas asociadas al costo
                    cur.execute("""
                        SELECT idmateria_prima, dco_cantidad
                        FROM detalle_costos
                        WHERE idcosto = %s
                    """, (idcosto,))
                    materias_primas = cur.fetchall()

                    if not materias_primas:
                        raise ValueError(f"No se encontraron materias primas para el costo {idcosto}.")

                    for materia in materias_primas:
                        idmateria_prima = materia[0]
                        cantidad_requerida = materia[1]

                        # Verificar stock actual
                        cur.execute("SELECT mat_cantidad FROM materias_primas WHERE idmateria_prima = %s", (idmateria_prima,))
                        stock_actual = cur.fetchone()

                        if not stock_actual:
                            raise ValueError(f"No se encontró la materia prima con ID {idmateria_prima}.")

                        stock_actual = float(stock_actual[0])

                        if stock_actual < cantidad_requerida:
                            raise ValueError(f"Stock insuficiente para la materia prima {idmateria_prima}. (Requerido: {cantidad_requerida}, Disponible: {stock_actual})")

                        # Actualizar el stock de materias primas
                        cur.execute("""
                            UPDATE materias_primas
                            SET mat_cantidad = mat_cantidad - %s
                            WHERE idmateria_prima = %s
                        """, (cantidad_requerida, idmateria_prima))

                # Cambiar el estado de la orden de producción a "procesada" (por ejemplo, estado 3)
                cur.execute("""
                    UPDATE orden_produccion
                    SET estado = 3
                    WHERE idorden_produccion = %s
                """, (id,))
                
                con.commit()  # Confirmar transacción
                return True  # Indicar éxito
            elif estado[0] == 6:
                cur.execute("""
                    UPDATE orden_produccion
                    SET estado = 3
                    WHERE idorden_produccion = %s
                """, (id,))
                con.commit()  # Confirmar transacción
                return True  # Indicar éxito
            else:
                raise ValueError("La orden de producción no está en estado pendiente.")

        except Exception as e:
            app.logger.error(f"Error al procesar producción: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
    
    def finalizarProduccion(self, id):
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute("""
                    UPDATE orden_produccion
                    SET estado = 4
                    WHERE idorden_produccion = %s
                """, (id,))
            con.commit()  # Confirmar transacción
            return True 
        except Exception as e:
            app.logger.error(f"Error al finalizar producción: {str(e)}")
            con.rollback()
            return False
        
    def mejorarProduccion(self, id):
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute("""
                    UPDATE orden_produccion
                    SET estado = 6
                    WHERE idorden_produccion = %s
                """, (id,))
            con.commit()  # Confirmar transacción
            return True 
        except Exception as e:
            app.logger.error(f"Error al mejorar producción: {str(e)}")
            con.rollback()
            return False
        
    def rechazarProduccion(self, id):
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute("""
                    UPDATE orden_produccion
                    SET estado = 5
                    WHERE idorden_produccion = %s
                """, (id,))
            con.commit()  # Confirmar transacción
            return True 
        except Exception as e:
            app.logger.error(f"Error al rechazar producción: {str(e)}")
            con.rollback()
            return False
        
    
    def updateMateriasPrimas(self, detalles):
        updateMateriaPrimaSQL = """
        UPDATE materias_primas
        SET mat_cantidad = mat_cantidad - %s
        WHERE idmateria_prima = %s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            for detalle in detalles:
                idmateria_prima = int(detalle['idmateria_prima'])
                cantidad = int(detalle['dco_cantidad'])

                # Actualizar stock
                cur.execute(updateMateriaPrimaSQL, (cantidad, idmateria_prima))

            con.commit()
            return True  # Indicar éxito si no hubo errores

        except Exception as e:
            app.logger.error(f"Error al actualizar materias primas: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteCosto(self, id):

        updateProduccionesQL = """
        DELETE FROM orden_produccion
        WHERE idcosto=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateProduccionesQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar produccion: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()