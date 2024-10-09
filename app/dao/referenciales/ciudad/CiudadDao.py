# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class CiudadDao:

    def getCiudades(self):

        ciudadSQL = """
        SELECT c.idciudad, c.ciu_nombre, d.iddepartamento, d.dep_nombre, p.pai_nombre
        FROM ciudades c,departamentos d,paises p where c.iddepartamento = d.iddepartamento and p.idpais = d.idpais
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(ciudadSQL)
            ciudades = cur.fetchall() # trae datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{'idciudad': ciudad[0], 'ciu_nombre': ciudad[1],'iddepartamento': ciudad[2],'dep_nombre': ciudad[3],'pai_nombre': ciudad[4]} for ciudad in ciudades]

        except Exception as e:
            app.logger.error(f"Error al obtener todas las ciudades: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getCiudadById(self, id):

        ciudadSQL = """
        SELECT c.idciudad, c.ciu_nombre, d.iddepartamento, d.dep_nombre
        FROM ciudades c,departamentos d where c.iddepartamento = d.iddepartamento and idciudad=%s
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(ciudadSQL, (id,))
            ciudadEncontrada = cur.fetchone() # Obtener una sola fila
            if ciudadEncontrada:
                return {
                        "idciudad": ciudadEncontrada[0],
                        "ciu_nombre": ciudadEncontrada[1],
                        "iddepartamento": ciudadEncontrada[2],
                        "dep_nombre": ciudadEncontrada[3]
                    }  # Retornar los datos de la ciudad
            else:
                return None # Retornar None si no se encuentra la ciudad
        except Exception as e:
            app.logger.error(f"Error al obtener ciudad: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarCiudad(self, descripcion,departamento_id):

        insertCiudadSQL = """
        INSERT INTO ciudades(ciu_nombre,iddepartamento) VALUES(%s,%s) RETURNING idciudad
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        # Ejecucion exitosa
        try:
            cur.execute(insertCiudadSQL, (descripcion,departamento_id))
            ciudad_id = cur.fetchone()[0]
            con.commit() # se confirma la insercion
            return ciudad_id

        # Si algo fallo entra aqui
        except Exception as e:
            app.logger.error(f"Error al insertar ciudad: {str(e)}")
            con.rollback() # retroceder si hubo error
            return False

        # Siempre se va ejecutar
        finally:
            cur.close()
            con.close()

    def updateCiudad(self, id, descripcion,departamento_id):

        updateCiudadSQL = """
        UPDATE ciudades
        SET ciu_nombre=%s,
        iddepartamento=%s
        WHERE idciudad=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateCiudadSQL, (descripcion,departamento_id, id,))
            filas_afectadas = cur.rowcount # Obtener el número de filas afectadas
            con.commit()

            return filas_afectadas > 0 # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar ciudad: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteCiudad(self, id):

        updateCiudadSQL = """
        DELETE FROM ciudades
        WHERE idciudad=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateCiudadSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar ciudad: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()