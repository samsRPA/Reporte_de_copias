
import os
from app.domain.interfaces.IGetDataService import IGetDataService
import logging
from app.application.dto.HoyPathsDto import HoyPathsDto
from app.domain.interfaces.IDataBase import IDataBase

from datetime import datetime


from  app.domain.interfaces.IProcessDataService import IProcessDataService
from  app.domain.interfaces.IMicrosoftAzureService import IMicrosoftAzureService
import requests
import json

from app.domain.interfaces.ISendMessageService import ISendMessageService
from app.domain.interfaces.IMonitoringReportService import IMonitoringReportService

class MonitoringReportService(IMonitoringReportService):

    def __init__(self,db: IDataBase, getData: IGetDataService,processData:IProcessDataService, microsoftAzureService:IMicrosoftAzureService, send_message_service:ISendMessageService):
        self.db=db
        self.getData = getData
        self.processData=  processData
        self.microsfotAzureService= microsoftAzureService
        self.send_message_service=send_message_service
        self.logger= logging.getLogger(__name__)
  
    async def scrapper(self):
        conn=None
        try:
            conn = await self.db.acquire_connection()
            monitoring_report =  await self.getData.get_monitoring_report(conn)
         
            if monitoring_report:
                self.logger.info(f"✅ Se extrayeron {len(monitoring_report)} filas ")

            column_names = await self.getData.get_columns_name(conn)

            # ========================
            # GENERAR EXCEL 
            # ========================
            excel_path= self.processData.generate_monitoring_report_xlsx(
                monitoring_report,column_names
            )

            # ========================
            # GENERAR IMG
            # ========================

            image_path,image_base64= self.processData.capture_img(excel_path)


            
            # ========================
            # AUTENTICAR EN AZURE
            # ========================

            headers = self.microsfotAzureService.authenticate_azure()

            # ========================
            # OBTENER DRIVE
            # ========================
            drive_id = self.microsfotAzureService.get_driver_id( headers)

            # ========================
            # SUBIR EXCEL
            # ========================
            excel_file_name = excel_path.name
            image_file_name = image_path.name
        
            
            excel_url_drive= self.microsfotAzureService.upload_archive_to_drive(headers=headers,drive_id=drive_id,  local_file_path=excel_path, remote_file_name=excel_file_name,file_type="Excel")
            img_url_drive= self.microsfotAzureService.upload_archive_to_drive(headers=headers,drive_id=drive_id,  local_file_path=image_path, remote_file_name=image_file_name,file_type="png")

            message = (
                "👋 Hola, \n\n"
                "📄 El informe de seguimiento notificaciones diarias ha sido generado y cargado correctamente.\n\n"
                "🔗 Puedes consultarlo en el siguiente enlace:\n"
                f"Excel 📊: {excel_url_drive}\n\n"
                f"Captura 🖼️ : {img_url_drive}\n\n"
                "¡Saludos!"
            )

            
            self.send_message_service.send_message(message,image_base64)

            try:
                for path in (excel_path, image_path):
                    if path and os.path.exists(path):
                        os.remove(path)
                        self.logger.info(f"🗑️ Archivo local eliminado: {path}")
            except Exception as e:
                self.logger.error(f"❌ Error eliminando archivos locales: {e}")
                    
            
        except Exception as e:
            self.logger.error(f"❌ Error : {e}")
            raise e
        finally:
            if conn:
                try:
                    await self.db.release_connection(conn)
                except Exception as e:
                    self.logger.warning(f"Error liberando conexión DB: {e}")




