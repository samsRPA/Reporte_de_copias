from dependency_injector import containers, providers
from app.application.services.scrapper.CrossQueryService import CrossQueryService
from app.domain.interfaces.ICrossQueryService import ICrossQueryService
from app.infrastucture.config.Settings import Settings
from app.domain.interfaces.IProcessDataService import IProcessDataService
from app.application.services.scrapper.ProcessDataService import ProcessDataService
from app.application.services.scrapper.GetDataService import GetDataService
from app.domain.interfaces.IGetDataService import IGetDataService
from app.domain.interfaces.IDataBase import IDataBase
from app.infrastucture.database.OracleDB import OracleDB
from app.application.services.scrapper.SendMessageService import SendMessageService
from app.domain.interfaces.ISendMessageService import ISendMessageService
from app.infrastucture.database.repositories.CrossQueryRep import CrossQueryRep



class Dependencies(containers.DeclarativeContainer):
    config = providers.Configuration()
    settings: providers.Singleton[Settings] = providers.Singleton(Settings)

    data_base: providers.Singleton[IDataBase] = providers.Singleton(
        OracleDB,
        db_user=settings.provided.data_base.DB_USER,
        db_password=settings.provided.data_base.DB_PASSWORD,
        db_host=settings.provided.data_base.DB_HOST,
        db_port=settings.provided.data_base.DB_PORT,
        db_service_name=settings.provided.data_base.DB_SERVICE_NAME,
    )
    
    cross_query_rep = providers.Factory(
        CrossQueryRep,

    )

    get_data_service: providers.Factory[IGetDataService] = providers.Factory(
        GetDataService,
        cross_query_rep  
        
    )
    
    process_data_service: providers.Factory[IProcessDataService] = providers.Factory(
        ProcessDataService,
       
    )

    send_message_service: providers.Factory[ISendMessageService] = providers.Factory(
        SendMessageService,
        number=settings.provided.api_whatsapp_config.NUMBER,
        url= settings.provided.api_whatsapp_config.URL,
       
    )

    cross_query_service: providers.Factory[ICrossQueryService] = providers.Factory(
        CrossQueryService,
        data_base,
        get_data_service,
        process_data_service,
        send_message_service
   
    )

  



   
