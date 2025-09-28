#!/usr/bin/env python3
"""
Agente de Iron Condor SPX - Versión Web Simplificada
Calcula automáticamente los strikes de un iron condor usando datos simulados

Autor: MiniMax Agent  
Fecha: 2025-09-28
"""

from datetime import datetime, timedelta
import math
from typing import Dict, Optional, Tuple
import random

class AgenteIronCondorSPX:
    """
    Agente para calcular automáticamente los strikes de un iron condor en SPX
    basado en Implied Volatility y parámetros configurables.
    Versión simplificada con datos simulados para máxima compatibilidad.
    """
    
    def __init__(self):
        self.spx_ticker = "^GSPC"  # S&P 500 Index
        self.vix_ticker = "^VIX"   # VIX para Implied Volatility
        self.alas_permitidas = [10, 15, 20, 25]
        self.periodos_disponibles = {
            'diario': 252,      # Días trading por año
            'semanal': 52,      # Semanas por año
            'mensual': 12,      # Meses por año
            'anual': 1          # Año completo
        }
        self.periodo_default = 'diario'  # Período por defecto más conservador
        
    def obtener_datos_mercado(self, fecha_objetivo: Optional[str] = None) -> Dict:
        """
        Obtiene datos simulados del SPX y VIX para garantizar funcionamiento
        
        Args:
            fecha_objetivo: Fecha en formato 'YYYY-MM-DD' (hasta 7 días en el futuro)
            
        Returns:
            Dict con valores simulados de SPX y VIX
        """
        return self._obtener_datos_simulados(fecha_objetivo)
    
    def _obtener_datos_simulados(self, fecha_objetivo: Optional[str] = None) -> Dict:
        """
        Genera datos simulados realistas para demostración
        """
        # Valores base realistas (aproximados a septiembre 2025)
        spx_base = 5650.0  # SPX aproximado
        vix_base = 18.5    # VIX típico
        
        # Agregar algo de variabilidad realista
        spx_variacion = random.uniform(-0.01, 0.01)  # ±1%
        vix_variacion = random.uniform(-0.05, 0.05)  # ±5%
        
        spx_simulado = round(spx_base * (1 + spx_variacion), 2)
        vix_simulado = round(vix_base * (1 + vix_variacion), 2)
        
        return {
            'spx_valor': spx_simulado,
            'vix_valor': vix_simulado,
            'fecha_datos': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'fecha_objetivo': fecha_objetivo or 'Actual',
            'fuente_datos': 'Datos Simulados (Demo)'
        }
    
    def validar_fecha(self, fecha_str: str) -> bool:
        """
        Valida que la fecha esté dentro del rango permitido (hasta 7 días en el futuro)
        """
        try:
            fecha_objetivo = datetime.strptime(fecha_str, '%Y-%m-%d')
            fecha_actual = datetime.now()
            diferencia = (fecha_objetivo - fecha_actual).days
            
            return 0 <= diferencia <= 7
        except:
            return False
    
    def redondear_multiplo_5_superior(self, valor: float) -> int:
        """
        Redondea al múltiplo de 5 superior
        """
        return int(math.ceil(valor / 5) * 5)
    
    def redondear_multiplo_5_inferior(self, valor: float) -> int:
        """
        Redondea al múltiplo de 5 inferior
        """
        return int(math.floor(valor / 5) * 5)
    
    def calcular_iv_puntos(self, spx_valor: float, vix_porcentaje: float, 
                          periodo: str = None, buffer: int = 10) -> Dict:
        """
        Convierte VIX (porcentaje) a puntos del SPX con ajuste temporal correcto
        
        Args:
            spx_valor: Valor actual del SPX
            vix_porcentaje: VIX en porcentaje (volatilidad anualizada)
            periodo: 'diario', 'semanal', 'mensual', 'anual'
            buffer: Buffer de seguridad en puntos
            
        Returns:
            Dict con IV calculado y detalles
        """
        if periodo is None:
            periodo = self.periodo_default
            
        if periodo not in self.periodos_disponibles:
            raise ValueError(f"Período debe ser uno de: {list(self.periodos_disponibles.keys())}")
        
        # Convertir VIX de porcentaje a decimal
        vix_decimal = vix_porcentaje / 100
        
        # Calcular movimiento anualizado
        iv_anual = spx_valor * vix_decimal
        
        # Ajustar por período temporal usando raíz cuadrada del tiempo
        factor_tiempo = self.periodos_disponibles[periodo]
        iv_periodo = iv_anual / math.sqrt(factor_tiempo)
        
        # Sumar buffer de seguridad
        iv_final = iv_periodo + buffer
        
        return {
            'iv_final': round(iv_final, 2),
            'iv_anual': round(iv_anual, 2),
            'iv_periodo': round(iv_periodo, 2),
            'periodo_usado': periodo,
            'factor_tiempo': factor_tiempo,
            'buffer_aplicado': buffer
        }
    
    def calcular_strikes(self, spx_valor: float, iv_puntos: float, ala: int) -> Dict:
        """
        Calcula todos los strikes del iron condor según la especificación
        
        Args:
            spx_valor: Valor del SPX
            iv_puntos: Implied Volatility en puntos + 10
            ala: Ancho del ala (10, 15, 20, 25)
            
        Returns:
            Dict con todos los strikes calculados
        """
        # Cálculo de Puts
        sell_put_raw = spx_valor - iv_puntos
        sell_put = self.redondear_multiplo_5_superior(sell_put_raw)
        buy_put = sell_put - ala
        
        # Cálculo de Calls
        sell_call_raw = spx_valor + iv_puntos
        sell_call = self.redondear_multiplo_5_inferior(sell_call_raw)
        buy_call = sell_call + ala
        
        return {
            'sell_put': sell_put,
            'buy_put': buy_put,
            'sell_call': sell_call,
            'buy_call': buy_call,
            'ancho_ala': ala,
            'rango_profit': sell_call - sell_put,
            'iv_usado': iv_puntos
        }
    
    def ejecutar_calculo_completo(self, fecha_objetivo: Optional[str] = None, 
                                 ala: int = 25, periodo: str = None, buffer: int = 10) -> Dict:
        """
        Ejecuta el cálculo completo del iron condor
        
        Args:
            fecha_objetivo: Fecha objetivo (opcional)
            ala: Ancho del ala (10, 15, 20, 25)
            
        Returns:
            Dict con todos los resultados
        """
        # Validaciones
        if ala not in self.alas_permitidas:
            raise ValueError(f"Ala debe ser uno de: {self.alas_permitidas}")
        
        if fecha_objetivo and not self.validar_fecha(fecha_objetivo):
            raise ValueError("Fecha debe estar entre hoy y 7 días en el futuro")
        
        # Obtener datos del mercado (simulados)
        datos_mercado = self.obtener_datos_mercado(fecha_objetivo)
        if not datos_mercado:
            raise Exception("No se pudieron obtener datos del mercado")
        
        # Calcular IV en puntos con ajuste temporal correcto
        iv_resultado = self.calcular_iv_puntos(
            datos_mercado['spx_valor'], 
            datos_mercado['vix_valor'],
            periodo=periodo,
            buffer=buffer
        )
        
        iv_puntos = iv_resultado['iv_final']
        
        # Calcular strikes
        strikes = self.calcular_strikes(
            datos_mercado['spx_valor'], 
            iv_puntos, 
            ala
        )
        
        # Agregar información del IV al resultado de strikes
        strikes.update({
            'iv_detalles': iv_resultado
        })
        
        # Compilar resultado completo
        resultado = {
            'datos_mercado': datos_mercado,
            'parametros': {
                'ala_elegida': ala,
                'iv_original_vix': datos_mercado['vix_valor'],
                'iv_puntos_calculado': iv_puntos,
                'periodo_temporal': iv_resultado['periodo_usado'],
                'iv_anualizado': iv_resultado['iv_anual'],
                'iv_ajustado_tiempo': iv_resultado['iv_periodo'],
                'buffer_agregado': iv_resultado['buffer_aplicado'],
                'factor_tiempo': iv_resultado['factor_tiempo']
            },
            'strikes': strikes,
            'resumen_estrategia': self._generar_resumen_estrategia(datos_mercado, strikes)
        }
        
        return resultado
    
    def _generar_resumen_estrategia(self, datos_mercado: Dict, strikes: Dict) -> Dict:
        """
        Genera un resumen de la estrategia calculada
        """
        spx_valor = datos_mercado['spx_valor']
        
        return {
            'tipo_estrategia': 'Iron Condor',
            'subyacente': 'SPX',
            'valor_spx': spx_valor,
            'strikes_puts': f"{strikes['buy_put']}/{strikes['sell_put']}",
            'strikes_calls': f"{strikes['sell_call']}/{strikes['buy_call']}",
            'rango_rentabilidad': f"{strikes['sell_put']} - {strikes['sell_call']}",
            'amplitud_rango': strikes['rango_profit'],
            'distancia_spx_sell_put': spx_valor - strikes['sell_put'],
            'distancia_spx_sell_call': strikes['sell_call'] - spx_valor,
            'simetria': abs((spx_valor - strikes['sell_put']) - (strikes['sell_call'] - spx_valor))
        }
    
    def mostrar_resultado_formateado(self, resultado: Dict):
        """
        Muestra el resultado en formato legible
        """
        print("\n" + "="*80)
        print("🎯 AGENTE IRON CONDOR SPX - RESULTADO FINAL")
        print("="*80)
        
        # Datos del mercado
        datos = resultado['datos_mercado']
        print(f"\n📊 DATOS DEL MERCADO:")
        print(f"   📈 SPX: ${datos['spx_valor']:,.2f}")
        print(f"   📊 VIX: {datos['vix_valor']:.2f}%")
        print(f"   🕒 Fecha: {datos['fecha_datos']}")
        print(f"   📍 Fuente: {datos['fuente_datos']}")
        
        # Parámetros
        params = resultado['parametros']
        print(f"\n⚙️ PARÁMETROS:")
        print(f"   🎯 Ala elegida: {params['ala_elegida']} puntos")
        print(f"   📊 IV original (VIX): {params['iv_original_vix']:.2f}%")
        print(f"   📈 IV anualizado: {params['iv_anualizado']:.2f} puntos")
        print(f"   ⏰ Período: {params['periodo_temporal']}")
        print(f"   📊 IV ajustado tiempo: {params['iv_ajustado_tiempo']:.2f} puntos")
        print(f"   🛡️ Buffer agregado: {params['buffer_agregado']} puntos")
        print(f"   🎯 IV final usado: {params['iv_puntos_calculado']:.2f} puntos")
        
        # Strikes
        strikes = resultado['strikes']
        print(f"\n🎯 STRIKES CALCULADOS:")
        print(f"   🔴 Buy Put:  ${strikes['buy_put']:,}")
        print(f"   🟢 Sell Put: ${strikes['sell_put']:,}")
        print(f"   🟢 Sell Call: ${strikes['sell_call']:,}")
        print(f"   🔴 Buy Call: ${strikes['buy_call']:,}")
        
        # Resumen de la estrategia
        resumen = resultado['resumen_estrategia']
        print(f"\n📋 RESUMEN DE LA ESTRATEGIA:")
        print(f"   📊 Tipo: {resumen['tipo_estrategia']}")
        print(f"   📈 Subyacente: {resumen['subyacente']}")
        print(f"   💰 Rango de rentabilidad: ${resumen['rango_rentabilidad']}")
        print(f"   📏 Amplitud del rango: {resumen['amplitud_rango']} puntos")
        print(f"   ⬇️ Distancia a Sell Put: {resumen['distancia_spx_sell_put']:.2f} puntos")
        print(f"   ⬆️ Distancia a Sell Call: {resumen['distancia_spx_sell_call']:.2f} puntos")
        print(f"   ⚖️ Simetría: {resumen['simetria']:.2f} puntos")
        
        print("\n" + "="*80)
        print("✅ Cálculo completado exitosamente")
        print("="*80)