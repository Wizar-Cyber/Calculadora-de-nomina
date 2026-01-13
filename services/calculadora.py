from datetime import datetime, timedelta
from config import *

class CalculadoraNomina:

    """Motor de cálculo de nómina por quincena.

    Responsabilidades:
    - Acumular devengado (salario base + recargos + extras + eventos)
    - Calcular deducciones base (salud/pensión) y manuales
    - Calcular cívicas y auxilio según reglas de negocio

    Nota: los turnos pueden cruzar medianoche; los cálculos contemplan ese caso.
    """

    # Calculadora principal:
    # - Acumula devengado (salario + recargos + extras)
    # - Lleva deducciones manuales y cálculo de deducciones base
    # - Calcula cívicas y auxilio según reglas de la quincena

    def __init__(self, quincena="30"):
        # Estado principal de la quincena
        self.devengado = SALARIO_QUINCENA
        self.quincena = quincena
        self.valor_dia_basico = SALARIO_QUINCENA / 15
        self.detalles_turnos = []  # Solo para cálculos intermedios
        self.detalles_desglose = []  # Para mostrar en el desglose
        self.deducciones_manuales = []
        self.dias_incapacidad = 0
        self.dias_trabajados = 15  # Por defecto 15 días de quincena
        self.recargos_agrupados = {}  # Agrupar recargos por tipo
        self.civicas_cantidad = 0
        self.civicas_valor = 0
        self.cp_agregado = False  # Bandera para rastrear si se agregó CP

    def reinicializar(self, quincena=None):
        """Reinicia la calculadora a su estado inicial"""
        if quincena is None:
            quincena = self.quincena
        self.__init__(quincena=quincena)

    def horas_turno_completo(self, turno):
        # Retorna horas totales del turno (incluye cruce de medianoche)
        inicio = turno.hora_inicio_obj()
        fin = turno.hora_fin_obj()
        if fin <= inicio:
            fin += timedelta(days=1)
        minutos = (fin - inicio).total_seconds() / 60
        return minutos / 60  # horas totales incluyendo descanso

    # ----------------------------
    # CÁLCULO DE RECARGOS
    # ----------------------------
    def calcular_horas_por_franja(self, turno):
        """Divide las horas reales del turno por franja horaria: diurna (6-21) y nocturna (21-6)"""
        inicio = turno.hora_inicio_obj()
        fin = turno.hora_fin_obj()
        
        if fin <= inicio:
            fin += timedelta(days=1)
        
        horas_diurnas = 0.0
        horas_nocturnas = 0.0
        
        # Encontrar puntos de transición que están DENTRO del rango del turno
        # Las transiciones son a las 06:00 y 21:00
        puntos_transicion = []
        
        # Crear puntos de transición para el día del inicio
        dia_inicio = inicio.date()
        hora_06_inicio = datetime.combine(dia_inicio, datetime.min.time().replace(hour=6))
        hora_21_inicio = datetime.combine(dia_inicio, datetime.min.time().replace(hour=21))
        
        if hora_06_inicio > inicio and hora_06_inicio < fin:
            puntos_transicion.append(hora_06_inicio)
        if hora_21_inicio > inicio and hora_21_inicio < fin:
            puntos_transicion.append(hora_21_inicio)
        
        # Crear puntos de transición para el día siguiente (si el turno cruza medianoche)
        dia_siguiente = dia_inicio + timedelta(days=1)
        hora_06_siguiente = datetime.combine(dia_siguiente, datetime.min.time().replace(hour=6))
        hora_21_siguiente = datetime.combine(dia_siguiente, datetime.min.time().replace(hour=21))
        
        if hora_06_siguiente > inicio and hora_06_siguiente < fin:
            puntos_transicion.append(hora_06_siguiente)
        if hora_21_siguiente > inicio and hora_21_siguiente < fin:
            puntos_transicion.append(hora_21_siguiente)
        
        # Ordenar puntos de transición
        puntos_transicion.sort()
        
        # Construir segmentos: inicio -> primer punto -> segundo punto -> ... -> fin
        segmentos = [inicio] + puntos_transicion + [fin]
        
        # Procesar cada segmento
        for i in range(len(segmentos) - 1):
            tiempo_inicio = segmentos[i]
            tiempo_fin = segmentos[i + 1]
            
            if tiempo_inicio >= tiempo_fin:
                continue
            
            minutos_segmento = (tiempo_fin - tiempo_inicio).total_seconds() / 60
            horas_segmento = minutos_segmento / 60
            
            # Determinar si este segmento es diurno o nocturno
            # Usamos la hora del inicio del segmento
            if tiempo_inicio.hour >= 21 or tiempo_inicio.hour < 6:
                horas_nocturnas += horas_segmento
            else:
                horas_diurnas += horas_segmento
        
        return horas_diurnas, horas_nocturnas

    def turno_toca_horas_nocturnas(self, turno):
        """Verifica si el turno incluye horas entre 21:00 y 06:00"""
        inicio = turno.hora_inicio_obj()
        fin = turno.hora_fin_obj()
        if fin <= inicio:
            fin += timedelta(days=1)
        
        # Si inicia en nocturno (21-06)
        if inicio.hour >= 21 or inicio.hour < 6:
            return True
        # Si termina en nocturno (después de las 21 o antes de las 6)
        if fin.hour >= 21 or fin.hour < 6:
            return True
        # Si pasa por la medianoche
        if inicio < fin and inicio.replace(hour=21, minute=0, second=0) < fin:
            return True
        return False

    def calcular_recargo(self, turno):
        """Calcula recargos de un turno según franja (diurna/nocturna) y festivo."""
        # Calcula el valor de recargos del turno y guarda detalles para el desglose.
        horas_diurnas, horas_nocturnas = self.calcular_horas_por_franja(turno)
        festivo = turno.festivo
        valor_total = 0

        # Festivo / dominical
        if festivo:
            # Recargo dominical diurno (6-21): +80%
            if horas_diurnas > 0:
                valor_diurno = horas_diurnas * VALOR_HORA * RECARGO_DOMINICAL_DIURNO
                valor_total += valor_diurno
                self.detalles_turnos.append(("R FESTIVO DIURN", valor_diurno, horas_diurnas))
                if "R FESTIVO DIURN" not in self.recargos_agrupados:
                    self.recargos_agrupados["R FESTIVO DIURN"] = {"valor": 0, "horas": 0}
                self.recargos_agrupados["R FESTIVO DIURN"]["valor"] += valor_diurno
                self.recargos_agrupados["R FESTIVO DIURN"]["horas"] += horas_diurnas
            
            # Recargo dominical nocturno (21-06): +210%
            if horas_nocturnas > 0:
                valor_nocturno = horas_nocturnas * VALOR_HORA * RECARGO_DOMINICAL_NOCTURNO
                valor_total += valor_nocturno
                self.detalles_turnos.append(("R FESTIVO NOCT", valor_nocturno, horas_nocturnas))
                if "R FESTIVO NOCT" not in self.recargos_agrupados:
                    self.recargos_agrupados["R FESTIVO NOCT"] = {"valor": 0, "horas": 0}
                self.recargos_agrupados["R FESTIVO NOCT"]["valor"] += valor_nocturno
                self.recargos_agrupados["R FESTIVO NOCT"]["horas"] += horas_nocturnas

        # Ordinario
        else:
            # Solo hay recargo nocturno en ordinario: +35%
            if horas_nocturnas > 0:
                valor_nocturno = horas_nocturnas * VALOR_HORA * RECARGO_ORDINARIO_NOCTURNO
                valor_total += valor_nocturno
                self.detalles_turnos.append(("R ORDINARIO NOC", valor_nocturno, horas_nocturnas))
                if "R ORDINARIO NOC" not in self.recargos_agrupados:
                    self.recargos_agrupados["R ORDINARIO NOC"] = {"valor": 0, "horas": 0}
                self.recargos_agrupados["R ORDINARIO NOC"]["valor"] += valor_nocturno
                self.recargos_agrupados["R ORDINARIO NOC"]["horas"] += horas_nocturnas
        
        return valor_total

    # ----------------------------
    # TURNOS
    # ----------------------------
    def agregar_turno(self, turno):
        """Agrega un turno base y suma únicamente los recargos correspondientes."""
        # Agrega un turno base y suma recargos según la franja y si es festivo/dominical.
        valor = self.calcular_recargo(turno)
        self.devengado += valor

    def agregar_dispo(self, inicio, fin, festivo):
        # Crea un turno especial "DISPO" y lo procesa como un turno normal.
        from models.turno import Turno
        t = Turno({
            "codigo": "DISPO",
            "descripcion": "Disponible",
            "hora_inicio": inicio,
            "hora_fin": fin,
            "festivo": festivo
        })
        self.agregar_turno(t)

    # ----------------------------
    # EVENTOS ESPECIALES
    # ----------------------------
    def agregar_cp(self):
        """Agrega un compensatorio (CP): suma una jornada completa al devengado."""
        # CP: agrega un día equivalente (jornada completa) al devengado.
        valor = HORAS_JORNADA * VALOR_HORA
        self.devengado += valor
        self.cp_agregado = True  # Marcar que se agregó CP

    def agregar_incapacidad(self):
        """Agrega un día de incapacidad: paga al 66.67% y ajusta días trabajados."""
        # Incapacidad: reduce días trabajados y paga al 66.67%.
        self.dias_incapacidad += 1
        self.dias_trabajados -= 1
        # Ya existe el día completo dentro del básico; solo se descuenta el 33.33%.
        self.devengado -= self.valor_dia_basico * (1 - 0.6667)

    def agregar_suspension(self):
        """Agrega suspensión: descuenta una jornada del básico y ajusta días trabajados."""
        # Suspensión: descuenta un día del básico.
        # Restar 6 horas (1 día) del básico
        self.devengado -= self.valor_dia_basico
        self.dias_trabajados -= 1

    def agregar_licencia(self):
        """Agrega licencia no remunerada: descuenta una jornada del básico."""
        # Licencia: descuenta un día del básico.
        # Restar 6 horas (1 día) del básico
        self.devengado -= self.valor_dia_basico
        self.dias_trabajados -= 1

    # ----------------------------
    # HORAS EXTRAS
    # ----------------------------
    def agregar_extra(self, minutos, recargo, nombre):
        # Agrega una hora extra: base por minuto * factor de recargo.
        base = minutos * VALOR_MINUTO
        valor = base * recargo
        self.devengado += valor
        horas = minutos / 60
        self.detalles_desglose.append((nombre, horas, valor))

    # ----------------------------
    # DEDUCCIONES
    # ----------------------------
    def agregar_deduccion_manual(self, nombre, valor):
        # Deducción ingresada por el usuario.
        self.deducciones_manuales.append((nombre, valor))

    def get_deducciones_desglosadas(self):
        """Retorna el detalle de deducciones (base + manuales) como dict concepto->valor."""
        # Retorna deducciones base (porcentaje del devengado) + deducciones manuales.
        deducciones = {}
        # Calcular porcentajes del devengado (sin cívicas ni auxilio, que no son salario)
        for concepto, porcentaje in DEDUCCIONES_BASE.items():
            valor = self.devengado * porcentaje
            deducciones[concepto] = valor
        # Agregar deducciones manuales
        for concepto, valor in self.deducciones_manuales:
            if concepto not in deducciones:
                deducciones[concepto] = 0
            deducciones[concepto] += valor
        return deducciones

    def total_deducciones(self):
        return sum(self.get_deducciones_desglosadas().values())

    # ----------------------------
    # CÍVICAS Y AUXILIO
    # ----------------------------
    def tiene_cp(self):
        # Indica si se agregó CP (impacta el cálculo de cívicas).
        return self.cp_agregado

    def tiene_suspension(self):
        # Detecta suspensión/licencia (impacta el cálculo de cívicas).
        return self.dias_trabajados < 15 and self.dias_incapacidad == 0

    def calcular_civicas(self):
        """Calcula cantidad y valor de cívicas según CP y suspensión/licencia."""
        # Calcula la cantidad/valor de cívicas según reglas y eventos agregados.
        # Comenzar con 22 civicas
        self.civicas_cantidad = PASAJES_CIVICA_CANTIDAD
        
        # Si hay CP, restar 1
        if self.tiene_cp():
            self.civicas_cantidad -= 1
        
        # Si hay suspensión, restar 2
        if self.tiene_suspension():
            self.civicas_cantidad -= 2
        
        # No puede ser negativo
        if self.civicas_cantidad < 0:
            self.civicas_cantidad = 0
        
        self.civicas_valor = self.civicas_cantidad * PASAJES_CIVICA_VALOR

    def total_civicas(self):
        self.calcular_civicas()
        return self.civicas_valor

    def total_auxilio(self):
        """Calcula auxilio de transporte para quincena 30, descontando días no laborados."""
        # Auxilio de transporte: $200.000 mensuales = $6.666,67 por día (200.000/30)
        # Se paga completo en quincena 30, pero se resta por cada día de suspensión/licencia/incapacidad
        if self.quincena == "30":
            valor_diario_auxilio = AUXILIO_TRANSPORTE / 30
            dias_descuento = 15 - self.dias_trabajados + self.dias_incapacidad
            auxilio = AUXILIO_TRANSPORTE - (dias_descuento * valor_diario_auxilio)
            return max(0, auxilio)  # No puede ser negativo
        return 0
