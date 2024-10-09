# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class TrabajoDao:

    def getTrabajos(self):

        trabajoSQL = """
        SELECT idtrabajo, tra_nombre
        FROM trabajos
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(trabajoSQL)
            trabajos = cur.fetchall()  # trae datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{'idtrabajo': trabajo[0], 'tra_nombre': trabajo[1]} for trabajo in trabajos]

        except Exception as e:
            app.logger.error(f"Error al obtener todos los trabajos: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getTrabajoById(self, id):

        trabajoSQL = """
        SELECT idtrabajo, tra_nombre
        FROM trabajos WHERE idtrabajo=%s
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(trabajoSQL, (id,))
            trabajoEncontrado = cur.fetchone()  # Obtener una sola fila
            if trabajoEncontrado:
                return {
                    "idtrabajo": trabajoEncontrado[0],
                    "tra_nombre": trabajoEncontrado[1]
                }  # Retornar los datos del trabajo
            else:
                return None  # Retornar None si no se encuentra el trabajo
        except Exception as e:
            app.logger.error(f"Error al obtener trabajo: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarTrabajo(self, nombre):

        insertTrabajoSQL = """
        INSERT INTO trabajos(tra_nombre) VALUES(%s) RETURNING idtrabajo
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        # Ejecución exitosa
        try:
            cur.execute(insertTrabajoSQL, (nombre,))
            trabajo_id = cur.fetchone()[0]
            con.commit()  # Confirmar la inserción
            return trabajo_id

        # Si algo falló
        except Exception as e:
            app.logger.error(f"Error al insertar trabajo: {str(e)}")
            con.rollback()  # Retroceder si hubo error
            return False

        finally:
            cur.close()
            con.close()

    def updateTrabajo(self, id, nombre):

        updateTrabajoSQL = """
        UPDATE trabajos
        SET tra_nombre=%s
        WHERE idtrabajo=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateTrabajoSQL, (nombre, id,))
            filas_afectadas = cur.rowcount  # Obtener el número de filas afectadas
            con.commit()

            return filas_afectadas > 0  # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar trabajo: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteTrabajo(self, id):

        deleteTrabajoSQL = """
        DELETE FROM trabajos
        WHERE idtrabajo=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deleteTrabajoSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar trabajo: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
