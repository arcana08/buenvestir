# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class DepositoDao:

    def getDepositos(self):

        depositoSQL = """
        SELECT iddeposito, dep_nombre
        FROM depositos
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(depositoSQL)
            depositos = cur.fetchall()  # trae datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{'iddeposito': deposito[0], 'dep_nombre': deposito[1]} for deposito in depositos]

        except Exception as e:
            app.logger.error(f"Error al obtener todos los depositos: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getDepositoById(self, id):

        depositoSQL = """
        SELECT iddeposito, dep_nombre
        FROM depositos WHERE iddeposito=%s
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(depositoSQL, (id,))
            depositoEncontrado = cur.fetchone()  # Obtener una sola fila
            if depositoEncontrado:
                return {
                    "iddeposito": depositoEncontrado[0],
                    "dep_nombre": depositoEncontrado[1]
                }  # Retornar los datos del depósito
            else:
                return None  # Retornar None si no se encuentra el depósito
        except Exception as e:
            app.logger.error(f"Error al obtener deposito: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarDeposito(self, nombre):

        insertDepositoSQL = """
        INSERT INTO depositos(dep_nombre) VALUES(%s) RETURNING iddeposito
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        # Ejecucion exitosa
        try:
            cur.execute(insertDepositoSQL, (nombre,))
            deposito_id = cur.fetchone()[0]
            con.commit()  # se confirma la insercion
            return deposito_id

        # Si algo fallo entra aqui
        except Exception as e:
            app.logger.error(f"Error al insertar deposito: {str(e)}")
            con.rollback()  # retroceder si hubo error
            return False

        # Siempre se va ejecutar
        finally:
            cur.close()
            con.close()

    def updateDeposito(self, id, nombre):

        updateDepositoSQL = """
        UPDATE depositos
        SET dep_nombre=%s
        WHERE iddeposito=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateDepositoSQL, (nombre, id,))
            filas_afectadas = cur.rowcount  # Obtener el número de filas afectadas
            con.commit()

            return filas_afectadas > 0  # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar deposito: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteDeposito(self, id):

        deleteDepositoSQL = """
        DELETE FROM depositos
        WHERE iddeposito=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deleteDepositoSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar deposito: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
