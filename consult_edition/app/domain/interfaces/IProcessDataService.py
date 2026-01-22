from abc import ABC, abstractmethod
from pathlib import Path

class IProcessDataService(ABC):

    @abstractmethod
    def generate_table_image(self,data, output_path):
        pass

