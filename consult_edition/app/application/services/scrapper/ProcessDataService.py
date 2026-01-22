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



    def generate_table_image(self, data):
        try:
            fecha_hoy = datetime.now().strftime("%Y-%m-%d")

            output_dir = Path("/app/output/img/edicion")
            output_dir.mkdir(parents=True, exist_ok=True)

            output_path = output_dir / f"edition_query_{fecha_hoy}.png"

            # 👉 Crear DataFrame SIN índice visible
            df = pd.DataFrame(data, columns=["ESTADO", "TOTAL"])

            fig, ax = plt.subplots(figsize=(5, 2))
            ax.axis("off")

            table = ax.table(
                cellText=df.values,
                colLabels=df.columns,
                cellLoc="center",
                loc="center"
            )

            table.auto_set_font_size(False)
            table.set_fontsize(10)
            table.scale(1.2, 1.6)

            # 🎨 Colores pastel
            header_color = "#cfe2f3"   # Azul pastel
            row_color_1 = "#f7f7f7"    # Gris muy claro
            row_color_2 = "#ffffff"   # Blanco

            # 👉 Estilizar celdas
            for (row, col), cell in table.get_celld().items():
                if row == 0:  # Header
                    cell.set_facecolor(header_color)
                    cell.set_text_props(weight="bold")
                else:
                    cell.set_facecolor(row_color_1 if row % 2 == 0 else row_color_2)

                cell.set_edgecolor("#d9d9d9")

            plt.savefig(output_path, bbox_inches="tight", dpi=200)
            plt.close()

            with open(output_path, "rb") as img_file:
                img_base64 = base64.b64encode(img_file.read()).decode("utf-8")

            return output_path, img_base64

        except Exception as e:
            self.logger.error(f"❌ Error : {e}")
            raise e


        
    



