import pandas as pd

LABELS_ESTRESORES = {
    "ESTRE[ESTRE01]": "Experiencias de discriminación en Duoc UC",
    "ESTRE[ESTRE02]": "Problemas en la relación con profesores",
    "ESTRE[ESTRE03]": "Panorama político internacional o cambios en el mundo",
    "ESTRE[ESTRE04]": "Espacios de clase no adecuados en Duoc UC",
    "ESTRE[ESTRE05]": "Recursos de la universidad poco actualizados",
    "ESTRE[ESTRE06]": "Problemas en la relación con compañeros",
    "ESTRE[ESTRE07]": "Duelos/pérdidas",
    "ESTRE[ESTRE08]": "Problemas de salud de un ser querido",
    "ESTRE[ESTRE09]": "Aislamiento",
    "ESTRE[ESTRE10]": "Crisis climática y desastres naturales",
    "ESTRE[ESTRE11]": "Problemas de inseguridad en tu barrio",
    "ESTRE[ESTRE12]": "Carga académica exigente",
    "ESTRE[ESTRE13]": "Panorama político y social del país",
    "ESTRE[ESTRE14]": "Problemas de inseguridad al entrar y salir de la sede (delincuencia)",
    "ESTRE[ESTRE15]": "Problemas en relación sentimental",
    "ESTRE[ESTRE16]": "Dificultad para compatibilizar trabajo y estudios",
    "ESTRE[ESTRE17]": "Dificultades de transporte y desplazamiento",
    "ESTRE[ESTRE18]": "Problemas de salud personales",
    "ESTRE[ESTRE19]": "Futuro laboral",
    "ESTRE[ESTRE20]": "Problemas en relaciones familiares",
    "ESTRE[ESTRE21]": "Situación económica compleja",
    "ESTRE[ESTRE22]": "Problemas de autoestima"
}

LABELS_EXIGENCIA = {
    "EXIG[1]": "Mi trabajo me quita más tiempo del que desearía",
    "EXIG[2]": "Tengo muchas responsabilidades en el hogar",
    "EXIG[3]": "Tengo dificultades para entender la materia",
    "EXIG[4]": "Tengo dificultades para concentrarme",
    "EXIG[5]": "Me faltan hábitos de estudio",
    "EXIG[6]": "Otro"
}

LABELS_AFRONTAMIENTO = {
        "ESTRA[ESTRA01]": "Busco distraerme haciendo otras cosas agradables para mí.",
        "ESTRA[ESTRA02]": "Pienso detenidamente escenarios de cómo solucionarlo.",
        "ESTRA[ESTRA03]": "Me hago cargo de solucionar el problema tomando acciones concretas.",
        "ESTRA[ESTRA04]": "Me digo a mí mismo 'esto no es real'.",
        "ESTRA[ESTRA05]": "Intento verlo con otros ojos, para hacer que parezca más positivo.",
        "ESTRA[ESTRA06]": "Me rindo a intentar ocuparme del problema.",
        "ESTRA[ESTRA07]": "Aprendo a vivir con ello."
    }

def conteo_simple(df, columna):
    counts = df[columna].value_counts().reset_index()
    counts.columns = [columna, "Valor"]
    return counts

def porcentaje_por_categoria(df, columna):
    porcentajes = df[columna].value_counts(normalize=True).reset_index()
    porcentajes.columns = [columna, "Porcentaje"]
    
    # Redondear a 2 decimales
    porcentajes["Porcentaje"] = porcentajes["Porcentaje"].round(2)
    
    return porcentajes

def conteo_multiple(df, columnas):
    counts = {}
    for col in columnas:
        temp = df[col].value_counts().rename_axis("Categoría").reset_index(name="Valor")
        counts[col] = temp
    return counts

def casos_validos_pss(df):
    return df[df[["PSS4[PSS01]", "PSS4[PSS02]", "PSS4[PSS03]", "PSS4[PSS04]"]].notna().all(axis=1)].copy()

def aplicar_regla_pss(df):
    inversion = {0: 4, 1: 3, 2: 2, 3: 1, 4: 0}
    df["PSS02_inv"] = df["PSS4[PSS02]"].map(inversion)
    df["PSS03_inv"] = df["PSS4[PSS03]"].map(inversion)
    
    df["puntaje_total"] = df["PSS4[PSS01]"] + df["PSS02_inv"] + df["PSS03_inv"] + df["PSS4[PSS04]"]
    df["pct_persona"] = df["puntaje_total"] / 16  # entre 0 y 1
    return df

def promedio_por_categoria(df, columnas, espacio=1):
    resultados = []

    for col in columnas:
        temp = df.groupby(col)["pct_persona"].mean().reset_index()
        temp.columns = [col, "Porcentaje"]
        temp["Variable"] = col
        temp["Categoria_label"] = temp[col].astype(str)  # solo el valor de la categoría

        resultados.append(temp)

    df_resultado = pd.concat(resultados, ignore_index=True)
    df_resultado["Porcentaje"] = df_resultado["Porcentaje"].replace(0, None)
    return df_resultado

def porcentaje_estresores(df, columnas, grupo=None, top=None):
    df_temp = df.copy()
    df_temp["marco_algo"] = df_temp[columnas].notna().any(axis=1)
    df_temp = df_temp[df_temp["marco_algo"]]

    resultados = []

    if grupo:
        grupos = df_temp[grupo].dropna().unique()
        for col in columnas:
            for g in grupos:
                grupo_df = df_temp[df_temp[grupo] == g]
                count = (grupo_df[col] == "Y").sum()
                total = len(grupo_df)
                pct = count / total if total > 0 else 0
                resultados.append({
                    "Categoria_label": LABELS_ESTRESORES.get(col, col),
                    "Porcentaje": pct,
                    "Variable": g
                })
    else:
        for col in columnas:
            count = (df_temp[col] == "Y").sum()
            total = len(df_temp)
            pct = count / total if total > 0 else 0
            resultados.append({
                "Categoria_label": LABELS_ESTRESORES.get(col, col),
                "Porcentaje": pct,
                "Variable": "Total"
            })

    df_resultado = pd.DataFrame(resultados)

    # ✅ Siempre ordenar de mayor a menor
    if grupo:
        df_resultado = df_resultado.sort_values(["Variable", "Porcentaje"], ascending=[True, False])
    else:
        df_resultado = df_resultado.sort_values("Porcentaje", ascending=False)

    # ✅ Si top está definido, limitar
    if top is not None:
        if grupo:
            df_resultado = df_resultado.groupby("Variable", group_keys=False).head(top)
        else:
            df_resultado = df_resultado.head(top)

    return df_resultado

def top_estresores_2022(df_wide, sede="Global", variable=None, top=5):
    if sede not in df_wide.columns:
        raise KeyError(f"No existe la columna '{sede}' en el DataFrame.")

    # Excluir la fila 'Nivel de estrés 2022' si existe
    df_filtered = df_wide.drop(index="Nivel de estrés 2022", errors="ignore")

    # Selecciona la columna de interés y obtiene el top N
    df_top = (
        df_filtered[[sede]]
        .rename(columns={sede: "Porcentaje"})
        .sort_values("Porcentaje", ascending=False)
        .head(top)
        .reset_index()
        .rename(columns={"index": "Categoria_label"})
    )

    # Añade la columna Variable (usada por tu chart_builder)
    df_top["Variable"] = sede

    return df_top


def porcentaje_estresores_exigencia(df, columnas_estres, filtro_columna=None, filtro_valores=None, marcar_col='ESTRE[ESTRE18]'):
    # Filtrar personas que marcaron Y en marcar_col
    df_temp = df[df[marcar_col] == 'Y'].copy()

    # Filtrar subgrupos si se pasa filtro_columna y valores
    if filtro_columna and filtro_valores is not None:
        df_temp = df_temp[df_temp[filtro_columna].isin(filtro_valores)]

    resultados = []

    # Determinar si se agrupa por series
    if filtro_columna:
        grupos = df_temp[filtro_columna].dropna().unique()
        for col in columnas_estres:
            for g in grupos:
                grupo_df = df_temp[df_temp[filtro_columna] == g]
                count = (grupo_df[col] == 'Y').sum()
                total = len(grupo_df)
                pct = count / total if total > 0 else 0
                resultados.append({
                    'Categoria_label': LABELS_EXIGENCIA.get(col, col),
                    'Porcentaje': pct,
                    'Variable': g
                })
    else:
        for col in columnas_estres:
            count = (df_temp[col] == 'Y').sum()
            total = len(df_temp)
            pct = count / total if total > 0 else 0
            resultados.append({
                'Categoria_label': LABELS_EXIGENCIA.get(col, col),
                'Porcentaje': pct,
                'Variable': 'Total'
            })

    df_resultado = pd.DataFrame(resultados)
    return df_resultado

def porcentaje_afrontamiento(df, columnas_items, valor_marcar=4, filtro_columna=None, filtro_valores=None):
    resultados = []

    # --- Filtrar filas que marcaron al menos un ítem en la escala ---
    df_temp = df[df[columnas_items].notna().any(axis=1)].copy()

    # --- Aplicar filtro por subgrupo si se pasa ---
    if filtro_columna and filtro_valores is not None:
        df_temp = df_temp[df_temp[filtro_columna].isin(filtro_valores)]

    # --- Calcular porcentaje por ítem ---
    if filtro_columna:
        grupos = df_temp[filtro_columna].dropna().unique()
        for col in columnas_items:
            for g in grupos:
                grupo_df = df_temp[df_temp[filtro_columna] == g]
                count = (grupo_df[col] == valor_marcar).sum()
                total = len(grupo_df)
                pct = count / total if total > 0 else 0
                resultados.append({
                    'Categoria_label': LABELS_AFRONTAMIENTO.get(col, col),
                    'Porcentaje': pct,
                    'Variable': g
                })
    else:
        for col in columnas_items:
            count = (df_temp[col] == valor_marcar).sum()
            total = len(df_temp)
            pct = count / total if total > 0 else 0
            resultados.append({
                'Categoria_label': LABELS_AFRONTAMIENTO.get(col, col),
                'Porcentaje': pct,
                'Variable': 'Total'
            })

    df_resultado = pd.DataFrame(resultados)
    # Ordenar de mayor a menor
    df_resultado = df_resultado.sort_values('Porcentaje', ascending=False).reset_index(drop=True)
    return df_resultado

def porcentaje_procrastinacion(df, columnas_items):
    # --- Valores que se cuentan como "marcado" ---
    valores_marcar = [4, 5]

    # --- Diccionario de labels internos ---
    LABELS = {
        "PROCAS[PROCA]": "A menudo + Muy a menudo",
        # Agregar más ítems si existieran
    }

    resultados = []

    # --- Filtrar filas que marcaron al menos un ítem ---
    df_temp = df[df[columnas_items].notna().any(axis=1)].copy()

    # --- Calcular porcentaje por ítem ---
    for col in columnas_items:
        count = df_temp[col].isin(valores_marcar).sum()
        total = df_temp[col].notna().sum()
        pct = count / total if total > 0 else 0
        resultados.append({
            'Categoria_label': LABELS.get(col, col),
            'Porcentaje': pct,
            'Variable': 'Total'
        })

    df_resultado = pd.DataFrame(resultados)
    # Ordenar de mayor a menor
    df_resultado = df_resultado.sort_values('Porcentaje', ascending=False).reset_index(drop=True)
    return df_resultado

def porcentaje_salud_cronica(df, columna_item, etiquetas):
    df_temp = df[df[columna_item].notna()]
    
    # Contar frecuencia relativa
    conteo = df_temp[columna_item].value_counts(normalize=True)
    
    # Crear DataFrame con labels y porcentajes
    resultados = [
        {"Categoria_label": etiquetas.get(int(valor), f"Otro ({valor})"),
         "Porcentaje": pct,
         "Variable": columna_item}
        for valor, pct in conteo.items()
    ]
    
    return pd.DataFrame(resultados)

def depresion_manejo_clinico(df, perma23_count, group_cols=None):
    phq_cols = [f"PHQ8[PHQ0{i}]" for i in range(1, 9)]

    # Casos válidos: los que respondieron los 8 ítems
    df_validos = df.dropna(subset=phq_cols).copy()
    if df_validos.empty:
        return pd.DataFrame(columns=["Categoria", "Serie", "Valor"])

    # Puntaje total + flag de malestar clínico
    df_validos["PUNTAJE_PHQ8"] = df_validos[phq_cols].sum(axis=1)
    df_validos["depresion_malestar_clinico"] = df_validos["PUNTAJE_PHQ8"].apply(lambda x: "Sí" if x >= 10 else "No")

    resultados = []

    if not group_cols:
        total_clinico = (df_validos["depresion_malestar_clinico"] == "Sí").sum()
        porcentaje = (total_clinico / perma23_count)
        resultados.append({"Categoria": "Global", "Serie": "Malestar clínico en depresión", "Valor": porcentaje})
    else:
        for col in group_cols:
            # Contar malestar clínico "Sí" por cada valor de la columna
            df_grouped = df_validos[df_validos["depresion_malestar_clinico"]=="Sí"].groupby(col).size().reset_index(name="total_clinico")
            df_grouped["porcentaje"] = (df_grouped["total_clinico"] / perma23_count)
            for _, row in df_grouped.iterrows():
                resultados.append({
                    "Categoria": row[col],  # Cada valor de la columna es la categoría
                    "Serie": "Malestar clínico en depresión",
                    "Valor": row["porcentaje"]
                })
        
    return pd.DataFrame(resultados)

def ansiedad_manejo_clinico(df, perma23_count, group_cols=None):
    gad_cols = [f"GAD7[GAD0{i}]" for i in range(1, 8)]

    # Casos válidos: los que respondieron los 7 ítems
    df_validos = df.dropna(subset=gad_cols).copy()
    if df_validos.empty:
        return pd.DataFrame(columns=["Categoria", "Serie", "Valor"])

    # Puntaje total + flag de malestar clínico
    df_validos["PUNTAJE_GAD7"] = df_validos[gad_cols].sum(axis=1)
    df_validos["ansiedad_malestar_clinico"] = df_validos["PUNTAJE_GAD7"].apply(lambda x: "Sí" if x >= 10 else "No")

    resultados = []

    if not group_cols:
        total_clinico = (df_validos["ansiedad_malestar_clinico"] == "Sí").sum()
        porcentaje = (total_clinico / perma23_count)
        resultados.append({"Categoria": "Global", "Serie": "Malestar clínico en ansiedad", "Valor": porcentaje})
    else:
        for col in group_cols:
            # Contar malestar clínico "Sí" por cada valor de la columna
            df_grouped = df_validos[df_validos["ansiedad_malestar_clinico"]=="Sí"].groupby(col).size().reset_index(name="total_clinico")
            df_grouped["porcentaje"] = (df_grouped["total_clinico"] / perma23_count)
            for _, row in df_grouped.iterrows():
                resultados.append({
                    "Categoria": row[col],  # Cada valor de la columna es la categoría
                    "Serie": "Malestar clínico en ansiedad",
                    "Valor": row["porcentaje"]
                })
        
    return pd.DataFrame(resultados)

def personalidad_manejo_clinico(df, perma23_count, group_cols=None):
    lpf_cols = ["LPFS[LPFS01]", "LPFS[LPFS02]", "LPFS[LPFS03]", "LPFS[LPFS04]", "LPFS[LPFS05]", "LPFS[LPFS06]", "LPFS[LPFS07]", "LPFS[LPFS08]", "LPFS[LPFS09]","LPFS[LPFS10]", "LPFS[LPFS11]", "LPFS[LPFS12]"]
    # Casos válidos: los que respondieron todos los ítems
    df_validos = df.dropna(subset=lpf_cols).copy()
    if df_validos.empty:
        return pd.DataFrame(columns=["Categoria", "Serie", "Valor"])
    # Puntaje total + flag de malestar clínico
    df_validos["PUNTAJE_LPFS"] = df_validos[lpf_cols].sum(axis=1)
    df_validos["personalidad_malestar_clinico"] = df_validos["PUNTAJE_LPFS"].apply(lambda x: "Sí" if x >= 27 else "No")
    resultados = []
    if not group_cols:
        total_clinico = (df_validos["personalidad_malestar_clinico"] == "Sí").sum()
        porcentaje = (total_clinico / perma23_count)
        resultados.append({"Categoria": "Global", "Serie": "Malestar clínico en trastorno de personalidad", "Valor": porcentaje})
    else:
        for col in group_cols:
            # Contar malestar clínico "Sí" por cada valor de la columna
            df_grouped = df_validos[df_validos["personalidad_malestar_clinico"]=="Sí"].groupby(col).size().reset_index(name="total_clinico")
            df_grouped["porcentaje"] = (df_grouped["total_clinico"] / perma23_count)
            for _, row in df_grouped.iterrows():
                resultados.append({
                    "Categoria": row[col],  # Cada valor de la columna es la categoría
                    "Serie": "Malestar clínico en trastorno de personalidad",
                    "Valor": row["porcentaje"]
                })
    return pd.DataFrame(resultados)

def clasificar_marihuana(x):
    if pd.isna(x):
        return pd.NA
    if x >= 4:
        return "Sí"
    if x == 3:
        return "No"
    return pd.NA

def marihuana_manejo_clinico(df, perma23_count, group_cols=None):
    marihuana_cols = [f"CAST[CAST0{i}]" for i in range(1, 7)]
    # Casos válidos: los que respondieron todos los ítems
    df_validos = df.dropna(subset=marihuana_cols).copy()
    if df_validos.empty:
        return pd.DataFrame(columns=["Categoria", "Serie", "Valor"])
    # Puntaje total + flag de malestar clínico
    df_validos["PUNTAJE_MARIHUANA"] = df_validos[marihuana_cols].sum(axis=1)
    df_validos["marihuana_malestar_clinico"] = df_validos["PUNTAJE_MARIHUANA"].apply(clasificar_marihuana)
    resultados = []
    if not group_cols:
        total_clinico = (df_validos["marihuana_malestar_clinico"] == "Sí").sum()
        porcentaje = (total_clinico / perma23_count)
        resultados.append({"Categoria": "Global", "Serie": "Malestar clínico por uso problemático de marihuana", "Valor": porcentaje})
    else:
        for col in group_cols:
            # Contar malestar clínico "Sí" por cada valor de la columna
            df_grouped = df_validos[df_validos["marihuana_malestar_clinico"]=="Sí"].groupby(col).size().reset_index(name="total_clinico")
            df_grouped["porcentaje"] = (df_grouped["total_clinico"] / perma23_count)
            for _, row in df_grouped.iterrows():
                resultados.append({
                    "Categoria": row[col],  # Cada valor de la columna es la categoría
                    "Serie": "Malestar clínico por uso problemático de marihuana",
                    "Valor": row["porcentaje"]
                })
    return pd.DataFrame(resultados)

def alcohol_manejo_clinico(df, perma23_count, group_cols=None):
    audit_cols = ["AUDIT01[AUDIT01]", "AUDIT02[AUDIT02]", "AUDIT38[AUDIT03]", "AUDIT38[AUDIT04]", "AUDIT38[AUDIT05]", "AUDIT38[AUDIT06]", "AUDIT38[AUDIT07]", "AUDIT38[AUDIT08]", "AUDIT910[AUDIT09]", "AUDIT910[AUDIT10]"]

    # Casos válidos: los que respondieron todos los ítems
    df_validos = df.dropna(subset=audit_cols).copy()
    if df_validos.empty:
        return pd.DataFrame(columns=["Categoria", "Serie", "Valor"])
    # Puntaje total + flag de malestar clínico
    df_validos["PUNTAJE_AUDIT"] = df_validos[audit_cols].sum(axis=1)
    df_validos["alcohol_malestar_clinico"] = df_validos["PUNTAJE_AUDIT"].apply(lambda x: "Sí" if x >= 16 else "No")
    resultados = []
    if not group_cols:
        total_clinico = (df_validos["alcohol_malestar_clinico"] == "Sí").sum()
        porcentaje = (total_clinico / perma23_count)
        resultados.append({"Categoria": "Global", "Serie": "Malestar clínico por uso problemático de alcohol", "Valor": porcentaje})
    else:
        for col in group_cols:
            # Contar malestar clínico "Sí" por cada valor de la columna
            df_grouped = df_validos[df_validos["alcohol_malestar_clinico"]=="Sí"].groupby(col).size().reset_index(name="total_clinico")
            df_grouped["porcentaje"] = (df_grouped["total_clinico"] / perma23_count)
            for _, row in df_grouped.iterrows():
                resultados.append({
                    "Categoria": row[col],  # Cada valor de la columna es la categoría
                    "Serie": "Malestar clínico por uso problemático de alcohol",
                    "Valor": row["porcentaje"]
                })
    return pd.DataFrame(resultados)
