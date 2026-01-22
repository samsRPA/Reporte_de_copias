
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ScrapperRequest(BaseModel):
    oracle_id: Optional[int] = None
    archivo_foto: Optional[str] = None
    fecha_creacion: Optional[datetime] = None
    despacho_id: Optional[int] = None
    localidad_id: Optional[int] = None
    notificacion_id: Optional[int] = None
    fecha_documento: Optional[datetime] = None
    correo: Optional[str] = None
    origen:Optional[str] = None
    fecha_modulo: Optional[datetime] = None
    error_modulo:Optional[str] = None
    fecha_torre: Optional[datetime] = None
    estado_torre:Optional[str] = None
    fecha_busca: Optional[datetime] = None
    
    # postgres_id: Optional[int] = None
    # ruta_aws: Optional[str] = None
    # archivo_aws_original: Optional[str] = None
    # archivo_aws: Optional[str] = None
    # archivo_abby: Optional[str] = None
    # archivo_csv: Optional[str] = None
    
    
    # fecha_descarga: Optional[datetime] = None
    # fecha_abby: Optional[datetime] = None
    # fecha_csv: Optional[datetime] = None
    # fecha_foto: Optional[datetime] = None
    # error_descarga: Optional[str] = None
    # error_abby: Optional[str] = None
    # error_csv: Optional[str] = None
    # error_foto: Optional[str] = None
    # observaciones: Optional[str] = None
    # hojas: Optional[int] = None
    # consecutivo: Optional[int] = None
    # registros: Optional[int] = None
    # comunicacion_id: Optional[int] = None
    # despacho_id: Optional[int] = None
    # localidad_id: Optional[int] = None
    # notificacion_id: Optional[int] = None
    # md5: Optional[str] = None
    # fecha_captura: Optional[datetime] = None
    # fecha_registro: Optional[datetime] = None
   
    # perfil_id: Optional[int] = None
    # correo: Optional[str] = None
    # error_pdf_s_bkp: Optional[str] = None
    # archivo_pdf_s_bkp: Optional[str] = None
    # fecha_pdf_s_bkp: Optional[str] = None
    # error_borra_pdf_aws: Optional[str] = None
    # archivo_borra_pdf_aws: Optional[str] = None
    # fecha_borra_pdf_aws: Optional[str] = None
    # error_csv_s4n: Optional[str] = None
    # archivo_csv_s4n: Optional[str] = None




    
    
    
    
    


   
         


