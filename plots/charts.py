from pptx.chart.data import CategoryChartData
import pandas as pd
import numpy as np

def crear_chart_data(df, categoria_col, valor_col, serie_col=None, usar_label=False):

    data = CategoryChartData()
    
    # 1. Determinar la columna de categorías
    col_categoria = "Categoria_label" if usar_label and "Categoria_label" in df.columns else categoria_col

    # 2. Definir las categorías del eje (en orden de aparición, CON spacers)
    # Esta lista la usaremos para el molde y para las etiquetas finales
    categorias_con_spacers = df[col_categoria].drop_duplicates().tolist()

    if serie_col and serie_col in df.columns:
        # --- CASO A: Múltiples Series ---
        
        # Crear un "molde" con todas las categorías (incluyendo los spacers únicos)
        df_scaffold = pd.DataFrame(categorias_con_spacers, columns=[col_categoria])

        for serie, grupo in df.groupby(serie_col):
            # Unir el molde con los datos del grupo actual
            df_merged = df_scaffold.merge(
                grupo[[col_categoria, valor_col]], 
                on=col_categoria, 
                how="left"
            )

            # Limpiar valores para PowerPoint (reemplazar "" y NaN por None)
            valores_series = df_merged[valor_col]
            valores_series = valores_series.replace("", np.nan)
            valores_series = valores_series.astype(object)
            valores = valores_series.where(pd.notna(valores_series), None).tolist()
            
            # Agregar la serie de datos al gráfico
            data.add_series(str(serie), valores)
    else:
        # --- CASO B: Serie Única ---
        valores_series = df[valor_col].replace("", np.nan).astype(object)
        valores = valores_series.where(pd.notna(valores_series), None).tolist()
        data.add_series(valor_col, valores)

    # --- INICIO DE LA CORRECCIÓN ---
    # 3. CREAR Y ASIGNAR LOS LABELS LIMPIOS
    # Ahora que los datos (series) están listos, creamos la lista final de 
    # etiquetas para el eje X, reemplazando los spacers por un espacio.
    categorias_limpias = [
        ' ' if str(c).startswith('_spacer_') else c 
        for c in categorias_con_spacers
    ]
    
    # Asignamos la lista limpia al objeto de datos del gráfico.
    data.categories = categorias_limpias 
    # --- FIN DE LA CORRECCIÓN ---

    return data
