# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class CostoDao:

    def getCostos(self):

        costoSQL = """
        SELECT c.idcosto,  p.idproducto,  p.pro_nombre, p.pro_color, c.cos_total 
        FROM  costos c,  productos p
        where p.idproducto=c.idproducto 
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(costoSQL)
            costos = cur.fetchall() # trae datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{
            'idcosto': costo[0],
            'idproducto': costo[1],
            'pro_nombre': costo[2],
            'pro_color': costo[3],
            'cos_total': costo[4]
            } for costo in costos]

        except Exception as e:
            app.logger.error(f"Error al obtener todos los costos: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getCostoById(self, id):

        costoSQL = """
        SELECT c.idcosto,  p.idproducto,  p.pro_nombre, p.pro_color, c.cos_total 
        FROM  costos c,  productos p
        where p.idproducto=c.idproducto and c.idcosto=%s 
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(costoSQL, (id,))
            costoEncontrada = cur.fetchone() # Obtener una sola fila
            if costoEncontrada:
                return {
                        'idcosto': costoEncontrada[0],
                        'idproducto': costoEncontrada[1],
                        'pro_nombre': costoEncontrada[2],
                        'pro_color': costoEncontrada[3],
                        'cos_total': costoEncontrada[4]
                        
                    }  # Retornar los datos de la costo
            else:
                return None # Retornar None si no se encuentra la costo
        except Exception as e:
            app.logger.error(f"Error al obtener costo: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def getDetallesByCostoId(self, costo_id):
        detallesSQL = """
        SELECT dc.idmateria_prima, mp.mat_nombre, mp.mat_costo, dc.dco_cantidad, mp.mat_cantidad, mp.mat_unidad_medida
        FROM detalle_costos dc
        JOIN materias_primas mp ON dc.idmateria_prima = mp.idmateria_prima
        WHERE dc.idcosto = %s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(detallesSQL, (costo_id,))
            detalles = cur.fetchall()
            return [
                {
                    'idmateriaprima': row[0],
                    'mp_nombre': row[1],
                    'precio': row[2],
                    'cantidad': row[3],
                    'stock': row[4],
                    'unidad': row[5]
                }
                for row in detalles
            ]
        except Exception as e:
            app.logger.error(f"Error al obtener detalles del costo: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()
    
    def guardarCosto(self, producto_id, detalles):
        insertCostoSQL = """
        INSERT INTO costos(idproducto) VALUES (%s) RETURNING idcosto
        """
        insertCostodetSQL = """
        INSERT INTO detalle_costos(dco_cantidad, idmateria_prima, idcosto) VALUES (%s, %s, %s)
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            # Inserta en costos y obtiene el idcosto
            cur.execute(insertCostoSQL, (producto_id,))
            costo_id = cur.fetchone()[0]  # Obtiene el id de la inserción en costos
            app.logger.info(f"Detalles a insertar: {detalles}")
            # Inserta cada detalle en detalle_costos
            for detalle in detalles:
                dco_cantidad, idmateria_prima = detalle
                cur.execute(insertCostodetSQL, (dco_cantidad, idmateria_prima, costo_id))

            # Confirmar todas las inserciones
            con.commit()
            
        except Exception as e:
            app.logger.error(f"Error al insertar detalle de costo para idproducto {producto_id}: {str(e)}")
            con.rollback()  # Retrocede si hubo error
            return False

        finally:
            cur.close()
            con.close()

        return True


    def actualizarCosto(self, costo_id, producto_id, detalles):
        eliminarDetallesSQL = """
        DELETE FROM detalle_costos WHERE idcosto = %s
        """
        actualizarCostoSQL = """
        UPDATE costos SET idproducto = %s WHERE idcosto = %s
        """
        insertarDetallesSQL = """
        INSERT INTO detalle_costos(dco_cantidad, idmateria_prima, idcosto) VALUES (%s, %s, %s)
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            # Actualizar cabecera del costo
            cur.execute(actualizarCostoSQL, (producto_id, costo_id))

            # Eliminar detalles existentes
            cur.execute(eliminarDetallesSQL, (costo_id,))

            # Insertar nuevos detalles
            for detalle in detalles:
                dco_cantidad, idmateria_prima = detalle
                cur.execute(insertarDetallesSQL, (dco_cantidad, idmateria_prima, costo_id))

            # Confirmar cambios
            con.commit()
            return True

        except Exception as e:
            app.logger.error(f"Error al actualizar costo y detalles para idcosto {costo_id}: {str(e)}")
            con.rollback()  # Revertir cambios si hubo error
            return False

        finally:
            cur.close()
            con.close()

    
            
    def deleteCosto(self, id):

        updateCostoSQL = """
        DELETE FROM costos
        WHERE idcosto=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateCostoSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar costo: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()