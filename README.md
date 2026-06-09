# Lab 9 — Automatización de Pruebas y Gestión de Defectos

**Asignatura:** Especialidad I: Calidad de Software  
**Carrera:** Ingeniería Civil Informática  
**Universidad Autónoma de Chile — Campus Talca**

---

## Configuración del entorno

```bash
# Crear y activar entorno virtual (Windows)
python -m venv .venv
.venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

---

## Ejecución de la suite de pruebas

```bash
# Tests unitarios (verbose)
pytest tests/ -v

# Tests con reporte de cobertura en terminal
pytest tests/ -v --cov=app --cov-report=term-missing

# Verificar umbral mínimo del 80%
pytest tests/ --cov=app --cov-fail-under=80

# Suite BDD con Behave
behave features/
```

---

## Bugs detectados en app/descuentos.py

### BUG-LAB9-001 — Falta validación de total negativo

| Campo | Detalle |
|-------|---------|
| **Módulo** | `app/descuentos.py` |
| **Función** | `calcular_descuento(total, codigo)` |
| **Severidad** | MEDIUM |
| **Prioridad** | P3 |
| **Test que lo detectó** | `test_descuento_no_acepta_total_negativo` |

**Código original (buggy):**
```python
porcentaje = CODIGOS_DESCUENTO.get(codigo, 0)
return total * porcentaje  # sin validación previa de total < 0
```

**Resultado actual:** `calcular_descuento(-50, 'PROMO10')` retorna `-5.0` sin lanzar excepción.  
**Resultado esperado:** Debe lanzar `ValueError('El total no puede ser negativo')`.  
**Fix aplicado:** Agregar al inicio del cuerpo de la función:
```python
if total < 0:
    raise ValueError("El total no puede ser negativo")
```

---

### BUG-LAB9-002 — Fórmula de descuento incorrecta

| Campo | Detalle |
|-------|---------|
| **Módulo** | `app/descuentos.py` |
| **Función** | `calcular_descuento(total, codigo)` |
| **Severidad** | HIGH |
| **Prioridad** | P2 |
| **Tests que lo detectaron** | `test_calcular_descuento[100-PROMO10-90.0]`, `test_calcular_descuento[200-PROMO20-160.0]`, `test_calcular_descuento[500-PROMO10-450.0]`, `test_calcular_descuento[100-INVALIDO-100.0]`, `test_calcular_descuento[100--100.0]` |

**Código original (buggy):**
```python
return total * porcentaje
```

**Resultado actual:** `calcular_descuento(100, 'PROMO10')` retorna `10.0` (solo el monto del descuento).  
**Resultado esperado:** Debe retornar `90.0` (el total después de aplicar el descuento).  
**Fix aplicado:** Cambiar la fórmula a:
```python
return total * (1 - porcentaje)
```

---

## Respuestas a las preguntas del laboratorio

### Pregunta f) ¿Por qué es incorrecto usar la PasarelaPago real en los tests automáticos?

Usar la `PasarelaPago` real en los tests automáticos es incorrecto por tres razones fundamentales:

1. **Efectos secundarios reales:** cada ejecución del test realizaría cobros reales, con consecuencias financieras directas.
2. **Falta de determinismo:** el test dependería de la disponibilidad de red y del servicio externo; si la pasarela cae, el test falla por razones ajenas al código bajo prueba.
3. **Violación del aislamiento unitario:** un test unitario debe probar exclusivamente la lógica del `ProcesadorPago`, sin involucrar infraestructura externa. Al usar un mock se controlan exactamente las respuestas (éxito, error, timeout) y se valida el comportamiento del sistema ante cada caso.

---

### Pregunta g) ¿Qué diferencia existe entre un Stub y un Mock? ¿Cuál usaste en `test_pago_exitoso_retorna_txn_id`?

| Concepto | Descripción |
|----------|-------------|
| **Stub** | Test double que devuelve respuestas predefinidas. **No verifica** cómo ni cuántas veces fue llamado. |
| **Mock** | Test double que devuelve respuestas predefinidas **y además verifica** que fue llamado con los argumentos correctos y la cantidad de veces esperada (usando `assert_called_once_with`, `call_count`, etc.). |

En `test_pago_exitoso_retorna_txn_id` el `MagicMock` actúa como **Stub**: se configura `cobrar.return_value` y solo se verifica el resultado retornado, sin comprobar cómo se invocó la pasarela. En cambio, `test_pago_llama_pasarela_con_monto_correcto` usa el mismo `MagicMock` como **Mock**, porque llama a `assert_called_once_with(monto=250.0)`.

---

### Pregunta k) ¿Qué líneas quedaron sin cubrir al ejecutar el primer reporte? ¿Por qué?

Al ejecutar el primer reporte de cobertura (antes de agregar tests adicionales), las líneas no cubiertas típicamente son:

- **`carrito.py` — `raise ValueError("El precio no puede ser negativo")`**: ningún test invoca `agregar()` con precio negativo, por lo que ese branch nunca se ejecuta.
- **`pagos.py` — `raise ValueError("El monto debe ser mayor que cero")`**: ningún test llama a `procesar()` con `monto <= 0`, dejando esa rama sin ejercitar.

Estas líneas quedan sin cubrir porque los tests iniciales solo validan el **camino feliz** (happy path). Para cubrir los branches de error se necesitan tests que explícitamente provoquen esas condiciones de borde.

---

### Pregunta l) ¿Significa cobertura 100% que el software no tiene bugs?

**No.** La cobertura de código mide que cada línea fue **ejecutada** al menos una vez, pero no garantiza que la lógica sea **correcta**.

Ejemplo concreto de este laboratorio: el bug en `descuentos.py` con la fórmula `return total * porcentaje`. El caso `(0, 'PROMO10', 0.0)` del test parametrizado ejecuta esa línea y **pasa** (porque `0 * 0.10 = 0.0`), alcanzando cobertura total de esa línea. Sin embargo, la fórmula es incorrecta para cualquier total distinto de cero. La línea está "cubierta" pero contiene un bug que solo se detecta con valores de entrada adecuados. La cobertura 100% indica ausencia de código muerto, no ausencia de defectos lógicos.

---

### Pregunta o) ¿Cuál fue la severidad que asignaste a cada bug? Justifica tu decisión.

- **BUG-LAB9-001 (validación faltante) → MEDIUM**: el impacto es acotado porque solo ocurre con un input inválido (total negativo) que el sistema no debería recibir en condiciones normales. No rompe el flujo principal de descuentos.

- **BUG-LAB9-002 (fórmula incorrecta) → HIGH**: afecta **todos** los cálculos de descuento para cualquier total distinto de cero. Es el corazón de la lógica del módulo; ningún descuento se aplica correctamente mientras el bug exista, lo que tiene impacto económico directo en todas las transacciones.

---

### Pregunta p) ¿En qué se diferencia la severidad de la prioridad?

- **Severidad** (impacto técnico): mide qué tan grave es el defecto para el funcionamiento del software. Escala: CRITICAL → HIGH → MEDIUM → LOW.
- **Prioridad** (urgencia de negocio): mide con qué urgencia debe corregirse según el contexto del negocio. Escala: P1 → P2 → P3 → P4.

**Ejemplo donde difieren:** Un error tipográfico en el banner principal de la tienda (`"Bienvenido"` escrito como `"Bienvenio"`) tiene **severidad LOW** (no afecta ninguna funcionalidad) pero podría tener **prioridad P1** si hay una campaña publicitaria activa y miles de usuarios verán el error en las próximas horas. A la inversa, un crash en la función de exportación de reportes internos (usada solo por un administrador, una vez al mes) tiene **severidad HIGH** pero **prioridad P4** porque no afecta a los usuarios finales y puede esperar al próximo sprint.

---

## Estructura del proyecto

```
lab9-qa-automatizacion/
├── app/
│   ├── __init__.py
│   ├── carrito.py
│   ├── descuentos.py        ← bugs corregidos
│   └── pagos.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_carrito.py
│   ├── test_descuentos.py
│   └── test_pagos.py
├── features/
│   ├── carrito.feature
│   ├── environment.py
│   └── steps/
│       └── carrito_steps.py
├── .github/
│   └── workflows/
│       └── quality.yml
├── pytest.ini
├── requirements.txt
└── README.md
```
