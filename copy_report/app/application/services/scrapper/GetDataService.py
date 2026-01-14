from pathlib import Path

import logging
from app.domain.interfaces.IGetDataService import IGetDataService


from app.infrastucture.database.repositories.CopyReportRep import CopyReportRep
from app.application.dto.ScrapperRequest import ScrapperRequest

from datetime import datetime, timedelta

class GetDataService(IGetDataService):
    
    logger= logging.getLogger(__name__)
    
    def __init__(self,copy_report_rep :CopyReportRep):
        self.copy_report_rep=copy_report_rep
        
    
    async def get_copy_report(self,conn):
        try:
            today = datetime.now()

            # Día de la semana: Monday=0 ... Friday=4
            weekday = today.weekday()

            if weekday == 4:  # Viernes
                delta_days = 14
            else:  # Lunes a Jueves (y fin de semana por seguridad)
                delta_days = 7

            start_date_dt = today - timedelta(days=delta_days)

            # Formato DD/MM/YYYY
            start_date = start_date_dt.strftime("%d/%m/%Y")
            final_date = today.strftime("%d/%m/%Y")

            self.logger.info(
            f"[CopyReport] 📅 Fecha a tomar → "
            f"desde {start_date} hasta {final_date} "
            f"(día actual: {today.strftime('%A')})"
            )
                
            raw_copies = await self.copy_report_rep.get_copy_report( conn, start_date, final_date) 
            if not raw_copies:
                self.logger.warning("⚠️ No se encontraron reporte de copias")
                return []
            copy_report = []

            for row in raw_copies:
                # row = (proceso_id, actuacion_procesal_id, copias, gestion_copia, ...)

                scrapper_request = ScrapperRequest(
                    proceso_id=row[0],
                    actuacion_procesal_id=row[1],
                    copias=self._upper(row[2]),
                    gestion_copia=self._upper(row[3]),
                    fecha_notificacion=row[4],
                    valor_mand=self._upper(row[5]),
                    despacho_nombre=self._upper(row[6]),
                    ciudad=self._upper(row[7]),
                    coordinador=self._upper(row[8]),
                    origen=self._upper(row[9]),
                    regional=self._upper(row[10]),
                    cedula_dependiente=self._upper(row[11]),
                    nombre_dependiente=self._upper(row[12]),
                    nombre_notificador=self._upper(row[13]),
                    tipo_proceso=self._upper(row[14]),
                    radicacion=row[15],
                    annio=row[16],
                    demandante=self._upper(row[17]),
                    demandado=self._upper(row[18]),
                    copias_1=self._upper(row[19]),
                    tp_proceso_id=row[20],
                    localidad_id=row[21],
                    despacho_id=row[22],
                    despacho_direccion=self._upper(row[23]),
                    despacho_telefono=self._upper(row[24]),
                    despacho_contacto=self._upper(row[25]),
                    actuacion_procesal_id_1=row[26],
                    despacho_id_1=row[27],
                    instancia_radicacion=row[28],
                    year=row[29],
                    notificacion_id=row[30],
                    tp_proceso_id_1=row[31],
                    etapa_id=row[32],
                    actuacion_id=row[33],
                    proceso_id_1=row[34],
                    actuacion_fecha=row[35],
                    actuacion_fecha_auto=row[36],
                    actuacion_fecha_carga=row[37],
                    etapa_nombre=self._upper(row[38]),
                    actuacion_nombre=self._upper(row[39]),
                    notifiacion_nombre=self._upper(row[40]),
                    cliente_id=row[41],
                    tipo_cliente=row[42],
                    cliente_nombre=self._upper(row[43]),
                    gestor=self._upper(row[44]),
                    resuelve=self._upper(row[45]),
                    autorizacion=self._upper(row[46]),
                )
                copy_report.append(scrapper_request)

                 
            return copy_report

        except Exception as e:
            self.logger.error(f"❌ Error : {e}")
            raise e



    def _upper(self, value):
        if isinstance(value, str):
            return value.strip().upper()
        return value
    

   