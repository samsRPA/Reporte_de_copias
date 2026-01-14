from dependency_injector import containers, providers
from app.infrastucture.config.Settings import Settings
from app.domain.interfaces.IProcessDataService import IProcessDataService
from app.application.services.scrapper.ProcessDataService import ProcessDataService
from app.application.services.scrapper.GetDataService import GetDataService
from app.domain.interfaces.IGetDataService import IGetDataService
from app.domain.interfaces.IDataBase import IDataBase
from app.infrastucture.database.OracleDB import OracleDB
from app.infrastucture.database.repositories.CopyReportRep import CopyReportRep
from app.domain.interfaces.ICopyReportService import ICopyReportService
from app.application.services.scrapper.CopyReportService import CopyReportService
from app.application.services.scrapper.MicrosoftAzureService import MicrosoftAzureService
from app.domain.interfaces.IMicrosoftAzureService import IMicrosoftAzureService
from app.application.services.scrapper.SendMessageService import SendMessageService
from app.domain.interfaces.ISendMessageService import ISendMessageService


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
    
    copy_report_rep = providers.Factory(
        CopyReportRep,

    )

    get_data_service: providers.Factory[IGetDataService] = providers.Factory(
        GetDataService,
        copy_report_rep 
        
    )
    
    process_data_service: providers.Factory[IProcessDataService] = providers.Factory(
        ProcessDataService,
       
    )


    microsoft_azure_service: providers.Factory[IMicrosoftAzureService] = providers.Factory(
      MicrosoftAzureService,
      client_id=settings.provided.microsoft_azure.CLIENT_ID,
      client_secret=settings.provided.microsoft_azure.CLIENT_SECRET,
      tenant_id=settings.provided.microsoft_azure.TENANT_ID,
      user_principal=settings.provided.microsoft_azure.USER_PRINCIPAL,
      folder_productividad_id=settings.provided.microsoft_azure.FOLDER_PRODUCTIVIDAD_ID,
    )





    send_message_service: providers.Factory[ISendMessageService] = providers.Factory(
        SendMessageService,
        number=settings.provided.microsoft_azure.NUMBER,
        url= settings.provided.microsoft_azure.URL,
       
    )


    copy_report_service: providers.Factory[ICopyReportService] = providers.Factory(
        CopyReportService,
        data_base,
        get_data_service,
        process_data_service,
        microsoft_azure_service,
        send_message_service
   
    )

  



   
