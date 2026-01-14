
from app.domain.interfaces.IGetDataService import IGetDataService
import logging
from app.application.dto.HoyPathsDto import HoyPathsDto
from app.domain.interfaces.IDataBase import IDataBase

from datetime import datetime

from app.domain.interfaces.ICopyReportService import ICopyReportService
from  app.domain.interfaces.IProcessDataService import IProcessDataService
from  app.domain.interfaces.IMicrosoftAzureService import IMicrosoftAzureService
import requests
import json

from app.domain.interfaces.ISendMessageService import ISendMessageService

class CopyReportService(ICopyReportService):

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
            copy_report =  await self.getData.get_copy_report(conn)
         
            if copy_report:
                self.logger.info(f"✅ Se extrayeron {len(copy_report)} informes de copias")

            fecha_actual = datetime.now()
            fecha = fecha_actual.strftime("%d-%m-%Y")
            hora = fecha_actual.hour
            # Si se ejecuta entre 4 y 7 (inclusive)
            if 4 <= hora <= 7:
                file_name = f"informe_copias_{fecha}_MAÑANA.xlsx"
            else:
                file_name = f"informe_copias_{fecha}_prueba.xlsx"

            output_path = f"/app/output/reports/{file_name}"

            # ========================
            # GENERAR EXCEL
            # ========================
            self.processData.generate_copy_report_xlsx(
                copy_report,
               output_path
            )


            
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
            file_url= self.microsfotAzureService.upload_excel_to_drive(
                headers=headers,
                drive_id=drive_id,
                local_file_path=output_path,
                remote_file_name=file_name
                )

            message = (
                "👋 Hola, \n\n"
                "📄 El *informe de copias* ha sido generado y cargado correctamente.\n\n"
                "🔗 Puedes consultarlo en el siguiente enlace:\n"
                f"{file_url}\n\n"
                "¡Saludos!"
            )
            
            self.send_message_service.send_message(message)
          

        except Exception as e:
            self.logger.error(f"❌ Error : {e}")
            raise e
        finally:
            if conn:
                try:
                    await self.db.release_connection(conn)
                except Exception as e:
                    self.logger.warning(f"Error liberando conexión DB: {e}")




