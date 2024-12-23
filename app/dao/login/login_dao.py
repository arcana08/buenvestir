
from flask import current_app as app
from app.conexion.Conexion import Conexion

class LoginDao:

    def buscarUsuario(self, usu_nick: str):

        buscar_usuario_sql = """
        SELECT u.idusuario, u.usu_nombre,u.usu_clave, u.usu_estado, r.rol_nombre,p.per_nombre,r.idrol 
        FROM usuarios u, roles r, personas p
        where u.idpersona=p.idpersona and u.idrol=r.idrol and u.usu_estado='A' and u.usu_nombre=%s
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(buscar_usuario_sql, (usu_nick,))
            usuario_encontrado = cur.fetchone() # Obtener una sola fila
            if usuario_encontrado:
                return {
                        "idusuario": usuario_encontrado[0]
                        , "usu_nombre": usuario_encontrado[1]
                        , "usu_clave": usuario_encontrado[2]
                        , "usu_estado": usuario_encontrado[3]
                        , "rol_nombre": usuario_encontrado[4]
                        , "per_nombre": usuario_encontrado[5]
                        , "idrol": usuario_encontrado[6]
                        
                    }  # Retornar los datos de la usuario
            else:
                return None # Retornar None si no se encuentra el usuario
        except Exception as e:
            app.logger.error(f"Error al obtener usuario: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()