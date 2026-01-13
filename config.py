"""Constantes y parámetros de negocio para el cálculo de nómina."""

# ----------------------------
# SALARIO / JORNADA
# ----------------------------
SALARIO_BASICO_MENSUAL = 2233612
SALARIO_QUINCENA = SALARIO_BASICO_MENSUAL / 2

HORAS_JORNADA = 6
VALOR_HORA = 12409  # Salario / 120
VALOR_MINUTO = VALOR_HORA / 60

# ----------------------------
# AUXILIO / CÍVICAS
# ----------------------------
AUXILIO_TRANSPORTE = 200000  # Mensual
PASAJES_CIVICA_CANTIDAD = 22
PASAJES_CIVICA_VALOR = 3430

# ----------------------------
# DEDUCCIONES
# ----------------------------
DEDUCCIONES_BASE = {
    "Salud": 0.04,
    "Pensión": 0.04,
}

# ----------------------------
# RECARGOS
# ----------------------------
# Porcentajes de recargo (se suman al valor hora base)
RECARGO_ORDINARIO_NOCTURNO = 0.35  # +35%
RECARGO_DOMINICAL_DIURNO = 0.80    # +80%
RECARGO_DOMINICAL_NOCTURNO = 2.10  # +210%

FRANJA_DIURNA = (6, 21)
FRANJA_NOCTURNA = (21, 6)
