from abc import ABC, abstractmethod
from pathlib import Path

class IProcessDataService(ABC):

    @abstractmethod
    def generate_table_image(self,data, output_path):
        pass

    @abstractmethod
    def normalize_cross_data(self, raw_data):
        pass

