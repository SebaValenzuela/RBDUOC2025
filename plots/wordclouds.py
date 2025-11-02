from wordcloud import WordCloud, ImageColorGenerator
from io import BytesIO
import pandas as pd
from PIL import Image
import numpy as np

def crear_wordcloud(df: pd.DataFrame, columnas: list, 
                    df_normalizacion: pd.DataFrame = None, # <-- 1. AÑADIDO
                    genero: str = None,
                    ancho=800, alto=400, max_words=200, 
                    mask_path="plots/images/cloud_mask.png") -> BytesIO:

    # --- 2. AÑADIDO: Crear el mapa de normalización ---
    mapa_normalizacion = {}
    if df_normalizacion is not None:
        # Asegurarse de que las columnas existan
        if 'Palabra original' in df_normalizacion.columns and 'Categoría' in df_normalizacion.columns:
            print("Creando mapa de normalización para WordCloud...")
            for _, row in df_normalizacion.iterrows():
                # La clave es la palabra original (limpia, en minúsculas)
                palabra = str(row['Palabra original']).strip().lower()
                # El valor es la categoría (con guion bajo, como tu lógica original)
                categoria = str(row['Categoría']).strip().replace(" ", "_")
                
                if palabra: # No añadir claves vacías
                    mapa_normalizacion[palabra] = categoria
        else:
            print("Warning: df_normalizacion no tiene 'Palabra original' o 'Categoría'. No se normalizará.")
    # --- FIN AÑADIDO ---

    # --- Lógica existente: Filtrar por género ---
    df_filtered = df.copy()
    if genero in ["Masculino", "Femenino"]:
        df_filtered = df_filtered[df_filtered["GENERO"] == genero]

    # --- 3. MODIFICADO: Lógica de recolección de frases ---
    frases = []
    for col in columnas:
        if col in df_filtered.columns:
            serie = df_filtered[col].dropna().astype(str)
            for texto in serie:
                texto_limpio = texto.strip()
                texto_lower = texto_limpio.lower()
                
                # Buscar la palabra en el mapa de normalización
                palabra_normalizada = mapa_normalizacion.get(texto_lower)
                
                if palabra_normalizada:
                    # Si se encuentra, usa la categoría (ej: "Abandono")
                    frases.append(palabra_normalizada)
                else:
                    # Si no, usa la lógica original (ej: "Palabra_Rara_No_Mapeada")
                    frases.append(texto_limpio.replace(" ", "_"))
    # --- FIN MODIFICADO ---

    texto_completo = " ".join(frases)

    # --- Lógica existente: Generación de WordCloud (sin cambios) ---
    if not texto_completo:
        print(f"Warning: No hay texto para generar wordcloud (Género: {genero})")
        return BytesIO()

    try:
        mask_img = Image.open(mask_path).convert("L")
        mask = np.array(mask_img)
        mask = 255 - mask
    except FileNotFoundError:
        print(f"Warning: No se encontró la máscara en {mask_path}. Se usará un rectángulo.")
        mask = None

    wc = WordCloud(
        width=ancho, height=alto, max_words=max_words,
        background_color="white",
        mask=mask,
        contour_color='black'
    ).generate(texto_completo)

    buf = BytesIO()
    wc.to_image().save(buf, format="PNG")
    buf.seek(0)
    return buf