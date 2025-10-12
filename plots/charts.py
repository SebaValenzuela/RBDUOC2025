from pptx.chart.data import CategoryChartData

def crear_chart_data(df, categoria_col, valor_col, serie_col=None, usar_label=False):

    data = CategoryChartData()

    # --- Columna de categorías ---
    col_categoria = "Categoria_label" if usar_label and "Categoria_label" in df.columns else categoria_col

    # --- Categorías únicas en orden de aparición ---
    categorias = df[col_categoria].drop_duplicates().tolist()

    if serie_col and serie_col in df.columns:
        data.categories = categorias
        for serie, grupo in df.groupby(serie_col):
            valores = [
                grupo.loc[grupo[col_categoria] == cat, valor_col].values[0]
                if cat in grupo[col_categoria].values else 0
                for cat in categorias
            ]
            data.add_series(str(serie), valores)
    else:
        data.categories = categorias
        data.add_series(valor_col, df[valor_col].tolist())

    return data
