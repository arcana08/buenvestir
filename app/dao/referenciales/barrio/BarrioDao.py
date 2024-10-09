# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class BarrioDao:

    def getBarrios(self):

        barrioSQL = """
        SELECT b.idbarrio,b.bar_nombre, c.idciudad, c.ciu_nombre, d.dep_nombre, p.pai_nombre
        FROM barrios b, ciudades c,departamentos d,paises p where b.idciudad=c.idciudad and c.iddepartamento = d.iddepartamento and p.idpais = d.idpais
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(barrioSQL)
            barrios = cur.fetchall() # trae datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{'idbarrio': barrio[0],'bar_nombre': barrio[1],'idciudad': barrio[2], 'ciu_nombre': barrio[3],'dep_nombre': barrio[4],'pai_nombre': barrio[5]} for barrio in barrios]

        except Exception as e:
            app.logger.error(f"Error al obtener todas las barrios: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getBarrioById(self, id):

        barrioSQL = """
        SELECT b.idbarrio,b.bar_nombre,c.idciudad, c.ciu_nombre
        FROM barrios b, ciudades c where b.idciudad=c.idciudad and idbarrio=%s
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(barrioSQL, (id,))
            barrioEncontrada = cur.fetchone() # Obtener una sola fila
            if barrioEncontrada:
                return {
                        "idbarrio": barrioEncontrada[0],
                        "bar_nombre": barrioEncontrada[1],
                        "idciudad": barrioEncontrada[2],
                        "ciu_nombre": barrioEncontrada[3]
                        
                    }  # Retornar los datos de la barrio
            else:
                return None # Retornar None si no se encuentra la barrio
        except Exception as e:
            app.logger.error(f"Error al obtener barrio: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarBarrio(self, descripcion,ciudad_id):

        insertBarrioSQL = """
        INSERT INTO barrios(bar_nombre,idciudad) VALUES(%s,%s) RETURNING idbarrio
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        # Ejecucion exitosa
        try:
            cur.execute(insertBarrioSQL, (descripcion,ciudad_id))
            barrio_id = cur.fetchone()[0]
            con.commit() # se confirma la insercion
            return barrio_id

        # Si algo fallo entra aqui
        except Exception as e:
            app.logger.error(f"Error al insertar barrio: {str(e)}")
            con.rollback() # retroceder si hubo error
            return False

        # Siempre se va ejecutar
        finally:
            cur.close()
            con.close()

    def updateBarrio(self, id, descripcion,ciudad_id):

        updateBarrioSQL = """
        UPDATE barrios
        SET bar_nombre=%s,
        idciudad=%s
        WHERE idbarrio=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateBarrioSQL, (descripcion,ciudad_id, id,))
            filas_afectadas = cur.rowcount # Obtener el número de filas afectadas
            con.commit()

            return filas_afectadas > 0 # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar barrio: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteBarrio(self, id):

        updateBarrioSQL = """
        DELETE FROM barrios
        WHERE idbarrio=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateBarrioSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar barrio: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()