# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class PersonaDao:

    def getPersonas(self):
        personaSQL = """
        SELECT p.idpersona, p.per_nombre, p.per_apellido, p.per_ci, p.per_fechanac, p.per_telefono, p.idbarrio, b.bar_nombre
        FROM personas p, barrios b where p.idbarrio = b.idbarrio 
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(personaSQL)
            personas = cur.fetchall()  # trae datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{'idpersona': persona[0], 'per_nombre': persona[1], 'per_apellido': persona[2], 'per_ci': persona[3], 
                     'per_fechanac': persona[4], 'per_telefono': persona[5], 'idbarrio': persona[6], 'bar_nombre': persona[7]} for persona in personas]

        except Exception as e:
            app.logger.error(f"Error al obtener todas las personas: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getPersonaById(self, id):
        personaSQL = """
        SELECT p.idpersona, p.per_nombre, p.per_apellido, p.per_ci, p.per_fechanac, p.per_telefono, p.idbarrio, b.bar_nombre
        FROM personas p, barrios b
        WHERE p.idbarrio=b.idbarrio and p.idpersona = %s
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(personaSQL, (id,))
            personaEncontrada = cur.fetchone()  # Obtener una sola fila
            if personaEncontrada:
                return {
                    'idpersona': personaEncontrada[0],
                    'per_nombre': personaEncontrada[1],
                    'per_apellido': personaEncontrada[2],
                    'per_ci': personaEncontrada[3],
                    'per_fechanac': personaEncontrada[4],
                    'per_telefono': personaEncontrada[5],
                    'idbarrio': personaEncontrada[6],
                    'bar_nombre': personaEncontrada[7]
                }  # Retornar los datos de la persona
            else:
                return None  # Retornar None si no se encuentra la persona
        except Exception as e:
            app.logger.error(f"Error al obtener persona: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarPersona(self, nombre, apellido, ci, fechanac, telefono, idbarrio):
        insertPersonaSQL = """
        INSERT INTO personas (per_nombre, per_apellido, per_ci, per_fechanac, per_telefono, idbarrio) 
        VALUES (%s, %s, %s, %s, %s, %s) RETURNING idpersona
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(insertPersonaSQL, (nombre, apellido, ci, fechanac, telefono, idbarrio))
            persona_id = cur.fetchone()[0]
            con.commit()  # se confirma la insercion
            return persona_id

        except Exception as e:
            app.logger.error(f"Error al insertar persona: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def updatePersona(self, id, nombre, apellido, ci, fechanac, telefono, idbarrio):
        updatePersonaSQL = """
        UPDATE personas
        SET per_nombre=%s, per_apellido=%s, per_ci=%s, per_fechanac=%s, per_telefono=%s, idbarrio=%s
        WHERE idpersona=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updatePersonaSQL, (nombre, apellido, ci, fechanac, telefono, idbarrio, id))
            filas_afectadas = cur.rowcount  # Obtener el número de filas afectadas
            con.commit()

            return filas_afectadas > 0  # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar persona: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deletePersona(self, id):
        deletePersonaSQL = """
        DELETE FROM personas
        WHERE idpersona=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deletePersonaSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar persona: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
