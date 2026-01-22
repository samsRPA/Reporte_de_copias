import asyncio
from datetime import datetime
import logging


class  ConsultEditionRep:

    
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
        
    async def  get_edition_data(self, conn) :
        try:
            query = """
            SELECT
                ESTADO,
                TOTAL
            FROM (/* -------- TORRE_ARCHIVOS_AWS -------- */
                SELECT
                    ESTADO,
                    COUNT(*) AS TOTAL
                FROM TORRE_ARCHIVOS_AWS
                WHERE ESTADO IN ('VARIOS', 'PTE', 'MANUAL')
                AND FECHA_CSV IS NULL
                AND FECHA_BUSCA IS NULL
                GROUP BY ESTADO
            UNION ALL/* -------- TEXTRACT -------- */
                SELECT
                    'TEXTRACT' AS ESTADO,
                    COUNT(DISTINCT ORACLE_ID) AS TOTAL
                FROM (
                    SELECT
                        REGEXP_SUBSTR(PDF,'[^_]+',6,6) AS ORACLE_ID
                    FROM TEXTRACT_FILAS
                    WHERE ESTADO NOT IN ('ok', 'ok_revisado')
                    AND AMBIENTE = 'produccion'
                    AND (
                            ESTADO_REVISION IS NULL
                        OR ESTADO_REVISION IN ('en_revision', 'pospuesto')
                    )
                    AND PDF_ID IN (
                            SELECT ID
                            FROM TEXTRACT_PDF
                            WHERE ESTADO = 'GENERADO CSV'
                    )
                    GROUP BY PDF_ID, PDF, ESTADO_REVISION, USUARIO_VERIFICADOR
                    HAVING COUNT(PDF_ID) = 1
                )
            )
            ORDER BY ESTADO
                 """

            async with conn.cursor() as cursor:
                await cursor.execute(query)
                rows = await cursor.fetchall() 

            return rows 
        except Exception as error:
            self.logger.error(f"❌ Error al traer la informacion de edicion : {error}")
            raise




