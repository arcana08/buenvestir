# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class FuncionarioDao:

    def getFuncionarios(self):
        funcionarioSQL = """
        SELECT f.idfuncionario, p.per_nombre, t.tra_nombre
        FROM funcionarios f, personas p, trabajos t
        WHERE f.idpersona = p.idpersona and f.idtrabajo = t.idtrabajo
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(funcionarioSQL)
            funcionarios = cur.fetchall()

            # Transformar los datos en una lista de diccionarios
            return [{'idfuncionario': funcionario[0], 'per_nombre': funcionario[1], 'tra_nombre': funcionario[2]} 
                    for funcionario in funcionarios]

        except Exception as e:
            app.logger.error(f"Error al obtener todos los funcionarios: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getFuncionarioById(self, id):
        funcionarioSQL = """
        SELECT f.idfuncionario, p.per_nombre, t.tra_nombre, f.idpersona, f.idtrabajo
        FROM funcionarios f, personas p, trabajos t
        WHERE f.idpersona = p.idpersona and f.idtrabajo = t.idtrabajo and f.idfuncionario = %s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(funcionarioSQL, (id,))
            funcionarioEncontrado = cur.fetchone()
            if funcionarioEncontrado:
                return {
                    'idfuncionario': funcionarioEncontrado[0],
                    'per_nombre': funcionarioEncontrado[1],
                    'tra_nombre': funcionarioEncontrado[2],
                    'idpersona': funcionarioEncontrado[3],
                    'idtrabajo': funcionarioEncontrado[4]
                }
            else:
                return None

        except Exception as e:
            app.logger.error(f"Error al obtener funcionario: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarFuncionario(self, idpersona, idtrabajo):
        insertFuncionarioSQL = """
        INSERT INTO funcionarios (idpersona, idtrabajo) 
        VALUES (%s, %s) RETURNING idfuncionario
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(insertFuncionarioSQL, (idpersona, idtrabajo))
            funcionario_id = cur.fetchone()[0]
            con.commit()
            return funcionario_id

        except Exception as e:
            app.logger.error(f"Error al insertar funcionario: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def updateFuncionario(self, id, idtrabajo):
        updateFuncionarioSQL = """
        UPDATE funcionarios
        SET idtrabajo=%s
        WHERE idfuncionario=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(updateFuncionarioSQL, (idtrabajo, id))
            filas_afectadas = cur.rowcount
            con.commit()
            return filas_afectadas > 0

        except Exception as e:
            app.logger.error(f"Error al actualizar funcionario: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteFuncionario(self, id):
        deleteFuncionarioSQL = """
        DELETE FROM funcionarios
        WHERE idfuncionario=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(deleteFuncionarioSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()
            return rows_affected > 0

        except Exception as e:
            app.logger.error(f"Error al eliminar funcionario: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
