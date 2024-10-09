# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class ProductoDao:

    def getProductos(self):
        productoSQL = """
        SELECT p.idproducto, p.pro_nombre, p.pro_color,  p.idcategoria, c.cat_nombre
        FROM productos p, categorias c
        where p.idcategoria = c.idcategoria 
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(productoSQL)
            productos = cur.fetchall()  # trae datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{'idproducto': producto[0], 'pro_nombre': producto[1], 'pro_color': producto[2],
                     'idcategoria': producto[3], 'cat_nombre': producto[4]} for producto in productos]

        except Exception as e:
            app.logger.error(f"Error al obtener todas las productos: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getProductoById(self, id):
        productoSQL = """
        SELECT p.idproducto, p.pro_nombre, p.pro_color,  p.idcategoria, c.cat_nombre
        FROM productos p, categorias c
        where p.idcategoria = c.idcategoria and p.idproducto = %s
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(productoSQL, (id,))
            productoEncontrada = cur.fetchone()  # Obtener una sola fila
            if productoEncontrada:
                return {
                    'idproducto': productoEncontrada[0],
                    'pro_nombre': productoEncontrada[1],
                    'pro_color': productoEncontrada[2],
                    'idcategoria': productoEncontrada[3],
                    'cat_nombre': productoEncontrada[4]
                    
                }  # Retornar los datos de el producto
            else:
                return None  # Retornar None si no se encuentra el producto
        except Exception as e:
            app.logger.error(f"Error al obtener producto: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarProducto(self, nombre, color, categoria):
        insertProductoSQL = """
        INSERT INTO productos (pro_nombre, pro_color,  idcategoria) 
        VALUES (%s, %s, %s) RETURNING idproducto
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(insertProductoSQL, ( nombre, color, categoria))
            producto_id = cur.fetchone()[0]
            con.commit()  # se confirma la insercion
            return producto_id

        except Exception as e:
            app.logger.error(f"Error al insertar producto: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def updateProducto(self, id,  nombre, color, categoria):
        updateProductoSQL = """
        UPDATE productos
        SET pro_nombre=%s, pro_color=%s, idcategoria=%s
        WHERE idproducto=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateProductoSQL, (nombre, color, categoria, id))
            filas_afectadas = cur.rowcount  # Obtener el número de filas afectadas
            con.commit()

            return filas_afectadas > 0  # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar producto: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteProducto(self, id):
        deleteProductoSQL = """
        DELETE FROM productos
        WHERE idproducto=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deleteProductoSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar producto: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
