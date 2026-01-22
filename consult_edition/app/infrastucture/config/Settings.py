from pydantic_settings import BaseSettings



from app.infrastucture.config.ApiwhatsappConfig import ApiwhatsappConfig
from app.infrastucture.config.DataBaseSettings import DataBaseSettings



class Settings(BaseSettings):

    data_base: DataBaseSettings = DataBaseSettings()
    api_whatsapp_config: ApiwhatsappConfig= ApiwhatsappConfig()
   

def load_config() -> Settings:
    return Settings()
