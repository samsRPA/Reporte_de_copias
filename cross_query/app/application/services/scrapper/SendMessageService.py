import logging
import requests
from app.domain.interfaces.ISendMessageService import ISendMessageService

class SendMessageService(ISendMessageService):
    
    

    
    def __init__(self, number, url):
        self.number= number
        self.url=url
        self.logger= logging.getLogger(__name__)
 




    def send_message(self, message,image_base64):
        
     

        # Headers (ajusta si tu API requiere Authorization)
        headers = {
            "Content-Type": "application/json"
            # "Authorization": "Bearer TU_TOKEN"  # si aplica
        }

        # Body del POST
        payload = {
            "numbers": [self.number],
            "message": {
                "header": "imagen",
                "informacion": {
                    "texto": message,
                    "imagenes": [
                        f"{image_base64}"  
                    ]
                }
            }
        }



        

        try:
            response = requests.post(
                self.url,
                headers=headers,
                json=payload,   # requests se encarga de convertir a JSON
                timeout=10
            )



            # Respuesta JSON
            data = response.json()
          

            # Ejemplo de validación
            if data.get("success"):
                for result in data.get("results", []):
                    self.logger.info(f"📨 Enviado a {result['recipient']} → OK: {result['ok']}")
                    
                return True

        except requests.exceptions.RequestException as e:
            self.logger.error(f"❌ Error al consumir el endpoint: {e}"  )
            return False



