from abc import ABC, abstractmethod
from pathlib import Path

class IGetDataService(ABC):
    
    @abstractmethod
    async def get_cross_data(self,conn):
          pass

    # @abstractmethod
    # async def get_columns_name(self,conn):
    #     pass

