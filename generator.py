from data.datasets import (
    atencion_psicologica2, atencion_psicologica5, condicion_academica, embajador_salud_mental3, embajador_salud_mental4, embajador_salud_mental4, embajador_salud_mental7, flow_percibido, apoyo_percibido, barreras_acceso_tratamiento,
    ansiedad_manejo_clinico, cupit_marihuana, ideacion_suicida_barras,
    porcentaje_para_barras_apiladas, cantidad_total_dms5, porcentaje_seleccion_multiple_y,
    promedio_factor_carga_enfermedad_grupo_rojo, promedio_factor_carga_enfermedad_grupo_amarillo,
    marihuana_manejo_clinico,
    personalidad_manejo_clinico, porcentaje_afrontamiento, porcentaje_estresores_exigencia,
    porcentaje_por_categoria, casos_validos_pss,
    aplicar_regla_pss, porcentaje_procrastinacion, porcentaje_salud_cronica,
    promedio_por_categoria, porcentaje_estresores,
    top_estresores_2022, depresion_manejo_clinico, alcohol_manejo_clinico,
    ideacion_suicida_manejo_clinico, salud_mental_grupo_verde, salud_mental_grupo_rojo,
    alimentacion, ingesta_liquidos, tabaquismo, nivel_bienestar, flow_percibido_positivo,
    salud_mental_2022, bienestar_2022, perma_2022_2025, nhl_2022_2025,
    porcentaje_grupo_amarillo_por_condicion, porcentaje_respuestas_appvivo, embajador_salud_mental9
)
from plots.charts import crear_chart_data
from plots.wordclouds import crear_wordcloud
from plots.pptx_updater import actualizar_graficos
import pandas as pd

def generar_reporte(df_global, df_participantes, df_estres, df_estresores_2022, df_estresores, df_exigencia, df_afrontamiento, df_procrastinacion, df_salud_cronica, df_depresion,
                    df_ansiedad, df_personalidad, df_marihuana, df_alcohol, df_suicidio, df_grupo_verde, df_grupo_rojo, df_necesidad_tratamiento, df_barreras, df_apoyo,
                    df_flow_states, df_act_fisica, df_alimentacion, df_ing_liquidos, df_tabaquismo, df_perma, df_salud_mental_2022, df_bienestar_2022, df_app_vivo,
                    df_embajador, df_atencion_psicologica, df_personas_cuidado, df_situacion_empleo, df_condicion_academica, df_espacios_sedes, df_encuesta_2022, df_palabras_normalizadas_wordcloud, df_salud_mental_2022_tres_grupos, tipo, filtro, nivel):
    
    template_path = f"reports/templates/template-{tipo}.pptx"
    output_path = f"reports/output/reporte-{filtro}.pptx"

    df_valido = casos_validos_pss(df_estres)
    df_valido = aplicar_regla_pss(df_valido)
    nivel_estres_promedio_2025 = df_valido["pct_persona"].mean()

    df_depresion_malestar_clinico = depresion_manejo_clinico(df_depresion, None)
    df_depresion_genero = depresion_manejo_clinico(df_depresion, ["GENERO"])
    depresion_manejo_clinico_global = df_depresion_malestar_clinico["Valor"].iloc[0]
    depresion_femenino = df_depresion_genero[df_depresion_genero["Categoria"] == "Femenino"]["Valor"].iloc[0]

    df_ansiedad_malestar_clinico = ansiedad_manejo_clinico(df_ansiedad, None)
    df_ansiedad_genero = ansiedad_manejo_clinico(df_ansiedad, ["GENERO"])
    ansiedad_manejo_clinico_global = df_ansiedad_malestar_clinico["Valor"].iloc[0]
    ansiedad_femenino = df_ansiedad_genero[df_ansiedad_genero["Categoria"] == "Femenino"]["Valor"].iloc[0]

    df_personalidad_malestar_clinico = personalidad_manejo_clinico(df_personalidad, None)
    df_personalidad_genero = personalidad_manejo_clinico(df_personalidad, ["GENERO"])
    personalidad_manejo_clinico_global = df_personalidad_malestar_clinico["Valor"].iloc[0]
    personalidad_femenino = df_personalidad_genero[df_personalidad_genero["Categoria"] == "Femenino"]["Valor"].iloc[0]

    df_marihuana_malestar_clinico = marihuana_manejo_clinico(df_marihuana, None)
    df_marihuana_genero = marihuana_manejo_clinico(df_marihuana, ["GENERO"])
    marihuana_manejo_clinico_global = df_marihuana_malestar_clinico["Valor"].iloc[0]
    marihuana_femenino = df_marihuana_genero[df_marihuana_genero["Categoria"] == "Femenino"]["Valor"].iloc[0]

    df_alcohol_manejo_clinico = alcohol_manejo_clinico(df_alcohol, None)
    df_alcohol_genero = alcohol_manejo_clinico(df_alcohol, ["GENERO"])
    alcohol_manejo_clinico_global = df_alcohol_manejo_clinico["Valor"].iloc[0]
    alcohol_femenino = df_alcohol_genero[df_alcohol_genero["Categoria"] == "Femenino"]["Valor"].iloc[0]

    df_ideacion_suicida_manejo_clinico = ideacion_suicida_manejo_clinico(df_suicidio, None)
    df_suicidio_genero = ideacion_suicida_manejo_clinico(df_suicidio, ["GENERO"])
    ideacion_suicida_manejo_clinico_global = df_ideacion_suicida_manejo_clinico["Valor"].iloc[0]
    suicidio_femenino = df_suicidio_genero[df_suicidio_genero["Categoria"] == "Femenino"]["Valor"].iloc[0]

    df_nivel_bienestar = nivel_bienestar(df_perma, None)
    nivel_bienestar_global = df_nivel_bienestar["Valor"].iloc[0]

    total_dms5 = cantidad_total_dms5(df_global)
    grupo_verde = round((salud_mental_grupo_verde(df_grupo_verde) / total_dms5), 2) * 100
    grupo_rojo = round((salud_mental_grupo_rojo(df_grupo_rojo) / total_dms5), 2) * 100
    grupo_amarillo = 100 - grupo_verde - grupo_rojo

    info_salud_mental_2022_grupos = salud_mental_2022(df_salud_mental_2022_tres_grupos)
    grupo_verde_2022 = info_salud_mental_2022_grupos.loc['Global', 'Promoción']
    grupo_amarillo_2022 = info_salud_mental_2022_grupos.loc['Global', 'Prevención indicada']
    grupo_rojo_2022 = info_salud_mental_2022_grupos.loc['Global', 'Manejo clínico']

    factor_carga_enfermedad_rojo = promedio_factor_carga_enfermedad_grupo_rojo(df_global)
    factor_carga_enfermedad_amarillo = promedio_factor_carga_enfermedad_grupo_amarillo(df_global)
    info_salud_mental_2022 = salud_mental_2022(df_salud_mental_2022)
    factor_carga_enfermedad_rojo_2022 = info_salud_mental_2022.loc['Global', 'Factor carga de enfermedad - Manejo clínico']
    factor_carga_enfermedad_amarillo_2022 = info_salud_mental_2022.loc['Global', 'Factor carga de enfermedad - Prevención']
    
    depresion_2022 = info_salud_mental_2022.loc['Global', 'depresion_manejo_clinico']
    ansiedad_2022 = info_salud_mental_2022.loc['Global', 'ansiedad_manejo_clinico']
    personalidad_2022 = info_salud_mental_2022.loc['Global', 'personalidad_manejo_clinico']
    marihuana_2022 = info_salud_mental_2022.loc['Global', 'marihuana_manejo_clinico']
    alcohol_2022 = info_salud_mental_2022.loc['Global', 'alcohol_manejo_clinico']
    suicidio_2022 = info_salud_mental_2022.loc['Global', 'suicidio_manejo_clinico']

    cupit_marihuana_porcentaje = cupit_marihuana(df_global)

    cantidad_salfis1 = df_salud_cronica['SALFIS01'].count()
    
    exig_columns = [col for col in df_exigencia.columns if col.startswith('EXIG[')]
    cantidad_exigencia = df_exigencia[exig_columns].notna().any(axis=1).sum()  
    
    flow_positivo = flow_percibido_positivo(df_flow_states)

    info_bienestar_2022 = bienestar_2022(df_bienestar_2022)
    bienestar_global_2022 = info_bienestar_2022.loc["Global", "PERMA COMPLETO"]

    # filtrar registros cuyo startdate sea posterior al 1 de octubre de 2025 a las 10:30
    df_app_vivo_filterdate = df_app_vivo.copy()
    df_app_vivo_filterdate['startdate'] = pd.to_datetime(df_app_vivo_filterdate['startdate'], errors='coerce')
    df_app_vivo_filterdate = df_app_vivo_filterdate.dropna(subset=['startdate'])
    cutoff = pd.Timestamp('2025-10-01 10:30')
    df_app_vivo_filterdate = df_app_vivo_filterdate[df_app_vivo_filterdate['startdate'] >= cutoff]
    respuestas_appvivo = df_app_vivo_filterdate["APPVI01"].notna().sum()

    respuestas_embajador1 = df_embajador[df_embajador["EMB01"].notna()]["EMB01"].count()
    respuestas_embajador2 = df_embajador[df_embajador["EMB06[EMBSM06]"].notna()]["EMB06[EMBSM06]"].count()
    respuestas_embajador3 = df_embajador[df_embajador["EMB01"] == "Y"]["EMB06[EMBSM06]"].count()
    respuestas_embajador4 = df_embajador[df_embajador["EMB03"].notna()]["EMB03"].count()
    respuestas_embajador5 = df_embajador[df_embajador["EMB04"].notna()]["EMB04"].count()
    respuestas_embajador6 = df_embajador[df_embajador["EMB10"].notna()]["EMB10"].count()
    respuestas_embajador7 = df_embajador[df_embajador["EMB10"] == "Y"]["EMB11"].count()

    respuestas_atencion_psiscologica1 = df_atencion_psicologica[df_atencion_psicologica["ATPSIC01"].notna()]["ATPSIC01"].count()

    respuestas_bienestar_integral = df_atencion_psicologica[df_atencion_psicologica["BIM01"].notna()]["BIM01"].count()

    respuestas_personas_cuidado1 = df_personas_cuidado[df_personas_cuidado["CUIDA01"].notna()]["CUIDA01"].count()
    respuestas_personas_cuidado2 = df_personas_cuidado[df_personas_cuidado["CUIDA02"].notna()]["CUIDA02"].count()

    respuestas_empleo = df_situacion_empleo[df_situacion_empleo["EMPLE01"].notna()]["EMPLE01"].count()

    columnas = ["CONDACAD[CON01]", "CONDACAD[CON02]", "CONDACAD[CON03]"]
    respuestas_condicion_academica = df_condicion_academica[columnas].notna().any(axis=1).sum()

    columnas_descom = [f"DESCOM01[{i}]" for i in range(1, 12)]
    respuestas_espacios_sedes = df_espacios_sedes[columnas_descom].notna().any(axis=1).sum()

    df_valido_global = df_valido.copy()
    df_depresion_global = df_depresion.copy()
    df_ansiedad_global = df_ansiedad.copy()
    df_personalidad_global = df_personalidad.copy()
    df_marihuana_global = df_marihuana.copy()
    df_alcohol_global = df_alcohol.copy()
    df_suicidio_global = df_suicidio.copy()
    df_perma_global = df_perma.copy()

    titulo = ""

    if nivel:
        if nivel == 1:
            titulo = "Sede"
        elif nivel == 2:
            titulo = "Escuela"
        df_participantes = df_participantes[df_participantes[tipo] == filtro]
        df_valido = df_valido[df_valido[tipo] == filtro]
        df_global = df_global[df_global[tipo] == filtro]
        
        nivel_estres_promedio_2025 = df_valido["pct_persona"].mean()
        df_estresores = df_estresores[df_estresores[tipo] == filtro]
        
        df_exigencia = df_exigencia[df_exigencia[tipo] == filtro]
        cantidad_exigencia = df_exigencia[exig_columns].notna().any(axis=1).sum() 
        
        df_afrontamiento = df_afrontamiento[df_afrontamiento[tipo] == filtro]
        df_procrastinacion = df_procrastinacion[df_procrastinacion[tipo] == filtro]
        
        df_salud_cronica = df_salud_cronica[df_salud_cronica[tipo] == filtro]
        cantidad_salfis1 = df_salud_cronica['SALFIS01'].count()

        grupo_verde_2022 = info_salud_mental_2022_grupos.loc[filtro, 'Promoción']
        grupo_amarillo_2022 = info_salud_mental_2022_grupos.loc[filtro, 'Prevención indicada']
        grupo_rojo_2022 = info_salud_mental_2022_grupos.loc[filtro, 'Manejo clínico']

        factor_carga_enfermedad_rojo = promedio_factor_carga_enfermedad_grupo_rojo(df_global)
        factor_carga_enfermedad_amarillo = promedio_factor_carga_enfermedad_grupo_amarillo(df_global)
        factor_carga_enfermedad_rojo_2022 = info_salud_mental_2022.loc[filtro, 'Factor carga de enfermedad - Manejo clínico']
        factor_carga_enfermedad_amarillo_2022 = info_salud_mental_2022.loc[filtro, 'Factor carga de enfermedad - Prevención']

        df_depresion = df_depresion[df_depresion[tipo] == filtro]
        df_depresion_malestar_clinico = depresion_manejo_clinico(df_depresion, None)
        depresion_manejo_clinico_global = df_depresion_malestar_clinico["Valor"].iloc[0]

        df_ansiedad = df_ansiedad[df_ansiedad[tipo] == filtro]
        df_ansiedad_malestar_clinico = ansiedad_manejo_clinico(df_ansiedad, None)
        ansiedad_manejo_clinico_global = df_ansiedad_malestar_clinico["Valor"].iloc[0]

        df_personalidad = df_personalidad[df_personalidad[tipo] == filtro]
        df_personalidad_malestar_clinico = personalidad_manejo_clinico(df_personalidad, None)
        personalidad_manejo_clinico_global = df_personalidad_malestar_clinico["Valor"].iloc[0]

        df_marihuana = df_marihuana[df_marihuana[tipo] == filtro]
        df_marihuana_malestar_clinico = marihuana_manejo_clinico(df_marihuana, None)
        marihuana_manejo_clinico_global = df_marihuana_malestar_clinico["Valor"].iloc[0]

        cupit_marihuana_porcentaje = cupit_marihuana(df_global)

        df_alcohol = df_alcohol[df_alcohol[tipo] == filtro]
        df_alcohol_manejo_clinico = alcohol_manejo_clinico(df_alcohol, None)
        alcohol_manejo_clinico_global = df_alcohol_manejo_clinico["Valor"].iloc[0]

        df_suicidio = df_suicidio[df_suicidio[tipo] == filtro]
        respuestas_suicidio = len(df_suicidio)
        df_ideacion_suicida_manejo_clinico = ideacion_suicida_manejo_clinico(df_suicidio, None)
        ideacion_suicida_manejo_clinico_global = df_ideacion_suicida_manejo_clinico["Valor"].iloc[0]

        df_necesidad_tratamiento = df_necesidad_tratamiento[df_necesidad_tratamiento[tipo] == filtro]

        df_barreras = df_barreras[df_barreras[tipo] == filtro]

        df_perma = df_perma[df_perma[tipo] == filtro]
        df_nivel_bienestar = nivel_bienestar(df_perma, None)
        nivel_bienestar_global = df_nivel_bienestar["Valor"].iloc[0]
        info_bienestar_2022 = bienestar_2022(df_bienestar_2022)
        bienestar_global_2022 = info_bienestar_2022.loc[filtro, "PERMA COMPLETO"]

        df_apoyo = df_apoyo[df_apoyo[tipo] == filtro]
        df_flow_states = df_flow_states[df_flow_states[tipo] == filtro]
        flow_positivo = flow_percibido_positivo(df_flow_states)

        df_act_fisica = df_act_fisica[df_act_fisica[tipo] == filtro]

        df_alimentacion = df_alimentacion[df_alimentacion[tipo] == filtro]

        df_ing_liquidos = df_ing_liquidos[df_ing_liquidos[tipo] == filtro]

        df_tabaquismo = df_tabaquismo[df_tabaquismo[tipo] == filtro]

        df_app_vivo_filterdate = df_app_vivo_filterdate[df_app_vivo_filterdate[tipo] == filtro]
        respuestas_appvivo = df_app_vivo_filterdate["APPVI01"].notna().sum()

        df_embajador = df_embajador[df_embajador[tipo] == filtro]
        respuestas_embajador1 = df_embajador[df_embajador["EMB01"].notna()]["EMB01"].count()
        respuestas_embajador2 = df_embajador[df_embajador["EMB06[EMBSM06]"].notna()]["EMB06[EMBSM06]"].count()
        respuestas_embajador3 = df_embajador[df_embajador["EMB01"] == "Y"]["EMB06[EMBSM06]"].count()
        respuestas_embajador4 = df_embajador[df_embajador["EMB03"].notna()]["EMB03"].count()
        respuestas_embajador5 = df_embajador[df_embajador["EMB04"].notna()]["EMB04"].count()
        respuestas_embajador6 = df_embajador[df_embajador["EMB10"].notna()]["EMB10"].count()
        respuestas_embajador7 = df_embajador[df_embajador["EMB10"] == "Y"]["EMB11"].count()

        df_atencion_psicologica = df_atencion_psicologica[df_atencion_psicologica[tipo] == filtro]
        respuestas_atencion_psiscologica1 = df_atencion_psicologica[df_atencion_psicologica["ATPSIC01"].notna()]["ATPSIC01"].count()
        respuestas_bienestar_integral = df_atencion_psicologica[df_atencion_psicologica["BIM01"].notna()]["BIM01"].count()

        df_personas_cuidado = df_personas_cuidado[df_personas_cuidado[tipo] == filtro]
        respuestas_personas_cuidado1 = df_personas_cuidado[df_personas_cuidado["CUIDA01"].notna()]["CUIDA01"].count()
        respuestas_personas_cuidado2 = df_personas_cuidado[df_personas_cuidado["CUIDA02"].notna()]["CUIDA02"].count()

        df_situacion_empleo = df_situacion_empleo[df_situacion_empleo[tipo] == filtro]
        respuestas_empleo = df_situacion_empleo[df_situacion_empleo["EMPLE01"].notna()]["EMPLE01"].count()

        df_condicion_academica = df_condicion_academica[df_condicion_academica[tipo] == filtro]
        respuestas_condicion_academica = df_condicion_academica[columnas].notna().any(axis=1).sum()

        df_espacios_sedes = df_espacios_sedes[df_espacios_sedes[tipo] == filtro]
        respuestas_espacios_sedes = df_espacios_sedes[columnas_descom].notna().any(axis=1).sum()

        df_grupo_verde = df_grupo_verde[df_grupo_verde[tipo] == filtro]
        df_grupo_rojo = df_grupo_rojo[df_grupo_rojo[tipo] == filtro]
        total_dms5 = cantidad_total_dms5(df_global)
        grupo_verde = round((salud_mental_grupo_verde(df_grupo_verde) / total_dms5), 2) * 100
        grupo_rojo = round((salud_mental_grupo_rojo(df_grupo_rojo) / total_dms5), 2) * 100
        grupo_amarillo = 100 - grupo_verde - grupo_rojo

    columnas_estresores = [
      "ESTRE[ESTRE01]", "ESTRE[ESTRE02]", "ESTRE[ESTRE03]", "ESTRE[ESTRE04]", "ESTRE[ESTRE05]",
      "ESTRE[ESTRE06]", "ESTRE[ESTRE07]", "ESTRE[ESTRE08]", "ESTRE[ESTRE09]", "ESTRE[ESTRE10]",
      "ESTRE[ESTRE11]", "ESTRE[ESTRE12]", "ESTRE[ESTRE13]", "ESTRE[ESTRE14]", "ESTRE[ESTRE15]",
      "ESTRE[ESTRE16]", "ESTRE[ESTRE17]", "ESTRE[ESTRE18]", "ESTRE[ESTRE19]", "ESTRE[ESTRE20]",
      "ESTRE[ESTRE21]", "ESTRE[ESTRE22]"
    ]
    etiquetas_salfis01 = {
    1: "Sí",
    2: "No",
    3: "Prefiero no responder"
    }

    etiquetas_salfis02 = {
        1: "Sí, en tratamiento médico regular",
        2: "No, pero la condición está diagnosticada",
        3: "No estoy seguro/a",
        4: "Prefiero no responder"
    }

    etiquetas_si__no = {
        "Y": "Sí",
        "N": "No"
    }

    etiquetas_categoria = {
        "CSS03": "Ha pensado cómo (i3)",
        "CSS04": "Ha tenido intención de hacerlo (i4)",
        "CSS05": "Ha hecho plan detallado y/o intenciones con plan (i5)"
    }

    etiquetas_phq09f = {
        0: "No",
        1: "Sí",
        2: "Sí",
        3: "Sí"
    }

    etiquetas_lugtto = {
        1: "Dentro de Duoc UC",
        2: "Fuera de Duoc UC"
    }

    etiquetas_tiptto = {
        1: "Psicólogico",
        2: "Médico/psiquiátrico",
        3: "Ambos"
    }

    etiquetas_act_fisica = {
        1: "Nunca",
        2: "Una vez por semana",
        3: "Dos veces por semana",
        4: "Tres o más veces por semana"
    }

    etiquetas_embajador2 = {
        1: "Nada/Poco",
        2: "Nada/Poco",
        3: "Algo",
        4: "Mucho/Bastante",
        5: "Mucho/Bastante"
    }

    etiquetas_cuidado1 = {
        1: "No, ninguna.",
        2: "Sí, hijo/a(s).",
        3: "Sí, hermano/a o sobrino/a.",
        4: "Sí, adulto/a mayor.",
        5: "Sí, persona enferma o con alguna discapacidad."
    }

    etiquetas_cuidado2 = {
        1: "Sí, de algún familiar",
        2: "Sí, de su padre/madre",
        3: "Sí, una institución de cuidados (sala cuna, jardín, guardería, escuela, etc.)",
        4: "Sí, pago para servicios de cuidado en casa (servicio doméstico, enfermera, etc.)",
        5: "No cuento con apoyo"
    }

    etiquetas_empleo = {
        0: "No trabajo ningún día",
        1: "Solo fines de semana",
        2: "Trabajo solo algunos días a la semana",
        3: "Media jornada todos los días",
        4: "Trabajo de jornada completa todos los días"
    }

    etiquetas_espacios_sedes = {
        "DESCOM01[1]": "Casino",
        "DESCOM01[2]": "Biblioteca",
        "DESCOM01[3]": "Punto estudiantil",
        "DESCOM01[4]": "Espacios deportivos (si aplica)",
        "DESCOM01[5]": "Áreas verdes (si aplica)",
        "DESCOM01[6]": "Otros espacios cercanos a tu sede (plazas, malls, etc.)",
        "DESCOM01[7]": "Portal VIVO Duoc",
        "DESCOM01[8]": "AVA (Ambiente Virtual de Aprendizaje)",
        "DESCOM01[9]": "Correo Institucional",
        "DESCOM01[10]": "Portal de acceso a clases",
        "DESCOM01[11]": "No utilizo mucho los espacios de Duoc UC",
    }

    columnas_para_wordcloud = ["PRAB01[PRA01]", "PRAB01[PRA02]", "PRAB01[PRA03]"]

    buffer_wc_global = crear_wordcloud(
        df_global, 
        columnas_para_wordcloud,
        df_palabras_normalizadas_wordcloud,
        mask_path="plots/images/cloud_mask.png"
    )

    buffer_wc_femenino = crear_wordcloud(
        df_global[df_global["GENERO"] == "Femenino"],
        columnas_para_wordcloud,
        df_palabras_normalizadas_wordcloud,
        mask_path="plots/images/cloud_mask.png"
    )

    buffer_wc_masculino = crear_wordcloud(
        df_global[df_global["GENERO"] == "Masculino"],
        columnas_para_wordcloud,
        df_palabras_normalizadas_wordcloud,
        mask_path="plots/images/cloud_mask.png"
    )

    buffer_wc_2022 = crear_wordcloud(
        df_encuesta_2022,
        columnas_para_wordcloud,
        df_palabras_normalizadas_wordcloud,
        mask_path="plots/images/cloud_mask.png"
    )

    buffer_wc_2025 = crear_wordcloud(
        df_global,
        columnas_para_wordcloud,
        df_palabras_normalizadas_wordcloud,
        mask_path="plots/images/cloud_mask.png"
    )

    graficos_config = {
        "escuelas_bar_chart": {
            "dataset_fn": porcentaje_por_categoria,
            "dataset_args": [df_participantes, "ESCUELA"],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["ESCUELA", "Porcentaje"],
        },
        "sedes_bar_chart": {
            "dataset_fn": porcentaje_por_categoria,
            "dataset_args": [df_participantes, "SEDE"],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["SEDE", "Porcentaje"],
        },
        "gender_pie_chart": {
            "dataset_fn": porcentaje_por_categoria,
            "dataset_args": [df_participantes, "GENERO"],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["GENERO", "Porcentaje"],
        },
        "student_day_pie_chart": {
            "dataset_fn": porcentaje_por_categoria,
            "dataset_args": [df_participantes, "JORNADA"],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["JORNADA", "Porcentaje"],
        },
        "student_type_pie_chart": {
            "dataset_fn": porcentaje_por_categoria,
            "dataset_args": [df_participantes, "TIPO_ALUMNO"],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["TIPO_ALUMNO", "Porcentaje"],
        },
        "nivel_estres_categorias": { 
            "dataset_fn": promedio_por_categoria,
            "dataset_args": [df_valido, ["GENERO", "JORNADA", "TIPO_ALUMNO", "ESCUELA"], 2],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Categoria_label", "Porcentaje", None, True],
        },
        "nivel_estres_sedes": {
            "dataset_fn": promedio_por_categoria,
            "dataset_args": [df_valido_global, ["SEDE"]],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["SEDE", "Porcentaje", None, True],
        },
        "estresores_por_genero": {
            "dataset_fn": porcentaje_estresores,
            "dataset_args": [df_estresores, columnas_estresores, "GENERO"],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Categoria_label", "Porcentaje", "Variable", True],
        },
        "estresores_por_jornada": {
            "dataset_fn": porcentaje_estresores,
            "dataset_args": [df_estresores, columnas_estresores, "JORNADA"],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Categoria_label", "Porcentaje", "Variable", True],
        },
        "exigencia_academica": {
            "dataset_fn": porcentaje_estresores_exigencia,
            "dataset_args": [df_exigencia, ["EXIG[1]", "EXIG[2]", "EXIG[3]", "EXIG[4]", "EXIG[5]", "EXIG[6]"], None, None],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Categoria_label", "Porcentaje", "Variable", True],
        },
        "exigencia_academica_inicio": {
            "dataset_fn": porcentaje_estresores_exigencia,
            "dataset_args": [df_exigencia, ["EXIG[1]", "EXIG[2]", "EXIG[3]", "EXIG[4]", "EXIG[5]", "EXIG[6]"], "TIPO_ALUMNO", ["Inicio"]],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Categoria_label", "Porcentaje", None, True],
        },
        "exigencia_academica_continuidad": {
            "dataset_fn": porcentaje_estresores_exigencia,
            "dataset_args": [df_exigencia, ["EXIG[1]", "EXIG[2]", "EXIG[3]", "EXIG[4]", "EXIG[5]", "EXIG[6]"], "TIPO_ALUMNO", ["Continuidad"]],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Categoria_label", "Porcentaje", None, True],
        },
        "exigencia_academica_admision_especial": {
            "dataset_fn": porcentaje_estresores_exigencia,
            "dataset_args": [df_exigencia, ["EXIG[1]", "EXIG[2]", "EXIG[3]", "EXIG[4]", "EXIG[5]", "EXIG[6]"], "TIPO_ALUMNO", ["Admisión Especial"]],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Categoria_label", "Porcentaje", None, True],
        },
        "afrontamiento_estres": {
            "dataset_fn": porcentaje_afrontamiento,
            "dataset_args": [df_afrontamiento, [
                "ESTRA[ESTRA01]", "ESTRA[ESTRA02]", "ESTRA[ESTRA03]", "ESTRA[ESTRA04]", "ESTRA[ESTRA05]",
                "ESTRA[ESTRA06]", "ESTRA[ESTRA07]"
            ], 4],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Categoria_label", "Porcentaje", None, True],
        },
        "procrastinacion": {
            "dataset_fn": porcentaje_procrastinacion,
            "dataset_args": [df_procrastinacion, ["PROCAS[PROCA]"]],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Categoria_label", "Porcentaje", None, True],
        },
        "salud_cronica1": {
            "dataset_fn": porcentaje_salud_cronica,
            "dataset_args": [df_salud_cronica, "SALFIS01", etiquetas_salfis01],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Categoria_label", "Porcentaje", None, True],
        },
        "salud_cronica2": {
            "dataset_fn": porcentaje_salud_cronica,
            "dataset_args": [df_salud_cronica, "SALFIS02", etiquetas_salfis02],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Categoria_label", "Porcentaje", None, True],
        },
        "estresores_top5_2025": {
            "dataset_fn": porcentaje_estresores,
            "dataset_args": [df_estresores, columnas_estresores, None, 5],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Categoria_label", "Porcentaje", "Variable", True],
        },
        "estresores_top5_2022": {
            "dataset_fn": top_estresores_2022,
            "dataset_args": [df_estresores_2022, filtro, None, 5],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Categoria_label", "Porcentaje", "Variable", True],
        },
        "depresion_manejo_clinico": {
            "dataset_fn": depresion_manejo_clinico,
            "dataset_args": [df_depresion, ["GENERO", "JORNADA", "TIPO_ALUMNO", "ESCUELA"], 1],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Categoria", "Valor", "Serie"],
        },
        "depresion_manejo_clinico_sede": {
            "dataset_fn": depresion_manejo_clinico,
            "dataset_args": [df_depresion_global, ["SEDE"]],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Categoria", "Valor", "Serie"],
        },
        "ansiedad_manejo_clinico": {
            "dataset_fn": ansiedad_manejo_clinico,
            "dataset_args": [df_ansiedad, ["GENERO", "JORNADA", "TIPO_ALUMNO", "ESCUELA"], 1],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Categoria", "Valor", "Serie"],
        },
        "ansiedad_manejo_clinico_sede": {
            "dataset_fn": ansiedad_manejo_clinico,
            "dataset_args": [df_ansiedad_global, ["SEDE"]],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Categoria", "Valor", "Serie"],
        },
        "personalidad_manejo_clinico": {
            "dataset_fn": personalidad_manejo_clinico,
            "dataset_args": [df_personalidad, ["GENERO", "JORNADA", "TIPO_ALUMNO", "ESCUELA"], 1],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Categoria", "Valor", "Serie"],
        },
        "personalidad_manejo_clinico_sede": {
            "dataset_fn": personalidad_manejo_clinico,
            "dataset_args": [df_personalidad_global, ["SEDE"]],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Categoria", "Valor", "Serie"],
        },
        "marihuana_manejo_clinico": {
            "dataset_fn": marihuana_manejo_clinico,
            "dataset_args": [df_marihuana, ["GENERO", "JORNADA", "TIPO_ALUMNO", "ESCUELA"], 1],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Categoria", "Valor", "Serie"],
        },
        "marihuana_manejo_clinico_sede": {
            "dataset_fn": marihuana_manejo_clinico,
            "dataset_args": [df_marihuana_global, ["SEDE"]],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Categoria", "Valor", "Serie"],
        },
        "alcohol_manejo_clinico": {
            "dataset_fn": alcohol_manejo_clinico,
            "dataset_args": [df_alcohol, ["GENERO", "JORNADA", "TIPO_ALUMNO", "ESCUELA"], 1],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Categoria", "Valor", "Serie"],
        },
        "alcohol_manejo_clinico_sede": {
            "dataset_fn": alcohol_manejo_clinico,
            "dataset_args": [df_alcohol_global, ["SEDE"]],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Categoria", "Valor", "Serie"],
        },
        "suicidio_manejo_clinico": {
            "dataset_fn": ideacion_suicida_manejo_clinico,
            "dataset_args": [df_suicidio, ["GENERO", "JORNADA", "TIPO_ALUMNO", "ESCUELA"], 1],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Categoria", "Valor", "Serie"],
        },
        "suicidio_manejo_clinico_sede": {
            "dataset_fn": ideacion_suicida_manejo_clinico,
            "dataset_args": [df_suicidio_global, ["SEDE"]],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Categoria", "Valor", "Serie"],
        },
        "ideacion_suicida_1_pie_chart": {
            "dataset_fn": porcentaje_por_categoria,
            "dataset_args": [df_suicidio, "PHQ09[PHQ09F]", etiquetas_phq09f, True],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Etiqueta", "Porcentaje"],
        },
        "ideacion_suicida_2_pie_chart": {
            "dataset_fn": porcentaje_por_categoria,
            "dataset_args": [df_suicidio, "CSS01", etiquetas_si__no, True],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Etiqueta", "Porcentaje"],
        },
        "ideacion_suicida_3_pie_chart": {
            "dataset_fn": porcentaje_por_categoria,
            "dataset_args": [df_suicidio, "CSS02", etiquetas_si__no, True],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Etiqueta", "Porcentaje"],
        },
        "ideacion_suicida_4_bar_chart": {
            "dataset_fn": ideacion_suicida_barras,
            "dataset_args": [df_suicidio, ["CSS03", "CSS04", "CSS05"], etiquetas_si__no, etiquetas_categoria],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Categoria", "Porcentaje", "Respuesta"]
        },
        "ideacion_suicida_5_pie_chart": {
            "dataset_fn": porcentaje_por_categoria,
            "dataset_args": [df_suicidio, "CSS06", etiquetas_si__no, True],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Etiqueta", "Porcentaje"],
        },
        "nectto_pie_chart": {
            "dataset_fn": porcentaje_por_categoria,
            "dataset_args": [df_necesidad_tratamiento, "NECTTO", etiquetas_si__no, True],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Etiqueta", "Porcentaje"],
        },
        "acctto_pie_chart": {
            "dataset_fn": porcentaje_por_categoria,
            "dataset_args": [df_necesidad_tratamiento, "ACCTTO", etiquetas_si__no, True],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Etiqueta", "Porcentaje"],
        },
        "lugtto_pie_chart": {
            "dataset_fn": porcentaje_por_categoria,
            "dataset_args": [df_necesidad_tratamiento, "LUGTTO", etiquetas_lugtto, True],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Etiqueta", "Porcentaje"],
        },
        "tiptto_pie_chart": {
            "dataset_fn": porcentaje_por_categoria,
            "dataset_args": [df_necesidad_tratamiento, "TIPTTO", etiquetas_tiptto, True],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Etiqueta", "Porcentaje"],
        },
        "barreras_acceso_tratamiento": {
            "dataset_fn": barreras_acceso_tratamiento,
            "dataset_args": [df_barreras],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Categoria", "Porcentaje"],
        },
        "apoyo_percibido": {
            "dataset_fn": apoyo_percibido,
            "dataset_args": [df_apoyo],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Categoria", "Porcentaje", "Respuesta"]
        },
        "flow_states": {
            "dataset_fn": flow_percibido,
            "dataset_args": [df_flow_states],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Categoria", "Porcentaje", "Respuesta"]
        },
        "actividad_fisica_pie_chart": {
            "dataset_fn": porcentaje_por_categoria,
            "dataset_args": [df_act_fisica, "ACTFIS01[ACTFIS01]", etiquetas_act_fisica, True],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Etiqueta", "Porcentaje"],
        },
        "alimentacion3": {
            "dataset_fn": alimentacion,
            "dataset_args": [df_alimentacion, ["ALIMEN[ALIMEN03]"]],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Categoria", "Porcentaje", "Respuesta"]
        },
        "alimentacion": {
            "dataset_fn": alimentacion,
            "dataset_args": [df_alimentacion, ["ALIMEN[ALIMEN01]", "ALIMEN[ALIMEN02]", "ALIMEN[ALIMEN04]"]],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Categoria", "Porcentaje", "Respuesta"]
        },
        "ingesta_liquidos": {
            "dataset_fn": ingesta_liquidos,
            "dataset_args": [df_ing_liquidos],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Respuesta", "Porcentaje", "Categoria"]
        },
        "tabaquismo": {
            "dataset_fn": tabaquismo,
            "dataset_args": [df_tabaquismo],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Respuesta", "Porcentaje", "Categoria"]
        },
        "nivel_bienestar": {
            "dataset_fn": nivel_bienestar,
            "dataset_args": [df_perma, ["GENERO", "JORNADA", "TIPO_ALUMNO", "ESCUELA"]],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Categoria", "Valor", "Serie"],
        },
        "nivel_bienestar_sede": {
            "dataset_fn": nivel_bienestar,
            "dataset_args": [df_perma_global, ["SEDE"]],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Categoria", "Valor", "Serie"],
        },
        "perma_2022_2025_chart": {
            "dataset_fn": perma_2022_2025,
            "dataset_args": [df_bienestar_2022, df_perma],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Categoria", "Valor", "Serie"] 
        },
        "nhl_2022_2025_chart": {
            "dataset_fn": nhl_2022_2025,
            "dataset_args": [df_bienestar_2022, df_perma],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Categoria", "Valor", "Serie"] 
        },
        "porcentaje_grupo_amarillo_por_condicion": {
            "dataset_fn": porcentaje_grupo_amarillo_por_condicion,
            "dataset_args": [df_global, filtro],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Condición", "Valor", "Serie"]
        },
        "porcentaje_app_vivo1": {
            "dataset_fn": porcentaje_por_categoria,
            "dataset_args": [df_app_vivo_filterdate, "APPVI01", etiquetas_si__no, True],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Etiqueta", "Porcentaje",]
        },
        "porcentaje_app_vivo1.2": {
            "dataset_fn": porcentaje_por_categoria,
            "dataset_args": [df_app_vivo_filterdate, "APPVI01", etiquetas_si__no, True],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Etiqueta", "Porcentaje",]
        },
        "porcentaje_app_vivo3": {
            "dataset_fn": porcentaje_por_categoria,
            "dataset_args": [df_app_vivo_filterdate, "APPVI03", etiquetas_si__no, True],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Etiqueta", "Porcentaje"]
        },
        "porcentaje_app_vivo2": {
            "dataset_fn": porcentaje_respuestas_appvivo,
            "dataset_args": [df_app_vivo_filterdate, ["APPVI02[1]", "APPVI02[2]", "APPVI02[3]"]],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["CategoriaLabel", "Porcentaje", "Variable"]
        },
        "porcentaje_app_vivo2.2": {
            "dataset_fn": porcentaje_respuestas_appvivo,
            "dataset_args": [df_app_vivo_filterdate, ["APPVI02[1]", "APPVI02[2]", "APPVI02[3]"]],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["CategoriaLabel", "Porcentaje", "Variable"]
        },
        "embajador_salud_mental1": {
            "dataset_fn": porcentaje_por_categoria,
            "dataset_args": [df_embajador, "EMB01", etiquetas_si__no, True],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Etiqueta", "Porcentaje"]
        },
        "embajador_salud_mental2": {
            "dataset_fn": porcentaje_por_categoria,
            "dataset_args": [df_embajador, "EMB06[EMBSM06]", etiquetas_embajador2, True],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Etiqueta", "Porcentaje"]
        },
        "embajador_salud_mental3": {
            "dataset_fn": embajador_salud_mental3,
            "dataset_args": [df_embajador],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Respuesta", "Porcentaje", "Categoria"]
        },
        "embajador_salud_mental4": {
            "dataset_fn": embajador_salud_mental4,
            "dataset_args": [df_embajador],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Respuesta", "Porcentaje", "Categoria"]
        },
        "embajador_salud_mental5": {
            "dataset_fn": porcentaje_por_categoria,
            "dataset_args": [df_embajador, "EMBSM09", etiquetas_si__no, True],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Etiqueta", "Porcentaje"],
        },
        "embajador_salud_mental6": {
            "dataset_fn": porcentaje_por_categoria,
            "dataset_args": [df_embajador, "EMB03", etiquetas_si__no, True],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Etiqueta", "Porcentaje"],
        },
        "embajador_salud_mental7": {
            "dataset_fn": embajador_salud_mental7,
            "dataset_args": [df_embajador],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Respuesta", "Porcentaje", "Categoria"]
        },
        "embajador_salud_mental8": {
            "dataset_fn": porcentaje_por_categoria,
            "dataset_args": [df_embajador, "EMB10", etiquetas_si__no, True],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Etiqueta", "Porcentaje"],
        },
        "embajador_salud_mental9": {
            "dataset_fn": embajador_salud_mental9,
            "dataset_args": [df_embajador],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Respuesta", "Porcentaje", "Categoria"],
        },
        "atencion_psicologica1": {
            "dataset_fn": porcentaje_por_categoria,
            "dataset_args": [df_atencion_psicologica, "ATPSIC01", etiquetas_si__no, True],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Etiqueta", "Porcentaje"],
        },
        "atencion_psicologica2": {
            "dataset_fn": atencion_psicologica2,
            "dataset_args": [df_atencion_psicologica],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Respuesta", "Porcentaje", "Categoria"],
        },
        "atencion_psicologica3": {
            "dataset_fn": porcentaje_por_categoria,
            "dataset_args": [df_atencion_psicologica, "ATPSIC03", etiquetas_si__no, True],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Etiqueta", "Porcentaje"],
        },
        "atencion_psicologica4": {
            "dataset_fn": porcentaje_por_categoria,
            "dataset_args": [df_atencion_psicologica, "BIM01", etiquetas_si__no, True],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Etiqueta", "Porcentaje"],
        },
        "atencion_psicologica5": {
            "dataset_fn": atencion_psicologica5,
            "dataset_args": [df_atencion_psicologica],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Respuesta", "Porcentaje", "Categoria"],
        },
        "atencion_psicologica6": {
            "dataset_fn": porcentaje_por_categoria,
            "dataset_args": [df_atencion_psicologica, "BIM03", etiquetas_si__no, True],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Etiqueta", "Porcentaje"],
        },
        "atencion_psicologica1.2": {
            "dataset_fn": porcentaje_por_categoria,
            "dataset_args": [df_atencion_psicologica, "ATPSIC01", etiquetas_si__no, True],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Etiqueta", "Porcentaje"],
        },
        "atencion_psicologica2.2": {
            "dataset_fn": atencion_psicologica2,
            "dataset_args": [df_atencion_psicologica],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Respuesta", "Porcentaje", "Categoria"],
        },
        "atencion_psicologica3.2": {
            "dataset_fn": porcentaje_por_categoria,
            "dataset_args": [df_atencion_psicologica, "ATPSIC03", etiquetas_si__no],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Etiqueta", "Porcentaje"],
        },
        "atencion_psicologica4.2": {
            "dataset_fn": porcentaje_por_categoria,
            "dataset_args": [df_atencion_psicologica, "BIM01", etiquetas_si__no, True],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Etiqueta", "Porcentaje"],
        },
        "atencion_psicologica5.2": {
            "dataset_fn": atencion_psicologica5,
            "dataset_args": [df_atencion_psicologica],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Respuesta", "Porcentaje", "Categoria"],
        },
        "atencion_psicologica6.2": {
            "dataset_fn": porcentaje_por_categoria,
            "dataset_args": [df_atencion_psicologica, "BIM03", etiquetas_si__no],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Etiqueta", "Porcentaje"],
        },
        "personas_cuidado1": {
            "dataset_fn": porcentaje_por_categoria,
            "dataset_args": [df_personas_cuidado, "CUIDA01", etiquetas_cuidado1],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Etiqueta", "Porcentaje"],
        },
        "personas_cuidado2": {
            "dataset_fn": porcentaje_por_categoria,
            "dataset_args": [df_personas_cuidado, "CUIDA02", etiquetas_cuidado2],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Etiqueta", "Porcentaje"],
        },
        "situacion_empleo": {
            "dataset_fn": porcentaje_por_categoria,
            "dataset_args": [df_situacion_empleo, "EMPLE01", etiquetas_empleo],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Etiqueta", "Porcentaje"],
        },
        "condicion_academica1": {
            "dataset_fn": condicion_academica,
            "dataset_args": [df_condicion_academica, ["CONDACAD[CON01]", "CONDACAD[CON02]"]],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Categoria", "Porcentaje", "Respuesta"],
        },
        "condicion_academica2": {
            "dataset_fn": condicion_academica,
            "dataset_args": [df_condicion_academica, ["CONDACAD[CON03]"]],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Categoria", "Porcentaje", "Respuesta"],
        },
        "espacio_sede1": {
            "dataset_fn": porcentaje_seleccion_multiple_y,
            "dataset_args": [df_espacios_sedes, ["DESCOM01[1]", "DESCOM01[2]", "DESCOM01[3]", "DESCOM01[4]", "DESCOM01[5]", "DESCOM01[6]", "DESCOM01[7]", "DESCOM01[8]", "DESCOM01[9]", "DESCOM01[10]", "DESCOM01[11]"], etiquetas_espacios_sedes, 1],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["CategoriaLabel", "Porcentaje", "Variable"]
        },
        "espacio_sede2": {
            "dataset_fn": porcentaje_seleccion_multiple_y,
            "dataset_args": [df_espacios_sedes, ["DESCOM01[1]", "DESCOM01[2]", "DESCOM01[3]", "DESCOM01[4]", "DESCOM01[5]", "DESCOM01[6]", "DESCOM01[7]", "DESCOM01[8]", "DESCOM01[9]", "DESCOM01[10]", "DESCOM01[11]"], etiquetas_espacios_sedes, 2],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["CategoriaLabel", "Porcentaje", "Variable"]
        },
    }

    # Textos dinámicos — puedes agregar todos los que quieras
    textos_config = {
        "total_participantes": {
            "texto": f"CASOS VÁLIDOS (N={len(df_participantes):,})",
            "estilo": {
                "fuente": "Calibri Light",
                "tamano": 14,
                "bold": True,
                "color": (58, 67, 76)
            }
        },
        "total_participantes_2": {
            "texto": f"CASOS VÁLIDOS (N={len(df_participantes):,})",
            "estilo": {
                "fuente": "Calibri Light",
                "tamano": 14,
                "bold": True,
                "color": (58, 67, 76)
            }
        },
        "nivel_estres_promedio_2022": {
            "texto": f"{df_estresores_2022[filtro]['Nivel de estrés 2022']:.0%}",
            "estilo": {
                "fuente": "Calibri Light",
                "tamano": 25,
                "bold": True,
                "color": (255, 255, 255)
            }
        },
        "nivel_estres_promedio_2025": {
            "texto": f"{nivel_estres_promedio_2025:.0%}",
            "estilo": {
                "fuente": "Calibri Light",
                "tamano": 60,
                "bold": True,
                "color": (255, 255, 255)
            }
        },
        "nivel_estres_promedio_2025_2": {
            "texto": f"{nivel_estres_promedio_2025:.0%}",
            "estilo": {
                "fuente": "Calibri Light",
                "tamano": 25,
                "bold": True,
                "color": (255, 255, 255)
            }
        },
        "depresion_manejo_clinico_global": {
            "texto": f"{depresion_manejo_clinico_global:.0%}",
            "estilo": {
                "fuente": "Calibri Light",
                "tamano": 60,
                "bold": True,
                "color": (255, 255, 255)
            }
        },
        "ansiedad_manejo_clinico_global": {
            "texto": f"{ansiedad_manejo_clinico_global:.0%}",
            "estilo": {
                "fuente": "Calibri Light",
                "tamano": 60,
                "bold": True,
                "color": (255, 255, 255)
            }
        },
        "personalidad_manejo_clinico_global": {
            "texto": f"{personalidad_manejo_clinico_global:.0%}",
            "estilo": {
                "fuente": "Calibri Light",
                "tamano": 60,
                "bold": True,
                "color": (255, 255, 255)
            }
        },
        "marihuana_manejo_clinico_global": {
            "texto": f"{marihuana_manejo_clinico_global:.0%}",
            "estilo": {
                "fuente": "Calibri Light",
                "tamano": 60,
                "bold": True,
                "color": (255, 255, 255)
            }
        },
        "alcohol_manejo_clinico_global": {
            "texto": f"{alcohol_manejo_clinico_global:.0%}",
            "estilo": {
                "fuente": "Calibri Light",
                "tamano": 60,
                "bold": True,
                "color": (255, 255, 255)
            }
        },
        "ideacion_suicida_manejo_clinico_global": {
            "texto": f"{ideacion_suicida_manejo_clinico_global:.0%}",
            "estilo": {
                "fuente": "Calibri Light",
                "tamano": 60,
                "bold": True,
                "color": (255, 255, 255)
            }
        }, 
        "grupo_verde": {
            "texto": f"{grupo_verde:.0f}%",
            "estilo": {
                "fuente": "Calibri Light",
                "tamano": 60,
                "bold": True,
                "color": (255, 255, 255)
            }
        },
        "grupo_amarillo": {
            "texto": f"{grupo_amarillo:.0f}%",
            "estilo": {
                "fuente": "Calibri Light",
                "tamano": 60,
                "bold": True,
                "color": (255, 255, 255)
            }
        },
        "grupo_amarillo2": {
            "texto": f"{grupo_amarillo:.0f}%",
            "estilo": {
                "fuente": "Calibri Light",
                "tamano": 60,
                "bold": True,
                "color": (255, 255, 255)
            }
        },
        "grupo_rojo": {
            "texto": f"{grupo_rojo:.0f}%",
            "estilo": {
                "fuente": "Calibri Light",
                "tamano": 60,
                "bold": True,
                "color": (255, 255, 255)
            }
        },
        "factor_carga_enfermedad_rojo":{
            "texto": f"{factor_carga_enfermedad_rojo:.0f}",
            "estilo": {
                "fuente": "Calibri Light",
                "tamano": 60,
                "bold": True,
                "color": (255, 255, 255)
            }
        },
        "factor_carga_enfermedad_amarillo":{
            "texto": f"{factor_carga_enfermedad_amarillo:.0f}",
            "estilo": {
                "fuente": "Calibri Light",
                "tamano": 60,
                "bold": True,
                "color": (255, 255, 255)
            }
        },
        "cupit_marihuana_porcentaje": {
            "texto": f"{cupit_marihuana_porcentaje:.0f}%",
            "estilo": {
                "fuente": "Calibri Light",
                "tamano": 60,
                "bold": True,
                "color": (255, 255, 255)
            }
        },
        "cantidad_salfis1": {
            "texto": f"Nota: esta pregunta incluye un total de {cantidad_salfis1} respuestas.",
            "estilo": {
                "fuente": "Calibri Light",
                "tamano": 12,
                "bold": False,
                "color": (82, 82, 82)
            }
        },
        "depresion_femenino": {
            "texto": f"Los datos presentados por sexo, jornada, tipo de alumno y sede, corresponden al porcentaje de prevalencia para cada categoría. Por ejemplo, el {depresion_femenino*100:.0f}% de las mujeres que participaron del estudio presentan síntomas clínicos de depresión.",
            "estilo": {
                "fuente": "Calibri Light",
                "tamano": 12,
                "bold": False,
                "color": (82, 82, 82)
            }
        },
        "ansiedad_femenino": {
            "texto": f"Los datos presentados por sexo, jornada, tipo de alumno y sede, corresponden al porcentaje de prevalencia para cada categoría. Por ejemplo, el {ansiedad_femenino*100:.0f}% de las mujeres que participaron del estudio presentan síntomas clínicos de ansiedad generalizada.",
            "estilo": {
                "fuente": "Calibri Light",
                "tamano": 12,
                "bold": False,
                "color": (82, 82, 82)
            }
        },
        "personalidad_femenino": {
            "texto": f"Los datos presentados por sexo, jornada, tipo de alumno y sede, corresponden al porcentaje de prevalencia para cada categoría. Por ejemplo, el {personalidad_femenino*100:.0f}% de las mujeres que participaron del estudio presentan síntomas clínicos de trastorno de la personalidad.",
            "estilo": {
                "fuente": "Calibri Light",
                "tamano": 12,
                "bold": False,
                "color": (82, 82, 82)
            }
        },
        "marihuana_femenino": {
            "texto": f"Los datos presentados por sexo, jornada, tipo de alumno y sede, corresponden al porcentaje de prevalencia para cada categoría. Por ejemplo, el {marihuana_femenino*100:.0f}% de las mujeres que participaron del estudio presentan síntomas clínicos de consumo problemático de marihuana.",
            "estilo": {
                "fuente": "Calibri Light",
                "tamano": 12,
                "bold": False,
                "color": (82, 82, 82)
            }
        },
        "alcohol_femenino": {
            "texto": f"Los datos presentados por sexo, jornada, tipo de alumno y sede, corresponden al porcentaje de prevalencia para cada categoría. Por ejemplo, el {alcohol_femenino*100:.0f}% de las mujeres que participaron del estudio presentan síntomas clínicos de consumo problemático de alcohol.",
            "estilo": {
                "fuente": "Calibri Light",
                "tamano": 12,
                "bold": False,
                "color": (82, 82, 82)
            }
        },
        "suicidio_femenino": {
            "texto": f"Los datos presentados por sexo, jornada, tipo de alumno y sede, corresponden al porcentaje de prevalencia para cada categoría. Por ejemplo, el {suicidio_femenino*100:.0f}% de las mujeres que participaron del estudio presentan sospecha de  ideación suicida.",
            "estilo": {
                "fuente": "Calibri Light",
                "tamano": 12,
                "bold": False,
                "color": (82, 82, 82)
            }
        },
        "nota_exigencia": {
            "texto": f"Nota: esta pregunta incluye un total de {cantidad_exigencia} respuestas.",
            "estilo": {
                "fuente": "Calibri Light",
                "tamano": 12,
                "bold": False,
                "color": (82, 82, 82)
            }
        },
        "nivel_bienestar_global": {
            "texto": f"{nivel_bienestar_global:.1f}",
            "estilo": {
                "fuente": "Calibri Light",
                "tamano": 60,
                "bold": True,
                "color": (255, 255, 255)
            }
        },
        "flow_positivo": {
            "texto": f"{flow_positivo:.0f}%",
            "estilo": {
                "fuente": "Arial (Cuerpo)",
                "tamano": 66,
                "bold": True,
                "color": (0, 0, 0)
            }
        },
        "grupo_verde_2022": {
            "texto": f"{grupo_verde_2022*100:.0f}%",
            "estilo": {
                "fuente": "Calibri Light",
                "tamano": 25,
                "bold": True,
                "color": (255, 255, 255)
            }
        },
        "grupo_amarillo_2022": {
            "texto": f"{grupo_amarillo_2022*100:.0f}%",
            "estilo": {
                "fuente": "Calibri Light",
                "tamano": 25,
                "bold": True,
                "color": (255, 255, 255)
            }
        },
        "grupo_rojo_2022": {
            "texto": f"{grupo_rojo_2022*100:.0f}%",
            "estilo": {
                "fuente": "Calibri Light",
                "tamano": 25,
                "bold": True,
                "color": (255, 255, 255)
            }
        },
        "factor_carga_enfermedad_amarillo_2022": {
            "texto": f"{factor_carga_enfermedad_amarillo_2022:.0f}",
            "estilo": {
                "fuente": "Calibri Light",
                "tamano": 25,
                "bold": True,
                "color": (255, 255, 255)
            }
        },
        "factor_carga_enfermedad_rojo_2022": {
            "texto": f"{factor_carga_enfermedad_rojo_2022:.0f}",
            "estilo": {
                "fuente": "Calibri Light",
                "tamano": 25,
                "bold": True,
                "color": (255, 255, 255)
            }
        },
        "depresion_2022": {
            "texto": f"{depresion_2022*100:.0f}%",
            "estilo": {
                "fuente": "Calibri Light",
                "tamano": 25,
                "bold": True,
                "color": (255, 255, 255)
            }
        },
        "ansiedad_2022": {
            "texto": f"{ansiedad_2022*100:.0f}%",
            "estilo": {
                "fuente": "Calibri Light",
                "tamano": 25,
                "bold": True,
                "color": (255, 255, 255)
            }
        },
        "personalidad_2022": {
            "texto": f"{personalidad_2022*100:.0f}%",
            "estilo": {
                "fuente": "Calibri Light",
                "tamano": 25,
                "bold": True,
                "color": (255, 255, 255)
            }
        },
        "marihuana_2022": {
            "texto": f"{marihuana_2022*100:.0f}%",
            "estilo": {
                "fuente": "Calibri Light",
                "tamano": 25,
                "bold": True,
                "color": (255, 255, 255)
            }
        },
        "alcohol_2022": {
            "texto": f"{alcohol_2022*100:.0f}%",
            "estilo": {
                "fuente": "Calibri Light",
                "tamano": 25,
                "bold": True,
                "color": (255, 255, 255)
            }
        },
        "suicidio_2022": {
            "texto": f"{suicidio_2022*100:.0f}%",
            "estilo": {
                "fuente": "Calibri Light",
                "tamano": 25,
                "bold": True,
                "color": (255, 255, 255)
            }
        },
        "bienestar_global_2022": {
            "texto": f"{bienestar_global_2022:.1f}",
            "estilo": {
                "fuente": "Calibri Light",
                "tamano": 25,
                "bold": True,
                "color": (255, 255, 255)
            }
        },
        "respuestas_suicidio": {
            "texto": f"Nota: esta sección incluye un total de {respuestas_suicidio} respuestas.",
            "estilo": {
                "fuente": "Calibri Light",
                "tamano": 12,
                "bold": False,
                "color": (82, 82, 82)
            }
        },
        "respuestas_appvivo": {
            "texto": f"Nota: esta sección incluye un total de {respuestas_appvivo} respuestas.",
            "estilo": {
                "fuente": "Calibri Light",
                "tamano": 12,
                "bold": False,
                "color": (82, 82, 82)
            }
        },
        "respuestas_appvivo2": {
            "texto": f"Nota: esta sección incluye un total de {respuestas_appvivo} respuestas.",
            "estilo": {
                "fuente": "Calibri Light",
                "tamano": 12,
                "bold": False,
                "color": (82, 82, 82)
            }
        },
        "respuestas_embajador1": {
            "texto": f"¿Eres un Embajador/a del Bienestar y la Salud Mental en tu sede? N = {respuestas_embajador1}",
            "estilo": {
                "fuente": "Calibri Light",
                "tamano": 16,
                "bold": False,
                "color": (82, 82, 82)
            }
        },
        "respuestas_embajador2": {
            "texto": f"¿En qué medida el curso de embajadores ha aportado a tu bienestar y salud mental? N = {respuestas_embajador2}",
            "estilo": {
                "fuente": "Calibri Light",
                "tamano": 16,
                "bold": False,
                "color": (82, 82, 82)
            }
        },
        "respuestas_embajador3": {
            "texto": f"Nota: esta sección incluye un total de {respuestas_embajador3} respuestas.",
            "estilo": {
                "fuente": "Calibri Light",
                "tamano": 12,
                "bold": False,
                "color": (82, 82, 82)
            }
        },
        "respuestas_embajador4": {
            "texto": f"Con la información que acabas de leer sobre el programa, ¿te interesaría ser un Embajador/a del Bienestar y la Salud Mental? N = {respuestas_embajador4}",
            "estilo": {
                "fuente": "Calibri Light",
                "tamano": 16,
                "bold": False,
                "color": (82, 82, 82)
            }
        },
        "respuestas_embajador5": {
            "texto": f"¿Cuál de las siguientes alternativas representa la razón por la que no te interesaría ser Embajador/a? N = {respuestas_embajador5}",
            "estilo": {
                "fuente": "Calibri Light",
                "tamano": 16,
                "bold": False,
                "color": (82, 82, 82)
            }
        },
        "respuestas_embajador6": {
            "texto": f"¿En algún momento has buscado o recibido apoyo, orientación o información sobre bienestar y salud mental a través de alguien de la comunidad Duoc UC? (N={respuestas_embajador6})",
            "estilo": {
                "fuente": "Calibri Light",
                "tamano": 16,
                "bold": False,
                "color": (82, 82, 82)
            }
        },
        "respuestas_embajador7": {
            "texto": f"¿Recuerdas si esa persona era un Embajador/a del Bienestar y la Salud Mental? (N={respuestas_embajador7})",
            "estilo": {
                "fuente": "Calibri Light",
                "tamano": 16,
                "bold": False,
                "color": (82, 82, 82)
            }
        },
        "respuestas_atencion_psiscologica1": {
            "texto": f"Nota: esta sección incluye un total de {respuestas_atencion_psiscologica1} respuestas.",
            "estilo": {
                "fuente": "Calibri Light",
                "tamano": 12,
                "bold": False,
                "color": (82, 82, 82)
            }
        },
        "respuestas_atencion_psiscologica1.2": {
            "texto": f"Nota: esta sección incluye un total de {respuestas_atencion_psiscologica1} respuestas.",
            "estilo": {
                "fuente": "Calibri Light",
                "tamano": 12,
                "bold": False,
                "color": (82, 82, 82)
            }
        },
        "respuestas_bienestar_integral": {
            "texto": f"Nota: esta sección incluye un total de {respuestas_bienestar_integral} respuestas.",
            "estilo": {
                "fuente": "Calibri Light",
                "tamano": 12,
                "bold": False,
                "color": (82, 82, 82)
            }
        },
        "respuestas_bienestar_integral1.2": {
            "texto": f"Nota: esta sección incluye un total de {respuestas_bienestar_integral} respuestas.",
            "estilo": {
                "fuente": "Calibri Light",
                "tamano": 12,
                "bold": False,
                "color": (82, 82, 82)
            }
        },
        "respuestas_personas_cuidado1": {
            "texto": f"¿Tienes a alguna persona a tu cuidado? N = {respuestas_personas_cuidado1}",
            "estilo": {
                "fuente": "Calibri Light",
                "tamano": 16,
                "bold": False,
                "color": (82, 82, 82)
            }
        },
        "respuestas_personas_cuidado2": {
            "texto": f"¿Cuentas con apoyo para el cuidado de esa(s) persona(s) mientras estudias? N = {respuestas_personas_cuidado2}",
            "estilo": {
                "fuente": "Calibri Light",
                "tamano": 16,
                "bold": False,
                "color": (82, 82, 82)
            }
        },
        "respuestas_empleo": {
            "texto": f"¿Cuál de estas situaciones refleja de mejor forma tu trabajo actual? N = {respuestas_empleo}",
            "estilo": {
                "fuente": "Calibri Light",
                "tamano": 16,
                "bold": False,
                "color": (82, 82, 82)
            }
        },
        "respuestas_condicion_academica": {
            "texto": f"De acuerdo a las condiciones que tienes para desarrollar tus actividades académicas, ¿cuán de acuerdo estás con las siguientes afirmaciones? N = {respuestas_condicion_academica}",
            "estilo": {
                "fuente": "Calibri Light",
                "tamano": 16,
                "bold": False,
                "color": (82, 82, 82)
            }
        },
        "respuestas_espacios_sedes": {
            "texto": f"Nota: esta pregunta incluye un total de {respuestas_espacios_sedes} respuestas y se desplegó a modo de pregunta de descompresión solo a quienes habían profundizado en ideación suicida.",
            "estilo": {
                "fuente": "Calibri Light",
                "tamano": 12,
                "bold": False,
                "color": (82, 82, 82)
            }
        },
        "titulo":{
            "texto": f"{titulo} {filtro}",
            "estilo": {
                "fuente": "Calibri Light",
                "tamano": 40,
                "bold": False,
                "color": (255, 255, 255)
            }
        },
        "titulo2":{
            "texto": f"{titulo} {filtro}",
            "estilo": {
                "fuente": "Calibri Light",
                "tamano": 40,
                "bold": False,
                "color": (255, 255, 255)
            }
        },
    }

    subtitulo_texto = f"{titulo} {filtro}"
    subtitulo_estilo = {
        "fuente": "Calibri Light",
        "tamano": 31,
        "bold": True,
        "color": (58, 67, 76)
    }

    nombres_placeholders_subtitulo = [f"subtitulo_sede_{i}" for i in range(1, 41)]

    config_subtitulos_repetidos = {}
    for nombre in nombres_placeholders_subtitulo:
        config_subtitulos_repetidos[nombre] = {
            "texto": subtitulo_texto,
            "estilo": subtitulo_estilo
        }
    
    textos_config.update(config_subtitulos_repetidos)

    imagenes_config = {
        "wordcloud_global": {
            "buffer": buffer_wc_global
        },
        "wordcloud_mujeres": {
            "buffer": buffer_wc_femenino
        },
        "wordcloud_hombres": {
            "buffer": buffer_wc_masculino
        },
        "wordcloud_2022": {
            "buffer": buffer_wc_2022
        },
        "wordcloud_2025": {
            "buffer": buffer_wc_2025
        },
    }

    actualizar_graficos(template_path, output_path, graficos_config, textos_config, imagenes_config)