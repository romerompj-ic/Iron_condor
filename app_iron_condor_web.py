#!/usr/bin/env python3
"""
Aplicación Web - Iron Condor SPX Calculator
Interfaz web moderna para calcular Iron Condors

Autor: MiniMax Agent
Fecha: 2025-09-28
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import time
from agente_iron_condor_final import AgenteIronCondorSPX

# Importación robusta de plotly
try:
    import plotly.graph_objects as go
    import plotly.express as px
    PLOTLY_AVAILABLE = True
except ImportError:
    st.warning("⚠️ Plotly no está disponible. Los gráficos se mostrarán con matplotlib.")
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    PLOTLY_AVAILABLE = False

# Configuración de la página
st.set_page_config(
    page_title="🎯 Iron Condor SPX Calculator",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #2c3e50, #3498db);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #3498db;
        margin: 0.5rem 0;
    }
    .strike-box {
        background: #2c3e50;
        color: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        margin: 0.5rem;
    }
    .success-box {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=300)  # Cache por 5 minutos
def get_agente():
    """Obtener instancia del agente (con cache)"""
    return AgenteIronCondorSPX()

def main():
    """Función principal de la aplicación web"""
    
    # Header principal
    st.markdown("""
    <div class="main-header">
        <h1>🎯 Iron Condor SPX Calculator</h1>
        <p>Calculadora profesional de Iron Condors con datos en tiempo real</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar para configuración
    with st.sidebar:
        st.header("⚙️ Configuración")
        
        # Parámetros
        ala = st.selectbox(
            "🔧 Ancho del Ala",
            [10, 15, 20, 25],
            index=3,  # Por defecto 25
            help="Diferencia en puntos entre strikes de compra y venta"
        )
        
        periodo = st.selectbox(
            "⏱️ Período Temporal",
            ["diario", "semanal", "mensual", "anual"],
            index=0,  # Por defecto diario
            help="Período para ajustar la volatilidad implícita"
        )
        
        buffer = st.slider(
            "🛡️ Buffer de Seguridad",
            min_value=0,
            max_value=50,
            value=10,
            help="Puntos adicionales de seguridad agregados al IV"
        )
        
        st.markdown("---")
        
        # Información del período
        if periodo == "diario":
            st.info("📅 **Diario**: Movimiento esperado por día de trading (recomendado para Iron Condors)")
        elif periodo == "semanal":
            st.info("📅 **Semanal**: Movimiento esperado por semana")
        elif periodo == "mensual":
            st.info("📅 **Mensual**: Movimiento esperado por mes")
        else:
            st.info("📅 **Anual**: Movimiento esperado por año completo")
    
    # Columnas principales
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📊 Cálculo del Iron Condor")
        
        if st.button("🚀 CALCULAR IRON CONDOR", type="primary", use_container_width=True):
            with st.spinner("🔄 Obteniendo datos del mercado y calculando..."):
                try:
                    # Obtener agente y calcular
                    agente = get_agente()
                    resultado = agente.ejecutar_calculo_completo(
                        ala=ala,
                        periodo=periodo,
                        buffer=buffer
                    )
                    
                    # Guardar en session state
                    st.session_state['resultado'] = resultado
                    st.session_state['calculado'] = True
                    
                    st.success("✅ ¡Cálculo completado exitosamente!")
                    
                except Exception as e:
                    st.error(f"❌ Error: {e}")
                    st.session_state['calculado'] = False
    
    with col2:
        st.subheader("ℹ️ Información")
        st.markdown("""
        **🎯 Iron Condor**: Estrategia neutral que busca beneficiarse de baja volatilidad.
        
        **📈 Componentes**:
        - **Sell Put**: Vender put fuera del dinero
        - **Buy Put**: Comprar put más fuera del dinero  
        - **Sell Call**: Vender call fuera del dinero
        - **Buy Call**: Comprar call más fuera del dinero
        
        **💰 Objetivo**: Que el SPX se mantenga entre los strikes vendidos.
        """)
    
    # Mostrar resultados si están disponibles
    if st.session_state.get('calculado', False) and 'resultado' in st.session_state:
        mostrar_resultados(st.session_state['resultado'])

def mostrar_resultados(resultado):
    """Mostrar los resultados del cálculo"""
    
    datos = resultado['datos_mercado']
    params = resultado['parametros']
    strikes = resultado['strikes']
    resumen = resultado['resumen_estrategia']
    
    st.markdown("---")
    st.header("📊 Resultados del Cálculo")
    
    # Datos del mercado
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📈 SPX",
            value=f"${datos['spx_valor']:,.2f}",
            help="Valor actual del S&P 500 Index"
        )
    
    with col2:
        st.metric(
            label="📉 VIX",
            value=f"{datos['vix_valor']:.2f}%",
            help="Volatilidad implícita anualizada"
        )
    
    with col3:
        st.metric(
            label="📊 IV Final",
            value=f"{params['iv_puntos_calculado']:.1f}",
            help="Implied Volatility ajustada por tiempo + buffer"
        )
    
    with col4:
        st.metric(
            label="📏 Rango",
            value=f"{strikes['rango_profit']} pts",
            help="Amplitud del rango de rentabilidad"
        )
    
    # Strikes del Iron Condor
    st.subheader("🎯 Strikes del Iron Condor")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="strike-box">
            <h4>📉 Buy Put</h4>
            <h2>${strikes['buy_put']:,}</h2>
            <p>COMPRAR</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="strike-box" style="background: #27ae60;">
            <h4>📈 Sell Put</h4>
            <h2>${strikes['sell_put']:,}</h2>
            <p>VENDER ⭐</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="strike-box" style="background: #27ae60;">
            <h4>📈 Sell Call</h4>
            <h2>${strikes['sell_call']:,}</h2>
            <p>VENDER ⭐</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="strike-box">
            <h4>📉 Buy Call</h4>
            <h2>${strikes['buy_call']:,}</h2>
            <p>COMPRAR</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Gráfico visual
    crear_grafico_iron_condor(datos, strikes)
    
    # Análisis detallado
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Análisis de la Estrategia")
        
        st.markdown(f"""
        **💰 Rango de Rentabilidad**: ${strikes['sell_put']:,} - ${strikes['sell_call']:,}
        
        **📐 Amplitud**: {strikes['rango_profit']} puntos
        
        **⬇️ Distancia a Sell Put**: {resumen['distancia_spx_sell_put']:.1f} puntos
        
        **⬆️ Distancia a Sell Call**: {resumen['distancia_spx_sell_call']:.1f} puntos
        
        **⚖️ Simetría**: {resumen['simetria']:.1f} puntos
        """)
    
    with col2:
        st.subheader("⚙️ Detalles del Cálculo")
        
        st.markdown(f"""
        **🔧 Ala elegida**: {params['ala_elegida']} puntos
        
        **⏱️ Período**: {params['periodo_temporal']} (factor: √{params['factor_tiempo']})
        
        **📊 IV anualizado**: {params['iv_anualizado']:.2f} puntos
        
        **📊 IV ajustado**: {params['iv_ajustado_tiempo']:.2f} puntos
        
        **🛡️ Buffer**: +{params['buffer_agregado']} puntos
        """)
    
    # Instrucciones de trading
    st.markdown(f"""
    <div class="success-box">
        <h3>📋 Instrucciones de Trading</h3>
        <ol>
            <li><strong>VENDER</strong> Put ${strikes['sell_put']:,} (recibir prima)</li>
            <li><strong>COMPRAR</strong> Put ${strikes['buy_put']:,} (pagar prima)</li>
            <li><strong>VENDER</strong> Call ${strikes['sell_call']:,} (recibir prima)</li>
            <li><strong>COMPRAR</strong> Call ${strikes['buy_call']:,} (pagar prima)</li>
        </ol>
        <p><strong>🎯 Objetivo</strong>: Que el SPX se mantenga entre ${strikes['sell_put']:,} y ${strikes['sell_call']:,} al vencimiento.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tabla resumen
    crear_tabla_resumen(resultado)

def crear_grafico_iron_condor(datos, strikes):
    """Crear gráfico visual del Iron Condor"""
    
    st.subheader("📈 Visualización del Iron Condor")
    
    # Rango de precios para el gráfico
    spx_actual = datos['spx_valor']
    rango_inferior = strikes['buy_put'] - 50
    rango_superior = strikes['buy_call'] + 50
    
    if PLOTLY_AVAILABLE:
        # Versión con Plotly
        fig = go.Figure()
        
        # Línea vertical del SPX actual
        fig.add_vline(
            x=spx_actual, 
            line_dash="dash", 
            line_color="blue",
            annotation_text=f"SPX Actual: ${spx_actual:,.0f}"
        )
        
        # Strikes
        strikes_data = [
            (strikes['buy_put'], "Buy Put", "red"),
            (strikes['sell_put'], "Sell Put", "green"),
            (strikes['sell_call'], "Sell Call", "green"),
            (strikes['buy_call'], "Buy Call", "red")
        ]
        
        for strike, label, color in strikes_data:
            fig.add_vline(
                x=strike,
                line_color=color,
                annotation_text=f"{label}: ${strike:,}",
                annotation_position="top"
            )
        
        # Zona de rentabilidad
        fig.add_vrect(
            x0=strikes['sell_put'],
            x1=strikes['sell_call'],
            fillcolor="green",
            opacity=0.2,
            annotation_text="Zona de Ganancia",
            annotation_position="inside top"
        )
        
        fig.update_layout(
            title="Iron Condor - Distribución de Strikes",
            xaxis_title="Precio del SPX",
            yaxis_title="P&L",
            height=400,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    else:
        # Versión alternativa con matplotlib y datos tabulares
        st.write("**Iron Condor - Distribución de Strikes**")
        
        # Crear tabla visual de los strikes
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="🔴 Buy Put",
                value=f"${strikes['buy_put']:,}",
                delta=f"{strikes['buy_put'] - spx_actual:+,.0f}"
            )
        
        with col2:
            st.metric(
                label="🟢 Sell Put", 
                value=f"${strikes['sell_put']:,}",
                delta=f"{strikes['sell_put'] - spx_actual:+,.0f}"
            )
        
        with col3:
            st.metric(
                label="🟢 Sell Call",
                value=f"${strikes['sell_call']:,}",
                delta=f"{strikes['sell_call'] - spx_actual:+,.0f}"
            )
        
        with col4:
            st.metric(
                label="🔴 Buy Call",
                value=f"${strikes['buy_call']:,}",
                delta=f"{strikes['buy_call'] - spx_actual:+,.0f}"
            )
        
        # Información adicional
        st.info(f"📍 **SPX Actual**: ${spx_actual:,.0f}")
        st.success(f"💰 **Zona de Ganancia**: ${strikes['sell_put']:,} - ${strikes['sell_call']:,}")
        
        # Crear gráfico simple con métricas
        ranges_data = {
            'Strike': ['Buy Put', 'Sell Put', 'SPX Actual', 'Sell Call', 'Buy Call'],
            'Precio': [strikes['buy_put'], strikes['sell_put'], spx_actual, strikes['sell_call'], strikes['buy_call']],
            'Tipo': ['🔴 Compra', '🟢 Venta', '📍 Actual', '🟢 Venta', '🔴 Compra']
        }
        
        df_ranges = pd.DataFrame(ranges_data)
        st.dataframe(df_ranges, use_container_width=True)

def crear_tabla_resumen(resultado):
    """Crear tabla resumen de resultados"""
    
    st.subheader("📋 Resumen Completo")
    
    datos = resultado['datos_mercado']
    params = resultado['parametros']
    strikes = resultado['strikes']
    
    # Crear DataFrame
    resumen_data = {
        "Parámetro": [
            "SPX Actual",
            "VIX",
            "Ala Elegida",
            "Período",
            "IV Final",
            "Buy Put",
            "Sell Put",
            "Sell Call", 
            "Buy Call",
            "Rango de Ganancia",
            "Amplitud del Rango"
        ],
        "Valor": [
            f"${datos['spx_valor']:,.2f}",
            f"{datos['vix_valor']:.2f}%",
            f"{params['ala_elegida']} puntos",
            params['periodo_temporal'],
            f"{params['iv_puntos_calculado']:.2f} puntos",
            f"${strikes['buy_put']:,}",
            f"${strikes['sell_put']:,}",
            f"${strikes['sell_call']:,}",
            f"${strikes['buy_call']:,}",
            f"${strikes['sell_put']:,} - ${strikes['sell_call']:,}",
            f"{strikes['rango_profit']} puntos"
        ],
        "Descripción": [
            "Valor actual del S&P 500",
            "Volatilidad implícita anualizada",
            "Diferencia entre strikes compra/venta",
            "Horizonte temporal del cálculo",
            "IV ajustada por tiempo + buffer",
            "Strike del put que compras",
            "Strike del put que vendes 🎯",
            "Strike del call que vendes 🎯",
            "Strike del call que compras",
            "Rango donde la estrategia es rentable",
            "Amplitud total del rango"
        ]
    }
    
    df = pd.DataFrame(resumen_data)
    st.dataframe(df, hide_index=True, use_container_width=True)
    
    # Timestamp
    st.caption(f"🕒 Calculado el {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Inicializar session state
if 'calculado' not in st.session_state:
    st.session_state['calculado'] = False

# Ejecutar aplicación
if __name__ == "__main__":
    main()