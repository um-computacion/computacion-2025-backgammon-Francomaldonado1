## [0.0.1] 23/08/2025
### ADDED
- Estructura inicial del juego, Carpeta principal Backgammon con carpeta Core donde se encuentran las clases basicas del juego (vacias)

## [0.0.2] 24/08/2025
### ADDED
- Se agrega la estructura final del juego:
- Carpeta Test (con archivo de test para cada clase e interfaces)
- Carpeta Interfaces (con CLI y PygameUI correspondientes a la intefaz de texto y grafica) (interfaces vacias)
- Archivos .md: prompts y changelog
- Creamos tambien una milestone correspondiente a las interfaces, una milestone para los tests y una milestone para los avances en archivos .md y sus correspondientes issues. 

### CHANGED
- Se cambia el nombre de la carpeta principal a Backgammon
- Se volvió a pushear la estructura de las clases debido a este cambio


## [0.0.3] 25/08/2025
### ADDED
- Se agrega la clase Board.py inicial, con algunos metodos, cada metodo tiene su documentación haciendo enfoque en lo que recibe, hace y devuelve (Args y Returns)
- Se agregan Tests para la clase Board en Tests/Test_board.py.
- Se actualiza prompts-desarrollo.md y prompts-testing.md con los prompts y las indicaciones que se utilizaron para desarrollar y probar la clase Board.
- Se agrego archivos __init__.py en Core, Interfaces y Tests para que los tests puedan importar correctamente.
- Se agrego archivo .gitignore con archivo __pycache__.


## [0.0.4] 26/08/2025
### ADDED
- Se agrega la clase Checker.py inicial, con algunos metodos, cada metodo tiene su documentación haciendo enfoque en lo que recibe, hace y devuelve (Args y Returns)
- Se agregan Tests para la clase Checker en Tests/Test_Checker.py.
- Se actualiza prompts-desarrollo.md y prompts-testing.md con los prompts y las indicaciones que se utilizaron para desarrollar y probar la clase Checker.
- Actualizamos clase Board.py con algunos metodos que surgieron al hacer la clase Checker, y agregamos tests para ellos para asegurar una cobertura de código alta.
- Se agrega el archivo JUSTIFICACIÓN.md con la justificación de la implementación de Checker.


## [0.0.5] 27/08/2025
### ADDED
- Se agrega la clase Dice.py inicial, con algunos metodos, cada metodo tiene su documentación haciendo enfoque en lo que recibe, hace y devuelve (Args y Returns)
- Se agrega la clase Player.py inicial, con algunos metodos, cada metodo tiene su documentación haciendo enfoque en lo que recibe, hace y devuelve (Args y Returns)
- Se agregan Tests para la clase Dice y Player en Tests/Test_Dice.py y Tests/Test_Player.py respectivamente.
- Se actualiza prompts-desarrollo.md y prompts-testing.md con los prompts y las indicaciones que se utilizaron para desarrollar y probar la clase Dice y Player.

## [0.0.6] 28/08/2025
### CHANGED
- Se actualiza la clase Board con nuevos metodos correspondientes a los movimientos posibles a partir de las posiciones del tablero y los valores obtenidos de la clase Dice (dados), Cada metodo tiene su documentación haciendo enfoque en lo que recibe, hace y devuelve (Args y Returns)
- Se agregan nuevos tests para los nuevos metodos de la clase Board. (No funcionales actualmente) 
- Se actualiza prompts-desarrollo.md y prompts-testing.md con los prompts y las indicaciones que se utilizaron para desarrollar y probar los nuevos metodos de la clase Board.

## [0.0.7] 31/08/2025
### ADDED
- Se agrega el metodo set_dados_para_test a la clase Dice, para que los tests puedan configurar los dados manualmente.
- Se actualiza prompts-desarrollo.md y prompts-testing.md con los prompts y las indicaciones que se utilizaron para desarrollar y probar los nuevos metodos de clase Board (funcionan todos)

### CHANGED
- Se actualiza el codigo de Board, y de test_board para que funcionen correctamente los tests de los nuevos metodos agregados en la ultima versión.

## [0.0.8] 01/09/2025
### ADDED
- Se agrega la interfaz de línea de comandos (CLI) (Con algunos errores a actualizar mas tarde)
- Se actualiza prompts-desarrollo.md con las indicaciones que se utilizaron para desarrollar la interfaz de línea de comandos (CLI).

### CHANGED 01/09/2025 (22:00 hs)
- Se actualiza el codigo de CLI para que funcione correctamente. (funciona mejor, todavia no del todo bien)
- Se agregan tests para CLI.py iniciales.
- Se actualiza prompts-desarrollo.md y prompts-testing.md con los prompts y las indicaciones que se utilizaron para desarrollar y probar la interfaz de línea de comandos (CLI).

## [0.0.9] 03/09/2025
### ADDED  
- Se agregan nuevos metodos a la clase Board para el bearing off (salida de fichas a casa) por que era una de las cosas que estaba fallando en el CLI.

### CHANGED 
- Se actualiza el codigo de CLI siguiendo lo pedido en los prompts, (cambio de tablero, cambio de fichas, nuevas validaciones)
- Se actualiza prompts-desarrollo.md y prompts-testing.md con los prompts y las indicaciones que se utilizaron para desarrollar y probar la interfaz de línea de comandos (CLI).

 ## [0.0.10] 04/09/2025

### ADDED
- Se agrega archivo requirements.txt con Coverage para probar el porcentaje de cobertura de código.
- Se crea entorno virtual (venv).
- Se actualiza prompts-testing.md con los prompts y las indicaciones que se utilizaron para probar los tests de la interfaz de línea de comandos (CLI).
- Se prueba por primera vez la cobertura de codigo con Coverage (actualmente 90%).

### CHANGED
- Se actualiza el codigo de CLI para pasar los tests y asegurar una cobertura de código alta.
- Se actualiza el codigo de test_CLI.py para que funcionen todos los tests.

## [0.0.11] 05/09/2025
### ADDED
- Se agrega esqueleto incial de interfaz grafica con pygame.
- Se instala pygame agregandolo a archivo requirements.txt.
- Se actualiza prompts-desarrollo.md con los prompts y las indicaciones que se utilizaron para desarrollar la interfaz grafica pygame inicial.

## [0.0.12] 06/09/2025
### CHANGED
- Se cambia la interfaz grafica a una pantalla de 1280x720.
- Se crean unas figuras iniciales (Cuadrados, circulos, lineas) para ver que funciona bien la interfaz.
- Se definen algunos colores para las figuras de prueba (que podremos usar luego para el tablero y el juego) 
- Se actualiza prompts-desarrollo.md con los prompts y las indicaciones que se utilizaron para desarrollar las primeras figuras de prueba.


### CHANGED 06/09/2025 (17:00 hs)
- Se cambia la interfaz grafica a una pantalla de 1600x900.
- Se actualiza el codigo de PygameUI.py para que muestre el tablero de Backgammon. 
- Se actualiza prompts-desarrollo.md con los prompts y las indicaciones que se utilizaron para desarrollar el tablero de Backgammon.
- Se actualizan tambien los atributos de la interfaz PygameUI.py para cumplan con los principios SOLID, agregando doble guion bajo antes y despues de los atributos, para acceder unicamente con self.

### ADDED 06/09/2025 (22:00 hs)
- Se agrega archivo test_PygameUI.py con tests para la interfaz grafica PygameUI (Actualmente no funcionan todos los tests)
- Se actualiza prompts-testing.md con los prompts y las indicaciones que se utilizaron para probar los primeros eventos de la interfaz grafica PygameUI.

## [0.0.13] 07/09/2025
### ADDED
- Se actualiza el codigo de PygameUI.py para que muestre las fichas en el tablero.
- Se actualiza prompts-desarrollo.md con los prompts y las indicaciones que se utilizaron para desarrollar dicha implementación. 


## [0.0.14] 08/09/2025
### CHANGED
- Se cambia el archivo de tests de PygameUI.py cubriendo los casos de la implementación de las fichas al tablero grafico al pygame.
- Se vuelve a probar cobertura de codigo con Coverage (actualmente 90%).
- Se actualiza prompts-testing.md con los prompts y las indicaciones que se utilizaron para probar los tests de la interfaz grafica PygameUI.

## [0.0.15] 09/09/2025
### ADDED
- Se agrega un nuevo metodo __get_point_from_mouse_pos en PygameUI.py para identificar los puntos en el tablero a partir de las coordenadas del click del ratón.

### CHANGED
- Se actualiza prompts-desarrollo.md con los prompts y las indicaciones que se utilizaron para desarrollar y probar el nuevo metodo __get_point_from_mouse_pos.
- Se actualiza prompts-testing.md con los prompts y las indicaciones que se utilizaron para probar el nuevo metodo __get_point_from_mouse_pos.
- Se actualiza el codigo de test_PygameUI.py agregando nueva clase de tests para probar la detección de clics en el tablero. 

## [0.0.16] 13/09/2025
### ADDED
- Se agrega un nuevo metodo __roll_to_start en PygameUI.py para decidir que jugador empieza a jugar. 

### CHANGED
- Se actualiza prompts-desarrollo.md con los prompts y las indicaciones que se utilizaron para desarrollar y probar el nuevo metodo __roll_to_start.
- Se actualiza prompts-testing.md con los prompts y las indicaciones que se utilizaron para probar el nuevo metodo __roll_to_start.
- Se actualiza el codigo de test_PygameUI.py agregando nueva clase de tests para probar el nuevo metodo __roll_to_start.

## [0.0.17] 19/09/2025
### ADDED
- Se agrega un nuevo metodo __validate_and_report_move en PygameUI.py para validar y mostrar el resultado de un movimiento.
- Se agrega un nuevo metodo roll_player_dice en PygameUI.py para tirar los dos dados del jugador actual. (El que gana en roll_to_start)

### CHANGED
- Se actualiza prompts-desarrollo.md con los prompts y las indicaciones que se utilizaron para desarrollar y probar los nuevos metodos __validate_and_report_move y roll_player_dice. 


