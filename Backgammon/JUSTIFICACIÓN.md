# Justificación del Diseño de las Clases Core

---

## Filosofía: Diseño Minimalista

### Razones para el diseño minimalista

- **Separación de responsabilidades**  
  Las clases Core representan entidades del dominio.  
  La lógica de coordinación está en `Board` y las Interfaces.

---

## Principio de Responsabilidad Única

- **Checker:** "Soy una ficha de un color"  
- **Player:** "Soy un jugador con un nombre y color"  
- **Dice:** "Genero números aleatorios para dados"

---

## Facilidad de Testing

- Clases simples → Tests simples  
- Menos métodos → Menos casos de prueba  
- Menos dependencias → Menos mocks necesarios

---

## Inmutabilidad Conceptual

- Una ficha no cambia su naturaleza  
- Un jugador no cambia su identidad  
- Un dado siempre hace lo mismo: generar números

---

# Detalle de cada Clase Core

---

## Checker (Ficha)

### Responsabilidad
Representar una ficha del juego con su color y posición.

### Métodos disponibles

- `obtener_color()`: Devuelve el color de la ficha  
- `obtener_posicion()`: Devuelve la posición actual  
- `establecer_posicion()`: Modifica la posición  
- `esta_fuera()`: Verifica si está fuera del tablero

### Justificación del diseño minimalista

- ✅ No tiene método `mover()` porque el movimiento depende del estado completo del tablero (validaciones, capturas, etc.)  
- ✅ No tiene método `validar()` porque la validación requiere conocer reglas que cambian según la variante  
- ✅ Solo gestiona datos porque una ficha es esencialmente una entidad de datos, no un comportamiento

### Principios SOLID

- **SRP:** Una ficha solo se encarga de mantener su estado (color y posición)  
- **ISP:** Interfaz mínima — solo expone lo que un cliente necesita de una ficha  
- **OCP:** Se puede extender para crear `SpecialChecker` sin modificar la clase base  
- **LSP:** Cualquier subclase de `Checker` puede usarse donde se espera `Checker`  
- **DIP:** No depende de ninguna otra clase del proyecto

---

## Player (Jugador)

### Responsabilidad
Representar la identidad y recursos de un jugador.

### Métodos disponibles

- `obtener_nombre()`: Devuelve el nombre del jugador  
- `obtener_color()`: Devuelve el color asignado  
- `obtener_fichas()`: Devuelve lista de 15 fichas  
- `obtener_dados()`: Devuelve el objeto `Dice` del jugador

### Justificación del diseño minimalista

- ✅ No tiene método `hacer_movimiento()` porque la lógica de ejecución está en `Board`  
- ✅ No tiene método `calcular_estrategia()` porque eso es responsabilidad de:
  - La interfaz (para jugadores humanos)  
  - Una subclase `AIPlayer` (para jugadores computadora)  
- ✅ No gestiona turnos porque eso es responsabilidad de `GameStateManager`

### ¿Por qué Player tiene Dice?

En el backgammon tradicional, cada jugador tiene su propio set de dados.  
Esto permite:

- Representación fiel del juego real  
- Extensibilidad para variantes donde los dados son diferentes  
- Posibilidad de juego por turnos asincrónicos (cada uno con sus dados)

### Principios SOLID

- **SRP:** Solo representa identidad y recursos, no lógica de juego  
- **ISP:** Interfaz simple de identificación y acceso a recursos  
- **OCP:** Extensible para crear `AIPlayer`, `RemotePlayer` sin modificar la base  
- **LSP:** Subclases pueden sustituir a `Player` manteniendo el contrato  
- **DIP:** Depende de abstracciones (`Checker`, `Dice`), no de implementaciones concretas

---

## Dice (Dados)

### Responsabilidad
Generar números aleatorios para simular tiradas de dados.

### Métodos disponibles

- `tirar()`: Genera dos números aleatorios (1-6)  
- `obtener_dado1()`, `obtener_dado2()`: Devuelven valores individuales  
- `obtener_valores()`: Devuelve tupla con ambos valores  
- `es_doble()`: Indica si ambos dados tienen el mismo valor  
- `han_sido_tirados()`: Verifica si se ha realizado una tirada  
- `reiniciar()`: Prepara para una nueva tirada  
- `set_dados_para_test()`: Permite inyectar valores para testing

### Justificación del diseño minimalista

- ✅ No tiene método `calcular_movimientos()` porque interpretar los dados (por ejemplo, dobles = 4 movimientos) es lógica de backgammon, no de dados genéricos  
- ✅ No tiene método `validar_movimiento()` porque validar requiere conocer el estado del tablero  
- ✅ Separación de generación e interpretación permite reutilizar `Dice` en otros juegos de dados

---

### Separación de responsabilidades en el proyecto

- **Dice:** Genera números aleatorios → “Obtuve 3 y 5”  
- **DiceMovesCalculator:** Interpreta los números → “Tienes 2 movimientos: [3, 5]” o “Tienes 4 movimientos: [6, 6, 6, 6]”  
- **MovementValidator:** Valida si esos movimientos son posibles → “Puedes usar el 3 pero no el 5”

---

### Principios SOLID

- **SRP:** Solo genera números aleatorios, no interpreta resultados  
- **OCP:** Se puede extender para crear `LoadedDice`, `WeightedDice` sin modificar la base  
- **LSP:** Cualquier tipo de dado puede sustituir a `Dice`  
- **ISP:** Interfaz enfocada en generación, no en reglas de juego  
- **DIP:** Completamente independiente, no depende de otras clases

---
