


from abc import ABC, abstractmethod


class IMicrosoftAzureService(ABC):

    @abstractmethod
    def authenticate_azure(self):
        pass
    
    @abstractmethod
    def get_driver_id(self, headers):
        pass

    @abstractmethod
    def upload_excel_to_drive(self, headers, drive_id, local_file_path, remote_file_name):
        pass