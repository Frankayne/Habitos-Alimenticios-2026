# ─────────────────────────────────────────────────────────────
# IMPORTACIONES
# ─────────────────────────────────────────────────────────────
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import os


# ─────────────────────────────────────────────────────────────
# CONFIGURACIÓN DE LA PÁGINA
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Salud Infantil",
    page_icon="👶",
    layout="wide",
)


# ─────────────────────────────────────────────────────────────
# FUNCIÓN: GENERAR DATASET DE EJEMPLO (original)
# ─────────────────────────────────────────────────────────────
def generar_datos_ejemplo():
    np.random.seed(42)
    n = 200
    regiones = ["Norte", "Centro", "Sur", "Este", "Oeste"]
    edades = np.random.randint(0, 15, n)
    df = pd.DataFrame({
        "id_nino": range(1, n + 1),
        "region": np.random.choice(regiones, n),
        "edad": edades,
        "peso_kg": np.round(np.random.uniform(3, 55, n), 1),
        "altura_cm": np.round(np.random.uniform(50, 160, n), 1),
        "vacunado": np.random.choice(["Sí", "No"], n, p=[0.8, 0.2]),
        "consultas_anuales": np.random.randint(0, 8, n),
        "imc": np.round(np.random.uniform(12, 22, n), 1),
    })
    return df


@st.cache_data
def cargar_datos():
    ruta = "data/salud_ninos.csv"
    if os.path.exists(ruta):
        return pd.read_csv(ruta)
    else:
        df = generar_datos_ejemplo()
        os.makedirs("data", exist_ok=True)
        df.to_csv(ruta, index=False)
        return df


df = cargar_datos()


# ─────────────────────────────────────────────────────────────
# BARRA LATERAL: FILTROS (original)
# ─────────────────────────────────────────────────────────────
st.sidebar.title("🔎 Filtros")
regiones_disponibles = sorted(df["region"].unique())
regiones_sel = st.sidebar.multiselect(
    "Región", options=regiones_disponibles, default=regiones_disponibles,
)
edad_min, edad_max = int(df["edad"].min()), int(df["edad"].max())
rango_edad = st.sidebar.slider(
    "Rango de edad (años)", min_value=edad_min, max_value=edad_max, value=(edad_min, edad_max),
)
vacunados_sel = st.sidebar.radio("¿Vacunado?", options=["Todos", "Sí", "No"], index=0)

df_filtrado = df[
    (df["region"].isin(regiones_sel)) &
    (df["edad"].between(rango_edad[0], rango_edad[1]))
]
if vacunados_sel != "Todos":
    df_filtrado = df_filtrado[df_filtrado["vacunado"] == vacunados_sel]


# ─────────────────────────────────────────────────────────────
# ENCABEZADO Y MÉTRICAS (original)
# ─────────────────────────────────────────────────────────────
st.title("👶 Panel de Salud Infantil")
st.markdown("Explorá indicadores de salud de niños y niñas de forma interactiva.")
st.markdown("---")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Niños registrados", f"{len(df_filtrado):,}")
col2.metric("Edad promedio", f"{df_filtrado['edad'].mean():.1f} años")
col3.metric("Peso promedio", f"{df_filtrado['peso_kg'].mean():.1f} kg")
col4.metric("% Vacunados", f"{(df_filtrado['vacunado'].eq('Sí').mean()*100):.1f}%")


# ─────────────────────────────────────────────────────────────
# PESTAÑAS PRINCIPALES (se agrega una nueva: Encuestas)
# ─────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["📊 Distribución", "📍 Por Región", "📈 Relaciones", "📋 Datos", "📝 Encuestas"]
)

# ── TAB 1: Distribución (original) ────────────────────────────
with tab1:
    st.subheader("Distribución de edades")
    fig_edad = px.histogram(
        df_filtrado, x="edad", nbins=15, color="vacunado",
        title="Cantidad de niños por edad y estado de vacunación",
        labels={"edad": "Edad (años)", "count": "Cantidad"},
    )
    st.plotly_chart(fig_edad, use_container_width=True)

    st.subheader("Estado de vacunación")
    conteo_vac = df_filtrado["vacunado"].value_counts().reset_index()
    conteo_vac.columns = ["vacunado", "cantidad"]
    fig_pie = px.pie(
        conteo_vac, names="vacunado", values="cantidad",
        title="Proporción de vacunados", color="vacunado",
        color_discrete_map={"Sí": "#2ecc71", "No": "#e74c3c"},
    )
    st.plotly_chart(fig_pie, use_container_width=True)


# ── TAB 2: Por Región (original) ──────────────────────────────
with tab2:
    st.subheader("Peso promedio por región")
    peso_region = (
        df_filtrado.groupby("region", as_index=False)["peso_kg"]
        .mean().round(1).sort_values("peso_kg", ascending=False)
    )
    fig_bar = px.bar(
        peso_region, x="region", y="peso_kg", color="peso_kg",
        title="Peso promedio por región (kg)", color_continuous_scale="Blues", text="peso_kg",
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    st.subheader("Consultas anuales promedio por región")
    consultas_region = (
        df_filtrado.groupby("region", as_index=False)["consultas_anuales"].mean().round(1)
    )
    fig_consultas = px.bar(
        consultas_region, x="region", y="consultas_anuales",
        color="region", title="Consultas anuales promedio",
    )
    st.plotly_chart(fig_consultas, use_container_width=True)


# ── TAB 3: Relaciones (original) ──────────────────────────────
with tab3:
    st.subheader("Edad vs. Peso (por región)")
    fig_scatter = px.scatter(
        df_filtrado, x="edad", y="peso_kg", color="region", size="altura_cm",
        hover_data=["id_nino", "vacunado"], title="Edad vs. Peso (tamaño = altura)",
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

    st.subheader("IMC promedio por grupo de edad")
    df_filtrado = df_filtrado.copy()
    df_filtrado["grupo_edad"] = pd.cut(
        df_filtrado["edad"], bins=[-1, 2, 5, 10, 15], labels=["0-2", "3-5", "6-10", "11-14"],
    )
    imc_grupo = (
        df_filtrado.groupby("grupo_edad", as_index=False, observed=True)["imc"].mean().round(1)
    )
    fig_linea = px.line(
        imc_grupo, x="grupo_edad", y="imc", markers=True,
        title="IMC promedio por grupo de edad",
    )
    st.plotly_chart(fig_linea, use_container_width=True)


# ── TAB 4: Datos (original) ───────────────────────────────────
with tab4:
    st.subheader("Datos filtrados")
    st.write(f"Mostrando **{len(df_filtrado)}** registros de **{len(df)}** totales.")
    st.dataframe(df_filtrado, use_container_width=True, height=400)
    csv = df_filtrado.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Descargar datos filtrados (CSV)",
        data=csv, file_name="datos_filtrados.csv", mime="text/csv",
    )


# ─────────────────────────────────────────────────────────────
# ── TAB 5: ENCUESTAS (NUEVO) ──────────────────────────────────
# ─────────────────────────────────────────────────────────────
with tab5:
    st.subheader("📝 Análisis de encuestas (EpiCollect 5)")
    st.markdown(
        "Subí el archivo CSV exportado desde EpiCollect 5. "
        "La app detecta automáticamente columnas numéricas y categóricas "
        "para generar gráficos exploratorios."
    )

    archivo_subido = st.file_uploader(
        "Seleccioná el CSV de la encuesta",
        type=["csv"],
        help="Exportá el formulario desde EpiCollect 5 como CSV y subilo acá.",
    )

    if archivo_subido is not None:
        try:
            # Leer CSV. Si EpiCollect exporta con encoding distinto, probar "latin-1"
            df_encuesta = pd.read_csv(archivo_subido)
        except UnicodeDecodeError:
            df_encuesta = pd.read_csv(archivo_subido, encoding="latin-1")

        st.success(f"Archivo cargado: **{archivo_subido.name}**")
        st.write(f"Filas: **{len(df_encuesta)}** · Columnas: **{len(df_encuesta.columns)}**")

        # Vista previa
        with st.expander("👀 Vista previa de los datos"):
            st.dataframe(df_encuesta.head(10), use_container_width=True)

        # Clasificar columnas automáticamente
        cols_numericas = df_encuesta.select_dtypes(include=["number"]).columns.tolist()
        cols_categoricas = df_encuesta.select_dtypes(include=["object", "category", "bool"]).columns.tolist()

        st.markdown("---")
        st.subheader("📊 Análisis exploratorio automático")

        # ── Gráficos para columnas categóricas ─────────────────
        if cols_categoricas:
            st.markdown("### Variables categóricas")
            for col in cols_categoricas:
                # Limitar a columnas con pocos valores únicos para evitar ruido
                n_unicos = df_encuesta[col].nunique()
                if n_unicos > 30:
                    st.caption(f"*{col}* tiene {n_unicos} valores únicos. Se omite el gráfico (demasiadas categorías).")
                    continue

                conteo = df_encuesta[col].value_counts().reset_index()
                conteo.columns = [col, "cantidad"]
                fig = px.bar(
                    conteo, x=col, y="cantidad",
                    title=f"Distribución de: {col}",
                    text="cantidad",
                )
                fig.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)

        # ── Gráficos para columnas numéricas ───────────────────
        if cols_numericas:
            st.markdown("### Variables numéricas")
            for col in cols_numericas:
                fig = px.histogram(
                    df_encuesta, x=col, nbins=20,
                    title=f"Distribución de: {col}",
                )
                st.plotly_chart(fig, use_container_width=True)

        # ── Cruce opcional entre una categórica y una numérica ─
        if cols_categoricas and cols_numericas:
            st.markdown("---")
            st.subheader("🔀 Cruce de variables (opcional)")

            col_cat = st.selectbox(
                "Variable categórica (eje X)",
                options=["(ninguna)"] + cols_categoricas,
                index=0,
            )
            col_num = st.selectbox(
                "Variable numérica (eje Y)",
                options=["(ninguna)"] + cols_numericas,
                index=0,
            )

            if col_cat != "(ninguna)" and col_num != "(ninguna)":
                # Limitar categorías para legibilidad
                top_cats = df_encuesta[col_cat].value_counts().head(10).index
                df_cruce = df_encuesta[df_encuesta[col_cat].isin(top_cats)]

                fig_cruce = px.box(
                    df_cruce, x=col_cat, y=col_num,
                    title=f"{col_num} según {col_cat}",
                    points="outliers",
                )
                fig_cruce.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig_cruce, use_container_width=True)

        # ── Tabla completa y descarga ───────────────────────────
        st.markdown("---")
        with st.expander("📋 Ver tabla completa de la encuesta"):
            st.dataframe(df_encuesta, use_container_width=True, height=400)

        csv_encuesta = df_encuesta.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Descargar encuesta original (CSV)",
            data=csv_encuesta,
            file_name="encuesta_epicollect.csv",
            mime="text/csv",
        )

    else:
        st.info("👆 Subí un archivo CSV para comenzar el análisis.")


# ─────────────────────────────────────────────────────────────
# PIE DE PÁGINA
# ─────────────────────────────────────────────────────────────
st.markdown("---")
st.caption("Aplicación desarrollada con Streamlit + Plotly + Pandas · Salud Infantil")
