# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class DepartamentoDao:

    def getDepartamentos(self):

        departamentoSQL = """
        SELECT iddepartamento, dep_nombre,d.idpais, pai_nombre
        FROM departamentos d,paises p where d.idpais=p.idpais
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(departamentoSQL)
            departamentos = cur.fetchall() # trae datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{
                'iddepartamento': departamento[0], 'dep_nombre': departamento[1],'idpais': departamento[2],'pai_nombre': departamento[3]
                } for departamento in departamentos]

        except Exception as e:
            app.logger.error(f"Error al obtener todas los departamentos: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getDepartamentoById(self, id):

        departamentoSQL = """
        SELECT iddepartamento, dep_nombre,d.idpais, pai_nombre
        FROM departamentos d,paises p where d.idpais=p.idpais and iddepartamento=%s
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(departamentoSQL, (id,))
            departamentoEncontrada = cur.fetchone() # Obtener una sola fila
            if departamentoEncontrada:
                return {
                        "iddepartamento": departamentoEncontrada[0],
                        "dep_nombre": departamentoEncontrada[1],
                        "idpais": departamentoEncontrada[2],
                        "pai_nombre": departamentoEncontrada[3]
                    }  # Retornar los datos del departamento
            else:
                return None # Retornar None si no se encuentra la ciudad
        except Exception as e:
            app.logger.error(f"Error al obtener departamento: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarDepartamento(self, descripcion, id_pais):

        insertDepartamentoSQL = """
        INSERT INTO departamentos(dep_nombre,idpais) VALUES(%s,%s) RETURNING iddepartamento
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        # Ejecucion exitosa
        try:
            cur.execute(insertDepartamentoSQL, (descripcion,id_pais))
            departamento_id = cur.fetchone()[0]
            con.commit() # se confirma la insercion
            return departamento_id

        # Si algo fallo entra aqui
        except Exception as e:
            app.logger.error(f"Error al insertar departamento: {str(e)}")
            con.rollback() # retroceder si hubo error
            return False

        # Siempre se va ejecutar
        finally:
            cur.close()
            con.close()

    def updateDepartamento(self, id, descripcion,idpais):

        updateDepartamentoSQL = """
        UPDATE departamentos
        SET dep_nombre=%s,
        idpais=%s
        WHERE iddepartamento=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateDepartamentoSQL, (descripcion,idpais, id,))
            filas_afectadas = cur.rowcount # Obtener el número de filas afectadas
            con.commit()

            return filas_afectadas > 0 # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar departamento: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteDepartamento(self, id):

        updateDepartamentoSQL = """
        DELETE FROM departamentos
        WHERE iddepartamento=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateDepartamentoSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar departamento: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()