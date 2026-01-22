import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import logging
import base64
from datetime import datetime
from app.domain.interfaces.IProcessDataService import IProcessDataService


class ProcessDataService(IProcessDataService):

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def normalize_cross_data(self, raw_data):
        counters = {}

        for cruzar_cm, _, total in raw_data:
            key = cruzar_cm.upper().strip()
            counters[key] = counters.get(key, 0) + total

        pendiente = (
            counters.get("CRUCEENPROCESORAMA", 0)
            + counters.get("CRUCEENPROCESODESPACHO", 0)
            + counters.get("PENDIENTEENCOLARCM", 0)
            + counters.get("CRUCEFINALIZADODESPACHO", 0)
        )

        total_general = (
            counters.get("CRUCEENPROCESORAMA", 0)
            + counters.get("CRUCEENPROCESODESPACHO", 0)
            + counters.get("PENDIENTEENCOLARCM", 0)
            + counters.get("CRUCEFINALIZADODESPACHO", 0)
            + counters.get("CRUCEFINALIZADORAMA", 0)
        )

        table_data = [
            ("CRUCEFINALIZADORAMA", counters.get("CRUCEFINALIZADORAMA", 0)),
            ("CRUCEFINALIZADODESPACHO", counters.get("CRUCEFINALIZADODESPACHO", 0)),
            ("CRUCEENPROCESORAMA", counters.get("CRUCEENPROCESORAMA", 0)),
            ("CRUCEENPROCESODESPACHO", counters.get("CRUCEENPROCESODESPACHO", 0)),
            ("CRUCEFINALIZADORAMA", counters.get("CRUCEFINALIZADORAMA", 0)),
            ("PENDIENTEENCOLARCM", counters.get("PENDIENTEENCOLARCM", 0)),
            ("PROCESO_SIN_FACTURACION", counters.get("PROCESO_SIN_FACTURACION", 0)),
            ("PENDIENTE", pendiente),
            ("TOTAL", total_general),
        ]


        table_data = [
            ("CruceFinalizadoRAMA", counters.get("CRUCEFINALIZADORAMA", 0)),
            ("CruceFinalizadoDESPACHO", counters.get("CRUCEFINALIZADODESPACHO", 0)),
            ("CruceEnProcesoRama", counters.get("CRUCEENPROCESORAMA", 0)),
            ("CruceEnProcesoDespacho", counters.get("CRUCEENPROCESODESPACHO", 0)),
            ("CruceFinalizadoRama", counters.get("CRUCEFINALIZADORAMA", 0)),
            ("PendienteEnColarCM", counters.get("PENDIENTEENCOLARCM", 0)),
            ("PROCESO_SIN_FACTURACION", counters.get("PROCESO_SIN_FACTURACION", 0)),
            ("PENDIENTE", pendiente),
            ("TOTAL", total_general),
        ]


        return table_data


    def generate_table_image(self, data):
        try:
            fecha_hoy = datetime.now().strftime("%Y-%m-%d")
            output_dir = Path("/app/output/img/cross_query")
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = output_dir / f"cross_query_{fecha_hoy}.png"

            df = pd.DataFrame(data, columns=["CRUZAR_CM", "COUNT(*)"])

            fig, ax = plt.subplots(figsize=(6, 3))
            ax.axis('off')

            table = ax.table(
                cellText=df.values,
                colLabels=df.columns,
                cellLoc='center',
                loc='center'
            )

            table.auto_set_font_size(False)
            table.set_fontsize(10)
            table.scale(1, 1.6)

            # ====== ESTILOS ======
            header_color = "#E6E6E6"
            pendiente_color = "#FFF2CC"
            total_color = "#FFE699"

            for (row, col), cell in table.get_celld().items():
                if row == 0:
                    cell.set_facecolor(header_color)
                    cell.set_text_props(weight='bold')
                else:
                    label = df.iloc[row - 1, 0]

                    if label == "PENDIENTE":
                        cell.set_facecolor(pendiente_color)
                        cell.set_text_props(weight='bold')

                    elif label == "TOTAL":
                        cell.set_facecolor(total_color)
                        cell.set_text_props(weight='bold')

                    else:
                        cell.set_facecolor("white")

            plt.savefig(output_path, bbox_inches='tight', dpi=200)
            plt.close()

            with open(output_path, "rb") as img_file:
                img_base64 = base64.b64encode(img_file.read()).decode("utf-8")

            return output_path, img_base64

        except Exception as e:
            self.logger.error(f"❌ Error : {e}")
            raise e

        
    



