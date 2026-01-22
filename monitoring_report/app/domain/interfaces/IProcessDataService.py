from abc import ABC, abstractmethod
from pathlib import Path

class IProcessDataService(ABC):

    @abstractmethod
    def generate_monitoring_report_xlsx(self, monitoring_report: list, column_names):
        pass

    @abstractmethod
    def capture_img(self, excel_path: Path):
        pass


