# Proyecto Backgammon

- **Autor:** Franco Maldonado

- Bienvenido a este proyecto. A continuación se detallan los pasos necesarios para la instalación, configuración y ejecución del programa y sus pruebas unitarias.

---

## Estructura del Proyecto
```bash
.
├── Backgammon/
│   ├── assets/
│   │   ├── images/
│   │   │   ├── UMLClassGeneral.png
│   │   │   └── UMLClassPygameUI.png
│   │   └── sounds/
│   │       ├── bearing_off.wav
│   │       ├── capture.wav
│   │       ├── dice_roll.wav
│   │       ├── error.wav
│   │       ├── move_piece.wav
│   │       └── win_game.wav
│   │
│   ├── Core/                    # Lógica principal del juego
│   │   ├── Board.py             # Representa el tablero y las posiciones
│   │   ├── Checker.py           # Define las fichas y su color
│   │   ├── Dice.py              # Simula los dados
│   │   ├── Player.py            # Maneja los jugadores y sus turnos
│   │   └── __init__.py
│   │
│   ├── Interfaces/              # Interfaces de usuario
│   │   ├── CLI.py               # Interfaz de consola
│   │   ├── PygameUI.py          # Interfaz gráfica con Pygame
│   │   └── __init__.py
│   │
│   ├── Persistence/             # Gestión de persistencia
│   │   ├── RedisManager.py      # Manejo de Redis para almacenamiento
│   │   └── __init__.py
│   │
│   ├── Tests/                   # Pruebas unitarias
│   │   ├── Test_Board.py
│   │   ├── Test_Checker.py
│   │   ├── Test_CLI.py
│   │   ├── Test_Dice.py
│   │   ├── Test_Player.py
│   │   ├── Test_PygameUI.py
│   │   ├── Test_RedisManager.py
│   │   └── __init__.py
│   │
│   ├── CHANGELOG.md             # Registro de cambios
│   ├── JUSTIFICACIÓN.md         # Justificación del proyecto
│   ├── prompts-desarrollo.md    # Prompts de desarrollo
│   ├── prompts-documentación.md # Prompts de documentación
│   ├── prompts-testing.md       # Prompts de testing
│   ├── requirements.txt         # Dependencias del proyecto
│   └── __init__.py
│
├── venv/                        # Entorno virtual (no incluir en git)
├── .coverage                    # Archivo de cobertura
├── .gitignore                   # Archivos ignorados por git
├── .pylintrc                    # Configuración de pylint
├── coverage_report.txt          # Reporte de cobertura
├── docker-compose.yml           # Configuración de Docker Compose
├── Dockerfile                   # Configuración de Docker
├── generate_reports.py          # Script para generar reportes
├── pylint_report.txt            # Reporte de pylint
├── README.md                    # Este archivo
└── REPORTS.md                   # Reportes del proyecto
```

---

## Instalación y Configuración

- Sigue estos pasos para configurar el entorno de desarrollo local.

### 1. Clonar el Repositorio (Opcional)

- Si aún no tienes el código, clónalo desde tu repositorio (reemplaza la URL):
```bash
git clone 
cd 
```

### 2. Configurar el Entorno Virtual

- Es una buena práctica usar un entorno virtual (venv) para aislar las dependencias del proyecto.

#### Crear el entorno virtual:
```bash
python3 -m venv venv
```

#### Activar el entorno virtual:

- **En macOS/Linux:**
```bash
source venv/bin/activate
```

- **En Windows (PowerShell):**
```bash
.\venv\Scripts\Activate.ps1
```

- **En Windows (CMD):**
```bash
venv\Scripts\activate.bat
```

#### Instalar las dependencias:

- Una vez activado el entorno, instala las librerías necesarias: 
```bash
pip install -r requirements.txt
```

---

## Cómo Ejecutar el Programa

- Puedes ejecutar el juego en dos modos diferentes desde la raíz del proyecto.

### Ejecutar en modo CLI (Interfaz de Terminal)
```bash
python3 -m Backgammon.Interfaces.CLI
```
## Botones para CLI:
# R: Tirar dados

### Ejecutar en modo GUI (Interfaz Gráfica)

- Asegúrate de tener Pygame y otras dependencias gráficas instaladas (deberían estar en Backgammon/requirements.txt).
```bash
python3 -m Backgammon.Interfaces.PygameUI
```
## Botones para PygameUI:
# R: Tirar dados
# G: Guardar partida
# L: Cargar partida

---

## 🧪 Ejecutar Pruebas (Tests)

- Para verificar que todo funcione correctamente, puedes ejecutar las pruebas unitarias.

### Ejecutar todos los tests

- El siguiente comando descubrirá y ejecutará automáticamente todos los archivos de prueba (Test_*.py) dentro del directorio Backgammon/Tests/.
```bash
python3 -m unittest discover -s Backgammon/Tests -p "Test_*.py"
```

### Ejecutar un archivo de test específico

- Si quieres ejecutar un solo archivo de prueba (por ejemplo, Backgammon/Tests/Test_Board.py cambia "Board" por el nombre del archivo que quieras testear): 
```bash
# Ejemplo para ejecutar: Backgammon/Tests/Test_Board.py
python3 -m unittest Backgammon/Tests/Test_Board.py
```

---

## Notas Adicionales

- Todos los comandos se ejecutan desde la raíz del proyecto. (Yo personalmente tengo un directorio "Backgammon" con toda la logica, por eso lo especifico al inicio de la ruta) 
- Asegúrate de mantener actualizado el archivo Backgammon/requirements.txt con todas las dependencias necesarias.
- Para desactivar el entorno virtual cuando termines, simplemente ejecuta: `deactivate`
- Los reportes de cobertura y pylint se pueden generar ejecutando el script generate_reports.py (Necesarios para un desarrollador)

