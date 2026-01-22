
from abc import ABC, abstractmethod


class ISendMessageService(ABC):



    @abstractmethod
    def send_message(self, message,image_base64):
        pass