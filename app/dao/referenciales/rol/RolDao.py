# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class RolDao:

    def getRoles(self):

        rolSQL = """
        SELECT idrol, rol_nombre
        FROM roles
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(rolSQL)
            roles = cur.fetchall()  # trae datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{'idrol': rol[0], 'rol_nombre': rol[1]} for rol in roles]

        except Exception as e:
            app.logger.error(f"Error al obtener todos los roles: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getRolById(self, id):

        rolSQL = """
        SELECT idrol, rol_nombre
        FROM roles WHERE idrol=%s
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(rolSQL, (id,))
            rolEncontrado = cur.fetchone()  # Obtener una sola fila
            if rolEncontrado:
                return {
                    "idrol": rolEncontrado[0],
                    "rol_nombre": rolEncontrado[1]
                }  # Retornar los datos del rol
            else:
                return None  # Retornar None si no se encuentra el rol
        except Exception as e:
            app.logger.error(f"Error al obtener rol: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarRol(self, nombre):

        insertRolSQL = """
        INSERT INTO roles(rol_nombre) VALUES(%s) RETURNING idrol
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        # Ejecucion exitosa
        try:
            cur.execute(insertRolSQL, (nombre,))
            rol_id = cur.fetchone()[0]
            con.commit()  # se confirma la insercion
            return rol_id

        # Si algo fallo entra aqui
        except Exception as e:
            app.logger.error(f"Error al insertar rol: {str(e)}")
            con.rollback()  # retroceder si hubo error
            return False

        # Siempre se va ejecutar
        finally:
            cur.close()
            con.close()

    def updateRol(self, id, nombre):

        updateRolSQL = """
        UPDATE roles
        SET rol_nombre=%s
        WHERE idrol=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateRolSQL, (nombre, id,))
            filas_afectadas = cur.rowcount  # Obtener el número de filas afectadas
            con.commit()

            return filas_afectadas > 0  # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar rol: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteRol(self, id):

        deleteRolSQL = """
        DELETE FROM roles
        WHERE idrol=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deleteRolSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar rol: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
