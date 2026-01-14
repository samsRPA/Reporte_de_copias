
from abc import ABC, abstractmethod

class ICopyReportService(ABC):

    @abstractmethod
    async def scrapper(self):
        pass