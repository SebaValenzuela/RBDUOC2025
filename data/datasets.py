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

def porcentaje_por_categoria(df, columna, etiquetas=None):
    porcentajes = df[columna].value_counts(normalize=True).reset_index()
    porcentajes.columns = [columna, "Porcentaje"]
    
    porcentajes["Porcentaje"] = porcentajes["Porcentaje"].round(2)
    
    if etiquetas:
        porcentajes["Etiqueta"] = porcentajes[columna].map(etiquetas)
        
        porcentajes = porcentajes.groupby("Etiqueta", as_index=False)["Porcentaje"].sum()
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
    df["pct_persona"] = df["puntaje_total"] / 16
    return df

def promedio_por_categoria(df, columnas, espacio=1):
    resultados = []

    for col in columnas:
        temp = df.groupby(col)["pct_persona"].mean().reset_index()
        temp.columns = [col, "Porcentaje"]
        temp["Variable"] = col
        temp["Categoria_label"] = temp[col].astype(str)

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

    if grupo:
        df_resultado = df_resultado.sort_values(["Variable", "Porcentaje"], ascending=[True, True])
    else:
        df_resultado = df_resultado.sort_values("Porcentaje", ascending=True)

    if top is not None:
        if grupo:
            df_resultado = df_resultado.groupby("Variable", group_keys=False).tail(top)
        else:
            df_resultado = df_resultado.tail(top)

    return df_resultado

def top_estresores_2022(df_wide, sede="Global", variable=None, top=5):
    if sede not in df_wide.columns:
        raise KeyError(f"No existe la columna '{sede}' en el DataFrame.")

    df_filtered = df_wide.drop(index="Nivel de estrés 2022", errors="ignore")

    df_top = (
        df_filtered[[sede]]
        .rename(columns={sede: "Porcentaje"})
        .sort_values("Porcentaje", ascending=True)
        .tail(top)
        .reset_index()
        .rename(columns={"index": "Categoria_label"})
    )

    df_top["Variable"] = sede

    return df_top


def porcentaje_estresores_exigencia(df, columnas_estres, filtro_columna=None, filtro_valores=None, marcar_col='ESTRE[ESTRE18]'):
    df_temp = df[df[marcar_col] == 'Y'].copy()

    if filtro_columna and filtro_valores is not None:
        df_temp = df_temp[df_temp[filtro_columna].isin(filtro_valores)]

    resultados = []

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

    df_temp = df[df[columnas_items].notna().any(axis=1)].copy()

    if filtro_columna and filtro_valores is not None:
        df_temp = df_temp[df_temp[filtro_columna].isin(filtro_valores)]

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
    df_resultado = df_resultado.sort_values('Porcentaje', ascending=True).reset_index(drop=True)
    return df_resultado

def porcentaje_procrastinacion(df, columnas_items):
    valores_marcar = [4, 5]

    LABELS = {
        "PROCAS[PROCA]": "A menudo + Muy a menudo",
    }

    resultados = []

    df_temp = df[df[columnas_items].notna().any(axis=1)].copy()

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
    df_resultado = df_resultado.sort_values('Porcentaje', ascending=False).reset_index(drop=True)
    return df_resultado

def porcentaje_salud_cronica(df, columna_item, etiquetas):
    df_temp = df[df[columna_item].notna()]
    
    conteo = df_temp[columna_item].value_counts(normalize=True)
    
    resultados = [
        {"Categoria_label": etiquetas.get(int(valor), f"Otro ({valor})"),
         "Porcentaje": pct,
         "Variable": columna_item}
        for valor, pct in conteo.items()
    ]
    
    return pd.DataFrame(resultados)

def depresion_manejo_clinico(df, group_cols=None):
    phq_cols = [f"PHQ8[PHQ0{i}]" for i in range(1, 9)]
    ed_cols = ["DSM5[DSM22]", "ED15[ED01]", "ED15[ED02]"]

    df_validos = df.dropna(subset=phq_cols).copy()
    if df_validos.empty:
        return pd.DataFrame(columns=["Categoria", "Serie", "Valor"])
    
    df_validos["PUNTAJE_PHQ8"] = df_validos[phq_cols].sum(axis=1)
    df_validos["depresion_malestar_clinico"] = df_validos["PUNTAJE_PHQ8"].apply(lambda x: "Sí" if x >= 10 else "No")

    resultados = []

    if not group_cols:
        dsm5_count = df[ed_cols].notna().any(axis=1).sum()
        if dsm5_count == 0:
            return pd.DataFrame(columns=["Categoria", "Serie", "Valor"])
        total_clinico = (df_validos["depresion_malestar_clinico"] == "Sí").sum()
        porcentaje = total_clinico / dsm5_count
        resultados.append({"Categoria": "Global", "Serie": "Malestar clínico en depresión", "Valor": porcentaje})
    else:
        for col in group_cols:
            categorias = df_validos[col].dropna().unique()
            for cat in categorias:
                df_cat = df_validos[df_validos[col] == cat]
                dsm_cols = ["DSM5[DSM" + str(i).zfill(2) + "]" for i in range(1, 23)] + ["ED15[ED01]", "ED15[ED02]"]
                denom = df[(df[col] == cat) & df[dsm_cols].notna().all(axis=1)].shape[0]
                if denom == 0:
                    porcentaje = 0
                else:
                    total_clinico = (df_cat["depresion_malestar_clinico"] == "Sí").sum()
                    porcentaje = total_clinico / denom
                resultados.append({
                    "Categoria": cat,
                    "Serie": "Malestar clínico en depresión",
                    "Valor": porcentaje
                })

    df_resultado = pd.DataFrame(resultados)
    return df_resultado


def ansiedad_manejo_clinico(df, group_cols=None):
    gad_cols = [f"GAD7[GAD0{i}]" for i in range(1, 8)]
    ed_cols = ["DSM5[DSM22]", "ED15[ED01]", "ED15[ED02]"]
    df_validos = df.dropna(subset=gad_cols).copy()
    if df_validos.empty:
        return pd.DataFrame(columns=["Categoria", "Serie", "Valor"])

    df_validos["PUNTAJE_GAD7"] = df_validos[gad_cols].sum(axis=1)
    df_validos["ansiedad_malestar_clinico"] = df_validos["PUNTAJE_GAD7"].apply(lambda x: "Sí" if x >= 10 else "No")

    resultados = []

    if not group_cols:
        dsm5_count = df[ed_cols].notna().any(axis=1).sum()
        if dsm5_count == 0:
            return pd.DataFrame(columns=["Categoria", "Serie", "Valor"])
        total_clinico = (df_validos["ansiedad_malestar_clinico"] == "Sí").sum()
        porcentaje = (total_clinico / dsm5_count)
        resultados.append({"Categoria": "Global", "Serie": "Malestar clínico en ansiedad", "Valor": porcentaje})
    else:
        for col in group_cols:
            categorias = df_validos[col].dropna().unique()
            for cat in categorias:
                df_cat = df_validos[df_validos[col] == cat]
                dsm_cols = ["DSM5[DSM" + str(i).zfill(2) + "]" for i in range(1, 23)] + ["ED15[ED01]", "ED15[ED02]"]
                denom = df[(df[col] == cat) & df[dsm_cols].notna().all(axis=1)].shape[0]
                if denom == 0:
                    porcentaje = 0
                else:
                    total_clinico = (df_cat["ansiedad_malestar_clinico"] == "Sí").sum()
                    porcentaje = total_clinico / denom
                resultados.append({
                    "Categoria": cat,
                    "Serie": "Malestar clínico en ansiedad",
                    "Valor": porcentaje
                })
        
    return pd.DataFrame(resultados)

def personalidad_manejo_clinico(df, group_cols=None):
    lpf_cols = ["LPFS[LPFS01]", "LPFS[LPFS02]", "LPFS[LPFS03]", "LPFS[LPFS04]", "LPFS[LPFS05]", "LPFS[LPFS06]", "LPFS[LPFS07]", "LPFS[LPFS08]", "LPFS[LPFS09]","LPFS[LPFS10]", "LPFS[LPFS11]", "LPFS[LPFS12]"]
    ed_cols = ["DSM5[DSM22]", "ED15[ED01]", "ED15[ED02]"]
    df_validos = df.dropna(subset=lpf_cols).copy()
    if df_validos.empty:
        return pd.DataFrame(columns=["Categoria", "Serie", "Valor"])

    df_validos["PUNTAJE_LPFS"] = df_validos[lpf_cols].sum(axis=1)
    df_validos["personalidad_malestar_clinico"] = df_validos["PUNTAJE_LPFS"].apply(lambda x: "Sí" if x >= 27 else "No")
    resultados = []
    if not group_cols:
        dsm5_count = df[ed_cols].notna().any(axis=1).sum()
        total_clinico = (df_validos["personalidad_malestar_clinico"] == "Sí").sum()
        porcentaje = (total_clinico / dsm5_count)
        resultados.append({"Categoria": "Global", "Serie": "Malestar clínico en trastorno de personalidad", "Valor": porcentaje})
    else:
        for col in group_cols:
            categorias = df_validos[col].dropna().unique()
            for cat in categorias:
                df_cat = df_validos[df_validos[col] == cat]
                dsm_cols = ["DSM5[DSM" + str(i).zfill(2) + "]" for i in range(1, 23)] + ["ED15[ED01]", "ED15[ED02]"]
                denom = df[(df[col] == cat) & df[dsm_cols].notna().all(axis=1)].shape[0]
                if denom == 0:
                    porcentaje = 0
                else:
                    total_clinico = (df_cat["personalidad_malestar_clinico"] == "Sí").sum()
                    porcentaje = total_clinico / denom
                resultados.append({
                    "Categoria": cat,
                    "Serie": "Malestar clínico en personalidad",
                    "Valor": porcentaje
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

def marihuana_manejo_clinico(df, group_cols=None):
    marihuana_cols = [f"CAST[CAST0{i}]" for i in range(1, 7)]
    ed_cols = ["DSM5[DSM22]", "ED15[ED01]", "ED15[ED02]"]
    df_validos = df.dropna(subset=marihuana_cols).copy()
    if df_validos.empty:
        return pd.DataFrame(columns=["Categoria", "Serie", "Valor"])
    df_validos["PUNTAJE_MARIHUANA"] = df_validos[marihuana_cols].sum(axis=1)
    df_validos["marihuana_malestar_clinico"] = df_validos["PUNTAJE_MARIHUANA"].apply(clasificar_marihuana)
    resultados = []
    if not group_cols:
        dsm5_count = df[ed_cols].notna().any(axis=1).sum()
        total_clinico = (df_validos["marihuana_malestar_clinico"] == "Sí").sum()
        porcentaje = (total_clinico / dsm5_count)
        resultados.append({"Categoria": "Global", "Serie": "Malestar clínico por uso problemático de marihuana", "Valor": porcentaje})
    else:
        for col in group_cols:
            categorias = df_validos[col].dropna().unique()
            for cat in categorias:
                df_cat = df_validos[df_validos[col] == cat]
                dsm_cols = ["DSM5[DSM" + str(i).zfill(2) + "]" for i in range(1, 23)] + ["ED15[ED01]", "ED15[ED02]"]
                denom = df[(df[col] == cat) & df[dsm_cols].notna().all(axis=1)].shape[0]
                if denom == 0:
                    porcentaje = 0
                else:
                    total_clinico = (df_cat["marihuana_malestar_clinico"] == "Sí").sum()
                    porcentaje = total_clinico / denom
                resultados.append({
                    "Categoria": cat,
                    "Serie": "Malestar clínico en marihuana",
                    "Valor": porcentaje
                })
    return pd.DataFrame(resultados)

def alcohol_manejo_clinico(df, group_cols=None):
    audit_cols = ["AUDIT01[AUDIT01]", "AUDIT02[AUDIT02]", "AUDIT38[AUDIT03]", "AUDIT38[AUDIT04]", "AUDIT38[AUDIT05]", "AUDIT38[AUDIT06]", "AUDIT38[AUDIT07]", "AUDIT38[AUDIT08]", "AUDIT910[AUDIT09]", "AUDIT910[AUDIT10]"]
    ed_cols = ["DSM5[DSM22]", "ED15[ED01]", "ED15[ED02]"]
    df_validos = df.dropna(subset=audit_cols).copy()
    if df_validos.empty:
        return pd.DataFrame(columns=["Categoria", "Serie", "Valor"])
    df_validos["PUNTAJE_AUDIT"] = df_validos[audit_cols].sum(axis=1)
    df_validos["alcohol_malestar_clinico"] = df_validos["PUNTAJE_AUDIT"].apply(lambda x: "Sí" if x >= 16 else "No")
    resultados = []
    if not group_cols:
        dsm5_count = df[ed_cols].notna().any(axis=1).sum()
        total_clinico = (df_validos["alcohol_malestar_clinico"] == "Sí").sum()
        porcentaje = (total_clinico / dsm5_count)
        resultados.append({"Categoria": "Global", "Serie": "Malestar clínico por uso problemático de alcohol", "Valor": porcentaje})
    else:
        for col in group_cols:
            categorias = df_validos[col].dropna().unique()
            for cat in categorias:
                df_cat = df_validos[df_validos[col] == cat]
                dsm_cols = ["DSM5[DSM" + str(i).zfill(2) + "]" for i in range(1, 23)] + ["ED15[ED01]", "ED15[ED02]"]
                denom = df[(df[col] == cat) & df[dsm_cols].notna().all(axis=1)].shape[0]
                if denom == 0:
                    porcentaje = 0
                else:
                    total_clinico = (df_cat["alcohol_malestar_clinico"] == "Sí").sum()
                    porcentaje = total_clinico / denom
                resultados.append({
                    "Categoria": cat,
                    "Serie": "Malestar clínico en alcohol",
                    "Valor": porcentaje
                })
    return pd.DataFrame(resultados)

def ideacion_suicida_manejo_clinico(df, group_cols=None):
    idea_cols = ["PHQ09[PHQ09F]"]
    df_validos = df.dropna(subset=idea_cols).copy()
    if df_validos.empty:
        return pd.DataFrame(columns=["Categoria", "Serie", "Valor"])
    df_validos["PUNTAJE_PHQ09"] = df_validos[idea_cols].sum(axis=1)
    df_validos["ideacion_suicida_malestar_clinico"] = df_validos["PUNTAJE_PHQ09"].apply(lambda x: "Sí" if x >= 1 else "-")
    resultados = []
    if not group_cols:
        total_clinico = (df_validos["ideacion_suicida_malestar_clinico"] == "Sí").sum()
        porcentaje = (total_clinico / len(df_validos))
        resultados.append({"Categoria": "Global", "Serie": "Malestar clínico por ideacion suicida", "Valor": porcentaje})
    else:
        for col in group_cols:
            categorias = df_validos[col].dropna().unique()
            for cat in categorias:
                df_cat = df_validos[df_validos[col] == cat]
                dsm_cols = ["DSM5[DSM" + str(i).zfill(2) + "]" for i in range(1, 23)] + ["ED15[ED01]", "ED15[ED02]"]
                denom = df[(df[col] == cat) & df[dsm_cols].notna().all(axis=1)].shape[0]
                if denom == 0:
                    porcentaje = 0
                else:
                    total_clinico = (df_cat["ideacion_suicida_malestar_clinico"] == "Sí").sum()
                    porcentaje = total_clinico / denom
                resultados.append({
                    "Categoria": cat,
                    "Serie": "Malestar clínico en suicidio",
                    "Valor": porcentaje
                })
    return pd.DataFrame(resultados)

def salud_mental_grupo_verde(df):
    grupo_verde_total = 0

    for _, row in df.iterrows():
        posible = 0
        if row["DSM5[DSM01]"] < 2 and row["DSM5[DSM02]"] < 2:
            posible += 1
        if row["DSM5[DSM03]"] < 2:
            posible += 1
        if row["DSM5[DSM04]"] < 2 and row["DSM5[DSM05]"] < 2:
            posible += 1
        if row["DSM5[DSM06]"] < 2 and row["DSM5[DSM07]"] < 2 and row["DSM5[DSM08]"] < 2:
            posible += 1
        if row["DSM5[DSM09]"] < 2 and row["DSM5[DSM10]"] < 2:
            posible += 1
        if row["DSM5[DSM11]"] < 1 and row["DSM5[DSM12]"] < 1:
            posible += 1
        if row["DSM5[DSM13]"] < 2:
            posible += 1
        if row["DSM5[DSM14]"] < 2:
            posible += 1
        if row["DSM5[DSM15]"] < 2 and row["DSM5[DSM16]"] < 2:
            posible += 1
        if row["DSM5[DSM17]"] < 2:
            posible += 1
        if row["DSM5[DSM18]"] < 2 and row["DSM5[DSM19]"] < 2:
            posible += 1
        if row["DSM5[DSM20]"] < 1:
            posible += 1
        if row["DSM5[DSM22]"] < 1:
            posible += 1
        if row["ED15[ED01]"] < 2 and row["ED15[ED02]"] < 2:
            posible += 1
        if posible == 14:
            grupo_verde_total += 1

    return grupo_verde_total


def salud_mental_grupo_rojo(df):
    grupo_rojo_total = 0
    phq_cols = [f"PHQ8[PHQ0{i}]" for i in range(1, 9)]
    gad_cols = [f"GAD7[GAD0{i}]" for i in range(1, 8)]
    lpf_cols = ["LPFS[LPFS01]", "LPFS[LPFS02]", "LPFS[LPFS03]", "LPFS[LPFS04]", "LPFS[LPFS05]", "LPFS[LPFS06]", "LPFS[LPFS07]", "LPFS[LPFS08]", "LPFS[LPFS09]","LPFS[LPFS10]", "LPFS[LPFS11]", "LPFS[LPFS12]"]
    marihuana_cols = [f"CAST[CAST0{i}]" for i in range(1, 7)]
    audit_cols = ["AUDIT01[AUDIT01]", "AUDIT02[AUDIT02]", "AUDIT38[AUDIT03]", "AUDIT38[AUDIT04]", "AUDIT38[AUDIT05]", "AUDIT38[AUDIT06]", "AUDIT38[AUDIT07]", "AUDIT38[AUDIT08]", "AUDIT910[AUDIT09]", "AUDIT910[AUDIT10]"]
    idea_cols = ["PHQ09[PHQ09F]"]
    for _, row in df.iterrows():
        posible = False
        if not row[phq_cols].isna().any():
            if row[phq_cols].sum() >= 10:
                posible = True
        if not row[gad_cols].isna().any():
            if row[gad_cols].sum() >= 10:
                posible = True
        if not row[lpf_cols].isna().any():
            if row[lpf_cols].sum() >= 27:
                posible = True
        if not row[marihuana_cols].isna().any():
            if row[marihuana_cols].sum() >= 4:
                posible = True
        if not row[audit_cols].isna().any():
            if row[audit_cols].sum() >= 16:
                posible = True
        if not row[idea_cols].isna().any():
            if row[idea_cols].sum() >= 1:
                posible = True
        if posible:
            grupo_rojo_total += 1
    
    return grupo_rojo_total

def cantidad_total_dms5(df):
    dsm_cols = ["DSM5[DSM" + str(i).zfill(2) + "]" for i in range(1, 23)] + ["ED15[ED01]", "ED15[ED02]"]    
    total = df[dsm_cols].notna().all(axis=1).sum()
    
    return total

def promedio_factor_carga_enfermedad_grupo_rojo(df):
    phq_cols = [f"PHQ8[PHQ0{i}]" for i in range(1, 9)]
    gad_cols = [f"GAD7[GAD0{i}]" for i in range(1, 8)]
    lpf_cols = [f"LPFS[LPFS{str(i).zfill(2)}]" for i in range(1, 13)]
    marihuana_cols = [f"CAST[CAST0{i}]" for i in range(1, 7)]
    audit_cols = ["AUDIT01[AUDIT01]", "AUDIT02[AUDIT02]"] + [f"AUDIT38[AUDIT0{i}]" for i in range(3, 9)] + [f"AUDIT910[AUDIT{str(i).zfill(2)}]" for i in range(9, 11)]
    idea_cols = ["PHQ09[PHQ09F]"]
    dsm_cols = [f"DSM5[DSM{str(i).zfill(2)}]" for i in range(1, 23)] + ["ED15[ED01]", "ED15[ED02]"]

    mask_red = pd.Series(False, index=df.index)
    
    mask_phq = df[phq_cols].notna().all(axis=1) & (df[phq_cols].sum(axis=1) >= 10)
    mask_gad = df[gad_cols].notna().all(axis=1) & (df[gad_cols].sum(axis=1) >= 10)
    mask_lpf = df[lpf_cols].notna().all(axis=1) & (df[lpf_cols].sum(axis=1) >= 27)
    mask_marihuana = df[marihuana_cols].notna().all(axis=1) & (df[marihuana_cols].sum(axis=1) >= 4)
    mask_audit = df[audit_cols].notna().all(axis=1) & (df[audit_cols].sum(axis=1) >= 16)
    mask_idea = df[idea_cols].notna().all(axis=1) & (df[idea_cols].sum(axis=1) >= 1)

    mask_red = mask_phq | mask_gad | mask_lpf | mask_marihuana | mask_audit | mask_idea

    df_red = df[mask_red & df[dsm_cols].notna().all(axis=1)]

    if len(df_red) > 0:
        promedio = df_red[dsm_cols].sum(axis=1).mean()
        return promedio
    else:
        return 0

def promedio_factor_carga_enfermedad_grupo_amarillo(df):
    dsm_cols = [f"DSM5[DSM{str(i).zfill(2)}]" for i in range(1, 23)] + ["ED15[ED01]", "ED15[ED02]"]
    
    df_valid = df[df[dsm_cols].notna().all(axis=1)].copy()
    
    mask_green = df_valid.apply(lambda row: (
        (row["DSM5[DSM01]"] < 2 and row["DSM5[DSM02]"] < 2) and
        (row["DSM5[DSM03]"] < 2) and
        (row["DSM5[DSM04]"] < 2 and row["DSM5[DSM05]"] < 2) and
        (row["DSM5[DSM06]"] < 2 and row["DSM5[DSM07]"] < 2 and row["DSM5[DSM08]"] < 2) and
        (row["DSM5[DSM09]"] < 2 and row["DSM5[DSM10]"] < 2) and
        (row["DSM5[DSM11]"] < 1 and row["DSM5[DSM12]"] < 1) and
        (row["DSM5[DSM13]"] < 2) and
        (row["DSM5[DSM14]"] < 2) and
        (row["DSM5[DSM15]"] < 2 and row["DSM5[DSM16]"] < 2) and
        (row["DSM5[DSM17]"] < 2) and
        (row["DSM5[DSM18]"] < 2 and row["DSM5[DSM19]"] < 2) and
        (row["DSM5[DSM20]"] < 1) and
        (row["DSM5[DSM22]"] < 1) and
        (row["ED15[ED01]"] < 2 and row["ED15[ED02]"] < 2)
    ), axis=1)

    phq_cols = [f"PHQ8[PHQ0{i}]" for i in range(1, 9)]
    gad_cols = [f"GAD7[GAD0{i}]" for i in range(1, 8)]
    lpf_cols = [f"LPFS[LPFS{str(i).zfill(2)}]" for i in range(1, 13)]
    marihuana_cols = [f"CAST[CAST0{i}]" for i in range(1, 7)]
    audit_cols = ["AUDIT01[AUDIT01]", "AUDIT02[AUDIT02]"] + [f"AUDIT38[AUDIT0{i}]" for i in range(3, 9)] + [f"AUDIT910[AUDIT{str(i).zfill(2)}]" for i in range(9, 11)]
    idea_cols = ["PHQ09[PHQ09F]"]
    
    mask_red = (
        ((df_valid[phq_cols].notna().all(axis=1)) & (df_valid[phq_cols].sum(axis=1) >= 10)) |
        ((df_valid[gad_cols].notna().all(axis=1)) & (df_valid[gad_cols].sum(axis=1) >= 10)) |
        ((df_valid[lpf_cols].notna().all(axis=1)) & (df_valid[lpf_cols].sum(axis=1) >= 27)) |
        ((df_valid[marihuana_cols].notna().all(axis=1)) & (df_valid[marihuana_cols].sum(axis=1) >= 4)) |
        ((df_valid[audit_cols].notna().all(axis=1)) & (df_valid[audit_cols].sum(axis=1) >= 16)) |
        ((df_valid[idea_cols].notna().all(axis=1)) & (df_valid[idea_cols].sum(axis=1) >= 1))
    )
    
    mask_yellow = ~mask_green & ~mask_red
    
    df_yellow = df_valid[mask_yellow]
    if len(df_yellow) > 0:
        promedio = df_yellow[dsm_cols].sum(axis=1).mean()
        return promedio
    else:
        return 0


def cupit_marihuana(df):
    dsm_cols = ["DSM5[DSM" + str(i).zfill(2) + "]" for i in range(1, 23)] + ["ED15[ED01]", "ED15[ED02]"]
    
    # Filtrar casos válidos (respondieron todo DSM5 y ED15)
    df_validos = df[df[dsm_cols].notna().all(axis=1)].copy()
    
    if df_validos.empty:
        return 0

    total_validos = len(df_validos)
    total_mayor_igual_3 = (df_validos["CUPIT"] >= 3).sum()
    resultado = total_mayor_igual_3 / total_validos if total_validos > 0 else 0

    return resultado * 100

def porcentaje_para_barras_apiladas(df, columnas, etiquetas_respuesta=None, etiquetas_categoria=None):
    resultados = []

    for col in columnas:
        conteo = df[col].value_counts(normalize=True)  # proporción por respuesta 
        for respuesta, porcentaje in conteo.items():
            # Mapear etiqueta de respuesta si existe
            etiqueta_resp = etiquetas_respuesta.get(respuesta, respuesta) if etiquetas_respuesta else respuesta
            
            # Mapear etiqueta de categoría si existe
            etiqueta_cat = etiquetas_categoria.get(col, col) if etiquetas_categoria else col
            
            resultados.append({
                "Categoria": etiqueta_cat,
                "Respuesta": etiqueta_resp,
                "Porcentaje": round(porcentaje, 2)
            })

    return pd.DataFrame(resultados)