from abc import ABC, abstractmethod
from pathlib import Path

class IGetDataService(ABC):
    
    @abstractmethod
    def get_monitoring_report(self,conn):
          pass

    @abstractmethod
    async def get_columns_name(self,conn):
        pass

