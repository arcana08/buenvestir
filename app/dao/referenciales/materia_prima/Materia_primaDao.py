# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class Materia_primaDao:

    def getMateria_primas(self):
        materia_primaSQL = """
        SELECT m.idmateria_prima, m.mat_nombre, m.mat_color, m.mat_unidad_medida, m.mat_cantidad,  m.idcategoria, c.cat_nombre
        FROM materias_primas m, categorias c
        where m.idcategoria = c.idcategoria 
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(materia_primaSQL)
            materia_primas = cur.fetchall()  # trae datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{'idmateria_prima': materia_prima[0], 'mat_nombre': materia_prima[1], 'mat_color': materia_prima[2], 'mat_unidad_medida': materia_prima[3], 
                     'mat_cantidad': materia_prima[4], 'idcategoria': materia_prima[5], 'cat_nombre': materia_prima[6]} for materia_prima in materia_primas]

        except Exception as e:
            app.logger.error(f"Error al obtener todas las materia_primas: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getMateria_primaById(self, id):
        materia_primaSQL = """
        SELECT m.idmateria_prima, m.mat_nombre, m.mat_color, m.mat_unidad_medida, m.mat_cantidad,  m.idcategoria, c.cat_nombre
        FROM materias_primas m, categorias c
        where m.idcategoria = c.idcategoria and m.idmateria_prima = %s
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(materia_primaSQL, (id,))
            materia_primaEncontrada = cur.fetchone()  # Obtener una sola fila
            if materia_primaEncontrada:
                return {
                    'idmateria_prima': materia_primaEncontrada[0],
                    'mat_nombre': materia_primaEncontrada[1],
                    'mat_color': materia_primaEncontrada[2],
                    'mat_unidad_medida': materia_primaEncontrada[3],
                    'mat_cantidad': materia_primaEncontrada[4],
                    'idcategoria': materia_primaEncontrada[5],
                    'cat_nombre': materia_primaEncontrada[6]
                    
                }  # Retornar los datos de la materia_prima
            else:
                return None  # Retornar None si no se encuentra la materia_prima
        except Exception as e:
            app.logger.error(f"Error al obtener materia_prima: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarMateria_prima(self, nombre, color, umedida, cantidad, categoria):
        insertMateria_primaSQL = """
        INSERT INTO materias_primas (mat_nombre, mat_color, mat_unidad_medida, mat_cantidad,  idcategoria) 
        VALUES (%s, %s, %s, %s, %s) RETURNING idmateria_prima
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(insertMateria_primaSQL, ( nombre, color, umedida, cantidad, categoria))
            materia_prima_id = cur.fetchone()[0]
            con.commit()  # se confirma la insercion
            return materia_prima_id

        except Exception as e:
            app.logger.error(f"Error al insertar materia_prima: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def updateMateria_prima(self, id,  nombre, color, umedida, cantidad, categoria):
        updateMateria_primaSQL = """
        UPDATE materias_primas
        SET mat_nombre=%s, mat_color=%s, mat_unidad_medida=%s, mat_cantidad=%s, idcategoria=%s
        WHERE idmateria_prima=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateMateria_primaSQL, (nombre, color, umedida, cantidad, categoria, id))
            filas_afectadas = cur.rowcount  # Obtener el número de filas afectadas
            con.commit()

            return filas_afectadas > 0  # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar materia_prima: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteMateria_prima(self, id):
        deleteMateria_primaSQL = """
        DELETE FROM materias_primas
        WHERE idmateria_prima=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deleteMateria_primaSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar materia_prima: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
