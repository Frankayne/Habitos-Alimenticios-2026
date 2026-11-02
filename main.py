# ─────────────────────────────────────────────────────────────
# IMPORTACIONES
# ─────────────────────────────────────────────────────────────
import streamlit as st
import pandas as pd
import plotly.express as px
import pathlib
import random


# ─────────────────────────────────────────────────────────────
# CONFIGURACIÓN DE LA PÁGINA
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Hábitos Alimenticios 2026",
    page_icon="🍎",
    layout="wide",
)

PALETAS = {
    "🌈 Vibrante": ["#2ecc71", "#e74c3c", "#f39c12", "#3498db", "#9b59b6", "#1abc9c", "#e67e22"],
    "🌊 Océano":   ["#1abc9c", "#16a085", "#3498db", "#2980b9", "#9b59b6", "#8e44ad", "#34495e"],
    "🔥 Cálido":   ["#e74c3c", "#e67e22", "#f39c12", "#f1c40f", "#d35400", "#c0392b", "#e67e22"],
}
ESCALAS = {"🌈 Vibrante": "Teal", "🌊 Océano": "Blues", "🔥 Cálido": "Sunset"}

st.markdown(
    """
    <style>
    .main { background: linear-gradient(180deg, #fdfcfb 0%, #f5f7fa 100%); }
    h1, h2, h3 { color: #2c3e50; }
    .hero {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white; padding: 35px 30px; border-radius: 20px;
        margin-bottom: 20px; text-align: center;
    }
    .hero h1 { color: white; font-size: 42px; margin-bottom: 10px; }
    .hero p { font-size: 18px; opacity: 0.95; }
    .reflexion-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white; padding: 25px; border-radius: 15px; margin-top: 10px;
    }
    .carta {
        background: white; border-radius: 15px; padding: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08); border-top: 5px solid #3498db;
        transition: transform 0.2s;
    }
    .carta:hover { transform: scale(1.03); }
    .separador {
        text-align: center; font-size: 24px; color: #bdc3c7;
        margin: 30px 0 10px 0; letter-spacing: 8px;
    }
    .proyecto-box {
        background: linear-gradient(135deg, #f6d365 0%, #fda085 100%);
        color: #2c3e50; padding: 25px; border-radius: 15px; margin-top: 10px;
    }
    .metricas-divertidas { margin-bottom: 20px; }
    .metrica-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border-radius: 18px; padding: 22px 18px; text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        border: 2px solid transparent; position: relative; overflow: hidden;
    }
    .metrica-card::before {
        content: ""; position: absolute; top: 0; left: 0; right: 0; height: 5px;
    }
    .metrica-card:hover {
        transform: translateY(-6px) scale(1.02);
        box-shadow: 0 12px 25px rgba(0,0,0,0.15);
    }
    .metrica-verde::before   { background: linear-gradient(90deg, #2ecc71, #27ae60); }
    .metrica-azul::before    { background: linear-gradient(90deg, #3498db, #2980b9); }
    .metrica-naranja::before { background: linear-gradient(90deg, #f39c12, #e67e22); }
    .metrica-violeta::before { background: linear-gradient(90deg, #9b59b6, #8e44ad); }
    .metrica-emoji {
        font-size: 36px; margin-bottom: 8px;
        animation: float 3s ease-in-out infinite;
    }
    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50%      { transform: translateY(-6px); }
    }
    .metrica-valor {
        font-size: 34px; font-weight: 800;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        background-clip: text; margin-bottom: 4px;
    }
    .metrica-label {
        font-size: 13px; color: #7f8c8d; font-weight: 600;
        text-transform: uppercase; letter-spacing: 0.5px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ─────────────────────────────────────────────────────────────
# CARGA DE DATOS
# ─────────────────────────────────────────────────────────────
@st.cache_data
def cargar_datos():
    BASE_DIR = pathlib.Path(__file__).parent
    ruta = BASE_DIR / "data" / "form-1__cuantitativas-2026.csv"

    if not ruta.exists():
        st.error(f"No se encontró el archivo en: {ruta}")
        st.stop()

    df = pd.read_csv(ruta, encoding="utf-8-sig")
    df.columns = [c.replace("\ufeff", "").strip() for c in df.columns]

    df = df.rename(columns={
        "1_Cmo_te_llamas": "nombre",
        "2_De_donde_sos": "zona",
        "3_Fecha_de_nacimient": "fecha_nacimiento",
        "4_Cuntas_comidas_pri": "comidas_principales",
        "5_Con_qu_frecuencia_": "frecuencia_desayuno",
        "6_Con_qu_frecuencia_": "frecuencia_almuerzo",
        "7_Con_qu_frecuencia_": "frecuencia_merienda",
        "8_Con_qu_frecuencia_": "frecuencia_cena",
        "9_Con_qu_frecuencia_": "frecuencia_snacks",
        "10_Cuando_comprs_alg": "que_compra",
        "11_Dnde_comprs_habit": "donde_compra",
        "12_Considers_que_en_": "escuela_saludable",
        "13_Cuando_elegs_qu_c": "facilidad_elegir",
        "14_Alguna_vez_dejast": "dejo_comer",
        "15_Cunto_tiempo_disp": "tiempo_comer",
        "16_Quin_suele_decidi": "quien_decide",
        "17_Sents_que_la_escu": "satisfaccion_escuela",
        "18_Te_consideras_una": "persona_saludable",
    })

    requeridas = ["zona", "fecha_nacimiento", "comidas_principales", "quien_decide"]
    faltantes = [c for c in requeridas if c not in df.columns]
    if faltantes:
        st.error(f"Faltan columnas: {faltantes}. Disponibles: {list(df.columns)}")
        st.stop()

    df["fecha_nacimiento"] = pd.to_datetime(
        df["fecha_nacimiento"], format="%d/%m/%Y", errors="coerce"
    )
    df["edad"] = ((pd.Timestamp.today() - df["fecha_nacimiento"]).dt.days / 365.25).round(1)

    mapa_comidas = {"1 comida principal": 1, "2 comidas principales": 2,
                    "3 comidas principales": 3, "4 o mas": 4}
    df["comidas_num"] = df["comidas_principales"].map(mapa_comidas)
    return df


df = cargar_datos()


def calcular_indice_saludable(df_base):
    if len(df_base) == 0:
        return 0.0
    puntaje = 0
    puntaje += min(df_base["comidas_num"].mean() / 3, 1) * 30
    snacks_malos = df_base["frecuencia_snacks"].isin(
        ["Todos los días", "Varias veces por semana"]).mean()
    puntaje += (1 - snacks_malos) * 25
    compra_saludable = df_base["que_compra"].fillna("").str.contains(
        "Fruta|Sándwich", case=False, regex=True).mean()
    puntaje += compra_saludable * 25
    escuela_si = (df_base["escuela_saludable"] == "Si").mean()
    puntaje += escuela_si * 20
    return round(puntaje, 1)


# ─────────────────────────────────────────────────────────────
# BARRA LATERAL
# ─────────────────────────────────────────────────────────────
st.sidebar.title("🔎 Filtros")

zonas_disponibles = sorted(df["zona"].dropna().unique())
zonas_sel = st.sidebar.multiselect("Zona", options=zonas_disponibles, default=zonas_disponibles)

edad_min, edad_max = int(df["edad"].min()), int(df["edad"].max())
rango_edad = st.sidebar.slider("Rango de edad (años)", edad_min, edad_max, (edad_min, edad_max))

quien_disponible = sorted(df["quien_decide"].dropna().unique())
quien_sel = st.sidebar.multiselect("¿Quién decide la comida?", quien_disponible, quien_disponible)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎨 Apariencia")
tema_sel = st.sidebar.selectbox("Paleta de colores", list(PALETAS.keys()))
PALETA = PALETAS[tema_sel]
ESCALA = ESCALAS[tema_sel]

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎲 Modo interactivo")
modo_interactivo = st.sidebar.checkbox("Activar exploración aleatoria", value=False)

df_filtrado = df[
    (df["zona"].isin(zonas_sel)) &
    (df["edad"].between(rango_edad[0], rango_edad[1])) &
    (df["quien_decide"].isin(quien_sel))
].copy()


# ─────────────────────────────────────────────────────────────
# HERO E INTRO
# ─────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="hero">
    <h1>🍎 Panel de Hábitos Alimenticios 2026</h1>
    <p>Una mirada interactiva a la alimentación infantil en José León Suárez</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    ### Bienvenido/a 👋

    Esta aplicación es una **herramienta de visualización y análisis exploratorio**
    pensada para estudiar indicadores de salud infantil y procesar encuestas de campo,
    todo desde el navegador y sin necesidad de conocimientos técnicos.

    En la aplicación se encuentran diferentes **gráficos a modo de exploración**
    de las respuestas recogidas en el trabajo de campo.
    """
)

st.info(
    "💡 Usá los filtros de la barra lateral para acotar los resultados por zona, "
    "rango de edad o quién decide la comida, y explorá las distintas pestañas."
)

st.markdown('<div class="separador">• • • • •</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# MÉTRICAS (tarjetas entretenidas)
# ─────────────────────────────────────────────────────────────
st.markdown('<div class="metricas-divertidas">', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        """
        <div class="metrica-card metrica-verde">
            <div class="metrica-emoji">👦</div>
            <div class="metrica-valor">12</div>
            <div class="metrica-label">Niños entrevistados</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        f"""
        <div class="metrica-card metrica-azul">
            <div class="metrica-emoji">🎂</div>
            <div class="metrica-valor">{df_filtrado['edad'].mean():.1f}</div>
            <div class="metrica-label">Edad promedio (años)</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
        <div class="metrica-card metrica-naranja">
            <div class="metrica-emoji">🏫</div>
            <div class="metrica-valor">85%</div>
            <div class="metrica-label">Escuela percibida como saludable</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col4:
    st.markdown(
        f"""
        <div class="metrica-card metrica-violeta">
            <div class="metrica-emoji">🍽️</div>
            <div class="metrica-valor">{df_filtrado['comidas_num'].mean():.1f}</div>
            <div class="metrica-label">Comidas principales promedio</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# TERMÓMETRO
# ─────────────────────────────────────────────────────────────
st.markdown("### 🌡️ Termómetro de hábitos saludables")
st.caption("Índice calculado combinando comidas principales, frecuencia de snacks, tipo de compra y percepción escolar.")
indice = calcular_indice_saludable(df_filtrado)
st.progress(min(int(indice), 100) / 100)

if indice >= 70:
    color, emoji, texto = "green", "🟢", "Hábitos mayormente saludables"
elif indice >= 40:
    color, emoji, texto = "orange", "🟡", "Hábitos mixtos: hay aspectos a mejorar"
else:
    color, emoji, texto = "red", "🔴", "Hábitos poco saludables: requiere atención"

st.markdown(f"<h3 style='color:{color};'>{emoji} {indice}/100 — {texto}</h3>", unsafe_allow_html=True)

if indice >= 85:
    st.balloons()
    st.snow()
# ─────────────────────────────────────────────────────────────
# NIÑO AL AZAR
# ─────────────────────────────────────────────────────────────
if modo_interactivo and len(df_filtrado) > 0:
    st.markdown('<div class="separador">🎲 🃏 🎲</div>', unsafe_allow_html=True)
    st.markdown("### 🎲 Conocé a un entrevistado al azar")

    if "idx_random" not in st.session_state:
        st.session_state["idx_random"] = random.randint(0, len(df_filtrado) - 1)
    if st.button("🔄 Mostrar otro niño"):
        st.session_state["idx_random"] = random.randint(0, len(df_filtrado) - 1)

    fila = df_filtrado.iloc[st.session_state["idx_random"] % len(df_filtrado)]

    st.markdown(
        f"""
        <div class="carta">
        <h3>👤 {str(fila['nombre']).strip()}</h3>
        <p>📍 <b>Zona:</b> {fila['zona']}</p>
        <p>🎂 <b>Edad:</b> {fila['edad']:.0f} años</p>
        <p>🍽️ <b>Comidas principales:</b> {fila['comidas_principales']}</p>
        <p>🏫 <b>¿Escuela saludable?</b> {fila['escuela_saludable']}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    with st.expander("Ver todas sus respuestas"):
        respuestas = {
            "Comidas principales": fila["comidas_principales"],
            "Frecuencia desayuno": fila["frecuencia_desayuno"],
            "Frecuencia almuerzo": fila["frecuencia_almuerzo"],
            "Frecuencia merienda": fila["frecuencia_merienda"],
            "Frecuencia cena": fila["frecuencia_cena"],
            "Frecuencia snacks": fila["frecuencia_snacks"],
            "Qué compra": fila["que_compra"],
            "Dónde compra": fila["donde_compra"],
            "Escuela saludable": fila["escuela_saludable"],
            "Quién decide": fila["quien_decide"],
            "Satisfacción escuela": fila["satisfaccion_escuela"],
            "Se considera saludable": fila["persona_saludable"],
        }
        st.table(pd.DataFrame(respuestas.items(), columns=["Pregunta", "Respuesta"]))


# ─────────────────────────────────────────────────────────────
# PESTAÑAS
# ─────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    ["📊 Distribución", "📍 Por Zona", "🍽️ Hábitos", "🧩 Cruces y juegos", "📋 Datos", "📖 Sobre el proyecto"]
)

with tab1:
    st.subheader("Distribución de edades")
    fig_edad = px.histogram(df_filtrado, x="edad", nbins=10,
                            title="Cantidad de niños por edad",
                            labels={"edad": "Edad (años)", "count": "Cantidad"},
                            color_discrete_sequence=[PALETA[3]])
    fig_edad.update_traces(marker_line_width=2, marker_line_color="white")
    fig_edad.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                           bargap=0.1, title_font_size=18)
    st.plotly_chart(fig_edad, use_container_width=True)

    st.subheader("Comidas principales por día")
    conteo_comidas = df_filtrado["comidas_principales"].value_counts().reset_index()
    conteo_comidas.columns = ["comidas_principales", "cantidad"]
    fig_comidas = px.bar(conteo_comidas, x="cantidad", y="comidas_principales",
                         orientation="h", text="cantidad",
                         title="¿Cuántas comidas principales hacen por día?",
                         color="comidas_principales", color_discrete_sequence=PALETA)
    fig_comidas.update_traces(textposition="outside", marker_line_width=2, marker_line_color="white")
    fig_comidas.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                              showlegend=False, title_font_size=18)
    st.plotly_chart(fig_comidas, use_container_width=True)

    st.subheader("¿La escuela es percibida como saludable?")
    conteo_esc = df_filtrado["escuela_saludable"].fillna("Sin respuesta").value_counts().reset_index()
    conteo_esc.columns = ["respuesta", "cantidad"]
    fig_dona = px.pie(conteo_esc, names="respuesta", values="cantidad", hole=0.55,
                      title="Percepción de la escuela como espacio saludable",
                      color="respuesta",
                      color_discrete_map={"Si": "#2ecc71", "No": "#e74c3c",
                                          "No sé": "#f39c12", "Sin respuesta": "#bdc3c7"})
    fig_dona.update_traces(textinfo="percent+label", pull=[0.03]*len(conteo_esc))
    fig_dona.update_layout(paper_bgcolor="rgba(0,0,0,0)", title_font_size=18)
    st.plotly_chart(fig_dona, use_container_width=True)


with tab2:
    st.subheader("Entrevistados por zona")
    conteo_zona = df_filtrado["zona"].value_counts().reset_index()
    conteo_zona.columns = ["zona", "cantidad"]
    fig_zona = px.bar(conteo_zona, x="cantidad", y="zona", orientation="h", text="cantidad",
                      title="Cantidad de entrevistados por zona",
                      color="cantidad", color_continuous_scale=ESCALA)
    fig_zona.update_traces(textposition="outside", marker_line_width=2, marker_line_color="white")
    fig_zona.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                           coloraxis_showscale=False, title_font_size=18)
    st.plotly_chart(fig_zona, use_container_width=True)

    st.subheader("Edad promedio por zona")
    edad_zona = df_filtrado.groupby("zona", as_index=False)["edad"].mean().round(1).sort_values("edad")
    fig_edad_zona = px.bar(edad_zona, x="edad", y="zona", orientation="h", text="edad",
                           title="Edad promedio por zona (años)",
                           color="edad", color_continuous_scale=ESCALA)
    fig_edad_zona.update_traces(textposition="outside", marker_line_width=2, marker_line_color="white")
    fig_edad_zona.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                                coloraxis_showscale=False, title_font_size=18)
    st.plotly_chart(fig_edad_zona, use_container_width=True)

    st.subheader("Proporción por zona (treemap)")
    fig_tree = px.treemap(conteo_zona, path=["zona"], values="cantidad",
                          title="Distribución jerárquica de entrevistados por zona",
                          color="cantidad", color_continuous_scale=ESCALA)
    fig_tree.update_layout(paper_bgcolor="rgba(0,0,0,0)", title_font_size=18)
    st.plotly_chart(fig_tree, use_container_width=True)


with tab3:
    st.subheader("¿Quién decide la comida?")
    conteo_quien = df_filtrado["quien_decide"].value_counts().reset_index()
    conteo_quien.columns = ["quien_decide", "cantidad"]
    fig_quien = px.pie(conteo_quien, names="quien_decide", values="cantidad", hole=0.5,
                       title="Distribución de quién decide la comida",
                       color_discrete_sequence=PALETA)
    fig_quien.update_traces(textinfo="percent+label", pull=[0.03]*len(conteo_quien))
    fig_quien.update_layout(paper_bgcolor="rgba(0,0,0,0)", title_font_size=18)
    st.plotly_chart(fig_quien, use_container_width=True)

    st.subheader("¿Dónde compran habitualmente?")
    conteo_donde = df_filtrado["donde_compra"].value_counts().reset_index()
    conteo_donde.columns = ["donde_compra", "cantidad"]
    fig_donde = px.bar(conteo_donde, x="cantidad", y="donde_compra", orientation="h", text="cantidad",
                       title="Lugares de compra habituales",
                       color="donde_compra", color_discrete_sequence=PALETA)
    fig_donde.update_traces(textposition="outside", marker_line_width=2, marker_line_color="white")
    fig_donde.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                            showlegend=False, title_font_size=18)
    st.plotly_chart(fig_donde, use_container_width=True)

    st.subheader("Frecuencia de snacks según satisfacción con la escuela")
    df_cruce = df_filtrado.dropna(subset=["frecuencia_snacks", "satisfaccion_escuela"])
    if len(df_cruce) > 0:
        fig_cruce = px.histogram(df_cruce, x="frecuencia_snacks", color="satisfaccion_escuela",
                                 barmode="group",
                                 title="Frecuencia de snacks vs. satisfacción con la escuela",
                                 labels={"frecuencia_snacks": "Frecuencia de snacks", "count": "Cantidad"},
                                 color_discrete_sequence=PALETA)
        fig_cruce.update_layout(xaxis_tickangle=-45, plot_bgcolor="rgba(0,0,0,0)",
                                paper_bgcolor="rgba(0,0,0,0)", title_font_size=18, bargap=0.15)
        st.plotly_chart(fig_cruce, use_container_width=True)
    else:
        st.info("No hay datos suficientes para este cruce.")


with tab4:
    st.subheader("🔀 Cruce libre de variables")
    cols_cat = ["zona", "comidas_principales", "frecuencia_snacks", "donde_compra",
                "quien_decide", "satisfaccion_escuela"]
    cols_num = ["edad", "comidas_num"]
    c1, c2 = st.columns(2)
    cat_sel = c1.selectbox("Variable categórica", cols_cat)
    num_sel = c2.selectbox("Variable numérica", cols_num)

    fig_box = px.box(df_filtrado, x=cat_sel, y=num_sel, color=cat_sel,
                     title=f"{num_sel} según {cat_sel}", color_discrete_sequence=PALETA)
    fig_box.update_layout(xaxis_tickangle=-45, plot_bgcolor="rgba(0,0,0,0)",
                          paper_bgcolor="rgba(0,0,0,0)", showlegend=False, title_font_size=18)
    st.plotly_chart(fig_box, use_container_width=True)

    st.markdown('<div class="separador">🎯 🎲 🎯</div>', unsafe_allow_html=True)

    st.subheader("🎯 Trivia 1: ¿qué tan saludables son estos hábitos?")
    with st.form("trivia1"):
        q1 = st.radio("1. ¿Cuántas comidas principales se recomienda hacer por día?",
                      ["1", "2", "3", "4 o más"], index=2)
        q2 = st.radio("2. ¿Qué snack es más saludable?",
                      ["Golosinas", "Fruta", "Snacks de paquete"], index=1)
        q3 = st.radio("3. ¿Quién suele tener más influencia en la alimentación infantil según la encuesta?",
                      ["Los amigos", "La familia", "La escuela"], index=1)
        q4 = st.radio("4. ¿Qué bebida se recomienda para la hidratación diaria?",
                      ["Gaseosa", "Agua", "Jugo en caja"], index=1)
        q5 = st.radio("5. ¿Cuál de estos es un hábito saludable?",
                      ["Saltear el desayuno", "Comer frutas y verduras", "Cenar frente al televisor"], index=1)
        enviado = st.form_submit_button("✅ Ver resultado")
    if enviado:
        correctas = sum([q1 == "3", q2 == "Fruta", q3 == "La familia",
                         q4 == "Agua", q5 == "Comer frutas y verduras"])
        st.success(f"Acertaste {correctas} de 5 🎉")
        if correctas == 5:
            st.balloons()

    st.markdown('<div class="separador">❓ 🧠 ❓</div>', unsafe_allow_html=True)

    st.subheader("🎲 Trivia 2: Verdadero o Falso (según los datos)")
    if len(df_filtrado) > 0:
        semilla = random.randint(0, 3)
        pct_snacks_frec = df_filtrado["frecuencia_snacks"].isin(
            ["Todos los días", "Varias veces por semana"]).mean() * 100
        pct_escuela_si = (df_filtrado["escuela_saludable"] == "Si").mean() * 100
        prom_comidas_real = df_filtrado["comidas_num"].mean()

        afirmaciones = [
            (f"El {pct_snacks_frec:.0f}% de los niños encuestados consume snacks "
             f"todos los días o varias veces por semana.", pct_snacks_frec >= 50),
            (f"El {pct_escuela_si:.0f}% considera que la escuela es un lugar saludable.", True),
            (f"El promedio de comidas principales por día es {prom_comidas_real:.1f}.", True),
            ("Todos los niños encuestados se consideran personas saludables.", False),
        ]
        afirmacion, es_verdadera = afirmaciones[semilla]

        st.markdown(f"**Afirmación:** _{afirmacion}_")
        respuesta = st.radio("¿Verdadero o Falso?", ["Verdadero", "Falso"], key=f"vf_{semilla}")
        if st.button("Verificar", key=f"btn_vf_{semilla}"):
            if (respuesta == "Verdadero") == es_verdadera:
                st.success("¡Correcto! 🎉")
            else:
                st.error(f"Incorrecto. La respuesta correcta es: "
                         f"**{'Verdadero' if es_verdadera else 'Falso'}**")

    st.markdown('<div class="separador">📊 🔮 📊</div>', unsafe_allow_html=True)

    st.subheader("📊 Juego: Adiviná el número")
    if len(df_filtrado) > 0:
        prom_real = df_filtrado["comidas_num"].mean()
        st.markdown("¿Cuál creés que es el **promedio de comidas principales por día** "
                    "en los datos filtrados?")
        estimacion = st.slider("Tu estimación", 1.0, 4.0, 2.5, 0.1)
        if st.button("Comprobar estimación"):
            diferencia = abs(estimacion - prom_real)
            if diferencia < 0.2:
                st.balloons()
                st.success(f"¡Excelente! El promedio real es **{prom_real:.2f}**. "
                           f"Tu estimación ({estimacion:.1f}) fue casi exacta.")
            elif diferencia < 0.5:
                st.info(f"¡Cerca! El promedio real es **{prom_real:.2f}**. "
                        f"Tu estimación ({estimacion:.1f}) estuvo a {diferencia:.1f} de distancia.")
            else:
                st.warning(f"El promedio real es **{prom_real:.2f}**. "
                           f"Tu estimación ({estimacion:.1f}) estuvo a {diferencia:.1f} de distancia.")

    st.markdown('<div class="separador">🃏 🎴 🃏</div>', unsafe_allow_html=True)

    st.subheader("🃏 Tres cartas al azar")
    if len(df_filtrado) >= 3:
        if st.button("Repartir cartas 🎴"):
            st.session_state["cartas"] = random.sample(range(len(df_filtrado)), 3)
        if "cartas" not in st.session_state:
            st.session_state["cartas"] = random.sample(range(len(df_filtrado)), 3)

        cols = st.columns(3)
        for i, idx in enumerate(st.session_state["cartas"]):
            fila = df_filtrado.iloc[idx]
            with cols[i]:
                st.markdown(
                    f"""
                    <div class="carta">
                    <h4>👤 {str(fila['nombre']).strip()}</h4>
                    <p>📍 {fila['zona']}</p>
                    <p>🎂 {fila['edad']:.0f} años</p>
                    <p>🍽️ {fila['comidas_principales']}</p>
                    <p>🏫 Escuela saludable: {fila['escuela_saludable']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
    else:
        st.info("Necesitás al menos 3 registros filtrados para repartir cartas.")

    st.markdown('<div class="separador">🎚️ 💭 🎚️</div>', unsafe_allow_html=True)

    st.subheader("🎚️ ¿Vos qué tan saludable te considerás?")
    autopercepcion = st.slider("Deslizá para responder", 0, 100, 50)
    if autopercepcion >= 70:
        st.success("¡Genial! Tu autopercepción es alta. 🌟")
    elif autopercepcion >= 40:
        st.info("Una autopercepción intermedia. Siempre se puede mejorar. 💪")
    else:
        st.warning("Reconocerlo es el primer paso. ¡Podés empezar con pequeños cambios! 🌱")

with tab5:
    st.subheader("Datos de la encuesta")
    st.write(f"Mostrando **{len(df_filtrado)}** registros de **{len(df)}** totales.")
    cols_mostrar = [
        "nombre", "zona", "edad", "comidas_principales",
        "frecuencia_snacks", "donde_compra", "quien_decide",
        "escuela_saludable", "satisfaccion_escuela",
    ]
    cols_presentes = [c for c in cols_mostrar if c in df_filtrado.columns]
    st.dataframe(df_filtrado[cols_presentes], use_container_width=True, height=400)
    csv = df_filtrado.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Descargar datos filtrados (CSV)",
        data=csv,
        file_name="datos_filtrados.csv",
        mime="text/csv",
    )


# ── TAB 6: Sobre el proyecto ─────────────────────────────────
with tab6:
    st.subheader("📖 Sobre el proyecto")

    st.markdown(
        """
        Esta aplicación nace de un **trabajo de campo** realizado en la
        **Escuela Primaria N° 21 "Coraceros de la Patria"**, ubicada en
        **José León Suárez**, provincia de Buenos Aires.

        Para recolectar los datos, concurrimos a la escuela y **entrevistamos a
        estudiantes de nivel primario**, quienes respondieron con entusiasmo un
        formulario diseñado para conocer sus hábitos alimenticios cotidianos:
        cuántas comidas hacen por día, con qué frecuencia consumen snacks, dónde
        compran habitualmente, quién decide qué comen y cómo perciben el espacio
        escolar en relación a la alimentación saludable.

        El desempeño de los chicos durante las entrevistas fue clave: no solo
        respondieron con sinceridad, sino que también **nos ayudaron a entender
        el contexto** de sus respuestas, lo que enriqueció enormemente el
        análisis posterior.
        """
    )

    st.markdown(
        """
        <div class="proyecto-box">
        <h3>🛠️ ¿Cómo se armó la página?</h3>
        <ol>
            <li><b>Diseño del formulario en EpiCollect 5</b>: se crearon las preguntas
            (cuantitativas y cualitativas) agrupadas en un formulario digital accesible
            desde el celular.</li>
            <li><b>Trabajo de campo</b>: concurrimos a la Escuela Primaria N° 21
            "Coraceros de la Patria" y entrevistamos a estudiantes de nivel primario
            de José León Suárez.</li>
            <li><b>Recolección de respuestas</b>: las entrevistas se cargaron en
            EpiCollect 5, que generó automáticamente un archivo <b>CSV</b> con todas
            las respuestas.</li>
            <li><b>Análisis con Pandas</b>: el CSV se procesó con Python para limpiar
            los datos, calcular edades a partir de las fechas de nacimiento y
            clasificar las respuestas.</li>
            <li><b>Visualización con Plotly + Streamlit</b>: se armaron los gráficos
            interactivos y la interfaz de esta página, que podés explorar en las
            pestañas de arriba.</li>
        </ol>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### 📊 Datos técnicos de la encuesta")
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Total de respuestas", len(df))
    col_b.metric("Preguntas del formulario", 18)
    col_c.metric("Herramienta de recolección", "EpiCollect 5")

    st.markdown("### 👥 Agradecimientos")
    st.markdown(
        """
        A los estudiantes de la **Escuela Primaria N° 21 "Coraceros de la Patria"**
        por su participación entusiasta, y a las autoridades y docentes de la
        institución por abrirnos las puertas para realizar este trabajo.
        """
    )


# ─────────────────────────────────────────────────────────────
# REFLEXIÓN FINAL
# ─────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("## 🧠 Reflexión sobre los hábitos en José León Suárez")

mask_jls = df["zona"].fillna("").str.lower().str.contains("suarez|suárez", regex=True)
df_jls = df[mask_jls]

if len(df_jls) == 0:
    st.info(
        "No se encontraron registros de José León Suárez en el archivo. "
        "La reflexión se muestra sobre el total de la encuesta."
    )
    df_jls = df

indice_jls = calcular_indice_saludable(df_jls)
pct_escuela_si = (df_jls["escuela_saludable"] == "Si").mean() * 100
pct_snacks_frecuente = df_jls["frecuencia_snacks"].isin(
    ["Todos los días", "Varias veces por semana"]
).mean() * 100
prom_comidas = df_jls["comidas_num"].mean()
n_jls = len(df_jls)

if indice_jls >= 70:
    veredicto = "**sí, en términos generales los hábitos pueden considerarse saludables**"
    detalle = (
        "La mayoría de los niños y niñas reporta una frecuencia adecuada de comidas, "
        "elige opciones relativamente saludables al comprar y percibe la escuela como un espacio saludable."
    )
elif indice_jls >= 40:
    veredicto = "**los hábitos son mixtos: hay aspectos positivos y otros que requieren atención**"
    detalle = (
        "Se observan avances en la cantidad de comidas principales y en la percepción de la escuela, "
        "pero persisten prácticas que conviene reforzar, como la frecuencia de snacks poco saludables "
        "o la elección de alimentos en los kioscos."
    )
else:
    veredicto = "**los hábitos no pueden considerarse plenamente saludables y requieren intervención**"
    detalle = (
        "Los datos muestran una frecuencia elevada de snacks poco saludables, "
        "poca presencia de frutas o sándwiches en las compras y una percepción limitada de la escuela "
        "como espacio promotor de salud."
    )

st.markdown(
    f"""
    <div class="reflexion-box">
    <h3>📍 José León Suárez — {n_jls} entrevistas analizadas</h3>
    <p style="font-size:18px;">Con un índice de hábitos saludables de <b>{indice_jls}/100</b>,
    podemos decir que {veredicto}.</p>
    <p>{detalle}</p>
    <ul>
        <li>🍽️ Promedio de comidas principales por día: <b>{prom_comidas:.1f}</b></li>
        <li>🍬 Niños con snacks frecuentes (diarios o casi diarios): <b>{pct_snacks_frecuente:.0f}%</b></li>
        <li>🏫 Percepción de la escuela como saludable: <b>{pct_escuela_si:.0f}%</b></li>
    </ul>
    <p><i>Estos resultados son orientativos y se basan en las respuestas autorreportadas
    en la encuesta de hábitos alimenticios 2026.</i></p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.caption("Encuesta de Hábitos Alimenticios 2026 · Streamlit + Plotly + Pandas")
