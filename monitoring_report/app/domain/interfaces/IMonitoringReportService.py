
from abc import ABC, abstractmethod

class IMonitoringReportService(ABC):

    @abstractmethod
    async def scrapper(self):
        pass