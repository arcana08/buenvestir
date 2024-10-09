# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class ClienteDao:

    def getClientes(self):
        clienteSQL = """
        SELECT c.idcliente, p.per_nombre
        FROM clientes c, personas p
        WHERE c.idpersona = p.idpersona 
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(clienteSQL)
            clientes = cur.fetchall()

            # Transformar los datos en una lista de diccionarios
            return [{'idcliente': cliente[0], 'per_nombre': cliente[1]} 
                    for cliente in clientes]

        except Exception as e:
            app.logger.error(f"Error al obtener todos los clientes: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getClienteById(self, id):
        clienteSQL = """
        SELECT c.idcliente, p.per_nombre, c.idpersona
        FROM clientes c, personas p, trabajos t
        WHERE c.idpersona = p.idpersona  and c.idcliente = %s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(clienteSQL, (id,))
            clienteEncontrado = cur.fetchone()
            if clienteEncontrado:
                return {
                    'idcliente': clienteEncontrado[0],
                    'per_nombre': clienteEncontrado[1],
                    'idpersona': clienteEncontrado[2]
                }
            else:
                return None

        except Exception as e:
            app.logger.error(f"Error al obtener cliente: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarCliente(self, idpersona):
        insertClienteSQL = """
        INSERT INTO clientes (idpersona) 
        VALUES ( %s) RETURNING idcliente
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(insertClienteSQL, (idpersona,))
            cliente_id = cur.fetchone()[0]
            con.commit()
            return cliente_id

        except Exception as e:
            app.logger.error(f"Error al insertar cliente: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def updateCliente(self, id, idpersona):
        updateClienteSQL = """
        UPDATE clientes
        SET idpersona=%s
        WHERE idcliente=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(updateClienteSQL, (idpersona, id))
            filas_afectadas = cur.rowcount
            con.commit()
            return filas_afectadas > 0

        except Exception as e:
            app.logger.error(f"Error al actualizar cliente: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteCliente(self, id):
        deleteClienteSQL = """
        DELETE FROM clientes
        WHERE idcliente=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(deleteClienteSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()
            return rows_affected > 0

        except Exception as e:
            app.logger.error(f"Error al eliminar cliente: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
