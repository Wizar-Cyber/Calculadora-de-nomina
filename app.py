import streamlit as st
import json
from models.turno import Turno
from services.calculadora import CalculadoraNomina
from config import SALARIO_QUINCENA, VALOR_HORA, HORAS_JORNADA

st.set_page_config(layout="wide")

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
        
        [data-testid="metric-container"] .stMetric {{
            color: white !important;
        }}
        
        [data-testid="stMetricValue"] {{
            color: white !important;
        }}
        
        div[data-testid="metric-container"] > div {{
            color: white !important;
        }}
        
        div[data-testid="metric-container"] span {{
            color: white !important;
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
            }}
            
            label {{
                font-size: 0.95rem !important;
            }}
        }}
    </style>
""", unsafe_allow_html=True)

if "calc" not in st.session_state:
    st.session_state.quincena = "30"
    st.session_state.calc = CalculadoraNomina(quincena="30")
    st.session_state.turnos_reg = []
    st.session_state.expandir_dispo = False
    st.session_state.expandir_extras = False
    st.session_state.expandir_deduccion = False

with open("turnos.json") as f:
    turnos_base = {t["codigo"]:Turno(t) for t in json.load(f)}

st.title("🧮 Nómina Conductores TA")

col1,col2 = st.columns(2)

with col1:
    st.markdown("""
        <style>
            .unified-container {
                background-color: rgba(0, 0, 0, 0.15) !important;
                padding: 15px !important;
                border-radius: 8px;
                border: 1px solid rgba(255, 255, 255, 0.15);
            }
        </style>
        <div class="unified-container">
    """, unsafe_allow_html=True)
    
    quincena = st.selectbox("Quincena",["15","30"], key="select_quincena")
    if quincena != st.session_state.quincena:
        st.session_state.quincena = quincena
        # Guardar los turnos actuales
        turnos_temp = st.session_state.turnos_reg.copy()
        # Reinicializar con la nueva quincena
        st.session_state.calc = CalculadoraNomina(quincena=quincena)
        st.session_state.turnos_reg = turnos_temp
        # Re-agregar todos los turnos
        for codigo, _, _ in turnos_temp:
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
        st.rerun()
    
    with st.form("form_turno", clear_on_submit=True):
        codigo = st.text_input("Código Turno")
        if st.form_submit_button("Agregar Turno"):
            if codigo in turnos_base:
                t = turnos_base[codigo]
                st.session_state.calc.agregar_turno(t)
                st.session_state.turnos_reg.append((codigo,t.inicio,t.fin))
                st.rerun()
            else:
                st.error("Código inválido")
    
    st.markdown("</div>", unsafe_allow_html=True)

st.divider()

st.subheader("📋 Registros agregados")
for i,r in enumerate(st.session_state.turnos_reg):
    colA,colB,colC,colD = st.columns([2,2.5,2.5,0.5])
    with colA:
        st.write(f"**{r[0]}**")
    with colB:
        st.write(f"{r[1]}")
    with colC:
        st.write(f"{r[2]}")
    with colD:
        if st.button("❌",key=i, use_container_width=True):
        st.session_state.turnos_reg.pop(i)
        # Recalcular todo desde cero
        st.session_state.calc.reinicializar(st.session_state.quincena)
        # Re-agregar los turnos que quedan
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
                pass  # Los DISPO se re-agregan con el código original
        st.rerun()

st.divider()

# Botones en fila para DISPO, EXTRAS, DEDUCCIÓN
col_dispo, col_extras, col_deduccion, col_susp, col_lic, col_cp, col_incap, col_reset = st.columns(8)

with col_dispo:
    if st.button("DISPO", use_container_width=True):
        st.session_state.expandir_dispo = not st.session_state.expandir_dispo

with col_extras:
    if st.button("EXTRAS", use_container_width=True):
        st.session_state.expandir_extras = not st.session_state.expandir_extras

with col_deduccion:
    if st.button("DEDUCCIÓN", use_container_width=True):
        st.session_state.expandir_deduccion = not st.session_state.expandir_deduccion

with col_susp:
    if st.button("SUSPENSIÓN", use_container_width=True):
        st.session_state.calc.agregar_suspension()
        st.session_state.turnos_reg.append(("SUSP","-","-"))
        st.rerun()

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
        st.rerun()

# Expandibles
if st.session_state.expandir_dispo:
    st.write("**Disponible**")
    col_hora_sugerida, col_entrada_manual = st.columns(2)
    
    with col_hora_sugerida:
        st.write("Selecciona de sugeridas:")
        inicio = st.time_input("Hora inicio (sugerida)", key="dispo_inicio_sug")
        fin = st.time_input("Hora fin (sugerida)", key="dispo_fin_sug")
    
    with col_entrada_manual:
        st.write("O ingresa manual:")
        inicio_manual = st.text_input("Hora inicio (HH:MM)", key="dispo_inicio_man")
        fin_manual = st.text_input("Hora fin (HH:MM)", key="dispo_fin_man")
    
    fest = st.checkbox("Festivo/Dominical")
    col1_dispo, col2_dispo = st.columns(2)
    
    with col1_dispo:
        if st.button("Agregar Dispo", use_container_width=True):
            h_init = inicio_manual if inicio_manual else str(inicio)[:5]
            h_fin = fin_manual if fin_manual else str(fin)[:5]
            st.session_state.calc.agregar_dispo(h_init, h_fin, fest)
            st.session_state.turnos_reg.append(("DISPO", h_init, h_fin))
            st.session_state.expandir_dispo = False
            st.rerun()
    
    with col2_dispo:
        if st.button("Cancelar", use_container_width=True):
            st.session_state.expandir_dispo = False
            st.rerun()

if st.session_state.expandir_extras:
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
        if st.button("Agregar Extra", use_container_width=True):
            rec = {"Extra Diurna (+25%)": 1.25,
                   "Extra Nocturna (+75%)": 1.75,
                   "Extra Diurna Festivo (+105%)": 2.05,
                   "Extra Nocturna Festivo (+155%)": 2.55}
            st.session_state.calc.agregar_extra(minutos, rec[tipo], tipo)
            st.session_state.expandir_extras = False
            st.rerun()
    
    with col2_extra:
        if st.button("Cancelar", use_container_width=True):
            st.session_state.expandir_extras = False
            st.rerun()

if st.session_state.expandir_deduccion:
    st.write("**Deducción Manual**")
    nom = st.text_input("Concepto", key="concepto_ded")
    val = st.number_input("Valor", 0, 500000, 0, key="valor_ded")
    col1_ded, col2_ded = st.columns(2)
    
    with col1_ded:
        if st.button("Agregar Deducción", use_container_width=True):
            st.session_state.calc.agregar_deduccion_manual(nom, val)
            st.session_state.expandir_deduccion = False
            st.rerun()
    
    with col2_ded:
        if st.button("Cancelar", use_container_width=True):
            st.session_state.expandir_deduccion = False
            st.rerun()

st.divider()

dev = st.session_state.calc.devengado
auxilio = st.session_state.calc.total_auxilio()
civicas = st.session_state.calc.total_civicas()
ded = st.session_state.calc.total_deducciones()
neto = dev + auxilio + civicas - ded

# Mostrar en formato tipo colilla
st.subheader("📋 NÓMINA")

col_dev, col_dedu = st.columns(2)

with col_dev:
    st.write("**DEVENGADOS**")
    st.write(f"SALARIO BÁSICO: ${SALARIO_QUINCENA:,.0f} | 15 días")
    
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
    
    # Días de incapacidad
    if st.session_state.calc.dias_incapacidad > 0:
        dias_norm = 15 - st.session_state.calc.dias_incapacidad
        val_normal = dias_norm * HORAS_JORNADA * VALOR_HORA
        val_incap = st.session_state.calc.dias_incapacidad * HORAS_JORNADA * VALOR_HORA * 0.6667
        st.write(f"DÍAS NORMALES: {dias_norm} | ${val_normal:,.0f}")
        st.write(f"INCAPACIDAD: {st.session_state.calc.dias_incapacidad} @ 66.67% | ${val_incap:,.0f}")
    
    # Cívicas
    if civicas > 0:
        st.write(f"CIVICA: {st.session_state.calc.civicas_cantidad} | ${civicas:,.0f}")
    
    # Auxilio (solo quincena 30)
    if st.session_state.quincena == "30":
        st.write(f"AUXILIO TRANSPORTE: - | ${auxilio:,.0f}")
    
    st.write(f"\n**TOTAL DEVENGADO: ${dev:,.0f}**")

with col_dedu:
    st.write("**DEDUCCIONES**")
    deducciones_desglose = st.session_state.calc.get_deducciones_desglosadas()
    
    for concepto, valor in deducciones_desglose.items():
        st.write(f"{concepto}: ${valor:,.0f}")
    
    st.write(f"\n**TOTAL DEDUCCIONES: ${ded:,.0f}**")

st.divider()
st.metric("NETO A PAGAR", f"${neto:,.0f}")

# Footer con marca de agua
st.markdown("""
    <style>
        .footer {
            position: fixed;
            bottom: 10px;
            right: 20px;
            font-size: 12px;
            font-style: italic;
            color: rgba(255, 255, 255, 0.5);
            z-index: 999;
        }
    </style>
    <div class="footer">
        <p>Power by: <strong>Reiber</strong></p>
    </div>
""", unsafe_allow_html=True)
