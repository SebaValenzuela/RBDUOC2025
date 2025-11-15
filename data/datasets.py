import pandas as pd
from io import StringIO

LABELS_ESTRESORES = {
    "ESTRE[ESTRE01]": "Problemas en relación sentimental",
    "ESTRE[ESTRE02]": "Problemas en relaciones familiares",
    "ESTRE[ESTRE03]": "Problemas en la relación con compañeros",
    "ESTRE[ESTRE04]": "Problemas en la relación con profesores",
    "ESTRE[ESTRE05]": "Aislamiento",
    "ESTRE[ESTRE06]": "Problemas de salud personales",
    "ESTRE[ESTRE07]": "Problemas de salud de un ser querido",
    "ESTRE[ESTRE08]": "Duelos/pérdidas",
    "ESTRE[ESTRE09]": "Problemas de autoestima",
    "ESTRE[ESTRE10]": "Situación económica compleja",
    "ESTRE[ESTRE11]": "Dificultad para compatibilizar trabajo y estudios",
    "ESTRE[ESTRE12]": "Dificultades de transporte y desplazamiento",
    "ESTRE[ESTRE13]": "Problemas de inseguridad al entrar y salir de la sede (delincuencia)",
    "ESTRE[ESTRE14]": "Problemas de inseguridad en tu barrio",
    "ESTRE[ESTRE15]": "Espacios de clase no adecuados en Duoc UC",
    "ESTRE[ESTRE16]": "Recursos de la universidad poco actualizados",
    "ESTRE[ESTRE17]": "Experiencias de discriminación en Duoc UC",
    "ESTRE[ESTRE18]": "Carga académica exigente",
    "ESTRE[ESTRE19]": "Futuro laboral",
    "ESTRE[ESTRE20]": "Panorama político y social del país",
    "ESTRE[ESTRE21]": "Panorama político internacional o cambios en el mundo (seguridad mundial, preocupación financiera)",
    "ESTRE[ESTRE22]": "Crisis climática y desastres naturales"
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

LABELS_BARRERAS = {
    "BARR[BARR01]": "No estabas seguro/a de que los tratamientos disponibles fueran muy eficaces.",
    "BARR[BARR02]": "Querías afrontar el problema por tu cuenta.",
    "BARR[BARR03]": "Te daba demasiada vergüenza.",
    "BARR[BARR04]": "Preferiste hablarlo con amigos/as o parientes.",
    "BARR[BARR05]": "Costaba demasiado dinero.",
    "BARR[BARR06]": "No estabas seguro de a dónde ir o a quién consultar.",
    "BARR[BARR07]": "Tuviste problemas de tiempo, desplazamientos o de horario.",
    "BARR[BARR08]": "Temías que pudiese perjudicar tu carrera académica.",
    "BARR[BARR09]": "Dificultad para conseguir una cita",
    "BARR[BARR10]": "Te preocupaba que la gente te tratara diferente si supiera que estabas en tratamiento."
}

LABELS_APOYO_ITEMS = {
    "APOYO[APOY01]": "Profesores/as",
    "APOYO[APOY02]": "Administrativos/as",
    "APOYO[APOY03]": "Autoridades de Duoc UC",
    "APOYO[APOY04]": "Familia",
    "APOYO[APOY05]": "Amistades dentro de Duoc UC",
    "APOYO[APOY06]": "Amistades fuera de Duoc UC"
}

LABELS_APOYO_RESPUESTAS = {
    1: "Muy insatisfecho",
    2: "Insatisfecho",
    3: "Ni satisfecho ni insatisfecho",
    4: "Satisfecho",
    5: "Muy satisfecho"
}

LABELS_FLOW_ITEMS = {
    "FLOW[FLOW01]": "Confío en mi capacidad para afrontar las altas exigencias de la situación.",
    "FLOW[FLOW02]": "Me siento completamente en control de mis acciones.",
    "FLOW[FLOW03]": "En cada paso, sé exactamente lo que tengo que hacer.",
    "FLOW[FLOW04]": "Estoy totalmente absorto/a en lo que estoy haciendo.",
    "FLOW[FLOW05]": "Estoy profundamente concentrado/a en lo que estoy haciendo.",
    "FLOW[FLOW06]": "Suelo perder la noción del tiempo.",
    "FLOW[FLOW07]": "No me importa lo que los demás puedan pensar de mí.",
    "FLOW[FLOW08]": "No me preocupa el juicio de los demás.",
    "FLOW[FLOW09]": "No me preocupa lo que los demás puedan pensar de mí.",
    "FLOW[FLOW10]": "Tengo la sensación de que estoy viviendo una experiencia muy emocionante.",
    "FLOW[FLOW11]": "Esta actividad me produce una sensación de bienestar.",
    "FLOW[FLOW12]": "Cuando hablo de esta actividad, siento una emoción tan profunda que quiero compartirla.",
}

LABELS_CONDICION_ACADEMICA = {
    "CONDACAD[CON01]": "En mi casa, cuento con un espacio adecuado para estudiar o hacer mis trabajos",
    "CONDACAD[CON02]": "En Duoc UC, cuento con un espacio adecuado para estudiar o hacer mis trabajos",
    "CONDACAD[CON03]": "Necesito apoyo y/o capacitación para utilizar las plataformas o herramientas tecnológicas requeridas en mi carrera (softwares, plataforma estudiantil, programas, etc.)"
}

# Este diccionario define tu regla de agrupación
FLOW_GROUPING_MAP = {
    1: "Apreciación negativa",
    2: "Apreciación negativa",
    3: "Apreciación neutra",
    4: "Apreciación neutra",
    5: "Apreciación neutra",
    6: "Apreciación positiva",
    7: "Apreciación positiva",
}

LABELS_APPVI02 = {
    "APPVI02[1]": "Reserva de hora psicológica",
    "APPVI02[2]": "Inscripción en charlas de salud mental",
    "APPVI02[3]": "Contenidos en salud mental"
}

def porcentaje_por_categoria(df, columna, etiquetas=None, invertir=False):
    porcentajes = df[columna].value_counts(normalize=True).reset_index()
    porcentajes.columns = [columna, "Porcentaje"]
    
    if etiquetas:
        porcentajes["Etiqueta"] = porcentajes[columna].map(etiquetas)
        porcentajes = porcentajes.groupby("Etiqueta", as_index=False)["Porcentaje"].sum()
    
    if invertir:
        porcentajes = porcentajes.iloc[::-1].reset_index(drop=True)
    
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
        if espacio > 0:
            spacer_rows = []
            for i in range(espacio):
                spacer_row = {
                    col: None,
                    "Porcentaje": None,
                    "Variable": col,
                    "Categoria_label": f"_spacer_{col}_{i}"
                }
                spacer_rows.append(spacer_row)
            df_spacer = pd.DataFrame(spacer_rows, columns=temp.columns)
            resultados.append(df_spacer)

    df_resultado = pd.concat(resultados, ignore_index=True)
    
    df_resultado["Porcentaje"] = df_resultado["Porcentaje"].replace(0, None)
    df_resultado["Porcentaje"] = df_resultado["Porcentaje"].fillna("")
    
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


def porcentaje_estresores_exigencia(df, columnas_estres, filtro_columna=None, filtro_valores=None):
    marcar_col='ESTRE[ESTRE18]'
    # df_temp = df[df[marcar_col].notna()].copy()
    # df_temp = df[df[marcar_col] == 'Y'].copy()
    df_temp = df[df[columnas_estres].notna().any(axis=1)].copy()

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

    columnas_esperadas = ['Categoria_label', 'Porcentaje', 'Variable']
    
    if not resultados:
        dummy_data = [{
            'Categoria_label': 'Sin datos',
            'Porcentaje': None,
            'Variable': 'Total'
        }]
        df_resultado = pd.DataFrame(dummy_data, columns=columnas_esperadas)
    else:
        df_resultado = pd.DataFrame(resultados, columns=columnas_esperadas)
        df_resultado = df_resultado.iloc[::-1].reset_index(drop=True)
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

def depresion_manejo_clinico(df, group_cols=None, espacio=0):
    """
    Calcula el porcentaje de malestar clínico por depresión,
    agregando espaciadores entre grupos.
    """
    phq_cols = [f"PHQ8[PHQ0{i}]" for i in range(1, 9)]
    ed_cols = ["DSM5[DSM" + str(i).zfill(2) + "]" for i in range(1, 23)] + ["ED15[ED01]", "ED15[ED02]"]

    df_validos = df.dropna(subset=phq_cols).copy()
    if df_validos.empty:
        return pd.DataFrame(columns=["Categoria", "Serie", "Valor"])
    
    df_validos["PUNTAJE_PHQ8"] = df_validos[phq_cols].sum(axis=1)
    df_validos["depresion_malestar_clinico"] = df_validos["PUNTAJE_PHQ8"].apply(lambda x: "Sí" if x >= 10 else "No")

    resultados = []

    if not group_cols:
        dsm5_count = df[ed_cols].notna().any(axis=1).sum()
        if dsm5_count == 0:
            # Retorna DF vacío pero con formato
            df_resultado = pd.DataFrame(columns=["Categoria", "Serie", "Valor"])
            df_resultado["Valor"] = df_resultado["Valor"].replace(0, None).fillna("")
            return df_resultado

        total_clinico = (df_validos["depresion_malestar_clinico"] == "Sí").sum()
        porcentaje = total_clinico / dsm5_count
        resultados.append({"Categoria": "Global", "Serie": "Malestar clínico en depresión", "Valor": porcentaje})
    else:
        for col in group_cols:
            categorias = sorted(df_validos[col].dropna().unique())
            
            for i, cat in enumerate(categorias):
                df_cat = df_validos[df_validos[col] == cat]
                
                # Definición de dsm_cols (lógica original)
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
            
            # --- INICIO: Lógica de espaciado añadida ---
            if espacio > 0:
                for i in range(espacio):
                    spacer_row = {
                        "Categoria": f"_spacer_{col}_{i}", # Etiqueta única
                        "Serie": "Malestar clínico en depresión", # Mantener serie
                        "Valor": None # Valor nulo para espaciado
                    }
                    resultados.append(spacer_row)
            # --- FIN: Lógica de espaciado añadida ---

    # Convertir lista de dicts a DataFrame
    df_resultado = pd.DataFrame(resultados)
    
    # --- INICIO: Lógica de formato añadida (como en promedio_por_categoria) ---
    df_resultado["Valor"] = df_resultado["Valor"].replace(0, None)
    df_resultado["Valor"] = df_resultado["Valor"].fillna("")
    # --- FIN: Lógica de formato añadida ---

    return df_resultado


def ansiedad_manejo_clinico(df, group_cols=None, espacio=0):
    gad_cols = [f"GAD7[GAD0{i}]" for i in range(1, 8)]
    ed_cols = ["DSM5[DSM" + str(i).zfill(2) + "]" for i in range(1, 23)] + ["ED15[ED01]", "ED15[ED02]"]
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
            categorias = sorted(df_validos[col].dropna().unique())
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
            if espacio > 0:
                for i in range(espacio):
                    spacer_row = {
                        "Categoria": f"_spacer_{col}_{i}", # Etiqueta única
                        "Serie": "Malestar clínico en ansiedad", # Mantener serie
                        "Valor": None # Valor nulo para espaciado
                    }
                    resultados.append(spacer_row)
        
    return pd.DataFrame(resultados)

def personalidad_manejo_clinico(df, group_cols=None, espacio=0):
    lpf_cols = ["LPFS[LPFS01]", "LPFS[LPFS02]", "LPFS[LPFS03]", "LPFS[LPFS04]", "LPFS[LPFS05]", "LPFS[LPFS06]", "LPFS[LPFS07]", "LPFS[LPFS08]", "LPFS[LPFS09]","LPFS[LPFS10]", "LPFS[LPFS11]", "LPFS[LPFS12]"]
    ed_cols = ["DSM5[DSM" + str(i).zfill(2) + "]" for i in range(1, 23)] + ["ED15[ED01]", "ED15[ED02]"]
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
            categorias = sorted(df_validos[col].dropna().unique())
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
            if espacio > 0:
                for i in range(espacio):
                    spacer_row = {
                        "Categoria": f"_spacer_{col}_{i}", # Etiqueta única
                        "Serie": "Malestar clínico en trastornos de personalidad", # Mantener serie
                        "Valor": None # Valor nulo para espaciado
                    }
                    resultados.append(spacer_row)
    return pd.DataFrame(resultados)

def clasificar_marihuana(x):
    if pd.isna(x):
        return pd.NA
    if x >= 4:
        return "Sí"
    if x == 3:
        return "No"
    return pd.NA

def marihuana_manejo_clinico(df, group_cols=None, espacio=0):
    marihuana_cols = [f"CAST[CAST0{i}]" for i in range(1, 7)]
    ed_cols = ["DSM5[DSM" + str(i).zfill(2) + "]" for i in range(1, 23)] + ["ED15[ED01]", "ED15[ED02]"]
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
            categorias = sorted(df_validos[col].dropna().unique())
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
            if espacio > 0:
                for i in range(espacio):
                    spacer_row = {
                        "Categoria": f"_spacer_{col}_{i}", # Etiqueta única
                        "Serie": "Malestar clínico en uso problematica por marihuana", # Mantener serie
                        "Valor": None # Valor nulo para espaciado
                    }
                    resultados.append(spacer_row)
    return pd.DataFrame(resultados)

def alcohol_manejo_clinico(df, group_cols=None, espacio=0):
    audit_cols = ["AUDIT01[AUDIT01]", "AUDIT02[AUDIT02]", "AUDIT38[AUDIT03]", "AUDIT38[AUDIT04]", "AUDIT38[AUDIT05]", "AUDIT38[AUDIT06]", "AUDIT38[AUDIT07]", "AUDIT38[AUDIT08]", "AUDIT910[AUDIT09]", "AUDIT910[AUDIT10]"]
    ed_cols = ["DSM5[DSM" + str(i).zfill(2) + "]" for i in range(1, 23)] + ["ED15[ED01]", "ED15[ED02]"]
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
            categorias = sorted(df_validos[col].dropna().unique())
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
            if espacio > 0:
                for i in range(espacio):
                    spacer_row = {
                        "Categoria": f"_spacer_{col}_{i}", # Etiqueta única
                        "Serie": "Malestar clínico en uso problematica de alcohol", # Mantener serie
                        "Valor": None # Valor nulo para espaciado
                    }
                    resultados.append(spacer_row)
    return pd.DataFrame(resultados)

def ideacion_suicida_manejo_clinico(df, group_cols=None, espacio=0):
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
            categorias = sorted(df_validos[col].dropna().unique())
            for cat in categorias:
                df_cat = df_validos[df_validos[col] == cat]
                dsm_cols = ["DSM5[DSM" + str(i).zfill(2) + "]" for i in range(1, 23)] + ["ED15[ED01]", "ED15[ED02]"]
                denom = df[(df[col] == cat) & df[dsm_cols].notna().all(axis=1)].shape[0]
                if denom == 0:
                    porcentaje = 0
                else:
                    total_clinico = (df_cat["ideacion_suicida_malestar_clinico"] == "Sí").sum()
                    porcentaje = total_clinico / len(df_cat)
                resultados.append({
                    "Categoria": cat,
                    "Serie": "Malestar clínico en suicidio",
                    "Valor": porcentaje
                })
            if espacio > 0:
                for i in range(espacio):
                    spacer_row = {
                        "Categoria": f"_spacer_{col}_{i}", # Etiqueta única
                        "Serie": "Malestar clínico en ideación suicida", # Mantener serie
                        "Valor": None # Valor nulo para espaciado
                    }
                    resultados.append(spacer_row)
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
        if row["DSM5[DSM21]"] < 1:
            posible += 1
        if row["DSM5[DSM22]"] < 1:
            posible += 1
        if row["ED15[ED01]"] < 2 and row["ED15[ED02]"] < 2:
            posible += 1
        if row["PHQ09[PHQ09F]"] < 1 or pd.isna(row["PHQ09[PHQ09F]"]):
            posible += 1
        if posible == 16:
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
        (row["DSM5[DSM21]"] < 1) and
        (row["DSM5[DSM22]"] < 1) and
        (row["ED15[ED01]"] < 2 and row["ED15[ED02]"] < 2) and
        (row["PHQ09[PHQ09F]"] < 1 | pd.isna(row["PHQ09[PHQ09F]"]))
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

def ideacion_suicida_barras(df, columnas, etiquetas_respuesta=None, etiquetas_categoria=None):
    resultados = []

    columnas_validas = ["CSS01", "CSS02", "CSS03", "CSS04", "CSS05", "CSS06"]
    df = df[columnas_validas].dropna().copy()

    for col in columnas:
        conteo = df[col].value_counts()
        for respuesta, cantidad in conteo.items():
            etiqueta_resp = etiquetas_respuesta.get(respuesta, respuesta) if etiquetas_respuesta else respuesta
            
            etiqueta_cat = etiquetas_categoria.get(col, col) if etiquetas_categoria else col
            
            resultados.append({
                "Categoria": etiqueta_cat,
                "Respuesta": etiqueta_resp,
                "Porcentaje": cantidad / len(df),
            })
    
    resultados = pd.DataFrame(resultados)
    return resultados

def porcentaje_para_barras_apiladas(df, columnas, etiquetas_respuesta=None, etiquetas_categoria=None):
    resultados = []

    for col in columnas:
        conteo = df[col].value_counts(normalize=True)
        for respuesta, porcentaje in conteo.items():
            etiqueta_resp = etiquetas_respuesta.get(respuesta, respuesta) if etiquetas_respuesta else respuesta
            
            etiqueta_cat = etiquetas_categoria.get(col, col) if etiquetas_categoria else col
            
            resultados.append({
                "Categoria": etiqueta_cat,
                "Respuesta": etiqueta_resp,
                "Porcentaje": porcentaje,
            })

    return pd.DataFrame(resultados)

def barreras_acceso_tratamiento(df):
    barreras_cols = [col for col in df.columns if col.startswith("BARR[")]
    
    if not barreras_cols:
        return pd.DataFrame(columns=['Categoria', 'Porcentaje', 'Variable'])

    valores_marcar = [4, 5]
    resultados = []
    df_temp = df.copy()
    for col in barreras_cols:
        count = df_temp[col].isin(valores_marcar).sum()
        total = df_temp[col].notna().sum()
        pct = count / total if total > 0 else 0
        label = LABELS_BARRERAS.get(col, col)
        resultados.append({
            'Categoria': label,
            'Porcentaje': pct,
            'Variable': 'Total'
        })
    df_resultado = pd.DataFrame(resultados)
    df_resultado = df_resultado.sort_values('Porcentaje', ascending=True).reset_index(drop=True)
    return df_resultado

def apoyo_percibido(df):
    columnas_apoyo = [col for col in df.columns if col.startswith("APOYO[")]
    if not columnas_apoyo:
         return pd.DataFrame(columns=['Categoria', 'Respuesta', 'Porcentaje'])
    df_resultado = porcentaje_para_barras_apiladas(
        df,
        columnas=columnas_apoyo,
        etiquetas_respuesta=LABELS_APOYO_RESPUESTAS,
        etiquetas_categoria=LABELS_APOYO_ITEMS
    )
    categorias_ordenadas = [
        "Amistades fuera de Duoc UC",
        "Amistades dentro de Duoc UC",
        "Familia",
        "Autoridades de Duoc UC",
        "Administrativos/as",
        "Profesores/as",
    ]
    orden_respuestas = [
        "Muy insatisfecho",
        "Insatisfecho",
        "Ni satisfecho ni insatisfecho",
        "Satisfecho",
        "Muy satisfecho"
    ]
    df_resultado_filtrado = df_resultado[df_resultado['Respuesta'].isin(orden_respuestas)].copy()
    df_resultado_filtrado["Respuesta"] = pd.Categorical(
        df_resultado_filtrado["Respuesta"],
        categories=orden_respuestas,
        ordered=True
    )

    categorias_ordenadas = [
        LABELS_APOYO_ITEMS.get(cat, cat) for cat in categorias_ordenadas
    ]

    df_resultado_filtrado["Categoria"] = pd.Categorical(
        df_resultado_filtrado["Categoria"],
        categories=categorias_ordenadas,
        ordered=True
    )

    df_resultado_final = df_resultado_filtrado.sort_values(
        by=['Categoria', 'Respuesta']
    ).reset_index(drop=True)
    
    return df_resultado_final

def flow_percibido(df):
    columnas_flow = [col for col in df.columns if col.startswith("FLOW[")]
    if not columnas_flow:
         return pd.DataFrame(columns=['Categoria', 'Respuesta', 'Porcentaje'])
    df_temp = df.copy()
    df_temp[columnas_flow] = df_temp[columnas_flow].apply(lambda x: x.map(FLOW_GROUPING_MAP))

    df_resultado = porcentaje_para_barras_apiladas(
        df_temp,
        columnas=columnas_flow,
        etiquetas_respuesta=None, 
        etiquetas_categoria=LABELS_FLOW_ITEMS
    )
    orden_respuestas = [
        "Apreciación negativa",
        "Apreciación neutra",
        "Apreciación positiva"
    ]
    df_resultado_filtrado = df_resultado[df_resultado['Respuesta'].isin(orden_respuestas)].copy()
    
    df_resultado_filtrado["Respuesta"] = pd.Categorical(
        df_resultado_filtrado["Respuesta"],
        categories=orden_respuestas,
        ordered=True
    )
    df_resultado_final = df_resultado_filtrado.sort_values(
        by=['Categoria', 'Respuesta']
    ).reset_index(drop=True)
    
    return df_resultado_final

def flow_percibido_positivo(df):
    columnas_flow = [col for col in df.columns if col.startswith("FLOW[")]
    
    if not columnas_flow:
        return 0.0

    df_temp = df.copy()
    df_temp[columnas_flow] = df_temp[columnas_flow].apply(lambda x: x.map(FLOW_GROUPING_MAP))
    conteo_positivas = (df_temp[columnas_flow] == "Apreciación positiva").sum().sum()
    total_respuestas_validas = df_temp[columnas_flow].count().sum()

    if total_respuestas_validas == 0:
        porcentaje_global = 0.0
    else:
        porcentaje_global = conteo_positivas / total_respuestas_validas
    return porcentaje_global * 100

def alimentacion(df, columnas):
    etiquetas_alimentacion_resp = {
        1: "Ningún día",
        2: "Algunos días",
        3: "La mayoría de los días",
        4: "Todos los días"
    }

    etiquetas_alimentacion_cat = {
        "ALIMEN[ALIMEN01]": "Consumes comidas rápidas, fritas, snacks o dulces",
        "ALIMEN[ALIMEN02]": "Consumes gaseosas o bebidas artificiales",
        "ALIMEN[ALIMEN03]": "Desayunas, almuerzas y comes en horarios habituales",
        "ALIMEN[ALIMEN04]": "Omites alguna de las comidas principales (desayuno, almuerzo y comida)",
    }
    
    orden_respuestas = [
        "Ningún día",
        "Algunos días",
        "La mayoría de los días",
        "Todos los días"
    ]
    
    if columnas is None:
        columnas_a_procesar = [
            col for col in df.columns 
            if col.startswith("ALIMEN[") and col in etiquetas_alimentacion_cat
        ]
    else:
        columnas_a_procesar = [
            col for col in columnas 
            if col in etiquetas_alimentacion_cat and col in df.columns
        ]
    
    if not columnas_a_procesar:
        return pd.DataFrame(columns=['Categoria', 'Respuesta', 'Porcentaje'])
    
    df_resultado = porcentaje_para_barras_apiladas(
        df,
        columnas=columnas_a_procesar,
        etiquetas_respuesta=etiquetas_alimentacion_resp,
        etiquetas_categoria=etiquetas_alimentacion_cat,
    )
    
    
    df_resultado_filtrado = df_resultado[df_resultado['Respuesta'].isin(orden_respuestas)].copy()
    
    df_resultado_filtrado["Respuesta"] = pd.Categorical(
        df_resultado_filtrado["Respuesta"],
        categories=orden_respuestas,
        ordered=True
    )
    
    df_resultado_final = df_resultado_filtrado.sort_values(
        by=['Categoria', 'Respuesta']
    ).reset_index(drop=True)
    
    return df_resultado_final

def ingesta_liquidos(df: pd.DataFrame) -> pd.DataFrame:
    columna_ingesta = "INGLIQ01"
    
    etiquetas_respuestas = {
        0: "Ninguno",
        1: "Entre 1 y 3",
        2: "Entre 4 y 8",
        3: "Entre 9 y 12",
        4: "Más de 12"
    }
    
    categoria_nombre = "Frecuencia de ingesta de bebidas azucaradas (vasos/semana)"
    
    orden_respuestas = [
        "Ninguno",
        "Entre 1 y 3",
        "Entre 4 y 8",
        "Entre 9 y 12",
        "Más de 12"
    ]

    if columna_ingesta not in df.columns:
        return pd.DataFrame(columns=['Categoria', 'Respuesta', 'Porcentaje'])
    
    conteo = df[columna_ingesta].value_counts(normalize=True) 
    
    resultados = []
    for respuesta_val, porcentaje in conteo.items():
        etiqueta_resp = etiquetas_respuestas.get(respuesta_val, respuesta_val) 
        
        resultados.append({
            "Categoria": categoria_nombre, 
            "Respuesta": etiqueta_resp, 
            "Porcentaje": porcentaje
        })
        
    df_resultado = pd.DataFrame(resultados)
    
    df_resultado_filtrado = df_resultado[df_resultado['Respuesta'].isin(orden_respuestas)].copy()
    
    df_resultado_filtrado["Respuesta"] = pd.Categorical(
        df_resultado_filtrado["Respuesta"],
        categories=orden_respuestas,
        ordered=True
    )
    
    df_resultado_final = df_resultado_filtrado.sort_values(
        by=['Categoria', 'Respuesta']
    ).reset_index(drop=True)
    
    return df_resultado_final

def tabaquismo(df):
    columna_tabaco = "DSM5[DSM21]"
    
    etiquetas_respuestas = {
        0: "Nada",
        1: "Muy poco",
        2: "Levemente",
        3: "Moderadamente",
        4: "Severamente"
    }
    
    categoria_nombre = "Frecuencia de F¿fumar cigarrillos, puros o pipas, o usar rapé (tabaco de ingesta nasal) o tabaco para mascar."
    
    orden_respuestas = [
        "Nada",
        "Muy poco",
        "Levemente",
        "Moderadamente",
        "Severamente"
    ]

    if columna_tabaco not in df.columns:
        return pd.DataFrame(columns=['Categoria', 'Respuesta', 'Porcentaje'])
    
    conteo = df[columna_tabaco].value_counts(normalize=True) 
    
    resultados = []
    for respuesta_val, porcentaje in conteo.items():
        etiqueta_resp = etiquetas_respuestas.get(respuesta_val, respuesta_val) 
        
        resultados.append({
            "Categoria": categoria_nombre, 
            "Respuesta": etiqueta_resp, 
            "Porcentaje": porcentaje
        })
        
    df_resultado = pd.DataFrame(resultados)
    
    df_resultado_filtrado = df_resultado[df_resultado['Respuesta'].isin(orden_respuestas)].copy()
    
    df_resultado_filtrado["Respuesta"] = pd.Categorical(
        df_resultado_filtrado["Respuesta"],
        categories=orden_respuestas,
        ordered=True
    )
    
    df_resultado_final = df_resultado_filtrado.sort_values(
        by=['Categoria', 'Respuesta']
    ).reset_index(drop=True)
    
    return df_resultado_final

def nivel_bienestar(df, group_cols=None, espacio=1):
    # 🔹 Ítems PERMA que deben incluirse en el promedio por persona
    indices_incluir = {1, 2, 3, 4, 5, 7, 8, 9, 10, 13, 14, 15, 16, 18, 19, 20}
    
    # Todas las columnas PERMA posibles
    todas_columnas_perma = [f"PERMA1[PER{i:02d}]" for i in range(1, 21)] + ["PERMA21", "PERMA22", "PERMA23"]

    # Solo las columnas que se deben usar para el promedio individual
    columnas_a_promediar = [
        col for i, col in enumerate(todas_columnas_perma, start=1)
        if i in indices_incluir and col in df.columns
    ]

    if not columnas_a_promediar:
        return pd.DataFrame(columns=["Categoria", "Serie", "Valor"])

    df_temp = df.copy()

    # 🔹 Solo personas con todas las columnas PERMA respondidas (todas las 23)
    df_validos = df_temp.dropna(subset=todas_columnas_perma).copy()

    # 🔹 Calcular el promedio individual con las columnas seleccionadas
    df_validos["Nivel Bienestar"] = df_validos[columnas_a_promediar].mean(axis=1)

    resultados = []

    if not group_cols:
        promedio_global = df_validos["Nivel Bienestar"].mean()
        resultados.append({
            "Categoria": "Global",
            "Serie": "Nivel Bienestar (Promedio)",
            "Valor": promedio_global if pd.notna(promedio_global) else None
        })
    else:
        segmentacion_existente = [col for col in group_cols if col in df.columns]
        for col_segmento in segmentacion_existente:
            for valor_segmento, df_seg in df_validos.groupby(col_segmento):
                prom_seg = df_seg["Nivel Bienestar"].mean()
                resultados.append({
                    "Categoria": valor_segmento,
                    "Serie": "Nivel Bienestar (Promedio)",
                    "Valor": prom_seg if pd.notna(prom_seg) else None
                })

            # Espaciado visual
            if espacio > 0:
                for i in range(espacio):
                    resultados.append({
                        "Categoria": f"_spacer_{col_segmento}_{i}",
                        "Serie": "Nivel Bienestar (Promedio)",
                        "Valor": None
                    })

    return pd.DataFrame(resultados)


def salud_mental_2022(df):
    if isinstance(df, str):
        df = pd.read_csv(StringIO(df), sep='\t', skipinitialspace=True)
    else:
        df = df.copy()

    df.rename(columns={df.columns[0]: 'Segmento'}, inplace=True)
    
    df.set_index('Segmento', inplace=True)

    porcentaje_cols = [col for col in df.columns if '%' in col]
    for col in porcentaje_cols:
        df[col] = df[col].astype(str).str.replace(' - ', 'nan', regex=False) \
                         .str.replace('%', '', regex=False) \
                         .str.strip()
        df[col] = pd.to_numeric(df[col], errors='coerce') / 100.0 

    otras_cols = [col for col in df.columns if col not in porcentaje_cols]
    for col in otras_cols:
         df[col] = df[col].astype(str).str.replace(' - ', 'nan', regex=False) \
                          .str.strip()
         df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df

def bienestar_2022(df):
    
    if isinstance(df, str):
        df = pd.read_csv(StringIO(df), sep='\t', skipinitialspace=True)
    else:
        df = df.copy()
    df.rename(columns={df.columns[0]: 'Segmento'}, inplace=True)    
    df['Segmento'] = df['Segmento'].astype(str).str.strip()
    df.set_index('Segmento', inplace=True)
    for col in df.columns:
        df[col] = df[col].astype(str).str.replace(' - ', 'nan', regex=False) \
                         .str.strip()
        df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

def perma_2022_2025(df_2022, df_2025):
    PERMA_FACTORS = {
        "P": [4, 9, 19],  # Positive emotions (P)
        "E": [3, 10, 18], # Engagement (E)
        "R": [5, 13, 16], # Positive relationship (R)
        "M": [1, 8, 15],  # Meaning (M)
        "A": [2, 7, 14],  # Accomplishment (A)
    }
    
    resultados = []

    # --- 1. PROCESAR DATOS 2022 ---
    df_2022_proc = bienestar_2022(df_2022)
    
    # Extraer los datos globales de 2022
    if 'Global' in df_2022_proc.index:
        serie_2022 = df_2022_proc.loc['Global']
        for factor in PERMA_FACTORS.keys():
            if factor in serie_2022:
                promedio_2022 = serie_2022[factor]
                valor_normalizado = promedio_2022
                resultados.append({
                    "Categoria": factor,
                    "Serie": "2022",
                    "Valor": valor_normalizado
                })

    # --- 2. PROCESAR DATOS 2025 ---
    
    perma_cols = [f"PERMA1[PER{i:02d}]" for i in range(1, 21)] + ["PERMA21", "PERMA22", "PERMA23"]
    perma_cols = [c for c in perma_cols if c in df_2025.columns]

    df_2025_temp = df_2025.dropna(subset=perma_cols).copy()
    
    for factor, indices in PERMA_FACTORS.items():
        # Construir nombres de columnas PERMA para 2025
        cols_perma_2025 = []
        for i in indices:
            if i <= 20:
                col_name = f"PERMA1[PER{i:02d}]"
            else:
                col_name = f"PERMA{i}" # (Asumiendo que PERMA21, PERMA22, PERMA23)
            
            if col_name in df_2025_temp.columns:
                cols_perma_2025.append(col_name)
        if cols_perma_2025:
            # Calcular el promedio de las columnas del factor para 2025
            # .mean(skipna=True) en el df_validos ya excluye filas con NaN en PERMA
            promedio_2025_factor = df_2025_temp[cols_perma_2025].mean().mean()

            if pd.notna(promedio_2025_factor):
                valor_normalizado = promedio_2025_factor
                resultados.append({
                    "Categoria": factor,
                    "Serie": "2025",
                    "Valor": valor_normalizado
                })

    # 3. CONSOLIDAR Y RETORNAR
    df_resultado = pd.DataFrame(resultados)
    
    # Ordenar por Categoria (P, E, R, M, A) y luego por Serie (2022, 2025)
    orden_categorias = list(PERMA_FACTORS.keys())
    df_resultado["Categoria"] = pd.Categorical(df_resultado["Categoria"], categories=orden_categorias, ordered=True)
    df_resultado = df_resultado.sort_values(by=["Categoria", "Serie"]).reset_index(drop=True)
    
    return df_resultado

def nhl_2022_2025(df_2022, df_2025):
    NHL_FACTORS = {
        "N": [6, 12, 17],
        "H": [21, 22, 23],
        "Lon": [11]
    }
    
    resultados = []

    df_2022_proc = bienestar_2022(df_2022)
    if 'Global' in df_2022_proc.index:
        serie_2022 = df_2022_proc.loc['Global']
        columnas_2022_map = {"N": "N", "H": "H", "Lon": "L"} 
        for factor_key, col_2022 in columnas_2022_map.items():
            if col_2022 in serie_2022:
                promedio_2022 = serie_2022[col_2022]
                valor_normalizado = promedio_2022
                resultados.append({
                    "Categoria": factor_key,
                    "Serie": "2022",
                    "Valor": valor_normalizado
                })
    perma_cols = [f"PERMA1[PER{i:02d}]" for i in range(1, 21)] + ["PERMA21", "PERMA22", "PERMA23"]
    perma_cols = [c for c in perma_cols if c in df_2025.columns]

    df_2025_temp = df_2025.dropna(subset=perma_cols).copy()
    for factor, indices in NHL_FACTORS.items():
        cols_nhl_2025 = []
        for i in indices:
            if i <= 20:
                col_name = f"PERMA1[PER{i:02d}]"
            else:
                col_name = f"PERMA{i}"
            if col_name in df_2025_temp.columns:
                cols_nhl_2025.append(col_name)
        if cols_nhl_2025:
            promedio_2025_factor = df_2025_temp[cols_nhl_2025].mean().mean()
            if pd.notna(promedio_2025_factor):
                valor_normalizado = promedio_2025_factor
                resultados.append({
                    "Categoria": factor,
                    "Serie": "2025",
                    "Valor": valor_normalizado
                })
    df_resultado = pd.DataFrame(resultados)
    orden_categorias = list(NHL_FACTORS.keys())
    df_resultado["Categoria"] = pd.Categorical(df_resultado["Categoria"], categories=orden_categorias, ordered=True)
    df_resultado = df_resultado.sort_values(by=["Categoria", "Serie"]).reset_index(drop=True)
    
    return df_resultado

def porcentaje_grupo_amarillo_por_condicion(df, filtro=None):
    dsm_cols = [f"DSM5[DSM{str(i).zfill(2)}]" for i in range(1, 23)] + ["ED15[ED01]", "ED15[ED02]"]
    df_valid = df[df[dsm_cols].notna().all(axis=1)].copy()

    mask_green_depresion = df_valid.apply(lambda row: (
        (row["DSM5[DSM01]"] < 2) and
        (row["DSM5[DSM02]"] < 2)
    ), axis=1)
    mask_green_ansiedad = df_valid.apply(lambda row: (
        (row["DSM5[DSM06]"] < 2) and
        (row["DSM5[DSM07]"] < 2) and
        (row["DSM5[DSM08]"] < 2)
    ), axis=1)
    mask_green_personalidad = df_valid.apply(lambda row: (
        (row["DSM5[DSM18]"] < 2) and
        (row["DSM5[DSM19]"] < 2)
    ), axis=1)
    mask_green_alcohol = df_valid.apply(lambda row: (row["DSM5[DSM20]"] < 1), axis=1)
    mask_green_marihuana = df_valid.apply(lambda row: (row["DSM5[DSM22]"] < 1), axis=1)
    mask_green_otros = df_valid.apply(lambda row: (
        (row["DSM5[DSM03]"] < 2) and
        (row["DSM5[DSM04]"] < 2) and
        (row["DSM5[DSM05]"] < 2) and
        (row["DSM5[DSM09]"] < 2) and
        (row["DSM5[DSM10]"] < 2) and
        (row["DSM5[DSM11]"] < 1) and
        (row["DSM5[DSM12]"] < 1) and
        (row["DSM5[DSM13]"] < 2) and
        (row["DSM5[DSM14]"] < 2) and
        (row["DSM5[DSM15]"] < 2) and
        (row["DSM5[DSM16]"] < 2) and
        (row["DSM5[DSM17]"] < 2) and
        (row["DSM5[DSM21]"] < 1) and
        (row["ED15[ED01]"] < 2) and
        (row["ED15[ED02]"] < 2)
    ), axis=1)

    phq_cols = [f"PHQ8[PHQ0{i}]" for i in range(1, 9)]
    gad_cols = [f"GAD7[GAD0{i}]" for i in range(1, 8)]
    lpf_cols = [f"LPFS[LPFS{str(i).zfill(2)}]" for i in range(1, 13)]
    marihuana_cols = [f"CAST[CAST0{i}]" for i in range(1, 7)]
    audit_cols = ["AUDIT01[AUDIT01]", "AUDIT02[AUDIT02]"] + \
                 [f"AUDIT38[AUDIT0{i}]" for i in range(3, 9)] + \
                 [f"AUDIT910[AUDIT{str(i).zfill(2)}]" for i in range(9, 11)]

    df_depresion = df_valid[~mask_green_depresion].copy()
    df_ansiedad = df_valid[~mask_green_ansiedad].copy()
    df_personalidad = df_valid[~mask_green_personalidad].copy()
    df_alcohol = df_valid[~mask_green_alcohol].copy()
    df_marihuana = df_valid[~mask_green_marihuana].copy()
    df_otros = df_valid[~mask_green_otros].copy()

    total = len(df_valid)
    if total == 0:
        return pd.DataFrame(columns=["Condición", "Serie", "Valor"])

    condiciones = {
        "Uso problemático marihuana": (df_marihuana[marihuana_cols].sum(axis=1) < 4),
        "Uso problemático alcohol": (df_alcohol[audit_cols].sum(axis=1) < 16),
        "Trastornos de personalidad": (df_personalidad[lpf_cols].sum(axis=1) < 27),
        "Ansiedad": (df_ansiedad[gad_cols].sum(axis=1) < 10),
        "Depresión": (df_depresion[phq_cols].sum(axis=1) < 10),
    }

    resultados = [{"Condición": "Malestar en áreas no profundizadas", "Sede": len(df_otros) / total}]
    for nombre, mask in condiciones.items():
        porcentaje = mask.sum() / total
        resultados.append({"Condición": nombre, "Sede": porcentaje})

    df_resultado = pd.DataFrame(resultados)

    if filtro != "Global":
        hardcoded = {
            "Depresión": 0.29,
            "Ansiedad": 0.44,
            "Trastornos de personalidad": 0.47,
            "Uso problemático alcohol": 0.28,
            "Uso problemático marihuana": 0.13,
            "Malestar en áreas no profundizadas": 0.96
        }

        df_resultado["Duoc UC"] = df_resultado["Condición"].map(hardcoded)

        # 🔹 Convertir a formato largo para el gráfico
        df_resultado = df_resultado.melt(
            id_vars=["Condición"],
            value_vars=["Sede", "Duoc UC"],
            var_name="Serie",
            value_name="Valor"
        )

    else:
        # 🔹 Si es global, mantener estructura simple
        df_resultado = df_resultado.rename(columns={"Sede": "Valor"})
        df_resultado["Serie"] = "Sede"

    return df_resultado

def porcentaje_respuestas_appvivo(df, columnas, labels_dict=LABELS_APPVI02, col_appvi01="APPVI01"):
    resultados = []
    total_yes = (df[col_appvi01] == "Y").sum()
    
    for col in columnas:
        if col in df.columns:
            count = (df[col] == "Y").sum()
            pct = count / total_yes
        else:
            pct = 0.0
        
        label = labels_dict.get(col, col) if labels_dict else col
        resultados.append({
            "CategoriaLabel": label,
            "Porcentaje": pct,
            "Variable": "Sí"
        })
    
    df_resultado = pd.DataFrame(resultados)
    df_resultado["Porcentaje"] = df_resultado["Porcentaje"]
    return df_resultado.rename(columns={"Variable": "Categoria"})

def embajador_salud_mental3(df) -> pd.DataFrame:
    columna_ingesta = "EMB07[EMBSM07]"
    
    etiquetas_respuestas = {
        0: "0",
        1: "Entre 1 y 3",
        2: "Entre 4 y 6",
        3: "Entre 7 y 9",
        4: "10 o más"
    }
    
    categoria_nombre = ""
    
    orden_respuestas = [
        "0",
        "Entre 1 y 3",
        "Entre 4 y 6",
        "Entre 7 y 9",
        "10 o más"
    ]

    if columna_ingesta not in df.columns:
        return pd.DataFrame(columns=['Categoria', 'Respuesta', 'Porcentaje'])
    
    conteo = df[columna_ingesta].value_counts(normalize=True) 
    
    resultados = []
    for respuesta_val, porcentaje in conteo.items():
        etiqueta_resp = etiquetas_respuestas.get(respuesta_val, respuesta_val) 
        
        resultados.append({
            "Categoria": categoria_nombre, 
            "Respuesta": etiqueta_resp, 
            "Porcentaje": porcentaje
        })
        
    df_resultado = pd.DataFrame(resultados)
    
    df_resultado_filtrado = df_resultado[df_resultado['Respuesta'].isin(orden_respuestas)].copy()
    
    df_resultado_filtrado["Respuesta"] = pd.Categorical(
        df_resultado_filtrado["Respuesta"],
        categories=orden_respuestas,
        ordered=True
    )
    
    df_resultado_final = df_resultado_filtrado.sort_values(
        by=['Categoria', 'Respuesta']
    ).reset_index(drop=True)
    
    return df_resultado_final

def embajador_salud_mental4(df) -> pd.DataFrame:
    columna_ingesta = "EMB08[EMBSM08]"
    
    etiquetas_respuestas = {
        1: "Muy insatisfecho/a",
        2: "Insatisfecho/a",
        3: "Neutro",
        4: "Satisfecho/a",
        5: "Muy satisfecho/a"
    }
    
    categoria_nombre = ""
    
    orden_respuestas = [
        "Muy insatisfecho/a",
        "Insatisfecho/a",
        "Neutro",
        "Satisfecho/a",
        "Muy satisfecho/a"
    ]

    if columna_ingesta not in df.columns:
        return pd.DataFrame(columns=['Categoria', 'Respuesta', 'Porcentaje'])
    
    conteo = df[columna_ingesta].value_counts(normalize=True) 
    
    resultados = []
    for respuesta_val, porcentaje in conteo.items():
        etiqueta_resp = etiquetas_respuestas.get(respuesta_val, respuesta_val) 
        
        resultados.append({
            "Categoria": categoria_nombre, 
            "Respuesta": etiqueta_resp, 
            "Porcentaje": porcentaje
        })
        
    df_resultado = pd.DataFrame(resultados)
    
    df_resultado_filtrado = df_resultado[df_resultado['Respuesta'].isin(orden_respuestas)].copy()
    
    df_resultado_filtrado["Respuesta"] = pd.Categorical(
        df_resultado_filtrado["Respuesta"],
        categories=orden_respuestas,
        ordered=True
    )
    
    df_resultado_final = df_resultado_filtrado.sort_values(
        by=['Categoria', 'Respuesta']
    ).reset_index(drop=True)
    
    return df_resultado_final

def embajador_salud_mental7(df) -> pd.DataFrame:
    columna_ingesta = "EMB04"
    etiquetas_respuestas = {
        1: "Poco tiempo",
        2: "Falta información",
        3: "No es importante",
        4: "Es para profesionales",
        5: "No creo ser bueno/a",
        6: "Otra razón"
    }
    
    categoria_nombre = ""
    
    orden_respuestas = [
        "Poco tiempo",
        "No creo ser bueno/a",
        "Es para profesionales",
        "No es importante",
        "Falta información",
        "Otra razón"
    ]

    if columna_ingesta not in df.columns:
        return pd.DataFrame(columns=['Categoria', 'Respuesta', 'Porcentaje'])
    
    conteo = df[columna_ingesta].value_counts(normalize=True) 
    
    resultados = []
    for respuesta_val, porcentaje in conteo.items():
        etiqueta_resp = etiquetas_respuestas.get(respuesta_val, respuesta_val) 
        
        resultados.append({
            "Categoria": categoria_nombre, 
            "Respuesta": etiqueta_resp, 
            "Porcentaje": porcentaje
        })
        
    df_resultado = pd.DataFrame(resultados)
    
    df_resultado_filtrado = df_resultado[df_resultado['Respuesta'].isin(orden_respuestas)].copy()
    
    df_resultado_filtrado["Respuesta"] = pd.Categorical(
        df_resultado_filtrado["Respuesta"],
        categories=orden_respuestas,
        ordered=True
    )
    
    df_resultado_final = df_resultado_filtrado.sort_values(
        by=['Categoria', 'Respuesta']
    ).reset_index(drop=True)
    
    return df_resultado_final

def embajador_salud_mental9(df) -> pd.DataFrame:
    columna_ingesta = "EMB11"
    etiquetas_respuestas = {
        1: "Si",
        2: "No",
        3: "No lo recuerdo",
    }
    
    categoria_nombre = ""
    
    orden_respuestas = [
        "Si",
        "No",
        "No lo recuerdo",
    ]

    if columna_ingesta not in df.columns:
        return pd.DataFrame(columns=['Categoria', 'Respuesta', 'Porcentaje'])
    
    conteo = df[columna_ingesta].value_counts(normalize=True) 
    
    resultados = []
    for respuesta_val, porcentaje in conteo.items():
        etiqueta_resp = etiquetas_respuestas.get(respuesta_val, respuesta_val) 
        
        resultados.append({
            "Categoria": categoria_nombre, 
            "Respuesta": etiqueta_resp, 
            "Porcentaje": porcentaje
        })
        
    df_resultado = pd.DataFrame(resultados)
    
    df_resultado_filtrado = df_resultado[df_resultado['Respuesta'].isin(orden_respuestas)].copy()
    
    df_resultado_filtrado["Respuesta"] = pd.Categorical(
        df_resultado_filtrado["Respuesta"],
        categories=orden_respuestas,
        ordered=True
    )
    
    df_resultado_final = df_resultado_filtrado.sort_values(
        by=['Categoria', 'Respuesta']
    ).reset_index(drop=True)
    
    return df_resultado_final

def atencion_psicologica2(df) -> pd.DataFrame:
    columna_ingesta = "ATPSIC2[ATPSIC02]"
    etiquetas_respuestas = {
        1: "Muy insatisfecho/a",
        2: "Insatisfecho/a",
        3: "Neutro",
        4: "Satisfecho/a",
        5: "Muy satisfecho/a"
    }
    
    categoria_nombre = ""
    
    orden_respuestas = [
        "Muy insatisfecho/a",
        "Insatisfecho/a",
        "Neutro",
        "Satisfecho/a",
        "Muy satisfecho/a"
    ]


    if columna_ingesta not in df.columns:
        return pd.DataFrame(columns=['Categoria', 'Respuesta', 'Porcentaje'])
    
    conteo = df[columna_ingesta].value_counts(normalize=True) 
    
    resultados = []
    for respuesta_val, porcentaje in conteo.items():
        etiqueta_resp = etiquetas_respuestas.get(respuesta_val, respuesta_val) 
        
        resultados.append({
            "Categoria": categoria_nombre, 
            "Respuesta": etiqueta_resp, 
            "Porcentaje": porcentaje
        })
        
    df_resultado = pd.DataFrame(resultados)
    
    df_resultado_filtrado = df_resultado[df_resultado['Respuesta'].isin(orden_respuestas)].copy()
    
    df_resultado_filtrado["Respuesta"] = pd.Categorical(
        df_resultado_filtrado["Respuesta"],
        categories=orden_respuestas,
        ordered=True
    )
    
    df_resultado_final = df_resultado_filtrado.sort_values(
        by=['Categoria', 'Respuesta']
    ).reset_index(drop=True)
    
    return df_resultado_final

def atencion_psicologica5(df) -> pd.DataFrame:
    columna_ingesta = "BIM02[BIM02]"
    etiquetas_respuestas = {
        1: "Nada",
        2: "Poco",
        3: "Algo",
        4: "Bastante",
        5: "Mucho"
    }
    
    categoria_nombre = ""
    
    orden_respuestas = [
        "Nada",
        "Poco",
        "Algo",
        "Bastante",
        "Mucho"
    ]

    if columna_ingesta not in df.columns:
        return pd.DataFrame(columns=['Categoria', 'Respuesta', 'Porcentaje'])
    
    conteo = df[columna_ingesta].value_counts(normalize=True) 
    
    resultados = []
    for respuesta_val, porcentaje in conteo.items():
        etiqueta_resp = etiquetas_respuestas.get(respuesta_val, respuesta_val) 
        
        resultados.append({
            "Categoria": categoria_nombre, 
            "Respuesta": etiqueta_resp, 
            "Porcentaje": porcentaje
        })
        
    df_resultado = pd.DataFrame(resultados)
    
    df_resultado_filtrado = df_resultado[df_resultado['Respuesta'].isin(orden_respuestas)].copy()
    
    df_resultado_filtrado["Respuesta"] = pd.Categorical(
        df_resultado_filtrado["Respuesta"],
        categories=orden_respuestas,
        ordered=True
    )
    
    df_resultado_final = df_resultado_filtrado.sort_values(
        by=['Categoria', 'Respuesta']
    ).reset_index(drop=True)
    
    return df_resultado_final

def condicion_academica(df, columnas):
    etiquetas_condicion_resp = {
        1: "Muy en desacuerdo",
        2: "En desacuerdo",
        3: "De acuerdo",
        4: "Muy de acuerdo"
    }

    etiquetas_condicion_cat = {
        "CONDACAD[CON01]": "En mi casa, cuento con un espacio adecuado para estudiar o hacer mis trabajos",
        "CONDACAD[CON02]": "En Duoc UC, cuento con un espacio adecuado para estudiar o hacer mis trabajos",
        "CONDACAD[CON03]": "Necesito apoyo y/o capacitación para utilizar las plataformas o herramientas tecnológicas requeridas en mi carrera (softwares, plataforma estudiantil, programas, etc.)",
    }
    
    orden_respuestas = [
        "Muy en desacuerdo",
        "En desacuerdo",
        "De acuerdo",
        "Muy de acuerdo"
    ]
    
    if columnas is None:
        columnas_a_procesar = [
            col for col in df.columns 
            if col.startswith("CONDACAD[") and col in etiquetas_condicion_cat
        ]
    else:
        columnas_a_procesar = [
            col for col in columnas 
            if col in etiquetas_condicion_cat and col in df.columns
        ]
    
    if not columnas_a_procesar:
        return pd.DataFrame(columns=['Categoria', 'Respuesta', 'Porcentaje'])
    
    df_resultado = porcentaje_para_barras_apiladas(
        df,
        columnas=columnas_a_procesar,
        etiquetas_respuesta=etiquetas_condicion_resp,
        etiquetas_categoria=etiquetas_condicion_cat,
    )
    
    
    df_resultado_filtrado = df_resultado[df_resultado['Respuesta'].isin(orden_respuestas)].copy()
    
    df_resultado_filtrado["Respuesta"] = pd.Categorical(
        df_resultado_filtrado["Respuesta"],
        categories=orden_respuestas,
        ordered=True
    )
    
    df_resultado_final = df_resultado_filtrado.sort_values(
        by=['Categoria', 'Respuesta']
    ).reset_index(drop=True)
    
    return df_resultado_final

def porcentaje_seleccion_multiple_y(df, columnas, labels_dict=None, since=None):
    resultados = []
    columnas_existentes = [col for col in columnas if col in df.columns]
    total_yes_responders = df[columnas_existentes].eq("Y").any(axis=1).sum()

    if since == 1:
        columnas_existentes = columnas_existentes[0:5]
    else:
        columnas_existentes = columnas_existentes[5:]
    for col in columnas_existentes:
        count = (df[col] == "Y").sum()
        pct = (count / total_yes_responders) if total_yes_responders > 0 else 0.0
        label = labels_dict.get(col, col) if labels_dict else col
        resultados.append({
            "CategoriaLabel": label,
            "Porcentaje": pct,
            "Variable": "Sí"
        })

    df_resultado = pd.DataFrame(resultados)
    df_resultado["Porcentaje"] = df_resultado["Porcentaje"]
    return df_resultado