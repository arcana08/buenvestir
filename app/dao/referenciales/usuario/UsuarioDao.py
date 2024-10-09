# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class UsuarioDao:

    def getUsuarios(self):
        usuarioSQL = """
        SELECT u.idusuario, u.usu_nombre, u.usu_estado, r.rol_nombre,p.per_nombre
        FROM usuarios u, roles r, personas p
        where u.idpersona=p.idpersona and u.idrol=r.idrol
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(usuarioSQL)
            usuarios = cur.fetchall()

            # Transformar los datos en una lista de diccionarios
            return [{'idusuario': usuario[0], 'usu_nombre': usuario[1], 'usu_estado': usuario[2], 
                     'rol_nombre': usuario[3], 'per_nombre': usuario[4]} 
                    for usuario in usuarios]

        except Exception as e:
            app.logger.error(f"Error al obtener todos los usuarios: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getUsuarioById(self, id):
        usuarioSQL = """
        SELECT u.idusuario, u.usu_nombre, u.usu_estado, r.rol_nombre,p.per_nombre,u.idrol,u.idpersona
        FROM usuarios u, roles r, personas p
        where u.idpersona=p.idpersona and u.idrol=r.idrol and u.idusuario = %s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(usuarioSQL, (id,))
            usuarioEncontrado = cur.fetchone()
            if usuarioEncontrado:
                return {
                    'idusuario': usuarioEncontrado[0],
                    'usu_nombre': usuarioEncontrado[1],
                    'usu_estado': usuarioEncontrado[2],
                    'rol_nombre': usuarioEncontrado[3],
                    'per_nombre': usuarioEncontrado[4],
                    'idrol': usuarioEncontrado[5],
                    'idpersona': usuarioEncontrado[6]
                }
            else:
                return None

        except Exception as e:
            app.logger.error(f"Error al obtener usuario: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarUsuario(self, nombre, clave, estado, idpersona, idrol):
        insertUsuarioSQL = """
        INSERT INTO usuarios (usu_nombre, usu_clave, usu_estado, idpersona, idrol) 
        VALUES (%s, %s, %s, %s, %s) RETURNING idusuario
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(insertUsuarioSQL, (nombre, clave, estado, idpersona, idrol))
            usuario_id = cur.fetchone()[0]
            con.commit()
            return usuario_id

        except Exception as e:
            app.logger.error(f"Error al insertar usuario: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def updateUsuario(self, id, nombre, clave, estado, idrol):
        updateUsuarioSQL = """
        UPDATE usuarios
        SET usu_nombre=%s, usu_clave=%s, usu_estado=%s, idrol=%s
        WHERE idusuario=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(updateUsuarioSQL, (nombre, clave, estado, idrol, id))
            filas_afectadas = cur.rowcount
            con.commit()
            return filas_afectadas > 0

        except Exception as e:
            app.logger.error(f"Error al actualizar usuario: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteUsuario(self, id):
        deleteUsuarioSQL = """
        DELETE FROM usuarios
        WHERE idusuario=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(deleteUsuarioSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()
            return rows_affected > 0

        except Exception as e:
            app.logger.error(f"Error al eliminar usuario: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
