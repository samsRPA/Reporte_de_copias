from pydantic import Field
from app.infrastucture.config.EnvConfig import EnvConfig


class MicrosoftAzureConfig(EnvConfig):
    CLIENT_ID: str = Field(..., alias="CLIENT_ID")
    CLIENT_SECRET: str = Field(..., alias="CLIENT_SECRET")
    TENANT_ID: str = Field(..., alias="TENANT_ID")
    USER_PRINCIPAL: str = Field(..., alias="USER_PRINCIPAL")
    FOLDER_PRODUCTIVIDAD_ID: str = Field(..., alias="FOLDER_PRODUCTIVIDAD_ID")

    NUMBER: str = Field(..., alias="NUMBER")
    URL: str = Field(..., alias="URL")
        

    