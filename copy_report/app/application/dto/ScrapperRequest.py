from pydantic import BaseModel
from typing import Optional
from datetime import date,datetime

class ScrapperRequest(BaseModel):
    proceso_id: Optional[int] = None
    actuacion_procesal_id: Optional[int] = None
    copias: Optional[str] = None
    gestion_copia: Optional[str] = None
    fecha_notificacion: Optional[str] = None
    valor_mand: Optional[float] = None
    despacho_nombre: Optional[str] = None
    ciudad: Optional[str] = None
    coordinador: Optional[str] = None
    origen: Optional[str] = None
    regional: Optional[str] = None
    cedula_dependiente: Optional[str] = None
    nombre_dependiente: Optional[str] = None
    nombre_notificador: Optional[str] = None
    tipo_proceso: Optional[str] = None
    radicacion : Optional[str] = None
    annio: Optional[int] = None
    demandante: Optional[str] = None
    demandado: Optional[str] = None
    copias_1: Optional[str] = None
    tp_proceso_id: Optional[int] = None
    localidad_id: Optional[int] = None
    despacho_id: Optional[int] = None
    despacho_direccion: Optional[str] = None
    despacho_telefono: Optional[str] = None
    despacho_contacto: Optional[str] = None
    actuacion_procesal_id_1: Optional[int] = None
    despacho_id_1: Optional[int] = None
    instancia_radicacion: Optional[str] = None
    year: Optional[int] = None
    notificacion_id: Optional[int] = None
    tp_proceso_id_1: Optional[int] = None
    etapa_id: Optional[int] = None
    actuacion_id: Optional[int] = None
    proceso_id_1: Optional[int] = None
    actuacion_fecha: Optional[datetime] = None
    actuacion_fecha_auto: Optional[datetime] = None
    actuacion_fecha_carga: Optional[datetime] = None
    etapa_nombre: Optional[str] = None
    actuacion_nombre: Optional[str] = None
    notifiacion_nombre: Optional[str] = None
    cliente_id: Optional[int] = None
    tipo_cliente: Optional[str] = None
    cliente_nombre: Optional[str] = None
    gestor: Optional[str] = None
    resuelve: Optional[str] = None
    autorizacion: Optional[str] = None
    
    
    
    
    
    
    
    


   
         


    @classmethod
    def fromRaw(cls, rawBody: str):
        try:
            data = json.loads(rawBody)
            return cls(**data)
        except (json.JSONDecodeError, ValidationError) as e:
            raise ValueError(f"Invalid scrapper request data: {e}")

