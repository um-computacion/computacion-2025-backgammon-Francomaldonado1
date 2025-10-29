# Backgammon - Instrucciones de Ejecución con Docker

Este documento explica cómo poner en funcionamiento el juego de Backgammon usando Docker tanto para testing como para jugar.

## Prerrequisitos

- Docker instalado en tu sistema
- Docker Compose instalado

## Construcción de la Imagen

Antes de ejecutar cualquier modo, construye la imagen de Docker:

```bash
docker-compose build
```

## Modo Testing

Para ejecutar todos los tests del proyecto:

```bash
docker-compose --profile test up
```

Este comando ejecutará todos los tests ubicados en `Backgammon/Tests/` usando el comando:
```bash
python3 -m unittest Backgammon/Tests/*.py
```

Para ver los resultados y que el contenedor se elimine automáticamente al finalizar:

```bash
docker-compose --profile test up --abort-on-container-exit --remove-orphans
```

Para eliminar el contenedor después de ejecutar los tests:

```bash
docker-compose --profile test down
```

## Modo Juego - CLI (Interfaz de Texto)

Para jugar usando la interfaz de línea de comandos desplegada con Docker:

```bash
docker-compose --profile game up
```

La interfaz CLI te permitirá interactuar con el juego directamente desde la terminal Docker.

Para detener el juego, presiona `Ctrl+C` y luego ejecuta:

```bash
docker-compose --profile game down
```

## Modo Juego - GUI (Interfaz Gráfica con Pygame)

La interfaz gráfica **NO se ejecuta con Docker** debido a limitaciones técnicas del display gráfico. Para usar la GUI, ejecuta el proyecto localmente:

### Configuración local:

1. Activar el entorno virtual:
```bash
source venv/bin/activate
```

2. Ejecutar la interfaz gráfica:
```bash
python3 -m Backgammon.Interfaces.PygameUI
```

## Resumen de Comandos

| Modo | Comando |
|------|---------|
| **Testing** | `docker-compose --profile test up` |
| **CLI** | `docker-compose --profile game up` |
| **GUI** | `source venv/bin/activate && python3 -m Backgammon.Interfaces.PygameUI` |

## Arquitectura del Proyecto

El proyecto está dividido en tres componentes principales:

- **Core**: Contiene las clases principales (Player, Checker, Dice, Board)
- **Interfaces**: CLI y PygameUI
- **Tests**: Tests unitarios de cada clase del Core y de cada interfaz

La clase `Board` maneja el flujo del juego y relaciona todas las demás clases del Core, siendo utilizada por ambas interfaces.

## Uso de Profiles

El archivo `docker-compose.yml` contiene dos servicios con profiles diferentes:
- **Profile `test`**: Ejecuta los tests
- **Profile `game`**: Ejecuta la interfaz CLI

Esto permite tener ambos servicios en un solo archivo y ejecutarlos selectivamente según se necesite.

## Solución de Problemas

### Los tests fallan
- Verifica que la estructura de directorios sea correcta
- Asegúrate de que todos los archivos de test estén en `Backgammon/Tests/`
- Reconstruye la imagen: `docker-compose build --no-cache`

### La CLI no responde o no puedo escribir
- Asegúrate de usar `docker-compose --profile game up` (NO uses el flag `-d`)
- Los flags `stdin_open` y `tty` en el docker-compose.yml son necesarios para la interacción

### Cambios en el código no se reflejan
- Los cambios se reflejan automáticamente gracias al volumen montado
- Si aún no se reflejan, reconstruye: `docker-compose build`

## Limpieza

Para eliminar contenedores, imágenes y volúmenes:

```bash
docker-compose down --rmi all --volumes
```