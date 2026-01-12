
# 🧮 Aplicación Web de Cálculo de Nómina por Turnos (Colombia)

Aplicación web **100 % frontend** para el **cálculo de nómina basada en turnos laborales**, desarrollada conforme a la **normativa laboral colombiana vigente**, sin base de datos, sin servidor dedicado y desplegable en **hosting gratuito**.

Diseñada para escenarios donde el trabajador **solo interactúa con códigos de turno**, sin acceso a valores sensibles como salario base o valor hora.

---

## 🎯 Objetivo

Calcular de forma **precisa, auditable y transparente**:

* Salario por turnos laborales
* Recargos legales (diurnos, nocturnos, festivos)
* Días especiales (suspensión, compensatorio, incapacidad)
* Auxilio de transporte ajustado
* Deducciones legales
* Neto final a pagar por quincena

---

## ⚙️ Características Principales

✔️ Aplicación **100 % web**
✔️ Desplegable en **Streamlit Cloud (gratuito)**
✔️ **Sin base de datos**
✔️ **Sin backend dedicado**
✔️ Turnos definidos en **JSON interno**
✔️ Usuario **NO edita JSON**
✔️ Usuario **NO ingresa salario ni valor hora**
✔️ Cálculo **por minuto trabajado**
✔️ Turnos que **cruzan medianoche**
✔️ Cumple normativa laboral colombiana

---

## 🏗️ Arquitectura del Proyecto

```
nomina_app/
├── app.py              # Interfaz web (Streamlit)
├── calculos.py         # Motor de cálculo de nómina
├── config.py           # Configuración salarial interna
├── turnos.json         # Turnos definidos por código
└── requirements.txt    # Dependencias
```

---

## 🔐 Seguridad y Control

| Elemento           | Acceso Usuario |
| ------------------ | -------------- |
| Salario base       | ❌ No editable  |
| Valor hora         | ❌ No editable  |
| Turnos             | ❌ No editable  |
| JSON               | ❌ No editable  |
| Deducciones base   | ❌ No editable  |
| Códigos de turno   | ✅ Sí           |
| Botones especiales | ✅ Sí           |

Todos los valores críticos están **blindados en código**.

---

## 🧾 Modelo de Turnos (`turnos.json`)

Cada turno representa **1 día laboral** y puede repetirse ilimitadamente.

```json
{
  "codigo": "D1",
  "descripcion": "Turno diurno normal",
  "hora_inicio": "06:00",
  "hora_fin": "14:00",
  "descanso": ["10:00", "10:30"],
  "festivo": false
}
```

### Reglas

* El descanso **nunca se paga**
* El turno puede cruzar medianoche
* El campo `festivo` define el recargo
* No se calcula calendario de festivos

---

## ⚖️ Normativa Laboral Colombiana Aplicada

### Franjas Horarias

* **Diurna:** 06:00 – 19:00
* **Nocturna:** 19:00 – 06:00

### Recargos

| Tipo               | % Pago |
| ------------------ | ------ |
| Ordinaria diurna   | 100 %  |
| Ordinaria nocturna | 135 %  |
| Extra diurna       | 125 %  |
| Extra nocturna     | 175 %  |
| Festivo diurno     | 175 %  |
| Festivo nocturno   | 210 %  |

---

## 🖥️ Interfaz de Usuario

El usuario puede:

* Seleccionar quincena (15 o 30)
* Ingresar códigos de turno
* Ver lista acumulada de turnos
* Agregar días especiales mediante botones
* Visualizar totales en tiempo real

### Botones Especiales

#### 🔴 SUSPENSIÓN (SUSPE)

* No se paga
* No genera recargos
* No cuenta como día trabajado
* Descuenta auxilio de transporte

#### 🟡 COMPENSATORIO (CP)

* Paga solo 6 horas básicas
* No genera recargos ni extras
* Sí cuenta como día trabajado
* No afecta auxilio

#### 🔵 INCAPACIDAD

* Pago al **66.67 %**
* No genera recargos
* No genera extras
* Descuenta auxilio
* No cuenta como día trabajado completo

---

## 🧮 Reglas de Cálculo

* Cálculo **por minuto**
* Descansos excluidos
* Turnos independientes
* Días especiales no usan turnos
* Auxilio solo en quincena 30
* Auxilio sin deducciones
* Auxilio proporcional a días no laborados

---

## 💰 Configuración Salarial (`config.py`)

Definida **exclusivamente en código**:

* Salario base mensual
* Valor hora
* Jornada diaria contractual (6 horas)
* Auxilio de transporte
* Porcentajes de deducciones legales

---

## 🚀 Despliegue en Streamlit Cloud

### Pasos

1. Crear repositorio en GitHub
2. Subir el proyecto completo
3. Ir a 👉 [https://share.streamlit.io](https://share.streamlit.io)
4. Conectar el repositorio
5. Seleccionar `app.py`
6. Deploy

⏱️ Tiempo estimado: **menos de 2 minutos**

---

## 📦 Requisitos

```
Python 3.10+
streamlit
```

---

## 🧠 Enfoque de Diseño

* Arquitectura **simple, auditable y mantenible**
* Sin dependencias innecesarias
* Ideal para:

  * Empresas pequeñas
  * Cooperativas
  * Control personal de nómina
  * Proyectos académicos
  * Simuladores laborales

---

## 📄 Licencia

Uso libre con fines educativos y de simulación.
Para uso empresarial, se recomienda validación legal adicional.

---

## ✨ Próximas Extensiones (Opcionales)

* Exportación a PDF
* Detalle diario por turno
* Auditoría de recargos
* Modo empresa multi-convenio
* Soporte multi-usuario (sin BD)

---

**Desarrollado como sistema de nómina real bajo normativa colombiana.**
**Sin atajos. Sin valores ocultos. Sin decisiones abiertas.**
