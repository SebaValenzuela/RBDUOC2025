from data.datasets import ansiedad_manejo_clinico, conteo_simple, marihuana_manejo_clinico, personalidad_manejo_clinico, porcentaje_afrontamiento, porcentaje_estresores_exigencia, porcentaje_por_categoria, casos_validos_pss, aplicar_regla_pss,porcentaje_procrastinacion, porcentaje_salud_cronica, promedio_por_categoria, porcentaje_estresores, top_estresores_2022, depresion_manejo_clinico, alcohol_manejo_clinico
from plots.charts import crear_chart_data
from plots.pptx_updater import actualizar_graficos

def generar_reporte(df_participantes, df_estres, df_estresores_2022, df_estresores, df_exigencia, df_afrontamiento, df_procrastinacion, df_salud_cronica, df_depresion,
                    df_ansiedad, df_personalidad, df_marihuana, df_alcohol):
    template_path = "reports/templates/template-prueba.pptx"
    output_path = "reports/output/reporte-generado.pptx"

    df_valido = casos_validos_pss(df_estres)
    df_valido = aplicar_regla_pss(df_valido)
    nivel_estres_promedio_2025 = df_valido["pct_persona"].mean()

    df_depresion_malestar_clinico = depresion_manejo_clinico(df_depresion, len(df_participantes), None)
    depresion_manejo_clinico_global = df_depresion_malestar_clinico["Valor"].iloc[0]
    df_ansiedad_malestar_clinico = ansiedad_manejo_clinico(df_ansiedad, len(df_participantes), None)
    ansiedad_manejo_clinico_global = df_ansiedad_malestar_clinico["Valor"].iloc[0]
    df_personalidad_malestar_clinico = personalidad_manejo_clinico(df_personalidad, len(df_participantes), None)
    personalidad_manejo_clinico_global = df_personalidad_malestar_clinico["Valor"].iloc[0]
    df_marihuana_malestar_clinico = marihuana_manejo_clinico(df_marihuana, len(df_participantes), None)
    marihuana_manejo_clinico_global = df_marihuana_malestar_clinico["Valor"].iloc[0]
    df_alcohol_manejo_clinico = alcohol_manejo_clinico(df_alcohol, len(df_participantes), None)
    alcohol_manejo_clinico_global = df_alcohol_manejo_clinico["Valor"].iloc[0]


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
            "dataset_args": [df_valido, ["GENERO", "JORNADA", "TIPO_ALUMNO", "ESCUELA"]],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Variable", "Porcentaje", None, True],
        },
        "nivel_estres_sedes": {
            "dataset_fn": promedio_por_categoria,
            "dataset_args": [df_valido, ["SEDE"]],
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
            "dataset_args": [df_exigencia, ["EXIG[1]", "EXIG[2]", "EXIG[3]", "EXIG[4]", "EXIG[5]", "EXIG[6]"], "ESTRE[ESTRE18]"],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Categoria_label", "Porcentaje", None, True],
        },
        "exigencia_academica_inicio": {
            "dataset_fn": porcentaje_estresores_exigencia,
            "dataset_args": [df_exigencia, ["EXIG[1]", "EXIG[2]", "EXIG[3]", "EXIG[4]", "EXIG[5]", "EXIG[6]"], "TIPO_ALUMNO", ["Inicio"], "ESTRE[ESTRE18]"],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Categoria_label", "Porcentaje", None, True],
        },
        "exigencia_academica_continuidad": {
            "dataset_fn": porcentaje_estresores_exigencia,
            "dataset_args": [df_exigencia, ["EXIG[1]", "EXIG[2]", "EXIG[3]", "EXIG[4]", "EXIG[5]", "EXIG[6]"], "TIPO_ALUMNO", ["Continuidad"], "ESTRE[ESTRE18]"],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Categoria_label", "Porcentaje", None, True],
        },
        "exigencia_academica_admision_especial": {
            "dataset_fn": porcentaje_estresores_exigencia,
            "dataset_args": [df_exigencia, ["EXIG[1]", "EXIG[2]", "EXIG[3]", "EXIG[4]", "EXIG[5]", "EXIG[6]"], "TIPO_ALUMNO", ["Admisión Especial"], "ESTRE[ESTRE18]"],
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
            "dataset_args": [df_estresores_2022, "Global", None, 5],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Categoria_label", "Porcentaje", "Variable", True],
        },
        "depresion_manejo_clinico": {
            "dataset_fn": depresion_manejo_clinico,
            "dataset_args": [df_depresion, len(df_participantes), ["GENERO", "JORNADA", "TIPO_ALUMNO"]],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Categoria", "Valor", "Serie"],
        },
        "depresion_manejo_clinico_sede": {
            "dataset_fn": depresion_manejo_clinico,
            "dataset_args": [df_depresion, len(df_participantes), ["SEDE"]],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Categoria", "Valor", "Serie"],
        },
        "ansiedad_manejo_clinico": {
            "dataset_fn": ansiedad_manejo_clinico,
            "dataset_args": [df_ansiedad, len(df_participantes), ["GENERO", "JORNADA", "TIPO_ALUMNO"]],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Categoria", "Valor", "Serie"],
        },
        "ansiedad_manejo_clinico_sede": {
            "dataset_fn": ansiedad_manejo_clinico,
            "dataset_args": [df_ansiedad, len(df_participantes), ["SEDE"]],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Categoria", "Valor", "Serie"],
        },
        "personalidad_manejo_clinico": {
            "dataset_fn": personalidad_manejo_clinico,
            "dataset_args": [df_personalidad, len(df_participantes), ["GENERO", "JORNADA", "TIPO_ALUMNO"]],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Categoria", "Valor", "Serie"],
        },
        "personalidad_manejo_clinico_sede": {
            "dataset_fn": personalidad_manejo_clinico,
            "dataset_args": [df_personalidad, len(df_participantes), ["SEDE"]],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Categoria", "Valor", "Serie"],
        },
        "marihuana_manejo_clinico": {
            "dataset_fn": marihuana_manejo_clinico,
            "dataset_args": [df_marihuana, len(df_participantes), ["GENERO", "JORNADA", "TIPO_ALUMNO"]],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Categoria", "Valor", "Serie"],
        },
        "marihuana_manejo_clinico_sede": {
            "dataset_fn": marihuana_manejo_clinico,
            "dataset_args": [df_marihuana, len(df_participantes), ["SEDE"]],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Categoria", "Valor", "Serie"],
        },
        "alcohol_manejo_clinico": {
            "dataset_fn": alcohol_manejo_clinico,
            "dataset_args": [df_alcohol, len(df_participantes), ["GENERO", "JORNADA", "TIPO_ALUMNO"]],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Categoria", "Valor", "Serie"],
        },
        "alcohol_manejo_clinico_sede": {
            "dataset_fn": alcohol_manejo_clinico,
            "dataset_args": [df_alcohol, len(df_participantes), ["SEDE"]],
            "chart_builder": crear_chart_data,
            "chart_builder_args": ["Categoria", "Valor", "Serie"],
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
        "nivel_estres_promedio_2022": {
            "texto": f"{df_estresores_2022['Global']['Nivel de estrés 2022']:.0%}",
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
        }
    }

    actualizar_graficos(template_path, output_path, graficos_config, textos_config)
