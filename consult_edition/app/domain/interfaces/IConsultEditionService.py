
from abc import ABC, abstractmethod

class IConsultEditionService(ABC):

    @abstractmethod
    async def scrapper(self):
        pass