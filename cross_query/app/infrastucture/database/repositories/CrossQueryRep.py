import asyncio
from datetime import datetime
import logging


class  CrossQueryRep:
   
    
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
        
    async def  get_cross_data(self, conn) :
        try:
            query = """
                

            SELECT CRUZAR_CM,
                CRUCE_ACTIVOS,
                COUNT(*) AS TOTAL
            FROM REGISTRO_1
            WHERE TRUNC(FECHA_CREACION) = TRUNC(SYSDATE)
            AND CRUZAR_CM NOT LIKE '%REGISTRO_DUPLICADO%'
            GROUP BY CRUZAR_CM, CRUCE_ACTIVOS

            UNION

            SELECT SUBSTR(CRUZAR_CM, 1, 18) AS CRUZAR_CM,
                CRUCE_ACTIVOS,
                COUNT(*) AS TOTAL
            FROM REGISTRO_1
            WHERE TRUNC(FECHA_CREACION) = TRUNC(SYSDATE)
            AND CRUZAR_CM LIKE '%REGISTRO_DUPLICADO%'
            GROUP BY SUBSTR(CRUZAR_CM, 1, 18), CRUCE_ACTIVOS

            ORDER BY 2 DESC
                 """

            async with conn.cursor() as cursor:
                await cursor.execute(query)
                rows = await cursor.fetchall() 

            return rows 
        except Exception as error:
            self.logger.error(f"❌ Error al traer la informacion del cruce : {error}")
            raise





