from pptx import Presentation
from pptx.shapes.graphfrm import GraphicFrame
from pptx.util import Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE_TYPE # <-- AÑADIR

# --- AÑADIR 'imagenes_config=None' a la firma de la función ---
def actualizar_graficos(pptx_path, output_path, graficos_config, textos_config=None, imagenes_config=None):
    prs = Presentation(pptx_path)
    charts_map = {}
    text_shapes_map = {}
    image_placeholders = {} # <-- AÑADIR este diccionario

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

            # --- AÑADIR: Lógica para indexar placeholders de imagen ---
            # MSO_SHAPE_TYPE.PICTURE es 13
            elif shape.shape_type == MSO_SHAPE_TYPE.PICTURE:
                key = (shape.name or "").strip().lower()
                if key: # Solo guardar si tiene un nombre (ej: "wordcloud_general")
                    image_placeholders[key] = (slide, shape)
            # --- FIN AÑADIR ---

    # --- INICIO DE TU CÓDIGO ORIGINAL (SIN CAMBIOS) ---
    charts_no_porcentaje = [
        "nivel_bienestar",
        "nivel_bienestar_sede",
        "perma_2022_2025_chart",
        "nhl_2022_2025_chart"
    ]

    charts_no_porcentaje_lower = [name.lower() for name in charts_no_porcentaje]
    
    # --- Actualizar gráficos ---
    for chart_name, cfg in graficos_config.items():
        chart_name_lower = chart_name.lower()
        chart = charts_map.get(chart_name_lower)
        if not chart:
            print(f"⚠️ No se encontró gráfico '{chart_name}'")
            continue

        df_preparado = cfg["dataset_fn"](*cfg["dataset_args"])
        chart_data = cfg["chart_builder"](df_preparado, *cfg["chart_builder_args"])
        chart.replace_data(chart_data)

        if chart_name_lower not in charts_no_porcentaje_lower:
            # Formatear Eje de Valores como porcentaje (SOLO para gráficos de porcentaje)
            try:
                if hasattr(chart, "value_axis"):
                    chart.value_axis.tick_labels.number_format = "0%"  # Eje numérico → 25%
                elif hasattr(chart, "category_axis"): # Esto es inusual para un eje de valor
                    chart.category_axis.tick_labels.number_format = "0%"
            except ValueError:
                pass

            # Formatear Etiquetas de Datos como porcentaje (SOLO para gráficos de porcentaje)
            for series in chart.series:
                series.has_data_labels = True
                series.data_labels.number_format = '0%'
        else:
            print("HOLA PROMEDIO")
            # 💡 Lógica opcional para PROMEDIOS: usar un formato decimal (ej: 0.0)
            try:
                if hasattr(chart, "value_axis"):
                    chart.value_axis.tick_labels.number_format = "0.0" 
            except ValueError:
                pass
            
            # Formatear Etiquetas de Datos para PROMEDIOS
            for series in chart.series:
                series.has_data_labels = True
                series.data_labels.number_format = '0.0'

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
    # --- FIN DE TU CÓDIGO ORIGINAL ---


    # --- AÑADIR: Lógica para actualizar imágenes ---
    if imagenes_config:
        print("--- Actualizando imágenes ---")
        for shape_name, cfg_img in imagenes_config.items():
            key = shape_name.lower()
            if key not in image_placeholders:
                print(f"⚠️ No se encontró placeholder de imagen '{shape_name}'")
                continue
            
            buffer = cfg_img.get("buffer")
            if not buffer or buffer.getbuffer().nbytes == 0:
                print(f"⚠️ Buffer vacío para imagen '{shape_name}', omitiendo.")
                continue

            slide, placeholder = image_placeholders[key]
            
            # Guardar posición y tamaño del placeholder
            left, top, width, height = (
                placeholder.left, placeholder.top, 
                placeholder.width, placeholder.height
            )

            # Añadir la nueva imagen desde el buffer
            try:
                slide.shapes.add_picture(buffer, left, top, width, height)

                # Eliminar el placeholder original
                sp = placeholder._element
                sp.getparent().remove(sp)
                
                print(f"🖼️ Imagen '{shape_name}' actualizada")
            
            except Exception as e:
                print(f"❌ Error al actualizar imagen '{shape_name}': {e}")
    # --- FIN AÑADIR ---

    # --- Guardar presentación ---
    prs.save(output_path)
    print(f"💾 Guardado en: {output_path}")