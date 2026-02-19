# Guía de arranque — Linear-Book

Plataforma interactiva de Álgebra Lineal para estudiantes.
Arquitectura: **FastAPI** (backend) + **HTML estático** (frontend).

---

## Requisitos previos

| Herramienta | Versión mínima | Verificar |
|-------------|---------------|-----------|
| Python      | 3.9+          | `python3 --version` |
| pip         | cualquiera    | `pip --version` |
| Quarto      | 1.5+ (opcional, para re-renderizar `.qmd`) | `quarto --version` |

---

## 1. Backend (API de calificación)

El backend es una API FastAPI que ejecuta y califica el código y las respuestas matemáticas de los estudiantes.

### Primera vez

```bash
cd Linear-Book/backend

# Crear entorno virtual
python3 -m venv venv

# Activar entorno
source venv/bin/activate          # macOS / Linux
# venv\Scripts\activate           # Windows

# Instalar dependencias
pip install -r requirements.txt

# Inicializar la base de datos
python3 -c "from app.db import init_db; init_db()"

# Cargar los problemas de la demo
python3 -c "
import sqlite3, json
conn = sqlite3.connect('test.db')
cur  = conn.cursor()
problems = [
    ('taller-demo', 'numpy_sum',   'Suma de vector NumPy',        'code', '6',  None, 0.01),
    ('taller-demo', 'dot_product', 'Producto punto (1,2)·(3,4)', 'math', None, '11', 0.01),
    ('taller-demo', 'matrix_det',  'Determinante de matriz 2×2', 'code', '-2', None, 0.01),
]
for section, pid, title, ptype, expected, correct, tol in problems:
    cur.execute(
        '''INSERT OR REPLACE INTO problems
           (section, problem_id, title, description, problem_type,
            expected_output, correct_answer, tolerance)
           VALUES (?,?,?,?,?,?,?,?)''',
        (section, pid, title, '', ptype, expected, correct, tol)
    )
conn.commit(); conn.close()
print('Problemas insertados.')
"
```

### Arranque diario

```bash
cd Linear-Book/backend
source venv/bin/activate
python3 run.py
```

El servidor queda disponible en:

- API: `http://localhost:8000`
- Documentación interactiva: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/api/v1/health`

> El backend usa **hot-reload**: guarda un archivo `.py` y se reinicia automáticamente.

---

## 2. Frontend (sitio web)

El frontend son archivos HTML estáticos en `docs/`. Se sirven con Python.

### Arrancar el servidor web

```bash
cd Linear-Book/docs
python3 -m http.server 4200
```

Abre el navegador en:

| Página | URL |
|--------|-----|
| Índice del curso | `http://localhost:4200/index.html` |
| **Taller Interactivo (demo)** | `http://localhost:4200/taller-interactive-demo.html` |
| Taller 1 | `http://localhost:4200/taller1.html` |
| Taller 2 | `http://localhost:4200/taller2.html` |

> **Importante:** el frontend en puerto `4200` y el backend en puerto `8000` deben estar corriendo **al mismo tiempo**.

---

## 3. Arranque completo (ambos servicios)

Abre **dos terminales** y ejecuta:

**Terminal 1 — Backend:**
```bash
cd Linear-Book/backend
source venv/bin/activate
python3 run.py
```

**Terminal 2 — Frontend:**
```bash
cd Linear-Book/docs
python3 -m http.server 4200
```

Luego abre `http://localhost:4200/taller-interactive-demo.html`.

---

## 4. Verificar que todo funciona

### Verificar el backend

```bash
# Health check
curl http://localhost:8000/api/v1/health

# Enviar código correcto (debe devolver is_correct: true)
curl -X POST http://localhost:8000/api/v1/submit/code \
  -H "Content-Type: application/json" \
  -d '{"problem_id":"numpy_sum","code":"import numpy as np\nv=np.array([1,2,3])\nprint(v.sum())","user_id":null}'

# Verificar respuesta matemática
curl -X POST http://localhost:8000/api/v1/submit/math \
  -H "Content-Type: application/json" \
  -d '{"problem_id":"dot_product","answer":"11","user_id":null}'
```

### Verificar el frontend

Abre `http://localhost:4200/taller-interactive-demo.html`, escribe código en el Problema 1 y haz clic en **"Ejecutar y verificar"**. Debes ver el feedback verde "¡Correcto!".

---

## 5. Agregar un nuevo problema

### Paso 1 — Registrar el problema en la base de datos

```bash
cd Linear-Book/backend
source venv/bin/activate
python3 -c "
from app.db import SessionLocal
from app.models import Problem

db = SessionLocal()
p = Problem(
    section     = 'taller1',          # sección a la que pertenece
    problem_id  = 'mi_problema',       # ID único (sin espacios)
    title       = 'Mi problema',
    description = 'Descripción para el estudiante.',
    problem_type= 'code',              # 'code' | 'math' | 'multiple_choice'
    expected_output = '42',            # para tipo 'code'
    # correct_answer  = '42',          # para tipo 'math'
    tolerance   = 0.01,
)
db.add(p); db.commit(); db.close()
print('Problema creado.')
"
```

### Paso 2 — Agregar el bloque HTML al taller

Copia uno de los bloques de `docs/taller-interactive-demo.html` y cambia los IDs para que coincidan con el `problem_id` que registraste.

**Bloque de código:**
```html
<div id="code-problem-mi_problema" class="interactive-problem">
  <div class="problem-header">
    <span class="problem-badge">⌨ Código Python</span>
    <h4>Mi problema</h4>
  </div>
  <div class="problem-description">Descripción aquí.</div>
  <div class="code-editor-container">
    <label for="code-input-mi_problema">Tu solución</label>
    <textarea id="code-input-mi_problema" class="code-editor-input">
# Tu código aquí
    </textarea>
  </div>
  <div class="problem-controls">
    <button class="btn btn-primary" onclick="submitCode('mi_problema')">▶ Ejecutar y verificar</button>
    <button class="btn btn-secondary" onclick="resetCodeDemo('mi_problema')">↺ Restablecer</button>
    <span id="loading-mi_problema" class="loading hidden">Ejecutando…</span>
  </div>
  <div id="feedback-mi_problema" class="feedback-container hidden">
    <div id="feedback-status-mi_problema"  class="feedback-status"></div>
    <div id="feedback-message-mi_problema" class="feedback-message"></div>
    <div id="feedback-output-mi_problema"  class="feedback-output"></div>
  </div>
</div>
```

**Bloque de respuesta matemática:**
```html
<div id="math-problem-mi_problema" class="interactive-problem">
  <div class="problem-header">
    <span class="problem-badge">∑ Respuesta matemática</span>
    <h4>Mi problema</h4>
  </div>
  <div class="problem-description">Descripción aquí.</div>
  <div class="answer-input-container">
    <label for="answer-input-mi_problema">Tu respuesta</label>
    <input type="text" id="answer-input-mi_problema" class="answer-input"
      placeholder="Escribe el resultado aquí…"
      onkeydown="if(event.key==='Enter') submitMath('mi_problema')">
  </div>
  <div class="problem-controls">
    <button class="btn btn-primary" onclick="submitMath('mi_problema')">✓ Verificar respuesta</button>
    <button class="btn btn-secondary" onclick="resetMath('mi_problema')">↺ Limpiar</button>
    <span id="loading-math-mi_problema" class="loading hidden">Verificando…</span>
  </div>
  <div id="feedback-math-mi_problema" class="feedback-container hidden">
    <div id="feedback-status-math-mi_problema"  class="feedback-status"></div>
    <div id="feedback-message-math-mi_problema" class="feedback-message"></div>
  </div>
</div>
```

---

## 6. Re-renderizar con Quarto (opcional)

Si tienes Quarto instalado, puedes modificar los archivos `.qmd` y re-generar el sitio:

```bash
# Instalar Quarto: https://quarto.org/docs/get-started/
# (requiere macOS GUI o sudo)

cd Linear-Book

# Renderizar todo el sitio en docs/
quarto render

# O solo un archivo
quarto render talleres/taller1.qmd

# Modo preview con live-reload (reemplaza al servidor Python)
quarto preview
# → abre el navegador automáticamente en http://localhost:4200
```

> Sin Quarto, los archivos `.qmd` no se pueden modificar y ver en el navegador. El sitio pre-renderizado en `docs/` funciona sin Quarto.

---

## 7. Solución de problemas

### El taller dice "No se pudo conectar al servidor"

```bash
# 1. Verificar que el backend está corriendo
curl http://localhost:8000/api/v1/health

# 2. Si no responde, arrancarlo
cd Linear-Book/backend && source venv/bin/activate && python3 run.py
```

### "Problem not found" al enviar una respuesta

El problema no está en la base de datos. Ejecuta el script de inserción del **Paso 1 de la sección 5**.

```bash
# Ver qué problemas existen
cd Linear-Book/backend && source venv/bin/activate
python3 -c "
from app.db import SessionLocal; from app.models import Problem
db = SessionLocal()
for p in db.query(Problem).all():
    print(f'{p.problem_id:20} | {p.problem_type:15} | {p.section}')
db.close()
"
```

### Reiniciar la base de datos desde cero

```bash
rm Linear-Book/backend/test.db
cd Linear-Book/backend && source venv/bin/activate
python3 -c "from app.db import init_db; init_db()"
# Luego volver a insertar los problemas (sección 1 de esta guía)
```

### El puerto 8000 o 4200 ya está en uso

```bash
# Ver qué proceso usa el puerto
lsof -i :8000
lsof -i :4200

# Terminar el proceso (reemplaza PID con el número real)
kill -9 <PID>
```

---

## 8. Estructura del proyecto

```
Linear-Book/
├── backend/                     # API FastAPI
│   ├── app/
│   │   ├── main.py              # Punto de entrada, CORS
│   │   ├── config.py            # Variables de entorno
│   │   ├── db.py                # Conexión SQLite / PostgreSQL
│   │   ├── models.py            # Modelos Problem, Submission
│   │   ├── schemas.py           # Validación Pydantic
│   │   ├── routes/
│   │   │   ├── health.py        # GET /api/v1/health
│   │   │   ├── problems.py      # GET /api/v1/problems/:id
│   │   │   └── submissions.py   # POST /api/v1/submit/code|math|multiple-choice
│   │   └── services/
│   │       └── grader.py        # Lógica de calificación
│   ├── run.py                   # Arranque del servidor
│   ├── requirements.txt
│   └── test.db                  # Base de datos SQLite (se crea automáticamente)
│
├── docs/                        # Sitio web pre-renderizado (servir con Python)
│   ├── taller-interactive-demo.html   ← Demo interactiva principal
│   ├── taller1.html … taller10.html
│   ├── section0.html … section13.html
│   ├── styles.css               # Sistema de estilos global
│   └── site_libs/               # Bootstrap, MathJax, Quarto JS
│
├── frontend-components/         # Plantillas reutilizables de componentes
│   ├── code-submission.html     # Widget de envío de código
│   └── math-submission.html     # Widget de respuesta matemática
│
├── talleres/                    # Fuentes .qmd de los talleres
├── sections/                    # Fuentes .qmd de las secciones teóricas
├── styles.css                   # Fuente del CSS (se copia a docs/ manualmente)
└── _quarto.yml                  # Configuración del sitio Quarto
```

---

## 9. Referencia rápida de la API

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET`  | `/api/v1/health` | Estado del servidor |
| `GET`  | `/api/v1/problems/{id}` | Datos de un problema |
| `GET`  | `/api/v1/problems/section/{section}` | Problemas de una sección |
| `POST` | `/api/v1/submit/code` | Enviar código Python |
| `POST` | `/api/v1/submit/math` | Enviar respuesta numérica |
| `POST` | `/api/v1/submit/multiple-choice` | Enviar opción múltiple |

Documentación completa con formularios en `http://localhost:8000/docs`.
