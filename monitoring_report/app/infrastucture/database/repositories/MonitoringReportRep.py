import asyncio
from datetime import datetime
import logging


class  MonitoringReportRep:
   
    
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
        
    async def  get_monitoring_report(self, conn) :
        try:
            query = """
                   SELECT DISTINCT *
                    FROM TORRE_ARCHIVOS_AWS TA
                    WHERE TRUNC(TA.FECHA_CREACION) = TRUNC(SYSDATE)
                 """

            async with conn.cursor() as cursor:
                await cursor.execute(query)
                rows = await cursor.fetchall() 

            return rows 
        except Exception as error:
            self.logger.error(f"❌ Error al traer los informes de seguimientos : {error}")
            raise

    async def  get_column_names(self, conn) :
        try:
            query = """
                SELECT  column_name
                FROM all_tab_columns
                WHERE table_name = 'TORRE_ARCHIVOS_AWS'
                ORDER BY column_id
                 """

            async with conn.cursor() as cursor:
                await cursor.execute(query)
                rows = await cursor.fetchall() 

            return rows 
        except Exception as error:
            self.logger.error(f"❌ Error al traer el nombre de las columnas : {error}")
            raise




