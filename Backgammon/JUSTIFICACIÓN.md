# JUSTIFICACIÓN DEL PROYECTO FINAL: BACKGAMMON
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
- **OCP:** Se puede extender para crear `SpecialChecker` sin modificar la clase base  
- **LSP:** Cualquier subclase de `Checker` puede usarse donde se espera `Checker`  
- **ISP:** Interfaz mínima — solo expone lo que un cliente necesita de una ficha  
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
- **OCP:** Extensible para crear `AIPlayer`, `RemotePlayer` sin modificar la base  
- **LSP:** Subclases pueden sustituir a `Player` manteniendo el contrato  
- **ISP:** Interfaz simple de identificación y acceso a recursos  
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


## Board (Tablero Principal)

### Responsabilidad
Centralizar la lógica del juego y coordinar las clases Core (`Checker`, `Player`, `Dice`), gestionando movimientos, validaciones, barra y casa.

### Métodos principales

- `inicializar_posiciones_estandar()`: Configura las posiciones iniciales del tablero  
- `calcular_destino()`: Determina el punto de destino según el color y el valor del dado  
- `mover_desde_barra()`: Reincorpora fichas desde la barra siguiendo las reglas  
- `realizar_movimiento_completo()`: Aplica un movimiento con validaciones  
- `realizar_movimiento_doble()`: Ejecuta movimientos encadenados con ambos dados  
- `puede_sacar_fichas()`: Evalúa si un jugador puede comenzar a sacar fichas  
- `ha_ganado()`: Determina si un jugador completó la partida  
- `obtener_movimientos_posibles()`: Lista los puntos desde donde puede moverse

---

### Justificación del diseño minimalista

- ✅ No gestiona interfaz ni turnos (separación de capas)  
- ✅ No crea jugadores ni dados (inyección de dependencias)  
- ✅ No maneja persistencia (solo estado temporal del juego)  
- ✅ Encapsula toda la lógica del tablero sin exponer estructuras internas

---

### Principios SOLID

- **SRP:** Gestiona la lógica del tablero, no entidades ni interfaz.  
  Cada método tiene una única responsabilidad (ej. `calcular_destino` no modifica estado).  

- **OCP:** Extensible para variantes del juego (por ejemplo, tableros de 12 puntos o movimientos alternativos).  
  Nuevas reglas pueden implementarse mediante herencia sin modificar la clase base.  

- **LSP:** Subclases que redefinan reglas de movimiento pueden sustituir `Board` manteniendo compatibilidad.  

- **ISP:** Expone una interfaz clara y necesaria para operar el tablero (`mover_desde_barra`, `obtener_movimientos_posibles`, `ha_ganado`).  

- **DIP:** Depende de abstracciones (`Dice`) en lugar de implementaciones; no instancia ni conoce detalles internos de `Checker` o `Player`.  

---

### Conclusión

El diseño de `Board` cumple el rol de **coordinador del dominio**, siendo el núcleo del modelo de negocio.  
Gracias a su diseño desacoplado, **permite testeo unitario**, extensión de reglas y reutilización del resto de clases Core sin generar dependencias circulares ni romper el principio de responsabilidad única.



## Estrategias de Testing y Cobertura

### Enfoque general

El testing sigue una **estrategia de cobertura orientada a principios SOLID**.  
Cada clase Core cuenta con un archivo de pruebas unitarias que:

1. Verifica funcionalidad esperada (tests de comportamiento).  
2. Evalúa cumplimiento explícito de principios SOLID (tests de arquitectura).  
3. Asegura independencia y testabilidad sin dependencias externas.

---

### Test_Checker.py

- Se verifican **constructor y setters/getters**, asegurando que el estado se maneja correctamente.  
- Los tests están organizados en dos clases:
  - `TestCheckerFunctionality`: prueba comportamiento concreto de `Checker`.  
  - `TestCheckerSOLID`: valida que se cumplan SRP, ISP, OCP, LSP y DIP.
- Se justifica cada test con un docstring que indica el principio evaluado.  
- Ejemplo:
  - `test_color_inmutable` verifica **SRP** (identidad inmutable).  
  - `test_isp_minimal_interface` confirma **ISP** (interfaz mínima).  
  - `test_ocp_extensible_sin_modificacion` demuestra **OCP** (extensión sin modificar la clase base).

---

### Test_Player.py

- Comprueba que `Player` solo gestiona identidad y recursos (fichas y dados).  
- Se testean independencia de fichas, composición sobre herencia (**DIP**) y extensibilidad (**OCP**) con subclases `AIPlayer` y `RemotePlayer`.  
- Casos específicos:
  - `test_dados_propios_jugador`: valida que cada jugador tenga dados independientes (**DIP**).  
  - `test_ocp_extensible_for_ai_player`: verifica que se pueda extender sin modificar la clase (**OCP**).  
  - `test_lsp_subtypes_maintain_contract`: comprueba que las subclases respeten el contrato (**LSP**).

---

### Test_Dice.py

- Tests de **comportamiento**: valores aleatorios, reinicio, detección de dobles, representación textual.  
- Tests de **arquitectura SOLID**: aseguran independencia de reglas del juego (**DIP**) y enfoque único (**SRP**).  
- Casos destacados:
  - `test_srp_only_generates_random_numbers`: demuestra que `Dice` solo genera números aleatorios.  
  - `test_ocp_extensible_for_variants`: comprueba extensión mediante `LoadedDice`.  
  - `test_dip_testable_without_mocks`: confirma independencia para testing mediante inyección controlada.

---

### Test_Board.py

- Evalúa la integración de las clases Core sin romper el desacoplamiento.  
- Se prueban:
  - Inicialización estándar del tablero.  
  - Cálculo de destinos y movimientos válidos.  
  - Condiciones de victoria y reincorporación de fichas.  
- Los docstrings explican qué principio SOLID se está verificando:
  - **SRP:** Cada método tiene una única función (ej. `calcular_destino`).  
  - **OCP:** El tablero permite variantes sin modificar la clase base.  
  - **DIP:** `Board` interactúa con `Dice` sin conocer su implementación.

---

### Conclusión del testing

- Todos los tests están documentados con el principio SOLID que justifican.  
- El enfoque de testing no se limita a probar resultados, sino que garantiza **calidad estructural del diseño**.  
- Gracias a la simplicidad de las clases Core y su bajo acoplamiento, el proyecto alcanza:
  - **Alta cobertura lógica** (todas las rutas de ejecución principales).  
  - **Alta cobertura conceptual SOLID** (cada principio validado en código y en pruebas).  

---

### Decisiones de diseño relevantes

- **Separación de dominio y coordinación:**  
  Las clases `Checker`, `Player`, y `Dice` son entidades puras del dominio, mientras `Board` actúa como coordinador.  
- **Testing guiado por principios SOLID:**  
  Cada test se escribe no solo para validar el “qué”, sino el “por qué” del diseño.  
- **Composición sobre herencia:**  
  Todas las clases evitan dependencias innecesarias y promueven extensibilidad segura.  

---

## Interfaz de texto (CLI)

### Responsabilidad
Gestionar la interacción textual entre el usuario y el dominio.  
La `CLI` actúa como capa de presentación: formatea y muestra el tablero, solicita entradas al usuario, orquesta el flujo de turnos y delega la lógica de reglas y validaciones al `Board` y a las clases Core.

---

### Métodos disponibles

- `iniciar_juego()`: Pide nombres de jugadores, inicializa el tablero y arranca el bucle principal.  
- `determinar_primer_jugador()`: Determina interactivamente quién comienza mediante tiradas.  
- `mostrar_tablero()`: Formatea y muestra el estado del tablero (puntos, barra y casa) por consola.  
- `loop_principal()`: Bucle principal que verifica condiciones de victoria y alterna turnos.  
- `turno_jugador()`: Gestiona el flujo de un turno (tirada, cálculo de movimientos posibles y delegación a los manejadores).  
- `mostrar_movimientos_disponibles()`: Presenta los puntos desde los cuales se pueden hacer movimientos.  
- `manejar_movimientos_normales()`: Orquesta el proceso de movimientos cuando no hay dobles.  
- `manejar_dobles()`: Orquesta el proceso de movimientos cuando la tirada es doble.  
- `realizar_movimiento_simple_con_dados(usar_dado1, usar_dado2)`: Solicita origen y ejecuta un intento de movimiento usando dados especificados.  
- `realizar_movimiento_simple()`: Versión legacy/compatibilidad que llama al anterior con un dado por defecto.  
- `realizar_movimiento_doble()`: Solicita origen/confirmación y ejecuta un movimiento doble.  
- `main()`: Punto de entrada que inicializa la CLI y maneja excepciones de alto nivel.

---

### Justificación del diseño minimalista

- ✅ **No contiene reglas de juego.** Toda la lógica de validación y movimiento reside en `Board`.  
- ✅ **No gestiona persistencia ni almacenamientos externos.** Sólo mantiene referencias a `Board` y `Dice` para la sesión activa.  
- ✅ **Encapsula presentación y orquestación.** Mantiene el código de I/O separado del dominio para facilitar sustitución por otras vistas.

---

### Principios SOLID

- **SRP (Single Responsibility):**  
  `CLI` se encarga únicamente de la interacción textual (I/O) y del flujo de la experiencia de usuario; no mezcla responsabilidades de dominio.

- **OCP (Open/Closed):**  
  La interfaz puede ampliarse (añadir opciones de menú, comandos adicionales o integración con plugins) sin modificar la lógica del dominio.

- **LSP (Liskov Substitution):**  
  Otra capa de presentación (por ejemplo, una clase GUI) que ofrezca el mismo contrato público puede sustituir la CLI sin afectar al núcleo del sistema.

- **ISP (Interface Segregation):**  
  La CLI expone solo las operaciones necesarias para interactuar con el juego (`iniciar_juego`, `mostrar_tablero`, `turno_jugador`, etc.), manteniendo métodos pequeños y focalizados.

- **DIP (Dependency Inversion):**  
  Depende de las abstracciones públicas del Core (`Board`, `Dice`) y no de sus implementaciones internas, lo que permite inyectar/falsificar componentes en pruebas o sustituir implementaciones.

---

### Conclusión (CLI)

La `CLI` cumple el rol de capa de presentación desacoplada y ligera, respetando los mismos criterios de diseño minimalista aplicados al Core.  
Al mantener las reglas dentro del dominio y la presentación en la interfaz, se facilita la mantenibilidad, la extensión (migración a GUI o Web) y la trazabilidad del comportamiento del sistema.