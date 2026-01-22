from pathlib import Path

import logging
from app.domain.interfaces.IGetDataService import IGetDataService



from app.application.dto.ScrapperRequest import ScrapperRequest

from datetime import datetime, timedelta

from app.infrastucture.database.repositories.MonitoringReportRep import MonitoringReportRep

class GetDataService(IGetDataService):
    
    logger= logging.getLogger(__name__)
    
    def __init__(self,monitoring_report_rep :MonitoringReportRep):
        self.monitoring_report_rep=monitoring_report_rep
        
    
    async def get_monitoring_report(self,conn):
        try:
            today = datetime.now()

            self.logger.info(
            f"[CopyReport] 📅 Fecha a tomar → "
            f"(día actual: {today.strftime('%A')})"
            )
                
            column_names = await self.monitoring_report_rep.get_monitoring_report(conn)
            if not    column_names:
                self.logger.warning("⚠️ No se encontraron informes de seguimiento")
                return []
            monitoring_report = []

            for row in    column_names:
   
            

                monitoring_report.append(row)
                 
            return monitoring_report

        except Exception as e:
            self.logger.error(f"❌ Error : {e}")
            raise e

    async def get_columns_name(self,conn):
        try:
        
            column_names = await self.monitoring_report_rep.get_column_names(conn)
            if not column_names:
                self.logger.warning("⚠️ No se encontraron el nombres de las columnas ")
                return []
            
            return column_names

        except Exception as e:
            self.logger.error(f"❌ Error : {e}")
            return []
            



    def _upper(self, value):
        if isinstance(value, str):
            return value.strip().upper()
        return value
    

   