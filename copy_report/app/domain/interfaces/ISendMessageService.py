
from abc import ABC, abstractmethod


class ISendMessageService(ABC):



    @abstractmethod
    def send_message(self, message):
        pass