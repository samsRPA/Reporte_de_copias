from abc import ABC, abstractmethod
from pathlib import Path

class IProcessDataService(ABC):

    @abstractmethod
    def generate_copy_report_xlsx(self, copy_report: list, output_path: str):
        pass

