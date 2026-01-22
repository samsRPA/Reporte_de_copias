import logging
from app.application.services.scrapper.CrossQueryService import CrossQueryService
from app.domain.interfaces.IGetDataService import IGetDataService
from datetime import datetime



class GetDataService(IGetDataService):
    
    logger= logging.getLogger(__name__)
    
    def __init__(self,cross_query_rep : CrossQueryService):
        self.cross_query_rep=cross_query_rep
        
    
    async def get_cross_data(self,conn):
        try:
            today = datetime.now()

                
            cross_data = await self.cross_query_rep.get_cross_data( conn)
            
            if not    cross_data:
                self.logger.warning("⚠️ No se encontraron informacion del cruce")
                return []
            list_cross_data = []

            for row in cross_data:

                list_cross_data.append(row)
                 
            return list_cross_data

        except Exception as e:
            self.logger.error(f"❌ Error : {e}")
            raise e




    def _upper(self, value):
        if isinstance(value, str):
            return value.strip().upper()
        return value
    

   