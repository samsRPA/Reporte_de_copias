

import logging
import msal
import requests

from app.domain.interfaces.IMicrosoftAzureService import IMicrosoftAzureService



class MicrosoftAzureService(IMicrosoftAzureService):

    
    logger= logging.getLogger(__name__)
    
    def __init__(self, client_id: str, client_secret: str, tenant_id: str, user_principal: str, folder_productividad_id: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.tenant_id = tenant_id
        self.user_principal = user_principal
        self.folder_productividad_id = folder_productividad_id

        

    def authenticate_azure(self):
    
        try:
            self.logger.info("🚀 Conectando con Microsoft Azure...")

            # AUTENTICACIÓN
            # ========================
            AUTHORITY = f"https://login.microsoftonline.com/{self.tenant_id}"
            SCOPES = ["https://graph.microsoft.com/.default"]

            app = msal.ConfidentialClientApplication(
                self.client_id,
                authority=AUTHORITY,
                client_credential=self.client_secret
            )

            result = app.acquire_token_for_client(scopes=SCOPES)
        

            if "access_token" in result:
                token = result["access_token"]
                headers = {"Authorization": f"Bearer {token}"}
                self.logger.info("🌐 Conectado con Microsoft Azure")
                return headers
            else:
                self.logger.error(f"❌ Error al autenticar con Microsoft Azure: {result.get('error_description', 'Error desconocido')}")
                return None
            
        except Exception as e:
            self.logger.error(f"❌ Error : {e}")
            raise e

    def get_driver_id(self, headers):
        try:   
            # ========================
            # OBTENER DRIVE
            # ========================
            self.logger.info("🌐 Extrayendo información del Drive de Microsoft...")
            resp = requests.get(
                f"https://graph.microsoft.com/v1.0/users/{self.user_principal}/drive",
                headers=headers
            )
            resp.raise_for_status()
            drive_id = resp.json()["id"]
            self.logger.info(f"✅ Drive obtenido correctamente: {drive_id}")


            return drive_id

        except Exception as e:
            self.logger.error(f"❌ Error al obtener archivos desde el Drive: {e}")
            raise e


    def upload_excel_to_drive(self, headers, drive_id, local_file_path, remote_file_name):
        try:
            self.logger.info("⬆️ Subiendo archivo Excel a Microsoft Drive...")

            # Leer archivo local
            with open(local_file_path, "rb") as f:
                file_content = f.read()

            # Endpoint para subir archivo
            upload_url = (
                f"https://graph.microsoft.com/v1.0/drives/{drive_id}"
                f"/items/{self.folder_productividad_id}"
                f":/{remote_file_name}:/content"
            )

            resp = requests.put(
                upload_url,
                headers={
                    **headers,
                    "Content-Type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                },
                data=file_content
            )

            resp.raise_for_status()

            file_info = resp.json()
            file_url = file_info["webUrl"]
            self.logger.info(
                f"✅ Archivo subido correctamente: {file_info.get('name')} "
                f"(ID: {file_info.get('id')})"
            )

            self.logger.info(f"🔗 Link del archivo: {file_url}")

            return file_url

        except Exception as e:
            self.logger.error(f"❌ Error al subir el archivo Excel: {e}")
            raise e
        