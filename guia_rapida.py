#!/usr/bin/env python3
"""
Guía Rápida - Agente Iron Condor SPX
Script de inicio rápido para usar el agente inmediatamente

Autor: MiniMax Agent
Fecha: 2025-09-28
"""

from agente_iron_condor_final import AgenteIronCondorSPX

def guia_rapida():
    """
    Guía rápida para usar el agente inmediatamente
    """
    print("\n" + "="*70)
    print("🎯 GUÍA RÁPIDA - AGENTE IRON CONDOR SPX")
    print("="*70)
    
    print("🚀 Inicializando agente...")
    agente = AgenteIronCondorSPX()
    
    print("\n🔄 Ejemplo 1: Cálculo con ala de 25 puntos (recomendado)")
    try:
        resultado = agente.ejecutar_calculo_completo(ala=25)
        agente.mostrar_resultado_formateado(resultado)
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "="*70)
    print("🔄 Ejemplo 2: Cálculo con ala de 15 puntos (más conservador)")
    try:
        resultado = agente.ejecutar_calculo_completo(ala=15)
        agente.mostrar_resultado_formateado(resultado)
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "="*70)
    print("📚 CÓMO USAR EL AGENTE PROGRAMATICAMENTE:")
    print("="*70)
    
    codigo_ejemplo = '''
# Importar el agente
from agente_iron_condor_final import AgenteIronCondorSPX

# Crear instancia
agente = AgenteIronCondorSPX()

# Opción 1: Cálculo básico
resultado = agente.ejecutar_calculo_completo(ala=25)
agente.mostrar_resultado_formateado(resultado)

# Opción 2: Cálculo con fecha futura
resultado = agente.ejecutar_calculo_completo(
    fecha_objetivo="2025-10-05",  # Hasta 7 días en el futuro
    ala=20
)

# Opción 3: Acceder a datos específicos
spx_valor = resultado['datos_mercado']['spx_valor']
vix_valor = resultado['datos_mercado']['vix_valor']
strikes = resultado['strikes']

print(f"SPX: ${spx_valor:,.2f}")
print(f"Sell Put: ${strikes['sell_put']:,}")
print(f"Sell Call: ${strikes['sell_call']:,}")
'''
    
    print(codigo_ejemplo)
    
    print("\n" + "="*70)
    print("📋 EXPLICACIÓN DE LA LÓGICA:")
    print("="*70)
    
    explicacion = '''
📊 PASO A PASO:

1. 📈 SPX: Obtiene el valor actual del S&P 500
2. 📉 VIX: Obtiene la implied volatility del mercado
3. ⚙️ IV: Convierte VIX a puntos del SPX y suma 10 de buffer
4. 📉 Sell Put: SPX - IV (redondeado al múltiplo de 5 superior)
5. 📉 Buy Put: Sell Put - Ala
6. 📈 Sell Call: SPX + IV (redondeado al múltiplo de 5 inferior)
7. 📈 Buy Call: Sell Call + Ala

🎯 OBJETIVO:
Crear un iron condor equilibrado que capture prima mientras
proporciona un rango de rentabilidad apropiado según la
volatilidad actual del mercado.

🔧 ALAS DISPONIBLES:
- 10 puntos: Más conservador, menor riesgo/recompensa
- 15 puntos: Equilibrado
- 20 puntos: Agresivo
- 25 puntos: Máximo riesgo/recompensa
'''
    
    print(explicacion)
    
    print("\n" + "="*70)
    print("✨ ¡LISTO PARA USAR!")
    print("📋 Para el demo interactivo, ejecute: python demo_interactivo.py")
    print("💻 Para uso programatico, importe: from agente_iron_condor_final import AgenteIronCondorSPX")
    print("="*70)

def ejemplo_uso_directo():
    """
    Ejemplo de uso directo del agente
    """
    print("\n🚀 Ejecutando ejemplo de uso directo...")
    
    # Crear agente
    agente = AgenteIronCondorSPX()
    
    # Obtener datos actuales del mercado
    datos = agente.obtener_datos_mercado()
    if datos:
        print(f"\n📊 Datos actuales:")
        print(f"   SPX: ${datos['spx_valor']:,.2f}")
        print(f"   VIX: {datos['vix_valor']:.2f}%")
        
        # Calcular IV
        iv = agente.calcular_iv_puntos(datos['spx_valor'], datos['vix_valor'])
        print(f"   IV calculado: {iv:.2f} puntos")
        
        # Calcular strikes para ala de 25
        strikes = agente.calcular_strikes(datos['spx_valor'], iv, 25)
        print(f"\n🎯 Strikes (Ala 25):")
        print(f"   Iron Condor: {strikes['buy_put']}/{strikes['sell_put']}/{strikes['sell_call']}/{strikes['buy_call']}")
        print(f"   Rango: ${strikes['sell_put']:,} - ${strikes['sell_call']:,} ({strikes['rango_profit']} puntos)")


if __name__ == "__main__":
    guia_rapida()
    ejemplo_uso_directo()
