from pathlib import Path
import logging
from app.domain.interfaces.IGetDataService import IGetDataService
from datetime import datetime
from app.infrastucture.database.repositories.ConsultEditionRep import ConsultEditionRep



class GetDataService(IGetDataService):
    
    logger= logging.getLogger(__name__)
    
    def __init__(self,consult_edition_rep : ConsultEditionRep):
        self.consult_edition_rep=consult_edition_rep
        
    
    async def get_edition_data(self,conn):
        try:
            today = datetime.now()

          
            edition_data = await self.consult_edition_rep.get_edition_data(conn)
            
            if not    edition_data:
                self.logger.warning("⚠️ No se encontraron informacion de edicion")
                return []
            list_edition_data = []

            for row in edition_data:

                list_edition_data.append(row)
                 
            return list_edition_data

        except Exception as e:
            self.logger.error(f"❌ Error : {e}")
            raise e




    def _upper(self, value):
        if isinstance(value, str):
            return value.strip().upper()
        return value
    

   