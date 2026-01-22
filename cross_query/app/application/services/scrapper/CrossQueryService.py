

import os
from app.domain.interfaces.ICrossQueryService import ICrossQueryService
from app.domain.interfaces.IGetDataService import IGetDataService
import logging
from app.domain.interfaces.IDataBase import IDataBase
from  app.domain.interfaces.IProcessDataService import IProcessDataService
from app.domain.interfaces.ISendMessageService import ISendMessageService

class CrossQueryService(ICrossQueryService):

    def __init__(self,db: IDataBase, getData: IGetDataService,processData:IProcessDataService, send_message_service:ISendMessageService):
        self.db=db
        self.getData = getData
        self.processData=  processData

        self.send_message_service=send_message_service
        self.logger= logging.getLogger(__name__)
  
    async def scrapper(self):
        conn=None
        try:
            conn = await self.db.acquire_connection()

            self.logger.info("📥 [DATA] Iniciando extracción de datos de cruce")
            cross_data=  await self.getData.get_cross_data(conn)
        
           

            # # ========================
            # # GENERAR IMG
            # # ========================
            self.logger.info("🧹 [PROCESS] Normalizando datos del cruce")
            processed_data = self.processData.normalize_cross_data(cross_data)

            self.logger.info("🖼️ [IMAGE] Generando imagen de la tabla")
            self.logger.info("📤 [MESSAGE] Enviando mensaje con imagen adjunta")
            image_path, image_b64 = self.processData.generate_table_image(processed_data)

       
    
            message = (
                "👋 Hola, \n\n"
                "📄 La imagen de la consulta del cruce ha sido generado.\n\n"

                "¡Saludos!"
            )

            
            self.send_message_service.send_message(message,image_b64)


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




