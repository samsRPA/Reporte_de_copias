from pydantic_settings import BaseSettings



from app.infrastucture.config.DataBaseSettings import DataBaseSettings

from app.infrastucture.config.MicrosoftAzureConfig import MicrosoftAzureConfig

class Settings(BaseSettings):

    data_base: DataBaseSettings = DataBaseSettings()
    microsoft_azure:MicrosoftAzureConfig = MicrosoftAzureConfig()
   

def load_config() -> Settings:
    return Settings()
