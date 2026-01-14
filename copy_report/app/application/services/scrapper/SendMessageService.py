import logging

import requests

from app.domain.interfaces.ISendMessageService import ISendMessageService


class SendMessageService(ISendMessageService):
    
    

    
    def __init__(self, number, url):
        self.number= number
        self.url=url
        self.logger= logging.getLogger(__name__)
 




    def send_message(self, message):
        
        # URL del endpoint
        url = "http://192.168.0.237:3001/send"  # reemplaza por el real

        # Headers (ajusta si tu API requiere Authorization)
        headers = {
            "Content-Type": "application/json"
            # "Authorization": "Bearer TU_TOKEN"  # si aplica
        }

        # Body del POST
        payload = {
            "numbers": [self.number],
            "message": {
                "header": "texto",
                "informacion":  f"{message}"
            }
        }

        try:
            response = requests.post(
                self.url,
                headers=headers,
                json=payload,   # requests se encarga de convertir a JSON
                timeout=10
            )

            # Ver status HTTP
            self.logger.info(f"Status code:  {response.status_code}" )

            # Respuesta JSON
            data = response.json()
          

            # Ejemplo de validación
            if data.get("success"):
                for result in data.get("results", []):
                    self.logger.info(f"📨 Enviado a {result['recipient']} → OK: {result['ok']}")

        except requests.exceptions.RequestException as e:
            self.logger.error(f"❌ Error al consumir el endpoint: {e}"  )



