import asyncio
from datetime import datetime
import logging


class CopyReportRep:
    
    
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
        
    async def  get_copy_report(self, conn, start_date, final_date) :
        try:
            query = """
                    SELECT DISTINCT
                    P.PROCESO_ID,
                    TO_CHAR(A.ACTUACION_PROCESAL_ID) AS ACTUACION_PROCESAL_ID,

                    CASE
                        WHEN DAP.DATO_VALOR IS NOT NULL THEN 'ConCopia'
                        ELSE 'SinCopia'
                    END AS COPIAS,

                    DAP3.DATO_VALOR AS GESTION_COPIA,
                    TO_CHAR(A.ACTUACION_FECHA, 'DD-MON-YYYY') AS FECHA_NOTIFICACION,
                    DAP2.DATO_VALOR AS VALOR_MAND,
                    P.DESPACHO_NOMBRE,
                    P.CIUDAD,
                    CN.COORDINADOR,

                    CASE
                        WHEN P.DESPACHO_ID IN (
                            SELECT DESPACHO_ID
                            FROM TORRE_DESPACHO
                            WHERE GESTOR_RAMA = 'SI'
                        ) THEN 'NOTIFICAD'
                        ELSE 'OPERAC'
                    END AS ORIGEN,

                    CN.REGIONAL,
                    TO_CHAR(F.FUNCIONARIO_ID) AS CEDULA_DEPENDIENTE,
                    F.FUNCIONARIO_NOMBRE || ' ' || F.FUNCIONARIO_APELLIDO AS NOMBRE_DEPENDIENTE,
                    F2.FUNCIONARIO_NOMBRE || ' ' || F2.FUNCIONARIO_APELLIDO AS NOMBRE_NOTIFICADOR,
                    P.TIPO_PROCESO,
                    '.' || P.RADICACION AS RADICACION,
                    P.AÑO,
                    P.DEMANDANTE,
                    P.DEMANDADO,
                    P.COPIAS,
                    P.TP_PROCESO_ID,
                    P.LOCALIDAD_ID,
                    P.DESPACHO_ID,
                    P.DESPACHO_DIRECCION,
                    P.DESPACHO_TELEFONO,
                    P.DESPACHO_CONTACTO,
                    A.*,
                    C.CLIENTE_ID,

                    CASE
                        WHEN CB.CLIENTE_ID IS NULL THEN 'OTROS_CLIENT'
                        ELSE 'CLIENTE_BANCO'
                    END AS TIPO_CLIENTE,

                    C.CLIENTE_NOMBRE1 || ' ' ||
                    C.CLIENTE_NOMBRE2 || ' ' ||
                    C.CLIENTE_NOMBRE3 || ' ' ||
                    C.CLIENTE_NOMBRE4 AS CLIENTE_NOMBRE,

                    F1.FUNCIONARIO_NOMBRE || ' ' || F1.FUNCIONARIO_APELLIDO AS GESTOR,
                    DAP1.DATO_VALOR AS RESUELVE,
                    DP.DATO_VALOR AS AUTORIZACION

                FROM VPROCESOS P

                INNER JOIN PROCESOS_CLIENTES PC
                    ON P.PROCESO_ID = PC.PROCESO_ID

                INNER JOIN CLIENTES C
                    ON PC.CLIENTE_ID = C.CLIENTE_ID
                AND C.CLIENTE_ID NOT IN (
                    0,10211,24567,23041,24470,24546,22766,24689,
                    20969,24849,25597,22042,24714,21854,22416,
                    10280,23263,25172
                )

                INNER JOIN VACTUACIONES A
                    ON P.PROCESO_ID = A.PROCESO_ID
                AND P.DESPACHO_ID = A.DESPACHO_ID

                LEFT OUTER JOIN TAREAS T
                    ON P.DESPACHO_ID = T.DESPACHO_ID

                LEFT OUTER JOIN DISPOSITIVOS D
                    ON T.DISPOSITIVO_ID = D.DISPOSITIVO_ID

                LEFT OUTER JOIN FUNCIONARIOS F
                    ON D.FUNCIONARIO_ID = F.FUNCIONARIO_ID

                LEFT OUTER JOIN DISPOSITIVOS D2
                    ON T.DISPOSITIVO_ID_NOTIF = D2.DISPOSITIVO_ID

                LEFT OUTER JOIN FUNCIONARIOS F2
                    ON D2.FUNCIONARIO_ID = F2.FUNCIONARIO_ID

                LEFT OUTER JOIN FUNCIONARIOS F1
                    ON C.FUNCIONARIO_ID = F1.FUNCIONARIO_ID

                LEFT OUTER JOIN DATOS_ACTUACION_PROCESAL DAP
                    ON A.ACTUACION_PROCESAL_ID = DAP.ACTUACION_PROCESAL_ID
                AND DAP.DATO_NOMBRE IN (
                    'ARCHIVO_RELACIONADO',
                    'ARCHIVO_RELACIONADO_1',
                    'ARCHIVO_RELACIONADO_2',
                    'PDF_AUTO',
                    'PDF'
                )
                AND DAP.DATO_VALOR IS NOT NULL

                LEFT OUTER JOIN DATOS_ACTUACION_PROCESAL DAP1
                    ON A.ACTUACION_PROCESAL_ID = DAP1.ACTUACION_PROCESAL_ID
                AND DAP1.DATO_NOMBRE = 'RESUELVE'

                LEFT OUTER JOIN DATOS_ACTUACION_PROCESAL DAP2
                    ON A.ACTUACION_PROCESAL_ID = DAP2.ACTUACION_PROCESAL_ID
                AND DAP2.DATO_NOMBRE = 'VALOR'

                LEFT OUTER JOIN DATOS_ACTUACION_PROCESAL DAP3
                    ON A.ACTUACION_PROCESAL_ID = DAP3.ACTUACION_PROCESAL_ID
                AND DAP3.DATO_NOMBRE = 'GESTION_COPIA'

                LEFT OUTER JOIN CUBRIMIENTO_NACIONAL CN
                    ON P.LOCALIDAD_ID = CN.CIUDAD_ID

                LEFT OUTER JOIN CLIENTES_BANCOS CB
                    ON PC.CLIENTE_ID = CB.CLIENTE_ID

                LEFT OUTER JOIN CLIENTES_INFORME_COPIAS CIC
                    ON CIC.CLIENTE_ID = C.CLIENTE_ID

                LEFT OUTER JOIN PROCESOS_MARCADOS PM
                    ON P.PROCESO_ID = PM.PROCESO_ID
                AND P.DESPACHO_ID = PM.DESPACHO_ID
                AND A.PROCESO_ID = PM.PROCESO_ID
                AND PC.PROCESO_ID = PM.PROCESO_ID
                AND PM.FECHA = SYSDATE - 1

                LEFT OUTER JOIN DATOS_PROCESOS DP
                    ON P.PROCESO_ID = DP.PROCESO_ID
                AND PC.PROCESO_ID = DP.PROCESO_ID
                AND DP.DATO_NOMBRE LIKE '%AUTORIZACION%'

                WHERE A.NOTIFICACION_ID NOT IN (29, 30, 27, 31, 35, 34)
                AND A.ACTUACION_FECHA >= TO_DATE(:start_date, 'DD/MM/YYYY')
                AND A.ACTUACION_FECHA <= TO_DATE(:final_date, 'DD/MM/YYYY')
                AND C.CLIENTE_ESTADO_FACTURACION = 'C'
                AND P.COPIAS = 'S'
                AND PC.CLIENTE_ID IN (
                        SELECT CLIENTE_ID
                        FROM CLIENTES
                        START WITH CLIENTE_ID = 0
                        CONNECT BY PRIOR CLIENTE_ID = CLIENTE_PADRE
                    )

                ORDER BY 2
            """

            async with conn.cursor() as cursor:
                await cursor.execute(query, {
                    "start_date": start_date,
                    "final_date":final_date
                })
                rows = await cursor.fetchall() 

            return rows 
        except Exception as error:
            self.logger.error(f"❌ Error al traer el reporte de copias : {error}")
            raise


