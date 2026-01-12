
# 🧮 Calculadora de Nómina por Turnos

Una aplicación web para calcular la nómina de conductores de TA en Colombia, considerando turnos, recargos, deducciones y beneficios laborales.

---

## ¿Qué Hace?

Calcula automáticamente:

- **Salario por turnos** - Ingresa códigos de turno (ej: D1, 162CC, 284M)
- **Recargos diurnos, nocturnos y festivos** - Según la hora del turno
- **Eventos especiales** - Suspensiones, licencias, compensatorios, incapacidades
- **Horas extras** - Con sus porcentajes correspondientes
- **Auxilio de transporte** - Ajustado según los días trabajados
- **Civicas (pasajes)** - Descuentos automáticos por eventos
- **Deducciones legales** - Salud y pensión
- **Neto final** - Resultado neto a pagar por quincena

---

## 📋 Características

✅ **100% Web** - Sin instalación, funciona en el navegador  
✅ **Cálculo exacto** - Por minuto trabajado  
✅ **Turnos nocturnos** - Soporta turnos que cruzan medianoche  
✅ **Recargos automáticos** - Calcula según franjas horarias  
✅ **Dos quincenas** - 15 y 30 días  
✅ **Transparente** - Desglose completo de todos los conceptos  

---

## 🚀 Cómo Usar

1. Selecciona la quincena (15 o 30)
2. Agrega turnos ingresando el código
3. Usa los botones para eventos especiales (Suspensión, Licencia, CP, Incapacidad)
4. Agrega horas extras si las hay
5. Visualiza el resultado con el desglose completo

---

## 💰 Qué Calcula

**Devengados:**
- Salario de turnos regulares
- Recargos por horas nocturnas (+35%)
- Recargos por horas dominicales (+80% diurno, +210% nocturno)
- Horas extras
- Auxilio de transporte
- Civicas (pasajes de transporte)

**Deducciones:**
- Salud (4%)
- Pensión (4%)
- Otras deducciones manuales

**Resultado:** Neto = Devengado + Auxilio + Civicas - Deducciones

---

## ⚡ Eventos Especiales

| Evento | Efecto |
|--------|--------|
| **Suspensión** | No se paga, descuenta civica y auxilio |
| **Licencia** | No se paga, descuenta civica y auxilio |
| **CP (Compensatorio)** | Paga 6 horas base, descuenta civica |
| **Incapacidad** | Paga 66.67%, descuenta civica y auxilio |

---

## 📁 Estructura

```
Calculadora-de-nomina/
├── app.py              # Interfaz principal
├── config.py           # Salarios y configuración
├── services/
│   └── calculadora.py  # Motor de cálculos
├── models/
│   └── turno.py        # Definición de turnos
├── turnos.json         # Base de códigos de turnos
└── requirements.txt    # Dependencias
```

---

## 📊 Recargos Aplicados

- **Nocturno ordinario:** +35%
- **Dominical diurno:** +80%
- **Dominical nocturno:** +210%

---

## 🔐 Seguridad

- Salarios y valores están protegidos en el código
- El usuario solo ingresa códigos de turnos
- Cálculos auditables y transparentes
- Sin base de datos

---

## 📦 Requisitos

- Python 3.10+
- Streamlit

---

**Desarrollado por:** Reiber
