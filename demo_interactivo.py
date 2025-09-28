#!/usr/bin/env python3
"""
Demo Interactivo - Agente Iron Condor SPX
Demostración con interfaz interactiva para probar diferentes configuraciones

Autor: MiniMax Agent
Fecha: 2025-09-28
"""

from agente_iron_condor_final import AgenteIronCondorSPX
from datetime import datetime, timedelta
import sys

def mostrar_menu_principal():
    """
    Muestra el menú principal de opciones
    """
    print("\n" + "="*60)
    print("🎯 DEMO INTERACTIVO - AGENTE IRON CONDOR SPX")
    print("="*60)
    print("📈 Opciones disponibles:")
    print("  1. Cálculo rápido (parámetros por defecto)")
    print("  2. Cálculo personalizado")
    print("  3. Comparar diferentes alas")
    print("  4. Ver información del sistema")
    print("  5. Salir")
    print("="*60)

def solicitar_ala():
    """
    Solicita al usuario que elija el ancho del ala
    """
    alas_permitidas = [10, 15, 20, 25]
    
    while True:
        try:
            print("\n🔧 Seleccione el ancho del ala:")
            for i, ala in enumerate(alas_permitidas, 1):
                print(f"  {i}. {ala} puntos")
            
            opcion = int(input("\n➡️ Su elección (1-4): "))
            
            if 1 <= opcion <= 4:
                return alas_permitidas[opcion - 1]
            else:
                print("❌ Opción inválida. Elija entre 1 y 4.")
                
        except ValueError:
            print("❌ Por favor ingrese un número válido.")

def solicitar_fecha():
    """
    Solicita al usuario una fecha objetivo (opcional)
    """
    print("\n📅 Fecha objetivo (opcional):")
    print("  1. Usar fecha actual")
    print("  2. Especificar fecha futura (hasta 7 días)")
    
    while True:
        try:
            opcion = int(input("\n➡️ Su elección (1-2): "))
            
            if opcion == 1:
                return None
            elif opcion == 2:
                fecha_str = input("📅 Ingrese fecha (YYYY-MM-DD): ")
                
                # Validar formato
                try:
                    fecha_obj = datetime.strptime(fecha_str, '%Y-%m-%d')
                    fecha_actual = datetime.now()
                    diferencia = (fecha_obj - fecha_actual).days
                    
                    if 0 <= diferencia <= 7:
                        return fecha_str
                    else:
                        print("❌ La fecha debe estar entre hoy y 7 días en el futuro.")
                        
                except ValueError:
                    print("❌ Formato de fecha inválido. Use YYYY-MM-DD.")
            else:
                print("❌ Opción inválida.")
                
        except ValueError:
            print("❌ Por favor ingrese un número válido.")

def calculo_rapido(agente):
    """
    Ejecuta un cálculo rápido con parámetros por defecto
    """
    print("\n🚀 Ejecutando cálculo rápido...")
    print("   Parámetros: Ala = 25 puntos, Período = Diario (movimiento conservador)")
    
    try:
        resultado = agente.ejecutar_calculo_completo(ala=25)
        agente.mostrar_resultado_formateado(resultado)
        return True
    except Exception as e:
        print(f"❌ Error en cálculo rápido: {e}")
        return False

def calculo_personalizado(agente):
    """
    Ejecuta un cálculo con parámetros personalizados
    """
    print("\n⚙️ Cálculo personalizado")
    
    # Solicitar parámetros
    ala = solicitar_ala()
    fecha = solicitar_fecha()
    
    print(f"\n🚀 Ejecutando cálculo personalizado...")
    print(f"   Ala: {ala} puntos")
    print(f"   Fecha: {fecha or 'Actual'}")
    
    try:
        resultado = agente.ejecutar_calculo_completo(fecha_objetivo=fecha, ala=ala)
        agente.mostrar_resultado_formateado(resultado)
        return True
    except Exception as e:
        print(f"❌ Error en cálculo personalizado: {e}")
        return False

def comparar_alas(agente):
    """
    Compara resultados con diferentes anchos de ala
    """
    print("\n🔄 Comparando diferentes anchos de ala...")
    
    alas = [10, 15, 20, 25]
    resultados = {}
    
    # Calcular para cada ala
    for ala in alas:
        try:
            print(f"   Calculando para ala de {ala} puntos...")
            resultado = agente.ejecutar_calculo_completo(ala=ala)
            resultados[ala] = resultado
        except Exception as e:
            print(f"   ❌ Error con ala {ala}: {e}")
            resultados[ala] = None
    
    # Mostrar comparación
    print("\n" + "="*80)
    print("📊 COMPARACIÓN DE DIFERENTES ALAS")
    print("="*80)
    
    if resultados[25]:  # Usar datos del mercado del primer cálculo exitoso
        datos = resultados[25]['datos_mercado']
        print(f"\n📊 Datos del mercado (SPX: ${datos['spx_valor']:,.2f}, VIX: {datos['vix_valor']:.2f}%)")
    
    print("\n🎯 Comparación de strikes:")
    print(f"{'Ala':<5} {'Buy Put':<10} {'Sell Put':<10} {'Sell Call':<10} {'Buy Call':<10} {'Rango':<8}")
    print("-" * 60)
    
    for ala in alas:
        if resultados[ala]:
            strikes = resultados[ala]['strikes']
            print(f"{ala:<5} {strikes['buy_put']:<10} {strikes['sell_put']:<10} "
                  f"{strikes['sell_call']:<10} {strikes['buy_call']:<10} {strikes['rango_profit']:<8}")
        else:
            print(f"{ala:<5} {'ERROR':<10} {'ERROR':<10} {'ERROR':<10} {'ERROR':<10} {'ERROR':<8}")
    
    print("\n📊 Análisis:")
    for ala in alas:
        if resultados[ala]:
            strikes = resultados[ala]['strikes']
            print(f"   Ala {ala}: Rango de {strikes['rango_profit']} puntos "
                  f"(${strikes['sell_put']:,} - ${strikes['sell_call']:,})")

def mostrar_info_sistema(agente):
    """
    Muestra información del sistema y configuración
    """
    print("\n" + "="*60)
    print("💻 INFORMACIÓN DEL SISTEMA")
    print("="*60)
    
    print(f"🎯 Sistema: Agente Iron Condor SPX")
    print(f"📈 Subyacente: {agente.spx_ticker} (S&P 500 Index)")
    print(f"📉 Volatilidad: {agente.vix_ticker} (VIX Index)")
    print(f"🔧 Alas permitidas: {agente.alas_permitidas}")
    print(f"📅 Fecha actual: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    print("\n⚙️ Lógica de cálculo:")
    print("   1. IV = (VIX/100 * SPX) + 10")
    print("   2. Sell Put = SPX - IV (redondeado al múltiplo de 5 superior)")
    print("   3. Buy Put = Sell Put - Ala")
    print("   4. Sell Call = SPX + IV (redondeado al múltiplo de 5 inferior)")
    print("   5. Buy Call = Sell Call + Ala")
    
    print("\n📏 Características:")
    print("   • Cálculo automático de strikes")
    print("   • Ajuste por implied volatility (VIX)")
    print("   • Buffer de seguridad (+10 puntos)")
    print("   • Redondeo a múltiplos de 5")
    print("   • Selección flexible de alas")
    print("   • Proyección hasta 7 días futuros")

def main():
    """
    Función principal del demo interactivo
    """
    agente = AgenteIronCondorSPX()
    
    print("🚀 Iniciando Demo Interactivo del Agente Iron Condor SPX...")
    
    while True:
        mostrar_menu_principal()
        
        try:
            opcion = int(input("\n➡️ Seleccione una opción (1-5): "))
            
            if opcion == 1:
                calculo_rapido(agente)
                
            elif opcion == 2:
                calculo_personalizado(agente)
                
            elif opcion == 3:
                comparar_alas(agente)
                
            elif opcion == 4:
                mostrar_info_sistema(agente)
                
            elif opcion == 5:
                print("\n👋 ¡Gracias por usar el Agente Iron Condor SPX!")
                print("🎆 Sistema desarrollado por MiniMax Agent")
                break
                
            else:
                print("❌ Opción inválida. Seleccione entre 1 y 5.")
            
            # Pausa para leer resultados
            if opcion in [1, 2, 3, 4]:
                input("\n⏸️ Presione Enter para continuar...")
                
        except ValueError:
            print("❌ Por favor ingrese un número válido.")
        except KeyboardInterrupt:
            print("\n\n🚫 Operación cancelada por el usuario.")
            break
        except Exception as e:
            print(f"\n❌ Error inesperado: {e}")
            print("Volviendo al menú principal...")


if __name__ == "__main__":
    main()
