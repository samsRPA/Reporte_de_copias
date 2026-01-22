from pydantic import Field
from app.infrastucture.config.EnvConfig import EnvConfig


class ApiwhatsappConfig(EnvConfig):

    NUMBER: str = Field(..., alias="NUMBER")
    URL: str = Field(..., alias="URL")
        

    