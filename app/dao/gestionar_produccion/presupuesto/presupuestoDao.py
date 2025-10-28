# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class PresupuestoDao:

    def getPresupuestos(self):
        presupuestosQL = """
        SELECT pr.idpresupuesto, p.per_nombre, p.per_apellido, p.per_ci, pr.pre_estado, pr.fecha_alta
        FROM presupuesto pr
        JOIN clientes c ON pr.id_cliente = c.idcliente
        JOIN personas p ON c.idpersona = p.idpersona
        ORDER BY pr.fecha_alta DESC
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(presupuestosQL)
            filas = cur.fetchall()
            return [
                {
                    'idpresupuesto': fila[0],
                    'per_nombre': fila[1],
                    'per_apellido': fila[2],
                    'per_ci': fila[3],
                    'pre_estado': fila[4],
                    'fecha_alta': fila[5]
                }
                for fila in filas
            ]
        except Exception as e:
            app.logger.error(f"Error al obtener todos los presupuestos: {e}")
            return []
        finally:
            cur.close()
            con.close()

    def getPresupuestoById(self, id):
        presupuestosQL = """
        SELECT pr.idpresupuesto, pr.id_cliente, p.per_nombre, p.per_apellido, p.per_ci,
               pr.pre_estado, pr.fecha_alta, pr.fecha_solicitud, pr.fecha_estado, pr.total
        FROM presupuesto pr
        JOIN clientes c ON pr.id_cliente = c.idcliente
        JOIN personas p ON c.idpersona = p.idpersona
        WHERE pr.idpresupuesto = %s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(presupuestosQL, (id,))
            fila = cur.fetchone()
            if fila:
                return {
                    'idpresupuesto': fila[0],
                    'id_cliente': fila[1],
                    'per_nombre': fila[2],
                    'per_apellido': fila[3],
                    'per_ci': fila[4],
                    'pre_estado': fila[5],
                    'fecha_alta': fila[6],
                    'fecha_solicitud': fila[7],
                    'fecha_estado': fila[8],
                    'total': fila[9]
                }
            return None
        except Exception as e:
            app.logger.error(f"Error al obtener presupuesto por id: {e}")
            return None
        finally:
            cur.close()
            con.close()

    def getDetallesByPresupuestoId(self, presupuesto_id):
        detallesSQL = """
        SELECT pd.id_costo, prd.pro_nombre, prd.pro_color, c.cos_total
        FROM presupuesto_detalle pd
        JOIN costos c ON pd.id_costo = c.idcosto
        JOIN productos prd ON c.idproducto = prd.idproducto
        WHERE pd.id_presupuesto = %s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(detallesSQL, (presupuesto_id,))
            filas = cur.fetchall()
            return [
                {
                    'idcosto': fila[0],
                    'pro_nombre': fila[1],
                    'pro_color': fila[2],
                    'cos_prenda': fila[3]
                } for fila in filas
            ]
        except Exception as e:
            app.logger.error(f"Error al obtener detalles del presupuesto: {e}")
            return []
        finally:
            cur.close()
            con.close()

    def guardarPresupuesto(self, cliente_id, detalles, total):
        insertPresupuestoQL = """
        INSERT INTO presupuesto (id_cliente, pre_estado, fecha_alta, total)
        VALUES (%s, %s, now(), %s)
        RETURNING idpresupuesto
        """
        insertDetalleSQL = """
        INSERT INTO presupuesto_detalle (id_presupuesto, id_costo) VALUES (%s, %s)
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(insertPresupuestoQL, (cliente_id, 'P', total))
            id_presupuesto = cur.fetchone()[0]
            app.logger.info(f"Nuevo presupuesto id={id_presupuesto}, detalles={detalles}, total={total}")
            for detalle in detalles:
                if isinstance(detalle, dict):
                    id_costo = detalle.get('idcosto') or detalle.get('id_costo') or detalle.get('idCosto')
                else:
                    id_costo = detalle
                cur.execute(insertDetalleSQL, (id_presupuesto, int(id_costo)))
            con.commit()
            return id_presupuesto
        except Exception as e:
            app.logger.error(f"Error al insertar presupuesto para cliente {cliente_id}: {e}")
            con.rollback()
            return None
        finally:
            cur.close()
            con.close()

    def procesarPresupuesto(self, id):
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute("SELECT pre_estado FROM presupuesto WHERE idpresupuesto = %s", (id,))
            fila = cur.fetchone()
            if not fila:
                raise ValueError("Presupuesto no encontrado.")
            estado = fila[0]

            # Solo procesar si está en estado pendiente ('P') o en otro estado permitido ('6')
            if estado in ('P', '6'):
                cur.execute("SELECT id_costo FROM presupuesto_detalle WHERE id_presupuesto = %s", (id,))
                costos = cur.fetchall()
                if not costos:
                    raise ValueError("No se encontraron costos asociados al presupuesto.")

                for costo_row in costos:
                    idcosto = costo_row[0]
                    cur.execute("""
                        SELECT idmateria_prima, dco_cantidad
                        FROM detalle_costos
                        WHERE idcosto = %s
                    """, (idcosto,))
                    materias_primas = cur.fetchall()
                    if not materias_primas:
                        raise ValueError(f"No se encontraron materias primas para el costo {idcosto}.")

                    for mp in materias_primas:
                        idmp = mp[0]
                        cantidad_requerida = float(mp[1])
                        cur.execute("SELECT mat_cantidad FROM materias_primas WHERE idmateria_prima = %s", (idmp,))
                        stock_row = cur.fetchone()
                        if not stock_row:
                            raise ValueError(f"No se encontró la materia prima con ID {idmp}.")
                        stock_actual = float(stock_row[0])
                        if stock_actual < cantidad_requerida:
                            raise ValueError(f"Stock insuficiente para la materia prima {idmp}. (Requerido: {cantidad_requerida}, Disponible: {stock_actual})")
                        cur.execute("""
                            UPDATE materias_primas
                            SET mat_cantidad = mat_cantidad - %s
                            WHERE idmateria_prima = %s
                        """, (cantidad_requerida, idmp))

                # actualizar estado del presupuesto a '3' (procesado)
                cur.execute("""
                    UPDATE presupuesto
                    SET pre_estado = %s, fecha_estado = now()
                    WHERE idpresupuesto = %s
                """, ('3', id))
                con.commit()
                return True
            else:
                raise ValueError("El presupuesto no está en estado procesable.")
        except Exception as e:
            app.logger.error(f"Error al procesar presupuesto: {e}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def finalizarPresupuesto(self, id):
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute("""
                UPDATE presupuesto
                SET pre_estado = %s, fecha_estado = now()
                WHERE idpresupuesto = %s
            """, ('4', id))
            con.commit()
            return cur.rowcount > 0
        except Exception as e:
            app.logger.error(f"Error al finalizar presupuesto: {e}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def mejorarPresupuesto(self, id):
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute("""
                UPDATE presupuesto
                SET pre_estado = %s, fecha_estado = now()
                WHERE idpresupuesto = %s
            """, ('6', id))
            con.commit()
            return cur.rowcount > 0
        except Exception as e:
            app.logger.error(f"Error al mejorar presupuesto: {e}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def rechazarPresupuesto(self, id):
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute("""
                UPDATE presupuesto
                SET pre_estado = %s, fecha_estado = now()
                WHERE idpresupuesto = %s
            """, ('5', id))
            con.commit()
            return cur.rowcount > 0
        except Exception as e:
            app.logger.error(f"Error al rechazar presupuesto: {e}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def updateMateriasPrimas(self, detalles):
        updateMateriaPrimaSQL = """
        UPDATE materias_primas
        SET mat_cantidad = mat_cantidad - %s
        WHERE idmateria_prima = %s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            for detalle in detalles:
                idmateria_prima = int(detalle['idmateria_prima'])
                cantidad = int(detalle['dco_cantidad'])
                cur.execute(updateMateriaPrimaSQL, (cantidad, idmateria_prima))
            con.commit()
            return True
        except Exception as e:
            app.logger.error(f"Error al actualizar materias primas: {e}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def deletePresupuesto(self, id):
        deleteSQL = """
        DELETE FROM presupuesto
        WHERE idpresupuesto = %s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(deleteSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()
            return rows_affected > 0
        except Exception as e:
            app.logger.error(f"Error al eliminar presupuesto: {e}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def aprobarPresupuesto(self, presupuesto_id):
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        from datetime import datetime
        fecha_actual = datetime.now()
        try:
            # 1. Verifica estado
            cur.execute("SELECT pre_estado, id_orden_produccion FROM presupuesto WHERE idpresupuesto = %s", (presupuesto_id,))
            row = cur.fetchone()
            if not row:
                return {'success': False, 'error': 'Presupuesto no encontrado.'}
            if row[0] == 'A' or row[1] is not None:
                return {'success': False, 'error': 'El presupuesto ya está aprobado o en producción.'}
            if row[0] == 'R':
                return {'success': False, 'error': 'El presupuesto está anulado.'}

            # 2. Trae cabecera y detalles
            cur.execute("SELECT id_cliente FROM presupuesto WHERE idpresupuesto = %s", (presupuesto_id,))
            cabecera = cur.fetchone()
            cur.execute("SELECT id_costo FROM presupuesto_detalle WHERE id_presupuesto = %s", (presupuesto_id,))
            detalles = cur.fetchall()

            # 3. Inserta en orden_produccion
            
            
            estado_orden = '2'  # O el estado inicial que corresponda
            cur.execute("""
                INSERT INTO public.orden_produccion(idcliente, estado, fecha)
                VALUES (%s, %s, %s)
                RETURNING idorden_produccion
            """, (cabecera[0], estado_orden, fecha_actual))
            id_orden = cur.fetchone()[0]

            # 4. Inserta detalles en detalle_produccion
            for det in detalles:
                cur.execute("""
                    INSERT INTO public.detalle_produccion(idorden_produccion, idcosto)
                    VALUES (%s, %s)
                """, (id_orden, det[0]))

            # 5. Actualiza presupuesto
            cur.execute("UPDATE presupuesto SET pre_estado = %s, id_orden_produccion = %s, fecha_alta = %s WHERE idpresupuesto = %s", ('A', id_orden, fecha_actual, presupuesto_id))
            con.commit()
            return {'success': True}
        except Exception as e:
            con.rollback()
            app.logger.error(f"Error al aprobar presupuesto: {e}")
            return {'success': False, 'error': str(e)}
        finally:
            cur.close()
            con.close()

    def anularPresupuesto(self, presupuesto_id):
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute("SELECT pre_estado, id_orden_produccion FROM presupuesto WHERE idpresupuesto = %s", (presupuesto_id,))
            row = cur.fetchone()
            if not row:
                return {'success': False, 'error': 'Presupuesto no encontrado.'}
            if row[1] is not None or row[0] == 'A':
                return {'success': False, 'error': 'No se puede anular un presupuesto en producción o aprobado.'}
            cur.execute("UPDATE presupuesto SET pre_estado = %s WHERE idpresupuesto = %s", ('R', presupuesto_id))
            con.commit()
            return {'success': True}
        except Exception as e:
            con.rollback()
            app.logger.error(f"Error al anular presupuesto: {e}")
            return {'success': False, 'error': str(e)}
        finally:
            cur.close()
            con.close()