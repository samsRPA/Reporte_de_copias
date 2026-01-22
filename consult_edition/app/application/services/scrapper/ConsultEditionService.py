


import os
from app.domain.interfaces.IGetDataService import IGetDataService
import logging
from app.domain.interfaces.IDataBase import IDataBase
from  app.domain.interfaces.IProcessDataService import IProcessDataService
from app.domain.interfaces.ISendMessageService import ISendMessageService
from app.domain.interfaces.IConsultEditionService import IConsultEditionService


class ConsultEditionService(IConsultEditionService):

    def __init__(self,db: IDataBase, getData: IGetDataService,processData:IProcessDataService, send_message_service:ISendMessageService):
        self.db=db
        self.getData = getData
        self.processData=  processData

        self.send_message_service=send_message_service
        self.logger= logging.getLogger(__name__)
  
    async def scrapper(self):
        conn=None
        try:
            self.logger.info("🔍 Iniciando proceso de extracción de edición")
            conn = await self.db.acquire_connection()
            edition_data=  await self.getData.get_edition_data(conn)
        
            self.logger.info("🖼️ Generando imagen de la tabla de edición")

            # # ========================
            # # GENERAR IMG
            # # ========================

            image_path,image_base64= self.processData.generate_table_image(edition_data )
    
            message = (
                "👋 Hola, \n\n"
                "🖼️ La imagen de la consulta de edicion ha sido generada.\n\n"
                "¡Saludos!"
            )

            self.logger.info("📤 Enviando mensaje con imagen adjunta")
            self.send_message_service.send_message(message,image_base64)
            self.logger.info("✅ Mensaje enviado correctamente")


            try:
                if os.path.exists(image_path):
                    os.remove(image_path)
                    self.logger.info(f"🗑️ Archivo local eliminado: {image_path}")
            except Exception as e:
                self.logger.error(f"❌ Error eliminando el archivo local: {e}")
          
            
        except Exception as e:
            self.logger.error(f"❌ Error : {e}")
            raise e
        finally:
            if conn:
                try:
                    await self.db.release_connection(conn)
                except Exception as e:
                    self.logger.warning(f"Error liberando conexión DB: {e}")




