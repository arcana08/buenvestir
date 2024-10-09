# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class PaisDao:

    def getPaises(self):

        paisSQL = """
        SELECT idpais, pai_nombre
        FROM paises
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(paisSQL)
            paises = cur.fetchall() # trae datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{'idpais': pais[0], 'pai_nombre': pais[1]} for pais in paises]

        except Exception as e:
            app.logger.error(f"Error al obtener todas las paises: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getPaisById(self, id):

        paisSQL = """
        SELECT idpais, pai_nombre
        FROM paises WHERE idpais=%s
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(paisSQL, (id,))
            paisEncontrada = cur.fetchone() # Obtener una sola fila
            if paisEncontrada:
                return {
                        "idpais": paisEncontrada[0],
                        "pai_nombre": paisEncontrada[1]
                    }  # Retornar los datos de la ciudad
            else:
                return None # Retornar None si no se encuentra la ciudad
        except Exception as e:
            app.logger.error(f"Error al obtener pais: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarPais(self, descripcion):

        insertPaisSQL = """
        INSERT INTO paises(pai_nombre) VALUES(%s) RETURNING idpais
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        # Ejecucion exitosa
        try:
            cur.execute(insertPaisSQL, (descripcion,))
            pais_id = cur.fetchone()[0]
            con.commit() # se confirma la insercion
            return pais_id

        # Si algo fallo entra aqui
        except Exception as e:
            app.logger.error(f"Error al insertar pais: {str(e)}")
            con.rollback() # retroceder si hubo error
            return False

        # Siempre se va ejecutar
        finally:
            cur.close()
            con.close()

    def updatePais(self, id, descripcion):

        updatePaisSQL = """
        UPDATE paises
        SET pai_nombre=%s
        WHERE idpais=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updatePaisSQL, (descripcion, id,))
            filas_afectadas = cur.rowcount # Obtener el número de filas afectadas
            con.commit()

            return filas_afectadas > 0 # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar pais: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deletePais(self, id):

        updatePaisSQL = """
        DELETE FROM paises
        WHERE idpais=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updatePaisSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar pais: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()