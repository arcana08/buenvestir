# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class EproDao:

    def getEtapasProduccion(self):

        etapaSQL = """
        SELECT idetapa_produccion, eta_nombre
        FROM etapas_producciones
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(etapaSQL)
            etapas = cur.fetchall()  # Trae los datos de la base de datos

            # Transformar los datos en una lista de diccionarios
            return [{'idetapa_produccion': etapa[0], 'eta_nombre': etapa[1]} for etapa in etapas]

        except Exception as e:
            app.logger.error(f"Error al obtener todas las etapas de producción: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getEtapaProduccionById(self, id):

        etapaSQL = """
        SELECT idetapa_produccion, eta_nombre
        FROM etapas_producciones WHERE idetapa_produccion=%s
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(etapaSQL, (id,))
            etapaEncontrada = cur.fetchone()  # Obtener una sola fila
            if etapaEncontrada:
                return {
                    "idetapa_produccion": etapaEncontrada[0],
                    "eta_nombre": etapaEncontrada[1]
                }  # Retornar los datos de la etapa de producción
            else:
                return None  # Retornar None si no se encuentra la etapa
        except Exception as e:
            app.logger.error(f"Error al obtener etapa de producción: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarEtapaProduccion(self, nombre):

        insertEtapaSQL = """
        INSERT INTO etapas_producciones(eta_nombre) VALUES(%s) RETURNING idetapa_produccion
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(insertEtapaSQL, (nombre,))
            etapa_id = cur.fetchone()[0]
            con.commit()  # Confirmar la inserción
            return etapa_id

        except Exception as e:
            app.logger.error(f"Error al insertar etapa de producción: {str(e)}")
            con.rollback()  # Retroceder si hubo error
            return False

        finally:
            cur.close()
            con.close()

    def updateEtapaProduccion(self, id, nombre):

        updateEtapaSQL = """
        UPDATE etapas_producciones
        SET eta_nombre=%s
        WHERE idetapa_produccion=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateEtapaSQL, (nombre, id,))
            filas_afectadas = cur.rowcount  # Obtener el número de filas afectadas
            con.commit()

            return filas_afectadas > 0  # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar etapa de producción: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteEtapaProduccion(self, id):

        deleteEtapaSQL = """
        DELETE FROM etapas_producciones
        WHERE idetapa_produccion=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deleteEtapaSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar etapa de producción: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
