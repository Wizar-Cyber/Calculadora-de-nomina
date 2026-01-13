import streamlit as st
import json
import pandas as pd
from models.turno import Turno
from services.calculadora import CalculadoraNomina
from config import SALARIO_QUINCENA, VALOR_HORA, HORAS_JORNADA
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

# UI: fondo y estilos globales (colores, botones, responsive)
# Cargar imagen en base64
import os
fondo_path = os.path.join(os.path.dirname(__file__), "fondo_base64.txt")
if os.path.exists(fondo_path):
    with open(fondo_path, "r", encoding="utf-8") as f:
        fondo_base64 = f.read()
else:
    # Fallback a imagen por defecto
    fondo_base64 = "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"

# Agregar CSS personalizado para el fondo
st.markdown(f"""
    <style>
        /* Fondo para toda la página */
        .stApp {{
            background: linear-gradient(rgba(0, 0, 0, 0.75), rgba(0, 0, 0, 0.75)), 
                        url('{fondo_base64}') no-repeat center center fixed;
            background-size: cover;
            background-attachment: fixed;
        }}
        
        /* Labels en blanco con mejor contraste - TODOS */
        label {{
            color: white !important;
            font-weight: 600;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.7);
        }}

        /* Texto de widgets (checkbox/radio) en blanco */
        div[data-testid="stCheckbox"] span,
        div[data-testid="stRadio"] span,
        div[data-testid="stRadio"] p,
        div[data-testid="stCheckbox"] p {{
            color: white !important;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.7);
        }}
        
        .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {{
            color: white !important;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.7);
        }}
        
        /* Selectbox con ancho full */
        .stSelectbox {{
            width: 100% !important;
        }}
        
        .stSelectbox > div > div > select {{
            background-color: rgba(255, 255, 255, 0.95) !important;
            color: #000 !important;
            border-radius: 5px;
            height: 40px !important;
            width: 100% !important;
        }}
        
        /* Inputs de texto */
        .stTextInput > div > div > input {{
            background-color: rgba(255, 255, 255, 0.95) !important;
            color: #000 !important;
            border-radius: 5px;
            height: 40px !important;
        }}
        
        /* Form container - simetrico con selectbox */
        .stForm {{
            background-color: rgba(0, 0, 0, 0.15) !important;
            padding: 15px !important;
            border-radius: 8px;
            border: 1px solid rgba(255, 255, 255, 0.15);
            margin-top: -8px !important;
        }}
        
        /* Botones */
        .stButton > button {{
            background-color: rgba(31, 119, 180, 0.95) !important;
            color: white !important;
            font-weight: bold;
            border-radius: 5px;
            border: none !important;
            height: 40px !important;
            font-size: 14px !important;
            white-space: nowrap !important;
            overflow: hidden !important;
            text-overflow: ellipsis !important;
        }}
        
        .stButton > button:hover {{
            background-color: rgba(31, 119, 180, 1) !important;
        }}
        
        /* Títulos */
        h1, h2, h3, h4, h5 {{
            color: white !important;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.9) !important;
            word-break: break-word;
        }}
        
        /* Título principal responsivo */
        h1 {{
            font-size: 2.5rem !important;
            line-height: 1.1 !important;
        }}
        
        /* Divisores en BLANCO */
        hr {{
            border-color: rgba(255, 255, 255, 0.7) !important;
            border-width: 1px !important;
            margin: 15px 0 !important;
        }}
        
        /* Metrics */
        [data-testid="metric-container"] {{
            background-color: rgba(0, 0, 0, 0.4);
            padding: 15px;
            border-radius: 10px;
        }}
        
        [data-testid="metric-container"] .metric-text {{
            color: white !important;
        }}
        
        [data-testid="metric-container"] p {{
            color: white !important;
        }}
        
        [data-testid="metric-label"] {{
            color: white !important;
        }}

        [data-testid="metric-container"] [data-testid="stMetricValue"] {{
            color: white !important;
        }}

        [data-testid="metric-container"] [data-testid="stMetricValue"] * {{
            color: white !important;
        }}

        [data-testid="metric-container"] [data-testid="stMetricValue"] > div {{
            color: white !important;
        }}

        [data-testid="metric-container"] [data-testid="stMetricValue"] > div * {{
            color: white !important;
        }}

        [data-testid="metric-container"] [data-testid="stMetricValue"] [data-component-name="<div />"] {{
            color: white !important;
        }}

        [data-testid="metric-container"] [data-component-name="<div />"] {{
            color: white !important;
        }}
        
        [data-testid="metric-container"] .stMetric {{
            color: white !important;
        }}
        
        div[data-testid="metric-container"] > div {{
            color: white !important;
        }}
        
        div[data-testid="metric-container"] span {{
            color: white !important;
        }}

        div[data-testid="stDataFrame"] {{
            background: transparent !important;
        }}

        div[data-testid="stDataFrame"] * {{
            background: transparent !important;
        }}

        div[data-testid="stDataEditor"] {{
            background: transparent !important;
        }}

        div[data-testid="stDataEditor"] * {{
            background: transparent !important;
        }}

        /* Data editor/grid: dejar celdas y header transparentes pero texto legible */
        div[data-testid="stDataFrame"] [role="grid"],
        div[data-testid="stDataEditor"] [role="grid"],
        div[data-testid="stDataFrame"] [role="grid"] * ,
        div[data-testid="stDataEditor"] [role="grid"] * {{
            background-color: transparent !important;
        }}

        div[data-testid="stDataFrame"] [role="columnheader"],
        div[data-testid="stDataEditor"] [role="columnheader"],
        div[data-testid="stDataFrame"] [role="gridcell"],
        div[data-testid="stDataEditor"] [role="gridcell"] {{
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
            border-color: rgba(255, 255, 255, 0.25) !important;
        }}
        
        /* Responsive para móvil */
        @media (max-width: 640px) {{
            h1 {{
                font-size: 1.8rem !important;
                line-height: 1.1 !important;
                margin-bottom: 0.5rem !important;
            }}
            
            h2, .stSubheader {{
                font-size: 1.4rem !important;
            }}
            
            .stWrite, .stMarkdown {{
                font-size: 0.95rem !important;
            }}
            
            .stButton > button {{
                font-size: 12px !important;
                height: 36px !important;
                padding: 6px 10px !important;
                white-space: normal !important;
                overflow: visible !important;
                text-overflow: clip !important;
            }}
            
            label {{
                font-size: 0.95rem !important;
            }}

            /* En móvil permitir que las columnas se apilen normalmente */
            div[data-testid="stHorizontalBlock"] {{
                flex-wrap: wrap !important;
                overflow-x: hidden !important;
            }}

            /* Registros: en móvil mantener una sola fila con scroll horizontal */
            .registros div[data-testid="stHorizontalBlock"] {{
                flex-wrap: nowrap !important;
                overflow-x: auto !important;
                gap: 8px !important;
            }}

            .registros div[data-testid="column"] {{
                flex: 0 0 auto !important;
            }}
        }}
    </style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=3600)
def _cargar_turnos_base():
    with open("turnos.json", encoding="utf-8") as f:
        data = json.load(f)
    return {t["codigo"]: Turno(t) for t in data}

if "calc" not in st.session_state:
    st.session_state.quincena = "30"
    st.session_state.calc = CalculadoraNomina(quincena="30")
    st.session_state.turnos_reg = []
    st.session_state.deducciones_reg = []
    st.session_state.expandir_dispo = False
    st.session_state.expandir_extras = False
    st.session_state.expandir_deduccion = False

turnos_base = _cargar_turnos_base()


# Recalcula la nómina cuando cambia la quincena:
# reinicia la calculadora, mantiene los registros y re-agrega cada ítem.
def _recalcular_por_quincena():
    quincena = st.session_state.select_quincena
    if quincena == st.session_state.quincena:
        return

    st.session_state.quincena = quincena
    turnos_temp = st.session_state.turnos_reg.copy()
    st.session_state.calc = CalculadoraNomina(quincena=quincena)
    st.session_state.turnos_reg = turnos_temp

    for codigo_tmp, _, _ in turnos_temp:
        if codigo_tmp in turnos_base:
            t = turnos_base[codigo_tmp]
            st.session_state.calc.agregar_turno(t)
        elif codigo_tmp == "SUSP":
            st.session_state.calc.agregar_suspension()
        elif codigo_tmp == "LIC":
            st.session_state.calc.agregar_licencia()
        elif codigo_tmp == "CP":
            st.session_state.calc.agregar_cp()
        elif codigo_tmp == "INCAP":
            st.session_state.calc.agregar_incapacidad()
        elif codigo_tmp == "DISPO":
            pass

    for nombre, valor in st.session_state.deducciones_reg:
        st.session_state.calc.agregar_deduccion_manual(nombre, valor)

    st.rerun()


# Limpia el mensaje de error de turno al modificar el input.
def _limpiar_error_turno():
    st.session_state.turno_error = ""

st.title("🧮 Nómina Conductores TA")

col1,col2 = st.columns(2)

with col1:
    if "turno_error" not in st.session_state:
        st.session_state.turno_error = ""

    with st.container(border=True):
        st.selectbox(
            "Quincena",
            ["15", "30"],
            key="select_quincena",
            on_change=_recalcular_por_quincena,
        )

        codigo = st.text_input("Código Turno", key="codigo_turno", on_change=_limpiar_error_turno)

        if st.button("Agregar Turno", use_container_width=True):
            codigo_norm = (codigo or "").strip().upper()
            if codigo_norm in turnos_base:
                st.session_state.turno_error = ""
                t = turnos_base[codigo_norm]
                st.session_state.calc.agregar_turno(t)
                st.session_state.turnos_reg.append((codigo_norm, t.inicio, t.fin))
                st.rerun()
            else:
                st.session_state.turno_error = "Código inválido"

        if st.session_state.turno_error:
            st.error(st.session_state.turno_error)

st.divider()

st.subheader("📋 Registros agregados")
if st.session_state.turnos_reg:
    df_reg = pd.DataFrame(st.session_state.turnos_reg, columns=["Código", "Ingreso", "Salida"])
    df_reg.insert(0, "X", False)

    edited = st.data_editor(
        df_reg,
        use_container_width=True,
        hide_index=True,
        disabled=["Código", "Ingreso", "Salida"],
        key="reg_editor",
    )

    if st.button("Eliminar seleccionados", key="btn_eliminar_registros", use_container_width=True):
        idxs = [i for i, v in enumerate(edited["X"].tolist()) if bool(v)]
        if idxs:
            for i in sorted(idxs, reverse=True):
                st.session_state.turnos_reg.pop(i)

            st.session_state.calc.reinicializar(st.session_state.quincena)
            for codigo, _, _ in st.session_state.turnos_reg:
                if codigo in turnos_base:
                    t = turnos_base[codigo]
                    st.session_state.calc.agregar_turno(t)
                elif codigo == "SUSP":
                    st.session_state.calc.agregar_suspension()
                elif codigo == "LIC":
                    st.session_state.calc.agregar_licencia()
                elif codigo == "CP":
                    st.session_state.calc.agregar_cp()
                elif codigo == "INCAP":
                    st.session_state.calc.agregar_incapacidad()
                elif codigo == "DISPO":
                    pass

            for nombre, valor in st.session_state.deducciones_reg:
                st.session_state.calc.agregar_deduccion_manual(nombre, valor)
            st.rerun()
else:
    st.write("(Sin registros)")

st.divider()

# UI: Botonera de acciones principales.
# Los formularios (DISPO/EXTRAS/DEDUCCIÓN) se renderizan inmediatamente debajo
# de esta primera fila para que no se vayan al final (y en móvil se hace scroll).
col_dispo, col_extras, col_deduccion, col_susp = st.columns(4)

with col_dispo:
    if st.button("DISPO", use_container_width=True):
        st.session_state.expandir_dispo = not st.session_state.expandir_dispo
        if st.session_state.expandir_dispo:
            st.session_state.expandir_extras = False
            st.session_state.expandir_deduccion = False
            st.session_state._scroll_to = "dispo"

with col_extras:
    if st.button("EXTRAS", use_container_width=True):
        st.session_state.expandir_extras = not st.session_state.expandir_extras
        if st.session_state.expandir_extras:
            st.session_state.expandir_dispo = False
            st.session_state.expandir_deduccion = False
            st.session_state._scroll_to = "extras"

with col_deduccion:
    if st.button("DEDUCCIÓN", use_container_width=True):
        st.session_state.expandir_deduccion = not st.session_state.expandir_deduccion
        if st.session_state.expandir_deduccion:
            st.session_state.expandir_dispo = False
            st.session_state.expandir_extras = False
            st.session_state._scroll_to = "deduccion"

with col_susp:
    if st.button("SUSPENSIÓN", use_container_width=True):
        st.session_state.calc.agregar_suspension()
        st.session_state.turnos_reg.append(("SUSP","-","-"))
        st.rerun()

# Formularios inmediatamente debajo de la primera fila de botones.
# Se usa _scroll_to para hacer scroll automático al abrir un formulario.
_scroll_to = st.session_state.get("_scroll_to")

if st.session_state.expandir_dispo:
    st.markdown('<div id="form-dispo"></div>', unsafe_allow_html=True)
    with st.container(border=True):
        st.write("**Disponible**")
        col_inicio, col_fin = st.columns(2)

        with col_inicio:
            inicio = st.time_input("Hora inicio", key="dispo_inicio")

        with col_fin:
            fin = st.time_input("Hora fin", key="dispo_fin")

        fest = st.checkbox("Festivo/Dominical", key="festivo_dispo")
        col1_dispo, col2_dispo = st.columns(2)

        with col1_dispo:
            if st.button("Agregar Dispo", use_container_width=True, key="btn_agregar_dispo"):
                h_init = str(inicio)[:5]
                h_fin = str(fin)[:5]
                st.session_state.calc.agregar_dispo(h_init, h_fin, fest)
                st.session_state.turnos_reg.append(("DISPO", h_init, h_fin))
                st.session_state.expandir_dispo = False
                st.session_state._scroll_to = None
                st.rerun()

        with col2_dispo:
            if st.button("Cancelar", use_container_width=True, key="btn_cancelar_dispo"):
                st.session_state.expandir_dispo = False
                st.session_state._scroll_to = None
                st.rerun()

if st.session_state.expandir_extras:
    st.markdown('<div id="form-extras"></div>', unsafe_allow_html=True)
    with st.container(border=True):
        st.write("**Horas Extra**")
        minutos = st.number_input("Minutos", 0, 500, 0, key="minutos_extra")
        tipo = st.selectbox("Tipo", [
            "Extra Diurna (+25%)",
            "Extra Nocturna (+75%)",
            "Extra Diurna Festivo (+105%)",
            "Extra Nocturna Festivo (+155%)"
        ], key="tipo_extra")
        col1_extra, col2_extra = st.columns(2)

        with col1_extra:
            if st.button("Agregar Extra", use_container_width=True, key="btn_agregar_extra"):
                rec = {"Extra Diurna (+25%)": 1.25,
                       "Extra Nocturna (+75%)": 1.75,
                       "Extra Diurna Festivo (+105%)": 2.05,
                       "Extra Nocturna Festivo (+155%)": 2.55}
                st.session_state.calc.agregar_extra(minutos, rec[tipo], tipo)
                st.session_state.expandir_extras = False
                st.session_state._scroll_to = None
                st.rerun()

        with col2_extra:
            if st.button("Cancelar", use_container_width=True, key="btn_cancelar_extra"):
                st.session_state.expandir_extras = False
                st.session_state._scroll_to = None
                st.rerun()

if st.session_state.expandir_deduccion:
    st.markdown('<div id="form-deduccion"></div>', unsafe_allow_html=True)
    with st.container(border=True):
        st.write("**Deducción**")
        nombre = st.text_input("Concepto", key="deduccion_nombre")
        valor = st.number_input("Valor", min_value=0.0, step=1000.0, format="%.0f", key="deduccion_valor")

        col1_ded, col2_ded = st.columns(2)
        with col1_ded:
            if st.button("Agregar Deducción", use_container_width=True, key="btn_agregar_deduccion"):
                nombre_norm = (nombre or "").strip()
                if not nombre_norm:
                    st.error("Ingresa el concepto de la deducción")
                else:
                    st.session_state.calc.agregar_deduccion_manual(nombre_norm, float(valor))
                    st.session_state.deducciones_reg.append((nombre_norm, float(valor)))
                    st.session_state.expandir_deduccion = False
                    st.session_state._scroll_to = None
                    st.rerun()

        with col2_ded:
            if st.button("Cancelar", use_container_width=True, key="btn_cancelar_deduccion"):
                st.session_state.expandir_deduccion = False
                st.session_state._scroll_to = None
                st.rerun()

# Scroll automático: en móvil evita que el usuario tenga que bajar buscando el formulario.
if _scroll_to == "dispo":
    components.html("""<script>document.getElementById('form-dispo')?.scrollIntoView({behavior:'smooth',block:'start'});</script>""", height=0)
    st.session_state._scroll_to = None
elif _scroll_to == "extras":
    components.html("""<script>document.getElementById('form-extras')?.scrollIntoView({behavior:'smooth',block:'start'});</script>""", height=0)
    st.session_state._scroll_to = None
elif _scroll_to == "deduccion":
    components.html("""<script>document.getElementById('form-deduccion')?.scrollIntoView({behavior:'smooth',block:'start'});</script>""", height=0)
    st.session_state._scroll_to = None

col_lic, col_cp, col_incap, col_reset = st.columns(4)

with col_lic:
    if st.button("LICENCIA", use_container_width=True):
        st.session_state.calc.agregar_licencia()
        st.session_state.turnos_reg.append(("LIC","-","-"))
        st.rerun()

with col_cp:
    if st.button("CP", use_container_width=True):
        st.session_state.calc.agregar_cp()
        st.session_state.turnos_reg.append(("CP","-","-"))
        st.rerun()

with col_incap:
    if st.button("INCAPACIDAD", use_container_width=True):
        st.session_state.calc.agregar_incapacidad()
        st.session_state.turnos_reg.append(("INCAP","-","-"))
        st.rerun()

with col_reset:
    if st.button("🔄", use_container_width=True):
        st.session_state.calc = CalculadoraNomina()
        st.session_state.turnos_reg = []
        st.session_state.deducciones_reg = []
        st.rerun()

st.divider()

dev = st.session_state.calc.devengado
auxilio = st.session_state.calc.total_auxilio()
civicas = st.session_state.calc.total_civicas()
ded = st.session_state.calc.total_deducciones()
neto = dev + auxilio + civicas - ded
total_ingresos = dev + auxilio + civicas

# Mostrar en formato tipo colilla
st.subheader("📋 NÓMINA")

col_dev, col_dedu = st.columns(2)

with col_dev:
    st.write("**DEVENGADOS**")
    dias_incap = st.session_state.calc.dias_incapacidad
    dias_full = st.session_state.calc.dias_trabajados
    dias_no_trab = max(0, 15 - dias_full - dias_incap)
    valor_dia = st.session_state.calc.valor_dia_basico

    val_full = dias_full * valor_dia
    st.write(f"SALARIO BÁSICO: ${val_full:,.0f} | {dias_full} días")

    # Mostrar recargos agrupados
    for concepto, datos in st.session_state.calc.recargos_agrupados.items():
        horas = datos["horas"]
        valor = datos["valor"]
        st.write(f"{concepto}: {horas:.2f}h | ${valor:,.0f}")
    
    # Mostrar otros detalles de desglose
    for concepto, cantidad, valor in st.session_state.calc.detalles_desglose:
        if "COMPENS" in concepto:
            st.write(f"{concepto}: 1 | ${valor:,.0f}")
        else:
            st.write(f"{concepto}: {cantidad:.2f}h | ${valor:,.0f}")
    
    # Días no laborados / incapacidad (ajustan el básico)
    if dias_no_trab > 0:
        st.write(f"LIC/SUSP: {dias_no_trab} día(s) sin pago")

    if dias_incap > 0:
        val_incap = dias_incap * valor_dia * 0.6667
        st.write(f"INCAPACIDAD: {dias_incap} día(s) (66.67%) | ${val_incap:,.0f}")
    
    # Cívicas
    if civicas > 0:
        st.write(f"CIVICA: {st.session_state.calc.civicas_cantidad} | ${civicas:,.0f}")
    
    # Auxilio (solo quincena 30)
    if st.session_state.quincena == "30":
        st.write(f"AUXILIO TRANSPORTE: - | ${auxilio:,.0f}")

    st.write(f"\n**TOTAL DEVENGADO: ${total_ingresos:,.0f}**")

with col_dedu:
    st.write("**DEDUCCIONES**")
    deducciones_desglose = st.session_state.calc.get_deducciones_desglosadas()
    
    for concepto, valor in deducciones_desglose.items():
        st.write(f"{concepto}: ${valor:,.0f}")
    
    st.write(f"\n**TOTAL DEDUCCIONES: ${ded:,.0f}**")

st.divider()
st.markdown(
    f"""
    <div style="background-color: rgba(0, 0, 0, 0.4); padding: 15px; border-radius: 10px;">
        <div style="color: rgba(255,255,255,0.85); font-size: 0.9rem; font-weight: 600;">NETO A PAGAR</div>
        <div style="color: #ffffff; font-size: 2rem; font-weight: 800; line-height: 1.1;">${neto:,.0f}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Footer con marca de agua
st.markdown("""
    <style>
        /* Forzar valor de métricas a blanco (CSS inyectado al final para ganar prioridad) */
        .stApp [data-testid="metric-container"],
        .stApp [data-testid="metric-container"] * {
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
            opacity: 1 !important;
            filter: none !important;
        }

        /* Evitar solapamiento con elementos fijos de Streamlit Community Cloud */
        footer { visibility: hidden; }

        .footer {
            position: fixed;
            bottom: 70px;
            right: 20px;
            font-size: 12px;
            font-style: italic;
            color: rgba(255, 255, 255, 0.5);
            z-index: 999999;
            pointer-events: none;
        }

        /* Responsive: ajustar footer y métricas en pantallas pequeñas */
        @media (max-width: 640px) {
            .footer {
                bottom: 110px;
                right: 12px;
                font-size: 11px;
            }

            .stApp [data-testid="metric-container"] {
                padding: 12px;
            }
        }
    </style>
    <div class="footer">
        <p>Power by: <strong>Reiber</strong></p>
    </div>
""", unsafe_allow_html=True)
