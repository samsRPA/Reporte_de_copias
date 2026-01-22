
from abc import ABC, abstractmethod

class ICrossQueryService(ABC):

    @abstractmethod
    async def scrapper(self):
        pass