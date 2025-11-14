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

    mapa_normalizacion = {}
    if df_normalizacion is not None:
        if 'Palabra original' in df_normalizacion.columns and 'Categoría' in df_normalizacion.columns:
            for _, row in df_normalizacion.iterrows():
                palabra = str(row['Palabra original']).strip().lower()
                categoria = str(row['Categoría']).strip().replace(" ", "_")
                
                if palabra:
                    mapa_normalizacion[palabra] = categoria

    df_filtered = df.copy()
    if genero in ["Masculino", "Femenino"]:
        df_filtered = df_filtered[df_filtered["GENERO"] == genero]

    frases = []
    for col in columnas:
        if col in df_filtered.columns:
            serie = df_filtered[col].dropna().astype(str)
            for texto in serie:
                texto_limpio = texto.strip()
                texto_lower = texto_limpio.lower()
                
                palabra_normalizada = mapa_normalizacion.get(texto_lower)
                
                if palabra_normalizada:
                    frases.append(palabra_normalizada)
                else:
                    frases.append(texto_limpio.replace(" ", "_"))

    texto_completo = " ".join(frases)

    if not texto_completo:
        return BytesIO()

    try:
        mask_img = Image.open(mask_path).convert("L")
        mask = np.array(mask_img)
        mask = 255 - mask
    except FileNotFoundError:
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