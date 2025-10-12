from pptx import Presentation
from pptx.shapes.graphfrm import GraphicFrame
from pptx.util import Pt
from pptx.dml.color import RGBColor

def actualizar_graficos(pptx_path, output_path, graficos_config, textos_config=None):
    prs = Presentation(pptx_path)
    charts_map = {}
    text_shapes_map = {}

    # --- Indexar shapes de tipo gráfico y texto ---
    for slide in prs.slides:
        for shape in slide.shapes:
            # Guardar gráficos
            if isinstance(shape, GraphicFrame) and shape.has_chart:
                key = (shape.name or "").strip().lower()
                charts_map[key] = shape.chart
            
            # Guardar shapes de texto con nombre asignado
            elif shape.has_text_frame:
                key = (shape.name or "").strip().lower()
                text_shapes_map[key] = shape

    # --- Actualizar gráficos ---
    for chart_name, cfg in graficos_config.items():
        chart = charts_map.get(chart_name.lower())
        if not chart:
            print(f"⚠️ No se encontró gráfico '{chart_name}'")
            continue

        df_preparado = cfg["dataset_fn"](*cfg["dataset_args"])
        chart_data = cfg["chart_builder"](df_preparado, *cfg["chart_builder_args"])
        chart.replace_data(chart_data)

        # Etiquetas de porcentaje
        for series in chart.series:
            series.has_data_labels = True
            series.data_labels.number_format = '0%'  # convierte decimales (0.25 → 25%)

        print(f"✅ {chart_name} actualizado correctamente")

    # --- Actualizar textos dinámicos ---
    if textos_config:
      for shape_name, cfg_texto in textos_config.items():
          shape = text_shapes_map.get(shape_name.lower())
          if not shape:
              print(f"⚠️ No se encontró shape de texto '{shape_name}'")
              continue

          # Soporta tanto texto plano como configuración extendida
          if isinstance(cfg_texto, str):
              nuevo_texto = cfg_texto
              estilo = {}
          else:
              nuevo_texto = cfg_texto.get("texto", "")
              estilo = cfg_texto.get("estilo", {})

          # Reemplazar texto completo
          shape.text_frame.clear()
          p = shape.text_frame.paragraphs[0]
          run = p.add_run()
          run.text = str(nuevo_texto)

          # Aplicar estilo
          font = run.font
          if "fuente" in estilo:
              font.name = estilo["fuente"]
          if "tamano" in estilo:
              font.size = Pt(estilo["tamano"])
          if "bold" in estilo:
              font.bold = estilo["bold"]
          if "italic" in estilo:
              font.italic = estilo["italic"]
          if "color" in estilo:
              r, g, b = estilo["color"]
              font.color.rgb = RGBColor(r, g, b)

          print(f"📝 Texto '{shape_name}' actualizado → {nuevo_texto}")

    # --- Guardar presentación ---
    prs.save(output_path)
    print(f"💾 Guardado en: {output_path}")
