import unittest
from unittest.mock import patch, Mock
import pygame
import os
import sys

# Asegura que los módulos del proyecto se encuentren
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Backgammon.Interfaces.PygameUI import *
from Backgammon.Core.Board import Board


# --- CLASE BASE PARA TESTS DE LÓGICA Y DIBUJO ---
# Esta clase centraliza la configuración para evitar código repetido.
class PygameUITestBase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Se ejecuta una vez por clase para preparar el entorno de Pygame sin pantalla.
        
        Principio SRP: Centraliza la configuración de Pygame (dummy driver)
        para todas las suites de tests que hereden de ella.
        """
        os.environ["SDL_VIDEODRIVER"] = "dummy"
        pygame.init()

    def setUp(self):
        """
        Se ejecuta antes de cada test. Crea una instancia de PygameUI segura,
        'parcheando' las funciones de Pygame para que el constructor se ejecute
        por completo pero sin crear una ventana real.
        
        Principio SRP: Aísla la creación de la instancia 'ui' para cada test,
        evitando efectos secundarios entre pruebas y separando la configuración.
        """
        with patch('pygame.display.set_mode', return_value=pygame.Surface((1600, 900))), \
             patch('pygame.font.Font'):
            self.ui = PygameUI()


# --- CLASE BASE PARA TESTS DE PYGAMEUI ---
# Se utiliza para centralizar la configuración y evitar código repetido.
class TestPygameUI(unittest.TestCase):
    """
    Pruebas unitarias para los métodos de dibujo y cálculo de PygameUI.
    
    Verifica:
        - Creación correcta de la instancia.
        - Existencia de métodos clave (públicos y privados).
        - Cálculos de posición de puntos en pantalla.
        - Llamadas a funciones de dibujo (mockeadas).
    
    Principios SOLID verificados:
        - SRP: Métodos de dibujo específicos (draw_checkers, draw_points).
        - LSP: Comportamiento consistente de dibujo (puntos 1-24, stacks).
        - DIP: La UI depende de abstracciones (Board) para obtener datos.
    """
    @classmethod
    def setUpClass(cls):
        """Se ejecuta una vez para preparar el entorno de Pygame sin pantalla.
        
        Principio SRP: Centraliza la configuración de Pygame para esta suite de tests.
        """
        os.environ["SDL_VIDEODRIVER"] = "dummy"
        pygame.init() # Es necesario para crear superficies

    def setUp(self):
        """
        Se ejecuta antes de cada test. Crea una instancia real de PygameUI
        con una superficie en memoria para poder probar las funciones de dibujado.
        
        Principio SRP: Configuración de test (crear 'ui' con superficie)
        separada del test mismo.
        """
        self.ui = PygameUI()
        # Se asigna una superficie real para que los métodos de dibujo no fallen
        self.ui._PygameUI__screen__ = pygame.Surface((1600, 900))

    def test_draw_backgammon_board_dibuja_elementos(self):
        """Debe poder llamar a las funciones de dibujo sin errores.
        
        Principio SRP: Verifica la responsabilidad única de __draw_backgammon_board
        de orquestar el dibujo del tablero (sin fallar).
        """
        try:
            self.ui._PygameUI__draw_backgammon_board()
        except Exception as e:
            self.fail(f"__draw_backgammon_board() falló con el error: {e}")

    def test_creacion_objeto(self):
        """Debe crear correctamente una instancia de PygameUI.
        
        Principio DIP: La inicialización de PygameUI crea sus dependencias
        (Board, Dice, Managers), demostrando la composición de abstracciones.
        """
        self.assertIsNotNone(self.ui)
        self.assertIsInstance(self.ui, PygameUI)

    def test_metodo_run_existe(self):
        """Debe tener el método run.
        
        Principio ISP: Confirma la existencia de un método clave en la
        interfaz pública de la clase.
        """
        self.assertTrue(hasattr(self.ui, 'run'))
        self.assertTrue(callable(self.ui.run))

    def test_metodo_handle_events_existe(self):
        """Debe tener el método privado __handle_events.
        
        Principio ISP: Confirma la existencia de un método en la
        interfaz interna de la clase.
        """
        self.assertTrue(hasattr(self.ui, '_PygameUI__handle_events'))

    def test_metodo_update_existe(self):
        """Debe tener el método privado __update.
        
        Principio ISP: Confirma la existencia de un método en la
        interfaz interna de la clase.
        """
        self.assertTrue(hasattr(self.ui, '_PygameUI__update'))

    def test_metodo_draw_existe(self):
        """Debe tener el método privado __draw.
        
        Principio ISP: Confirma la existencia de un método en la
        interfaz interna de la clase.
        """
        self.assertTrue(hasattr(self.ui, '_PygameUI__draw'))

    def test_metodo_draw_backgammon_board_existe(self):
        """Debe tener el método privado __draw_backgammon_board.
        
        Principio ISP: Confirma la existencia de un método en la
        interfaz interna de la clase.
        """
        self.assertTrue(hasattr(self.ui, '_PygameUI__draw_backgammon_board'))

    def test_metodo_draw_points_existe(self):
        """Debe tener el método privado __draw_points.
        
        Principio ISP: Confirma la existencia de un método en la
        interfaz interna de la clase.
        """
        self.assertTrue(hasattr(self.ui, '_PygameUI__draw_points'))

    def test_metodo_draw_triangle_point_existe(self):
        """Debe tener el método privado __draw_triangle_point.
        
        Principio ISP: Confirma la existencia de un método en la
        interfaz interna de la clase.
        """
        self.assertTrue(hasattr(self.ui, '_PygameUI__draw_triangle_point'))

    def test_metodo_draw_checkers_existe(self):
        """Debe tener el método privado __draw_checkers.
        
        Principio ISP: Confirma la existencia de un método en la
        interfaz interna de la clase.
        """
        self.assertTrue(hasattr(self.ui, '_PygameUI__draw_checkers'))

    def test_metodo_get_point_screen_position_existe(self):
        """Debe tener el método privado __get_point_screen_position.
        
        Principio ISP: Confirma la existencia de un método en la
        interfaz interna de la clase.
        """
        self.assertTrue(hasattr(self.ui, '_PygameUI__get_point_screen_position'))

    def test_metodo_draw_checker_stack_existe(self):
        """Debe tener el método privado __draw_checker_stack.
        
        Principio ISP: Confirma la existencia de un método en la
        interfaz interna de la clase.
        """
        self.assertTrue(hasattr(self.ui, '_PygameUI__draw_checker_stack'))

    def test_inicializacion_con_dimensiones_default(self):
        """Debe inicializarse con dimensiones por defecto.
        
        Principio LSP: El constructor se comporta correctamente (no falla)
        cuando se le llama sin parámetros opcionales.
        """
        ui_default = PygameUI()
        self.assertIsNotNone(ui_default)

    def test_inicializacion_con_dimensiones_custom(self):
        """Debe inicializarse con dimensiones personalizadas.
        
        Principio LSP: El constructor se comporta correctamente (no falla)
        cuando se le proporcionan parámetros opcionales.
        """
        ui_custom = PygameUI(board_width=1920, board_height=1080)
        self.assertIsNotNone(ui_custom)

    def test_posicion_punto_1_en_rango_valido(self):
        """El punto 1 debe tener una posición válida.
        
        Principio LSP: Verifica que el cálculo de posición
        (__get_point_screen_position) produce un resultado válido y
        consistente para un punto específico.
        """
        x, y = self.ui._PygameUI__get_point_screen_position(1)
        self.assertIsInstance(x, int)
        self.assertIsInstance(y, int)
        self.assertGreaterEqual(x, 0)
        self.assertGreaterEqual(y, 0)
        self.assertLess(x, 1600)
        self.assertLess(y, 900)

    def test_posicion_punto_24_en_rango_valido(self):
        """El punto 24 debe tener una posición válida.
        
        Principio LSP: Verifica la consistencia del cálculo de posición
        para un caso límite (punto 24).
        """
        x, y = self.ui._PygameUI__get_point_screen_position(24)
        self.assertIsInstance(x, int)
        self.assertIsInstance(y, int)
        self.assertGreaterEqual(x, 0)
        self.assertGreaterEqual(y, 0)
        self.assertLess(x, 1600)
        self.assertLess(y, 900)

    def test_todas_las_posiciones_puntos_validas(self):
        """Todos los puntos 1-24 deben tener posiciones válidas.
        
        Principio LSP: Verifica la consistencia del cálculo de posición
        para todo el rango de entradas válidas (1-24).
        """
        for punto in range(1, 25):
            x, y = self.ui._PygameUI__get_point_screen_position(punto)
            self.assertIsInstance(x, int, f"X del punto {punto} no es entero")
            self.assertIsInstance(y, int, f"Y del punto {punto} no es entero")
            self.assertGreaterEqual(x, 0, f"X del punto {punto} es negativo: {x}")
            self.assertGreaterEqual(y, 0, f"Y del punto {punto} es negativo: {y}")
            self.assertLess(x, 1600, f"X del punto {punto} fuera de pantalla: {x}")
            self.assertLess(y, 900, f"Y del punto {punto} fuera de pantalla: {y}")

    def test_cuadrantes_puntos_correctos(self):
        """Los puntos deben estar en sus cuadrantes correctos.
        
        Principio LSP: Verifica la consistencia del cálculo de posiciones
        para todos los cuadrantes del tablero.
        """
        # Puntos 1-6: cuadrante superior derecho
        for punto in range(1, 7):
            x, y = self.ui._PygameUI__get_point_screen_position(punto)
            self.assertGreater(x, 800, f"Punto {punto} debe estar en lado derecho")
            self.assertLess(y, 450, f"Punto {punto} debe estar arriba")

        # Puntos 7-12: cuadrante superior izquierdo
        for punto in range(7, 13):
            x, y = self.ui._PygameUI__get_point_screen_position(punto)
            self.assertLess(x, 800, f"Punto {punto} debe estar en lado izquierdo")
            self.assertLess(y, 450, f"Punto {punto} debe estar arriba")

        # Puntos 13-18: cuadrante inferior izquierdo
        for punto in range(13, 19):
            x, y = self.ui._PygameUI__get_point_screen_position(punto)
            self.assertLess(x, 800, f"Punto {punto} debe estar en lado izquierdo")
            self.assertGreater(y, 450, f"Punto {punto} debe estar abajo")

        # Puntos 19-24: cuadrante inferior derecho
        for punto in range(19, 25):
            x, y = self.ui._PygameUI__get_point_screen_position(punto)
            self.assertGreater(x, 800, f"Punto {punto} debe estar en lado derecho")
            self.assertGreater(y, 450, f"Punto {punto} debe estar abajo")

    @patch("pygame.draw.polygon")
    def test_draw_triangle_point_hacia_abajo(self, mock_polygon):
        """Debe dibujar triángulos apuntando hacia abajo.
        
        Principio SRP: Verifica la responsabilidad única de __draw_triangle_point
        de dibujar un triángulo en una dirección específica.
        """
        self.ui._PygameUI__screen__ = pygame.Surface((1600, 900))
        self.ui._PygameUI__draw_triangle_point(100, 100, 50, 100, (255, 0, 0), pointing_down=True)
        self.assertTrue(mock_polygon.called)
        self.assertEqual(mock_polygon.call_count, 2)  # Relleno + borde

    @patch("pygame.draw.polygon")
    def test_draw_triangle_point_hacia_arriba(self, mock_polygon):
        """Debe dibujar triángulos apuntando hacia arriba.
        
        Principio SRP: Verifica la responsabilidad única de __draw_triangle_point
        de dibujar un triángulo en la dirección opuesta.
        """
        self.ui._PygameUI__screen__ = pygame.Surface((1600, 900))
        self.ui._PygameUI__draw_triangle_point(100, 100, 50, 100, (0, 255, 0), pointing_down=False)
        self.assertTrue(mock_polygon.called)
        self.assertEqual(mock_polygon.call_count, 2)  # Relleno + borde

    @patch("pygame.draw.circle")
    def test_draw_checker_stack_fichas_blancas(self, mock_circle):
        """Debe dibujar stack de fichas blancas.
        
        Principio LSP: El método __draw_checker_stack se comporta
        consistentemente para diferentes colores (blanco).
        """
        self.ui._PygameUI__screen__ = pygame.Surface((1600, 900))
        self.ui._PygameUI__draw_checker_stack(400, 300, "blanco", 3, 6, 25)
        # 3 fichas + 3 bordes = 6 llamadas
        self.assertEqual(mock_circle.call_count, 6)

    @patch("pygame.draw.circle")
    def test_draw_checker_stack_fichas_negras(self, mock_circle):
        """Debe dibujar stack de fichas negras.
        
        Principio LSP: El método __draw_checker_stack se comporta
        consistentemente para diferentes colores (negro).
        """
        self.ui._PygameUI__screen__ = pygame.Surface((1600, 900))
        self.ui._PygameUI__draw_checker_stack(400, 300, "negro", 2, 19, 25)
        # 2 fichas + 2 bordes = 4 llamadas
        self.assertEqual(mock_circle.call_count, 4)

    @patch("pygame.draw.circle")
    def test_draw_checker_stack_limite_fichas_visibles(self, mock_circle):
        """No debe dibujar más de 10 fichas visibles.
        
        Principio LSP: El método __draw_checker_stack maneja
        consistentemente un caso límite (más de 10 fichas).
        """
        self.ui._PygameUI__screen__ = pygame.Surface((1600, 900))
        self.ui._PygameUI__draw_checker_stack(400, 300, "blanco", 15, 13, 25)
        # Máximo 10 fichas + 10 bordes = 20 llamadas
        self.assertEqual(mock_circle.call_count, 20)

    @patch("pygame.draw.rect")
    def test_draw_backgammon_board_dibuja_elementos(self, mock_rect):
        """Debe dibujar el fondo del tablero y la barra.
        
        Principio SRP: Verifica que el método __draw_backgammon_board cumple
        su responsabilidad de dibujar los componentes base.
        """
        self.ui._PygameUI__screen__ = pygame.Surface((1600, 900))
        self.ui._PygameUI__draw_backgammon_board()
        # Al menos 2 rectángulos: fondo del tablero + barra
        self.assertGreaterEqual(mock_rect.call_count, 2)

    @patch("pygame.draw.polygon")
    def test_draw_points_dibuja_24_triangulos(self, mock_polygon):
        """Debe dibujar los 24 triángulos del tablero.
        
        Principio SRP: Verifica la responsabilidad única de __draw_points de
        dibujar todos los triángulos.
        """
        self.ui._PygameUI__screen__ = pygame.Surface((1600, 900))
        self.ui._PygameUI__draw_points()
        # 24 triángulos × 2 (relleno + borde) = 48 llamadas
        self.assertEqual(mock_polygon.call_count, 48)

    def test_draw_checkers_no_falla_con_board_real(self):
        """El método draw_checkers debe funcionar con el board real.
        
        Principio DIP: El método __draw_checkers opera correctamente sobre
        la abstracción del Board, leyendo su estado para dibujar.
        """
        self.ui._PygameUI__screen__ = pygame.Surface((1600, 900))
        try:
            self.ui._PygameUI__draw_checkers()
        except Exception as e:
            self.fail(f"draw_checkers falló con board real: {e}")

    @patch("pygame.display.flip")
    def test_draw_llama_display_flip(self, mock_flip):
        """El método draw debe llamar a pygame.display.flip.
        
        Principio SRP: Confirma que la responsabilidad final de __draw es
        actualizar la pantalla (llamar a flip).
        """
        self.ui._PygameUI__screen__ = pygame.Surface((1600, 900))
        self.ui._PygameUI__draw()
        mock_flip.assert_called_once()

    def test_update_metodo_ejecutable(self):
        """El método __update debe ser ejecutable sin errores.
        
        Principio LSP: El método se comporta de forma estable (no falla)
        en un estado base o vacío.
        """
        try:
            self.ui._PygameUI__update()
        except Exception as e:
            self.fail(f"Método __update falló: {e}")

    def test_handle_events_sin_eventos(self):
        """Handle events debe funcionar sin eventos.
        
        Principio LSP: El método se comporta de forma estable (no falla)
        cuando la lista de eventos está vacía.
        """
        with patch("pygame.event.get", return_value=[]):
            try:
                self.ui._PygameUI__handle_events()
            except Exception as e:
                self.fail(f"__handle_events falló sin eventos: {e}")

    def test_draw_metodo_completo_ejecutable(self):
        """El método __draw completo debe ser ejecutable.
        
        Principio SRP: Verifica que el método principal de orquestación
        de dibujo (__draw) puede ejecutar todas sus sub-responsabilidades.
        """
        self.ui._PygameUI__screen__ = pygame.Surface((1600, 900))
        try:
            self.ui._PygameUI__draw()
        except Exception as e:
            self.fail(f"Método __draw completo falló: {e}")

    def test_puntos_extremos_posicionamiento_correcto(self):
        """Los puntos en las esquinas deben estar correctamente posicionados.
        
        Principio LSP: Verifica la consistencia del cálculo de posiciones
        en los casos extremos (esquinas).
        """
        # Punto 1: esquina superior derecha
        x1, y1 = self.ui._PygameUI__get_point_screen_position(1)

        # Punto 12: esquina superior izquierda
        x12, y12 = self.ui._PygameUI__get_point_screen_position(12)

        # Punto 13: esquina inferior izquierda
        x13, y13 = self.ui._PygameUI__get_point_screen_position(13)

        # Punto 24: esquina inferior derecha
        x24, y24 = self.ui._PygameUI__get_point_screen_position(24)

        # Verificar que están en lados correctos
        self.assertGreater(x1, x12, "Punto 1 debe estar más a la derecha que punto 12")
        self.assertLess(x13, x24, "Punto 13 debe estar más a la izquierda que punto 24")
        self.assertLess(y1, y24, "Punto 1 debe estar más arriba que punto 24")
        self.assertLess(y12, y13, "Punto 12 debe estar más arriba que punto 13")

    def test_draw_triangle_parametros_validos(self):
        """Los parámetros del triángulo deben ser manejados correctamente.
        
        Principio LSP: El método de dibujo es robusto y se comporta
        consistentemente con diferentes parámetros de entrada válidos.
        """
        self.ui._PygameUI__screen__ = pygame.Surface((1600, 900))

        # Test con diferentes parámetros válidos
        parametros_test = [
            (50, 50, 80, 150, (255, 0, 0), True),
            (200, 100, 90, 200, (0, 255, 0), False),
            (0, 0, 100, 300, (0, 0, 255), True),
        ]

        for x, y, width, height, color, pointing_down in parametros_test:
            try:
                self.ui._PygameUI__draw_triangle_point(x, y, width, height, color, pointing_down)
            except Exception as e:
                self.fail(f"Error con parámetros ({x}, {y}, {width}, {height}, {color}, {pointing_down}): {e}")

    def test_direccion_apilamiento_fichas(self):
        """Las fichas deben apilarse en la dirección correcta según el punto.
        
        Principio LSP: Verifica que __draw_checker_stack se comporta
        correctamente (apila hacia arriba/abajo) según la posición.
        """
        self.ui._PygameUI__screen__ = pygame.Surface((1600, 900))

        # Test para puntos que van hacia abajo (1-12)
        try:
            self.ui._PygameUI__draw_checker_stack(400, 200, "blanco", 3, 5, 25)
        except Exception as e:
            self.fail(f"Error apilando hacia abajo: {e}")

        # Test para puntos que van hacia arriba (13-24)
        try:
            self.ui._PygameUI__draw_checker_stack(400, 600, "negro", 3, 15, 25)
        except Exception as e:
            self.fail(f"Error apilando hacia arriba: {e}")

    def test_board_instancia_es_board(self):
        """La instancia interna debe ser de tipo Board.
        
        Principio DIP: Confirma que la UI mantiene una referencia a una abstracción
        de tipo Board (o una clase que hereda de ella).
        """
        # Acceder al board de manera más indirecta
        board_attr_names = [attr for attr in dir(self.ui) if 'board' in attr.lower()]
        self.assertGreater(len(board_attr_names), 0, "Debe tener al menos un atributo relacionado con board")


# --- NUEVA CLASE DE TESTS AÑADIDA ---
class TestPygameUIClickDetection(unittest.TestCase):
    """
    Suite de pruebas dedicada a verificar la correcta detección de clics en el tablero.
    
    Principios SOLID verificados:
        - SRP: El método __get_point_from_mouse_pos tiene la única
          responsabilidad de traducir coordenadas (x,y) a un número de punto.
        - LSP: El método se comporta de forma predecible y consistente
          en todos los cuadrantes y casos límite (barra, fuera del tablero).
    """
    @classmethod
    def setUpClass(cls):
        """Evita que pygame intente abrir una ventana durante los tests.
        
        Principio SRP: Centraliza la configuración del entorno para esta suite.
        """
        # Evita que pygame intente abrir una ventana durante los tests
        os.environ["SDL_VIDEODRIVER"] = "dummy"

    def setUp(self):
        """Crea una instancia de PygameUI para cada test.
        
        Principio SRP: Aísla la configuración de cada test.
        """
        with patch('pygame.init'), patch('pygame.display.set_mode'), patch('pygame.font.Font'):
         self.ui = PygameUI(board_width=1600, board_height=900)

    def test_get_point_from_mouse_pos_top_right_quadrant(self):
        """Prueba clics en cuadrante superior derecho (puntos 1-6).
        
        Principio LSP: Verifica el comportamiento consistente y correcto de
        __get_point_from_mouse_pos en un cuadrante específico.
        """
        # Punto 1 (más a la derecha)
        self.assertEqual(self.ui._PygameUI__get_point_from_mouse_pos((1500, 100)), 1)
        # Punto 3
        self.assertEqual(self.ui._PygameUI__get_point_from_mouse_pos((1250, 100)), 3)
        # Punto 6 (más cercano a la barra)
        self.assertEqual(self.ui._PygameUI__get_point_from_mouse_pos((850, 100)), 6)

    def test_get_point_from_mouse_pos_top_left_quadrant(self):
        """Prueba clics en cuadrante superior izquierdo (puntos 7-12).
        
        Principio LSP: Verifica el comportamiento consistente y correcto de
        __get_point_from_mouse_pos en un cuadrante específico.
        """
        # Punto 7 (más cercano a la barra)
        self.assertEqual(self.ui._PygameUI__get_point_from_mouse_pos((750, 100)), 7)
        # Punto 10
        self.assertEqual(self.ui._PygameUI__get_point_from_mouse_pos((400, 100)), 10)
        # Punto 12 (más a la izquierda)
        self.assertEqual(self.ui._PygameUI__get_point_from_mouse_pos((100, 100)), 12)

    def test_get_point_from_mouse_pos_bottom_left_quadrant(self):
        """Prueba clics en cuadrante inferior izquierdo (puntos 13-18).
        
        Principio LSP: Verifica el comportamiento consistente y correcto de
        __get_point_from_mouse_pos en un cuadrante específico.
        """
        # Punto 13 (más a la izquierda)
        self.assertEqual(self.ui._PygameUI__get_point_from_mouse_pos((100, 800)), 13)
        # Punto 15
        self.assertEqual(self.ui._PygameUI__get_point_from_mouse_pos((300, 800)), 15)
        # Punto 18 (más cercano a la barra)
        self.assertEqual(self.ui._PygameUI__get_point_from_mouse_pos((700, 800)), 18)

    def test_get_point_from_mouse_pos_bottom_right_quadrant(self):
        """Prueba clics en cuadrante inferior derecho (puntos 19-24).
        
        Principio LSP: Verifica el comportamiento consistente y correcto de
        __get_point_from_mouse_pos en un cuadrante específico.
        """
        # Punto 19 (más cercano a la barra)
        self.assertEqual(self.ui._PygameUI__get_point_from_mouse_pos((850, 800)), 19)
        # Punto 21
        self.assertEqual(self.ui._PygameUI__get_point_from_mouse_pos((1100, 800)), 21)
        # Punto 24 (más a la derecha)
        self.assertEqual(self.ui._PygameUI__get_point_from_mouse_pos((1500, 800)), 24)

    def test_get_point_from_mouse_pos_invalid_clicks(self):
        """Prueba que los clics fuera de las áreas de los puntos devuelven None o 0 (barra).
        
        Principio LSP: Verifica el comportamiento consistente del método en
        casos límite (fuera del tablero, barra).
        """
        # Click en el margen izquierdo
        self.assertIsNone(self.ui._PygameUI__get_point_from_mouse_pos((25, 450)))
        # Click en el margen superior
        self.assertIsNone(self.ui._PygameUI__get_point_from_mouse_pos((800, 25)))
        # Click en la barra central - AHORA DEVUELVE 0 (que es correcto)
        # Este test se elimina o se cambia para verificar que devuelve 0
        bar_result = self.ui._PygameUI__get_point_from_mouse_pos((790, 450))
        self.assertEqual(bar_result, 0, "Clic en la barra debe devolver 0")


# --- SUITE DE TESTS PARA LA LÓGICA DEL JUEGO (SIN DIBUJADO) ---
class TestPygameUILogic(unittest.TestCase):
    """
    Suite de pruebas para la lógica del juego (tiradas, selección, validación),
    sin depender de la renderización en pantalla.
    
    Principios SOLID verificados:
        - DIP: La UI (alto nivel) delega la validación y ejecución
          de movimientos a las abstracciones del Core (Board, Dice).
        - SRP: Cada test verifica una responsabilidad lógica
          específica (tirar dados, seleccionar, validar).
    """
    def setUp(self):
        """
        Se ejecuta antes de cada test. Inicializa PygameUI de forma segura.
        
        Principio SRP: Aísla la configuración (instancia de UI) para cada test.
        """
        with patch('pygame.init'), \
             patch('pygame.display.set_mode'), \
             patch('pygame.font.Font'):
            self.ui = PygameUI()

    # --- Helper Method ---
    def _simulate_click_on_point(self, point_number: int):
        """Helper para simular un evento de clic del ratón.
        
        Principio SRP: Encapsula la lógica de simulación de clics,
        reduciendo duplicación en los tests (principio DRY).
        """
        self.ui.__game_state_manager__.change_state('AWAITING_PIECE_SELECTION')
        self.ui.__current_player__ = "negro"
        with patch.object(self.ui, '_PygameUI__get_point_from_mouse_pos', return_value=point_number):
            mock_event = Mock(type=pygame.MOUSEBUTTONDOWN, button=1, pos=(100, 100))
            with patch('pygame.event.get', return_value=[mock_event]), \
                 patch('pygame.mouse.get_pos', return_value=(100, 100)):
                self.ui._PygameUI__handle_events()

    # --- Tests para la Tirada de Dados Inicial ---
    @patch('Backgammon.Core.Dice.Dice.tirar')
    @patch('Backgammon.Core.Dice.Dice.obtener_dado1')
    @patch('Backgammon.Core.Dice.Dice.obtener_dado2')
    def test_roll_to_start_negro_wins(self, mock_dado2, mock_dado1, mock_tirar):
        """Verifica que 'negro' gana la tirada inicial con un dado más alto.
        
        Principio DIP: La UI coordina la tirada, pero la lógica de 'tirar'
        y 'obtener_dado' reside en la abstracción (Mock) de Dice.
        """
        mock_dado1.return_value = 5
        mock_dado2.return_value = 3
        self.ui._PygameUI__roll_to_start()
        self.assertEqual(self.ui.__current_player__, "negro")

    @patch('Backgammon.Core.Dice.Dice.tirar')
    @patch('Backgammon.Core.Dice.Dice.obtener_dado1')
    @patch('Backgammon.Core.Dice.Dice.obtener_dado2')
    def test_roll_to_start_blanco_wins(self, mock_dado2, mock_dado1, mock_tirar):
        """Verifica que 'blanco' gana la tirada inicial con un dado más alto.
        
        Principio DIP: La UI coordina la tirada, pero la lógica de 'tirar'
        y 'obtener_dado' reside en la abstracción (Mock) de Dice.
        """
        mock_dado1.return_value = 2
        mock_dado2.return_value = 6
        self.ui._PygameUI__roll_to_start()
        self.assertEqual(self.ui.__current_player__, "blanco")

    @patch('Backgammon.Core.Dice.Dice.tirar')
    @patch('Backgammon.Core.Dice.Dice.obtener_dado1')
    @patch('Backgammon.Core.Dice.Dice.obtener_dado2')
    def test_roll_to_start_handles_tie(self, mock_dado2, mock_dado1, mock_tirar):
        """Verifica que el método vuelve a tirar los dados si ocurre un empate.
        
        Principio LSP: El método __roll_to_start maneja consistentemente
        el caso de un empate (un estado de entrada diferente).
        """
        mock_dado1.side_effect = [4, 6]
        mock_dado2.side_effect = [4, 1]
        self.ui._PygameUI__roll_to_start()
        self.assertEqual(self.ui.__current_player__, "negro")
        self.assertEqual(mock_tirar.call_count, 2)

    # --- Tests para Selección y Validación de Movimientos ---
    def test_select_valid_piece(self):
        """Verifica que se puede seleccionar un punto con fichas propias.
        
        Principio DIP: La UI interactúa con la abstracción del Board
        para validar la propiedad de la ficha antes de seleccionarla.
        """
        self.ui.__board__.colocar_ficha(1, "negro", 1)
        self._simulate_click_on_point(1)
        self.assertEqual(self.ui.__selected_point__, 1)

    def test_validate_move_valid(self):
        """Verifica que la UI reporta correctamente un movimiento válido.
        
        Principio DIP: La UI delega la validación del movimiento
        (__validate_and_report_move) a las reglas del Board y managers.
        """
        self.ui.__current_player__ = "negro"
        self.ui.__available_moves__ = [4]
        self.ui.__board__.colocar_ficha(19, "negro", 1)
        # Vaciamos el punto de destino para asegurar que el movimiento sea válido
        self.ui.__board__.colocar_ficha(23, "vacío", 0)
        result = self.ui._PygameUI__validate_and_report_move(origen=19, destino=23)
        self.assertTrue(result)

    def test_validate_move_invalid_blocked(self):
        """Verifica que la UI reporta correctamente un movimiento a un punto bloqueado.
        
        Principio DIP: La UI delega la validación de bloqueo
        a los componentes del Core (Board, CaptureValidator).
        """
        self.ui.__current_player__ = "negro"
        self.ui.__available_moves__ = [4]
        self.ui.__board__.colocar_ficha(19, "negro", 1)
        self.ui.__board__.colocar_ficha(23, "blanco", 2) # Bloqueamos el destino
        result = self.ui._PygameUI__validate_and_report_move(origen=19, destino=23)
        self.assertFalse(result)

    def test_move_direction_negro_valid(self):
        """Verifica que el jugador negro PUEDE mover hacia números mayores.
        
        Principio LSP: Confirma que la lógica de validación de dirección
        es consistente para el jugador 'negro'.
        """
        self.ui.__current_player__ = "negro"
        self.ui.__available_moves__ = [2]
        self.ui.__board__.colocar_ficha(1, "negro", 1)
        result = self.ui._PygameUI__validate_and_report_move(origen=1, destino=3)
        self.assertTrue(result)

    def test_move_direction_blanco_valid(self):
        """Verifica que el jugador blanco PUEDE mover hacia números menores.
        
        Principio LSP: Confirma que la lógica de validación de dirección
        es consistente para el jugador 'blanco'.
        """
        self.ui.__current_player__ = "blanco"
        self.ui.__available_moves__ = [2]
        self.ui.__board__.colocar_ficha(24, "blanco", 1)
        result = self.ui._PygameUI__validate_and_report_move(origen=24, destino=22)
        self.assertTrue(result)

    def test_move_direction_negro_edge_cases(self):
        """Tests adicionales para casos límite del jugador negro.
        
        Principio LSP: Verifica la consistencia de la validación
        en un caso límite (cruce de cuadrante) para 'negro'.
        """
        self.ui.__current_player__ = "negro"
        self.ui.__available_moves__ = [6]
        self.ui.__board__.colocar_ficha(1, "negro", 1)
        result = self.ui._PygameUI__validate_and_report_move(origen=1, destino=7)
        self.assertTrue(result)

    def test_move_direction_blanco_edge_cases(self):
        """Tests adicionales para casos límite del jugador blanco.
        
        Principio LSP: Verifica la consistencia de la validación
        en un caso límite (cruce de cuadrante) para 'blanco'.
        """
        self.ui.__current_player__ = "blanco"
        self.ui.__available_moves__ = [6]
        self.ui.__board__.colocar_ficha(24, "blanco", 1)
        # Vaciamos el punto de destino para asegurar que el movimiento sea válido
        self.ui.__board__.colocar_ficha(18, "vacío", 0)
        result = self.ui._PygameUI__validate_and_report_move(origen=24, destino=18)
        self.assertTrue(result)


# --- TESTS PARA BEARING OFF ---
class TestBearingOffFunctionality(unittest.TestCase):
    """
    Suite de tests completa para verificar la funcionalidad de bearing off.
    Cubre BearingOffValidator, HomeManager y la integración con PygameUI.
    
    Principios SOLID verificados:
        - SRP: Cada clase (BearingOffValidator, HomeManager) tiene una
          única responsabilidad. Este test las verifica por separado.
        - DIP: PygameUI depende de las abstracciones de estos
          managers, no implementa la lógica de 'bearing off' en sí misma.
    """
    
    def setUp(self):
        """Configura el entorno sin interfaz gráfica.
        
        Principio SRP: Centraliza la configuración e inicialización de los
        componentes bajo prueba (UI, managers, board).
        """
        os.environ["SDL_VIDEODRIVER"] = "dummy"
        pygame.init()
        with patch('pygame.display.set_mode', return_value=pygame.Surface((1600, 900))), \
             patch('pygame.font.Font'):
            self.ui = PygameUI()
            # CORREGIDO: Sin el prefijo             self.bearing_off_validator = self.ui.__bearing_off_validator__
            self.home_manager = self.ui.__home_manager__
            self.bearing_off_validator = self.ui.__bearing_off_validator__
            self.game_state_manager = self.ui.__game_state_manager__
            self.bar_manager = self.ui.__bar_manager__
            self.board = self.ui.__board__
            self.home_manager.__home_pieces__ = {"negro": 0, "blanco": 0}

    # --- Tests para BearingOffValidator.can_bear_off() ---
    
    def test_can_bear_off_negro_all_pieces_in_home(self):
        """Negro debe poder hacer bearing off cuando todas sus fichas están en 19-24.
        
        Principio SRP: Verifica la responsabilidad única de BearingOffValidator
        de determinar si el 'bearing off' está permitido (caso 'negro' válido).
        """
        # Limpiar tablero primero
        for i in range(24):
            self.board.__puntos__[i] = (None, 0)
        
        # Colocar fichas solo en home
        self.board.__puntos__[18] = ("negro", 5)  # punto 19
        self.board.__puntos__[19] = ("negro", 5)  # punto 20
        self.board.__puntos__[20] = ("negro", 5)  # punto 21
        
        result = self.bearing_off_validator.can_bear_off("negro")
        self.assertTrue(result)
    
    def test_can_bear_off_negro_pieces_outside_home(self):
        """Negro NO debe poder hacer bearing off si tiene fichas fuera de 19-24.
        
        Principio SRP: Verifica la responsabilidad única de BearingOffValidator
        (caso 'negro' inválido).
        """
        # Limpiar tablero
        for i in range(24):
            self.board.__puntos__[i] = (None, 0)
            
        self.board.__puntos__[18] = ("negro", 10)  # punto 19
        self.board.__puntos__[12] = ("negro", 5)   # punto 13 (fuera de home)
        
        result = self.bearing_off_validator.can_bear_off("negro")
        self.assertFalse(result)
    
    def test_can_bear_off_blanco_all_pieces_in_home(self):
        """Blanco debe poder hacer bearing off cuando todas sus fichas están en 1-6.
        
        Principio SRP: Verifica la responsabilidad única de BearingOffValidator
        (caso 'blanco' válido).
        """
        # Limpiar tablero
        for i in range(24):
            self.board.__puntos__[i] = (None, 0)
            
        self.board.__puntos__[0] = ("blanco", 5)  # punto 1
        self.board.__puntos__[1] = ("blanco", 5)  # punto 2
        self.board.__puntos__[2] = ("blanco", 5)  # punto 3
        
        result = self.bearing_off_validator.can_bear_off("blanco")
        self.assertTrue(result)
    
    def test_can_bear_off_blanco_pieces_outside_home(self):
        """Blanco NO debe poder hacer bearing off si tiene fichas fuera de 1-6.
        
        Principio SRP: Verifica la responsabilidad única de BearingOffValidator
        (caso 'blanco' inválido).
        """
        # Limpiar tablero
        for i in range(24):
            self.board.__puntos__[i] = (None, 0)
            
        self.board.__puntos__[0] = ("blanco", 10)  # punto 1
        self.board.__puntos__[10] = ("blanco", 5)  # punto 11 (fuera de home)
        
        result = self.bearing_off_validator.can_bear_off("blanco")
        self.assertFalse(result)

    # --- Tests para validate_bearing_off_move() ---
    
    def test_validate_bearing_off_negro_exact_dice(self):
        """Negro debe poder sacar con dado exacto (ej: ficha en 23, dado 2).
        
        Principio SRP: Verifica la responsabilidad de BearingOffValidator
        de validar un intento de 'bearing off' (caso dado exacto).
        """
        # Limpiar tablero
        for i in range(24):
            self.board.__puntos__[i] = (None, 0)
            
        self.board.__puntos__[22] = ("negro", 1)  # punto 23
        
        is_valid, msg = self.bearing_off_validator.validate_bearing_off_move("negro", 23, 2)
        self.assertTrue(is_valid)
        self.assertEqual(msg, "")
    
    def test_validate_bearing_off_negro_higher_dice_no_pieces_further(self):
        """Negro debe poder sacar con dado mayor si no hay fichas más alejadas.
        
        Principio SRP: Verifica la lógica de 'bearing off'
        (caso dado mayor, sin fichas más lejanas).
        """
        # Limpiar tablero
        for i in range(24):
            self.board.__puntos__[i] = (None, 0)
            
        self.board.__puntos__[22] = ("negro", 1)  # punto 23 (distancia 2)
        
        is_valid, msg = self.bearing_off_validator.validate_bearing_off_move("negro", 23, 5)
        self.assertTrue(is_valid)
    
    def test_validate_bearing_off_negro_higher_dice_pieces_further(self):
        """Negro NO debe poder sacar con dado mayor si hay fichas más alejadas.
        
        Principio SRP: Verifica la lógica de 'bearing off'
        (caso dado mayor, CON fichas más lejanas).
        """
        # Limpiar tablero
        for i in range(24):
            self.board.__puntos__[i] = (None, 0)
            
        self.board.__puntos__[22] = ("negro", 1)  # punto 23 (distancia 2)
        self.board.__puntos__[20] = ("negro", 1)  # punto 21 (más alejado)
        
        is_valid, msg = self.bearing_off_validator.validate_bearing_off_move("negro", 23, 5)
        self.assertFalse(is_valid)
        self.assertIn("fichas superiores", msg)
    
    def test_validate_bearing_off_blanco_exact_dice(self):
        """Blanco debe poder sacar con dado exacto (ej: ficha en 3, dado 3).
        
        Principio SRP: Verifica la lógica de 'bearing off'
        (caso 'blanco', dado exacto).
        """
        # Limpiar tablero
        for i in range(24):
            self.board.__puntos__[i] = (None, 0)
            
        self.board.__puntos__[2] = ("blanco", 1)  # punto 3
        
        is_valid, msg = self.bearing_off_validator.validate_bearing_off_move("blanco", 3, 3)
        self.assertTrue(is_valid)
        self.assertEqual(msg, "")
    
    def test_validate_bearing_off_blanco_higher_dice_no_pieces_further(self):
        """Blanco debe poder sacar con dado mayor si no hay fichas más alejadas.
        
        Principio SRP: Verifica la lógica de 'bearing off'
        (caso 'blanco', dado mayor, sin fichas lejanas).
        """
        # Limpiar tablero
        for i in range(24):
            self.board.__puntos__[i] = (None, 0)
            
        self.board.__puntos__[2] = ("blanco", 1)  # punto 3 (distancia 3)
        
        is_valid, msg = self.bearing_off_validator.validate_bearing_off_move("blanco", 3, 6)
        self.assertTrue(is_valid)
    
    def test_validate_bearing_off_piece_not_in_home(self):
        """No debe permitir bearing off si la ficha no está en home.
        
        Principio SRP: Verifica la validación de 'bearing off'
        (caso ficha fuera de 'home').
        """
        # Limpiar tablero
        for i in range(24):
            self.board.__puntos__[i] = (None, 0)
            
        self.board.__puntos__[12] = ("negro", 1)  # punto 13 (no home)
        
        is_valid, msg = self.bearing_off_validator.validate_bearing_off_move("negro", 13, 2)
        self.assertFalse(is_valid)
        self.assertIn("cuadrante casa", msg)
    
    def test_validate_bearing_off_insufficient_dice(self):
        """No debe permitir bearing off con dado menor al necesario.
        
        Principio SRP: Verifica la validación de 'bearing off'
        (caso dado insuficiente).
        """
        # Limpiar tablero
        for i in range(24):
            self.board.__puntos__[i] = (None, 0)
            
        self.board.__puntos__[18] = ("negro", 1)  # punto 19 (distancia 6)
        
        is_valid, msg = self.bearing_off_validator.validate_bearing_off_move("negro", 19, 3)
        self.assertFalse(is_valid)
        self.assertIn("al menos dado 6", msg)

    # --- Tests para _has_pieces_in_higher_positions() ---
    
    def test_has_pieces_in_higher_positions_negro_true(self):
        """Verifica detección correcta de fichas más alejadas para negro.
        
        Principio SRP: Prueba una sub-responsabilidad (método helper)
        de BearingOffValidator, asegurando su lógica interna.
        """
        # Limpiar tablero
        for i in range(24):
            self.board.__puntos__[i] = (None, 0)
            
        self.board.__puntos__[22] = ("negro", 1)  # punto 23
        self.board.__puntos__[19] = ("negro", 1)  # punto 20 (más alejado)
        
        result = self.bearing_off_validator._has_pieces_in_higher_positions("negro", 23)
        self.assertTrue(result)
    
    def test_has_pieces_in_higher_positions_negro_false(self):
        """Negro sin fichas más alejadas.
        
        Principio SRP: Prueba un método helper de BearingOffValidator
        (caso negativo).
        """
        # Limpiar tablero
        for i in range(24):
            self.board.__puntos__[i] = (None, 0)
            
        self.board.__puntos__[18] = ("negro", 1)  # punto 19 (la más alejada)
        
        result = self.bearing_off_validator._has_pieces_in_higher_positions("negro", 19)
        self.assertFalse(result)
    
    def test_has_pieces_in_higher_positions_blanco_true(self):
        """Verifica detección correcta de fichas más alejadas para blanco.
        
        Principio SRP: Prueba un método helper de BearingOffValidator
        (caso 'blanco', positivo).
        """
        # Limpiar tablero
        for i in range(24):
            self.board.__puntos__[i] = (None, 0)
            
        self.board.__puntos__[2] = ("blanco", 1)  # punto 3
        self.board.__puntos__[4] = ("blanco", 1)  # punto 5 (más alejado)
        
        result = self.bearing_off_validator._has_pieces_in_higher_positions("blanco", 3)
        self.assertTrue(result)
    
    def test_has_pieces_in_higher_positions_blanco_false(self):
        """Blanco sin fichas más alejadas.
        
        Principio SRP: Prueba un método helper de BearingOffValidator
        (caso 'blanco', negativo).
        """
        # Limpiar tablero
        for i in range(24):
            self.board.__puntos__[i] = (None, 0)
            
        self.board.__puntos__[5] = ("blanco", 1)  # punto 6 (la más alejada)
        
        result = self.bearing_off_validator._has_pieces_in_higher_positions("blanco", 6)
        self.assertFalse(result)

    # --- Tests para HomeManager ---
    
    def test_home_manager_initial_state(self):
        """Verifica estado inicial del HomeManager.
        
        Principio SRP: Verifica la responsabilidad única de HomeManager
        de rastrear el estado de 'casa' (estado inicial).
        """
        self.assertEqual(self.home_manager.get_pieces_count("negro"), 0)
        self.assertEqual(self.home_manager.get_pieces_count("blanco"), 0)
    
    def test_home_manager_add_piece(self):
        """Verifica que se puedan agregar fichas a casa.
        
        Principio SRP: Verifica la responsabilidad de HomeManager
        de agregar fichas a 'casa'.
        """
        self.home_manager.add_piece_to_home("negro")
        self.assertEqual(self.home_manager.get_pieces_count("negro"), 1)
        
        self.home_manager.add_piece_to_home("blanco")
        self.home_manager.add_piece_to_home("blanco")
        self.assertEqual(self.home_manager.get_pieces_count("blanco"), 2)
    
    def test_home_manager_has_won_false(self):
        """Verifica que no se detecte victoria prematura.
        
        Principio SRP: Verifica la responsabilidad de HomeManager
        de determinar la victoria (caso negativo).
        """
        for _ in range(14):
            self.home_manager.add_piece_to_home("negro")
        
        self.assertFalse(self.home_manager.has_won("negro"))
    
    def test_home_manager_has_won_true(self):
        """Verifica detección correcta de victoria.
        
        Principio SRP: Verifica la responsabilidad de HomeManager
        de determinar la victoria (caso positivo).
        """
        for _ in range(15):
            self.home_manager.add_piece_to_home("negro")
        
        self.assertTrue(self.home_manager.has_won("negro"))
    
    def test_home_manager_get_state(self):
        """Verifica que se pueda obtener el estado completo.
        
        Principio SRP: Verifica la responsabilidad de HomeManager
        de reportar su estado.
        """
        self.home_manager.add_piece_to_home("negro")
        self.home_manager.add_piece_to_home("blanco")
        self.home_manager.add_piece_to_home("blanco")
        
        state = self.home_manager.get_home_state()
        self.assertEqual(state, {"negro": 1, "blanco": 2})
    
    def test_home_manager_invalid_color_raises_error(self):
        """Verifica que color inválido genere error.
        
        Principio LSP: El HomeManager maneja correctamente
        entradas inválidas (lanzando excepción).
        """
        with self.assertRaises(ValueError):
            self.home_manager.add_piece_to_home("rojo")

    # --- Tests de integración para bearing off en PygameUI ---
    
    def test_calculate_bearing_off_dice_negro(self):
        """Verifica cálculo correcto de dado necesario para negro.
        
        Principio SRP: Prueba la responsabilidad de PygameUI de *calcular*
        el dado necesario para un movimiento de 'bearing off'.
        """
        self.ui.__current_player__ = "negro"
        
        self.assertEqual(self.ui._PygameUI__calculate_bearing_off_dice(19), 6)
        self.assertEqual(self.ui._PygameUI__calculate_bearing_off_dice(23), 2)
        self.assertEqual(self.ui._PygameUI__calculate_bearing_off_dice(24), 1)
    
    def test_calculate_bearing_off_dice_blanco(self):
        """Verifica cálculo correcto de dado necesario para blanco.
        
        Principio SRP: Prueba la responsabilidad de PygameUI de *calcular*
        el dado necesario (caso 'blanco').
        """
        self.ui.__current_player__ = "blanco"
        
        self.assertEqual(self.ui._PygameUI__calculate_bearing_off_dice(6), 6)
        self.assertEqual(self.ui._PygameUI__calculate_bearing_off_dice(3), 3)
        self.assertEqual(self.ui._PygameUI__calculate_bearing_off_dice(1), 1)
    
    def test_has_valid_bearing_off_moves_true(self):
        """Verifica detección de movimientos válidos de bearing off.
        
        Principio DIP: La UI coordina, preguntando a la abstracción
        BearingOffValidator si existen movimientos válidos.
        """
        self.ui.__current_player__ = "negro"
        self.ui.__available_moves__ = [2, 5]
        
        # Limpiar tablero
        for i in range(24):
            self.board.__puntos__[i] = (None, 0)
        self.board.__puntos__[22] = ("negro", 1)  # punto 23
        
        result = self.ui._PygameUI__has_valid_bearing_off_moves()
        self.assertTrue(result)
    
    def test_has_valid_bearing_off_moves_false(self):
        """Verifica cuando no hay movimientos válidos de bearing off.
        
        Principio DIP: La UI coordina, preguntando al Validator
        (caso negativo).
        """
        self.ui.__current_player__ = "negro"
        self.ui.__available_moves__ = [1, 2]
        
        # Limpiar tablero
        for i in range(24):
            self.board.__puntos__[i] = (None, 0)
        self.board.__puntos__[18] = ("negro", 1)  # punto 19 (necesita dado 6)
        
        result = self.ui._PygameUI__has_valid_bearing_off_moves()
        self.assertFalse(result)

    def test_attempt_bearing_off_success(self):
        """Verifica ejecución exitosa de bearing off.
        
        Principio DIP: La UI (alto nivel) orquesta el 'bearing off',
        dependiendo de las abstracciones (Board, HomeManager, Validator)
        para ejecutar y validar el estado.
        """
        self.ui.__current_player__ = "negro"
        self.ui.__available_moves__ = [2]
        self.ui.__selected_point__ = 23
        
        # Limpiar tablero - remover todas las fichas existentes
        for i in range(1, 25):
            estado = self.board.obtener_estado_punto(i)
            if estado:
                color, cantidad = estado
                try:
                    self.board.remover_ficha(i, cantidad)
                except:
                    pass
        
        # Colocar ficha en punto 23
        self.board.colocar_ficha(23, "negro", 1)
        
        # Ejecutar
        self.ui._PygameUI__attempt_bearing_off(23, 25)
        
        # Verificar
        self.assertEqual(self.home_manager.get_pieces_count("negro"), 1)
        self.assertEqual(len(self.ui.__available_moves__), 0)

    def test_attempt_bearing_off_victory(self):
        """Verifica detección de victoria al completar bearing off.
        
        Principio DIP: La UI orquesta el movimiento y depende de
        HomeManager para detectar la condición de victoria.
        """
        self.ui.__current_player__ = "negro"
        self.ui.__available_moves__ = [1]
        
        # 14 fichas ya en casa
        for _ in range(14):
            self.home_manager.add_piece_to_home("negro")
        
        # Limpiar tablero - remover todas las fichas existentes
        for i in range(1, 25):
            estado = self.board.obtener_estado_punto(i)
            if estado:
                color, cantidad = estado
                try:
                    self.board.remover_ficha(i, cantidad)
                except:
                    pass
        
        # Colocar última ficha en punto 24
        self.board.colocar_ficha(24, "negro", 1)
        
        # Ejecutar bearing off
        self.ui._PygameUI__attempt_bearing_off(24, 25)
        
        # Verificar victoria
        self.assertTrue(self.home_manager.has_won("negro"))
        self.assertIn("GANA", self.ui.__message__)
        
    # DENTRO de TestBearingOffFunctionality
    def test_attempt_bearing_off_higher_dice_succeeds(self):
        """Verifica que sacar con dado mayor (sin fichas atrás) es exitoso."""
        self.ui.__current_player__ = "negro"
        self.ui.__available_moves__ = [3, 5]

        # --- CORRECCIÓN SETUP ---
        # Limpiar tablero usando métodos públicos (más seguro)
        for i in range(1, 25):
            estado = self.board.obtener_estado_punto(i)
            if estado and estado[1] > 0:
                try:
                    # Intenta remover todas las fichas del punto
                    self.board.remover_ficha(i, estado[1])
                except ValueError:
                     # Ignora errores si el punto ya estaba vacío o tenía menos fichas
                     pass # Asegura que el tablero esté limpio para el test

        # Colocar ficha usando método público
        self.board.colocar_ficha(23, "negro", 1)
        # --- FIN CORRECCIÓN SETUP ---

        # Aseguramos que can_bear_off devuelva True
        with patch.object(self.ui.__bearing_off_validator__, 'can_bear_off', return_value=True):
            # Mockear los métodos que podrían fallar dentro del try block
            with patch.object(self.ui.__movement_validator__, 'has_any_valid_move', return_value=True), \
                 patch.object(self.ui, '_PygameUI__has_valid_bearing_off_moves', return_value=True):
                 self.ui._PygameUI__attempt_bearing_off(23, 25)

        # Verificar que el movimiento fue EXITOSO usando el dado 3
        self.assertNotIn("Necesitas dado", self.ui.__message__, "No debería pedir dado exacto si uno mayor es válido")
        # Hacemos la comprobación del mensaje de éxito un poco más robusta
        self.assertTrue(
            "Ficha sacada" in self.ui.__message__ or "¡Sacaste 1!" in self.ui.__message__,
             f"Debería mostrar mensaje de éxito, pero mostró: '{self.ui.__message__}'"
        )
        # Verificar que se usó el dado 3 y queda el 5
        self.assertEqual(len(self.ui.__available_moves__), 1)
        self.assertEqual(self.ui.__available_moves__[0], 5)
        self.assertNotIn(3, self.ui.__available_moves__)
        # Verificar estado del juego
        self.assertEqual(self.ui.__home_manager__.get_pieces_count("negro"), 1)
        # Verificar usando método público
        estado_punto_23 = self.board.obtener_estado_punto(23)
        self.assertIsNone(estado_punto_23, "El punto 23 debería estar vacío")
    
    def test_attempt_bearing_off_pieces_outside_home(self):
        """Verifica rechazo cuando tiene fichas fuera de home.
        
        Principio DIP: La UI delega la validación de "todas las
        fichas en casa" al BearingOffValidator.
        """
        self.ui.__current_player__ = "negro"
        self.ui.__available_moves__ = [2]
        
        # Limpiar tablero
        for i in range(24):
            self.board.__puntos__[i] = (None, 0)
        self.board.__puntos__[22] = ("negro", 1)  # punto 23
        self.board.__puntos__[12] = ("negro", 1)  # punto 13 (fuera)
        
        self.ui._PygameUI__attempt_bearing_off(23, 25)
        
        self.assertIn("fuera del cuadrante casa", self.ui.__message__)

    # --- Tests de mensajes ---
    
    def test_attempt_piece_selection_bearing_off_message(self):
        """Verifica mensaje cuando puede sacar ficha.
        
        Principio SRP: Verifica la responsabilidad de la UI de mostrar
        el mensaje correcto al usuario según el estado (puede sacar ficha).
        """
        self.ui.__current_player__ = "negro"
        self.ui.__available_moves__ = [2]
        self.ui.__game_state_manager__.change_state('AWAITING_PIECE_SELECTION')
        
        # Limpiar tablero
        for i in range(24):
            self.board.__puntos__[i] = (None, 0)
        self.board.__puntos__[22] = ("negro", 1)  # punto 23
        
        self.ui._PygameUI__attempt_piece_selection(23)
        
        self.assertIn("sacar", self.ui.__message__.lower())
        self.assertIn("CASA", self.ui.__message__)
    
    def test_attempt_piece_selection_no_bearing_off_message(self):
        """Verifica mensaje normal cuando no puede sacar.
        
        Principio SRP: Verifica la responsabilidad de la UI de mostrar
        el mensaje correcto al usuario (movimiento normal).
        """
        self.ui.__current_player__ = "negro"
        self.ui.__available_moves__ = [1]
        self.ui.__game_state_manager__.change_state('AWAITING_PIECE_SELECTION')
        
        # Limpiar tablero
        for i in range(24):
            self.board.__puntos__[i] = (None, 0)
        self.board.__puntos__[18] = ("negro", 1)  # punto 19
        
        self.ui._PygameUI__attempt_piece_selection(19)
        
        self.assertIn("seleccionado", self.ui.__message__.lower())
        self.assertNotIn("sacar", self.ui.__message__.lower())
    
    def test_bearing_off_with_remaining_moves(self):
        """Verifica que después de sacar una ficha, el turno continúa si quedan dados.
        
        Principio LSP: El estado de la UI (dados disponibles) se actualiza
        correctamente y de forma consistente tras un movimiento de 'bearing off'.
        """
        self.ui.__current_player__ = "negro"
        self.ui.__available_moves__ = [2, 5]
        
        # Limpiar tablero - remover todas las fichas existentes
        for i in range(1, 25):
            estado = self.board.obtener_estado_punto(i)
            if estado:
                color, cantidad = estado
                try:
                    self.board.remover_ficha(i, cantidad)
                except:
                    pass
        
        # Colocar 2 fichas en punto 23
        self.board.colocar_ficha(23, "negro", 2)
        
        # Ejecutar bearing off (usará el dado 2)
        self.ui._PygameUI__attempt_bearing_off(23, 25)
        
        # Verificar: debe quedar 1 dado (el 5)
        self.assertEqual(len(self.ui.__available_moves__), 1)
        self.assertEqual(self.ui.__available_moves__[0], 5)
        self.assertIn("sacada", self.ui.__message__.lower())


# --- TESTS PARA VALIDACIÓN DE DOBLES ---
class TestDoublesValidation(unittest.TestCase):
    """
    Suite de tests específica para validar la lógica de dobles en el Backgammon.
    
    Principios SOLID verificados:
        - LSP: El sistema maneja de forma consistente un estado
          especial (dobles) vs. un estado normal, alterando
          correctamente el número de movimientos.
        - DIP: La UI depende de DiceMovesCalculator (o Dice)
          para determinar si es un doble y cuántos movimientos generar.
    """
    def setUp(self):
        """Configura el entorno de test sin interfaz gráfica.
        
        Principio SRP: Aísla la configuración del test.
        """
        with patch('pygame.init'), \
             patch('pygame.display.set_mode'), \
             patch('pygame.font.Font'):
            self.ui = PygameUI()

    @patch('Backgammon.Core.Dice.Dice.tirar')
    @patch('Backgammon.Core.Dice.Dice.obtener_dado1')
    @patch('Backgammon.Core.Dice.Dice.obtener_dado2')
    def test_roll_doubles_generates_four_moves(self, mock_dado2, mock_dado1, mock_tirar):
        """Verifica que al sacar dobles se generen 4 movimientos del mismo valor.
        
        Principio LSP: El método __roll_player_dice se comporta
        correctamente (genera 4 movimientos) bajo la condición de 'dobles'.
        """
        mock_dado1.return_value = 3
        mock_dado2.return_value = 3
        self.ui.__current_player__ = "negro"
        self.ui._PygameUI__roll_player_dice()
        self.assertEqual(self.ui.__available_moves__, [3, 3, 3, 3])
        self.assertTrue(self.ui.__is_doubles_roll__)

    @patch('Backgammon.Core.Dice.Dice.tirar')
    @patch('Backgammon.Core.Dice.Dice.obtener_dado1')
    @patch('Backgammon.Core.Dice.Dice.obtener_dado2')
    def test_roll_normal_generates_two_moves(self, mock_dado2, mock_dado1, mock_tirar):
        """Verifica que al sacar dados normales se generen 2 movimientos.
        
        Principio LSP: El método __roll_player_dice se comporta
        correctamente (genera 2 movimientos) bajo una tirada normal.
        """
        mock_dado1.return_value = 2
        mock_dado2.return_value = 5
        self.ui.__current_player__ = "negro"
        self.ui._PygameUI__roll_player_dice()
        self.assertCountEqual(self.ui.__available_moves__, [2, 5])
        self.assertFalse(self.ui.__is_doubles_roll__)

    def test_execute_move_removes_one_die_from_doubles(self):
        """Verifica que al ejecutar un movimiento con dobles se remueva solo un dado.
        
        Principio LSP: El método __execute_move actualiza el estado de
        los dados disponibles de forma consistente con las reglas de 'dobles'.
        """
        self.ui.__current_player__ = "negro"
        self.ui.__available_moves__ = [4, 4, 4, 4]
        self.ui.__is_doubles_roll__ = True
        self.ui.__board__.colocar_ficha(1, "negro", 1)
        self.ui._PygameUI__execute_move(1, 5)
        self.assertEqual(self.ui.__available_moves__, [4, 4, 4])

    def test_complete_all_doubles_moves_ends_turn(self):
        """Verifica que usar todos los movimientos de dobles termine el turno.
        
        Principio LSP: El sistema maneja correctamente la transición de estado
        (fin de turno) al consumir el último movimiento de 'dobles'.
        """
        self.ui.__current_player__ = "negro"
        self.ui.__available_moves__ = [6]
        self.ui.__is_doubles_roll__ = True
        self.ui.__board__.colocar_ficha(1, "negro", 1)
        self.ui._PygameUI__execute_move(1, 7)
        self.assertEqual(self.ui.__current_player__, "blanco")
        self.assertFalse(self.ui.__is_doubles_roll__)
        self.assertEqual(self.ui.__game_state_manager__.get_current_state(), "AWAITING_ROLL")

    def test_validate_doubles_move_with_available_die(self):
        """Verifica que se pueda validar un movimiento cuando el dado está disponible en dobles.
        
        Principio LSP: El método de validación (__validate_and_report_move)
        funciona consistentemente con una lista de dados de 'dobles'.
        """
        self.ui.__current_player__ = "negro"
        self.ui.__available_moves__ = [5, 5, 5, 5]
        # Colocamos una ficha en el punto 2 (que está vacío por defecto)
        self.ui.__board__.colocar_ficha(2, "negro", 1)
        # El destino es el punto 7 (2 + 5), que también está vacío por defecto.
        # Esto representa el movimiento más simple y válido posible.
        result = self.ui._PygameUI__validate_and_report_move(2, 7)
        self.assertTrue(result)

    def test_validate_doubles_move_without_available_die(self):
        """Verifica que se rechace un movimiento cuando el dado no está disponible en dobles.
        
        Principio LSP: El método de validación (__validate_and_report_move)
        falla correctamente cuando el dado no está en la lista de 'dobles'.
        """
        self.ui.__current_player__ = "negro"
        self.ui.__available_moves__ = [3, 3, 3, 3]
        result = self.ui._PygameUI__validate_and_report_move(1, 6)
        self.assertFalse(result)
        self.assertIn("No tienes dado 5", self.ui.__message__)



# --- TESTS PARA VALIDACIÓN DE MOVIMIENTOS ---
class TestMovementValidator(unittest.TestCase):
    """Pruebas para la clase MovementValidator.
    
    Principios SOLID verificados:
        - SRP: Verifica la responsabilidad única de MovementValidator
          de determinar si existen movimientos válidos.
        - DIP: La UI depende de esta abstracción para saber si
          debe saltar un turno, en lugar de calcularlo ella misma.
    """

    def setUp(self):
        """
        Prepara el entorno para cada test, accediendo correctamente a los
        atributos internos del tablero.
        
        Principio SRP: Aísla la configuración del test, incluyendo la
        manipulación directa del estado del board para la prueba.
        """
        os.environ["SDL_VIDEODRIVER"] = "dummy"
        pygame.init()
        with patch('pygame.display.set_mode', return_value=pygame.Surface((1600, 900))), \
             patch('pygame.font.Font'):
            self.ui = PygameUI()
        
        self.board = self.ui.__board__
        self.bar_manager = self.ui.__bar_manager__
        self.validator = self.ui.__movement_validator__

        # **LA SOLUCIÓN CLAVE**: Accedemos al atributo __puntos__ directamente
        # para modificar la lista interna del tablero.
        self.board.__puntos__[:] = [(None, 0)] * 24
        self.bar_manager.bar = {"blanco": 0, "negro": 0}

    def test_has_no_valid_move_all_blocked(self):
        """Verifica que detecta cuando no hay movimientos válidos en un tablero controlado.
        
        Principio SRP: Prueba la lógica central de MovementValidator en un
        escenario donde no hay movimientos posibles.
        """
        # Colocamos las fichas directamente en la lista interna __puntos__.
        self.board.__puntos__[0] = ("negro", 1)
        self.board.__puntos__[3] = ("blanco", 2)
        self.board.__puntos__[5] = ("blanco", 2)
        
        # Ahora el test pasará porque el validador verá el tablero modificado
        # correctamente y no encontrará movimientos válidos.
        self.assertFalse(self.validator.has_any_valid_move("negro", [3, 5]))


# --- CLASE DE TESTS PARA LA FUNCIONALIDAD DE SALTAR TURNO ---
class TestSkipTurnFunctionality(unittest.TestCase):
    """Pruebas dedicadas a la lógica de saltar el turno.
    
    Principios SOLID verificados:
        - SRP: Verifica la responsabilidad de la UI de orquestar
          el flujo de "saltar turno" (cambiar estado, esperar confirmación).
        - DIP: La UI depende de MovementValidator (Mockeado) para
          tomar la decisión de iniciar el flujo de "saltar turno".
    """

    def setUp(self):
        """Configuración para cada test de esta clase.
        
        Principio SRP: Aísla la configuración del test.
        """
        os.environ["SDL_VIDEODRIVER"] = "dummy"
        pygame.init()
        with patch('pygame.display.set_mode', return_value=pygame.Surface((1600, 900))), \
             patch('pygame.font.Font'):
            self.ui = PygameUI()

    @patch('Backgammon.Interfaces.PygameUI.MovementValidator.has_any_valid_move', return_value=False)
    @patch('Backgammon.Interfaces.PygameUI.Dice')
    def test_skip_turn_when_no_moves_available(self, MockDice, mock_has_move):
        """Verifica que el estado cambia a confirmación si no hay movimientos después de tirar.
        
        Principio DIP: La UI (__handle_roll_request) depende de
        MovementValidator (Mockeado) para decidir el siguiente estado.
        """
        mock_dice_instance = MockDice.return_value
        mock_dice_instance.obtener_dado1.return_value = 1
        mock_dice_instance.obtener_dado2.return_value = 2

        self.ui.__current_player__ = "negro"
        self.ui.__game_state_manager__.change_state('AWAITING_ROLL')
        
        self.ui._PygameUI__handle_roll_request()
        
        self.assertEqual(self.ui.__game_state_manager__.get_current_state(), 'AWAITING_SKIP_CONFIRMATION')

    @patch('pygame.event.get')
    def test_skip_turn_confirmation_ends_turn(self, mock_event_get):
        """Verifica que confirmar el salto de turno cambia al siguiente jugador.
        
        Principio SRP: Prueba la responsabilidad de __handle_events de manejar
        la entrada del usuario para confirmar el salto de turno.
        """
        self.ui.__current_player__ = "negro"
        self.ui.__game_state_manager__.change_state('AWAITING_SKIP_CONFIRMATION')

        mock_event_get.return_value = [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_r)]
        self.ui._PygameUI__handle_events()

        self.assertEqual(self.ui.__current_player__, "blanco")
        self.assertEqual(self.ui.__game_state_manager__.get_current_state(), 'AWAITING_ROLL')


# --- CLASE DE TESTS DE INTEGRACIÓN ---
class TestIntegrationSkipTurn(unittest.TestCase):
    """Tests de integración que simulan un escenario completo.
    
    Principios SOLID verificados:
        - DIP: La UI interactúa con las abstracciones (Mocks)
          de Validator y Dice para completar un flujo de juego.
        - LSP: El sistema transiciona consistentemente entre
          estados (AWAITING_ROLL -> AWAITING_SKIP_CONFIRMATION -> AWAITING_ROLL).
    """

    def setUp(self):
        """Configuración para cada test de esta clase.
        
        Principio SRP: Aísla la configuración del test.
        """
        os.environ["SDL_VIDEODRIVER"] = "dummy"
        pygame.init()
        with patch('pygame.display.set_mode', return_value=pygame.Surface((1600, 900))), \
             patch('pygame.font.Font'):
            self.ui = PygameUI()

    @patch('Backgammon.Interfaces.PygameUI.MovementValidator.has_any_valid_move', return_value=False)
    @patch('Backgammon.Interfaces.PygameUI.Dice')
    @patch('pygame.event.get')
    def test_complete_skip_turn_scenario(self, mock_event_get, MockDice, mock_has_move):
        """Test completo: tirar dados, no poder mover, confirmar, cambiar turno.
        
        Principio LSP: Prueba la robustez y consistencia del manejador de
        estados a través de un ciclo completo de "saltar turno".
        """
        mock_dice_instance = MockDice.return_value
        mock_dice_instance.obtener_dado1.return_value = 2
        mock_dice_instance.obtener_dado2.return_value = 5

        self.ui.__current_player__ = "negro"
        self.ui.__game_state_manager__.change_state('AWAITING_ROLL')

        mock_event_get.return_value = [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_r)]
        self.ui._PygameUI__handle_events()
        
        self.assertEqual(self.ui.__game_state_manager__.get_current_state(), 'AWAITING_SKIP_CONFIRMATION')

        self.ui._PygameUI__handle_events()

        self.assertEqual(self.ui.__current_player__, "blanco")
        self.assertEqual(self.ui.__game_state_manager__.get_current_state(), 'AWAITING_ROLL')

    @patch('Backgammon.Interfaces.PygameUI.MovementValidator.has_any_valid_move', return_value=False)
    @patch('Backgammon.Interfaces.PygameUI.Dice')
    @patch('pygame.event.get')
    def test_both_players_skip_turn_scenario(self, mock_event_get, MockDice, mock_has_move):
        """Test donde ambos jugadores deben saltar turno consecutivamente.
        
        Principio LSP: Prueba la consistencia del manejador de estados
        al manejar el flujo de "saltar turno" para ambos jugadores.
        """
        mock_dice_instance = MockDice.return_value
        
        self.ui.__current_player__ = "negro"
        self.ui.__game_state_manager__.change_state('AWAITING_ROLL')
        mock_dice_instance.obtener_dado1.return_value = 1
        mock_dice_instance.obtener_dado2.return_value = 1

        mock_event_get.return_value = [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_r)]
        self.ui._PygameUI__handle_events()
        self.ui._PygameUI__handle_events()

        self.assertEqual(self.ui.__current_player__, "blanco")

        mock_dice_instance.obtener_dado1.return_value = 6
        mock_dice_instance.obtener_dado2.return_value = 6
        
        self.ui._PygameUI__handle_events()
        self.ui._PygameUI__handle_events()
        
        self.assertEqual(self.ui.__current_player__, "negro")
        self.assertEqual(self.ui.__game_state_manager__.get_current_state(), 'AWAITING_ROLL')


# --- CLASE DE TESTS PARA GameStateManager ---
class TestGameStateManagerSkipConfirmation(unittest.TestCase):
    """
    Pruebas para GameStateManager, enfocadas en el estado de confirmación de salto.
    
    Principios SOLID verificados:
        - SRP: Verifica que GameStateManager maneja correctamente
          la transición hacia y desde el estado AWAITING_SKIP_CONFIRMATION.
    """
    
    def setUp(self):
        """Configuración para cada test de esta clase.
        
        Principio SRP: Aísla la configuración del test.
        """
        os.environ["SDL_VIDEODRIVER"] = "dummy"
        pygame.init()
        with patch('pygame.display.set_mode', return_value=pygame.Surface((1600, 900))), \
             patch('pygame.font.Font'):
            self.ui = PygameUI()

    @patch('Backgammon.Interfaces.PygameUI.MovementValidator.has_any_valid_move', return_value=False)
    @patch('Backgammon.Interfaces.PygameUI.Dice')
    @patch('pygame.event.get')
    def test_both_players_skip_turn_scenario(self, mock_event_get, MockDice, mock_has_move):
        """Test donde ambos jugadores deben saltar turno consecutivamente.
        
        Principio LSP: Verifica la consistencia del GameStateManager al
        manejar el estado AWAITING_SKIP_CONFIRMATION
        múltiples veces seguidas.
        """
        mock_dice_instance = MockDice.return_value
        
        self.ui.__current_player__ = "negro"
        self.ui.__game_state_manager__.change_state('AWAITING_ROLL')
        mock_dice_instance.obtener_dado1.return_value = 1
        mock_dice_instance.obtener_dado2.return_value = 1

        mock_event_get.return_value = [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_r)]
        self.ui._PygameUI__handle_events()
        self.assertEqual(self.ui.__game_state_manager__.get_current_state(), 'AWAITING_SKIP_CONFIRMATION')
        self.ui._PygameUI__handle_events()
        self.assertEqual(self.ui.__current_player__, "blanco")

        mock_dice_instance.obtener_dado1.return_value = 6
        mock_dice_instance.obtener_dado2.return_value = 6
        
        self.ui._PygameUI__handle_events()
        self.assertEqual(self.ui.__game_state_manager__.get_current_state(), 'AWAITING_SKIP_CONFIRMATION')
        self.ui._PygameUI__handle_events()
        self.assertEqual(self.ui.__current_player__, "negro")
        self.assertEqual(self.ui.__game_state_manager__.get_current_state(), 'AWAITING_ROLL')


# --- TESTS DE PRINCIPIOS SOLID ---
class TestSOLIDPrinciples(unittest.TestCase):
    """
    Suite de tests específicamente diseñada para verificar el cumplimiento
    de los principios SOLID en la arquitectura de PygameUI.
    Esto es clave para demostrar buena orientación a objetos.
    """

    def setUp(self):
        """Configura el entorno sin interfaz gráfica.
        
        Principio SRP: Aísla la configuración del test.
        """
        with patch('pygame.init'), \
             patch('pygame.display.set_mode'), \
             patch('pygame.font.Font'):
            self.ui = PygameUI()

    # --- SINGLE RESPONSIBILITY PRINCIPLE (SRP) TESTS ---
    def test_srp_dice_calculator_only_handles_dice_logic(self):
        """
        [SRP] Verifica que DiceMovesCalculator solo maneja lógica de dados.
        SRP: Una clase debe tener una sola razón para cambiar.
        """
        # Test directo de la clase DiceMovesCalculator
        moves_normal = DiceMovesCalculator.calculate_available_moves(2, 5)
        moves_doubles = DiceMovesCalculator.calculate_available_moves(3, 3)
        is_doubles = DiceMovesCalculator.is_doubles_roll(3, 3)
        is_not_doubles = DiceMovesCalculator.is_doubles_roll(2, 5)

        self.assertEqual(moves_normal, [2, 5])
        self.assertEqual(moves_doubles, [3, 3, 3, 3])
        self.assertTrue(is_doubles)
        self.assertFalse(is_not_doubles)

    def test_srp_game_state_manager_only_handles_states(self):
        """
        [SRP] Verifica que GameStateManager solo maneja estados del juego.
        """
        manager = GameStateManager()

        # Verificar funcionamiento básico
        initial_state = manager.get_current_state()
        self.assertEqual(initial_state, 'START_ROLL')

        manager.change_state('AWAITING_ROLL')
        new_state = manager.get_current_state()
        self.assertEqual(new_state, 'AWAITING_ROLL')

        # Verificar validación
        with self.assertRaises(ValueError):
            manager.change_state('INVALID_STATE')

    def test_srp_message_manager_only_handles_messages(self):
        """
        [SRP] Verifica que MessageManager solo maneja generación de mensajes.
        """
        start_msg = MessageManager.get_start_message()
        doubles_msg = MessageManager.get_doubles_roll_message("negro", 4, [4, 4, 4, 4])
        normal_msg = MessageManager.get_normal_roll_message("blanco", [2, 6])

        self.assertIsInstance(start_msg, str)
        self.assertIsInstance(doubles_msg, str)
        self.assertIsInstance(normal_msg, str)
        # Cambiar de "DOBLES" a "dobles"
        self.assertIn("dobles", doubles_msg)
        self.assertIn("Presiona", start_msg)


    # --- OPEN/CLOSED PRINCIPLE (OCP) TESTS ---
    def test_ocp_game_state_manager_extensible_for_new_states(self):
        """
        [OCP] Verifica que GameStateManager sea extensible para nuevos estados
        sin modificar código existente.
        """
        manager = GameStateManager()
        current_states = manager.valid_states.copy()

        # Simular extensión
        manager.valid_states.add('NEW_GAME_STATE')
        manager.change_state('NEW_GAME_STATE')
        self.assertEqual(manager.get_current_state(), 'NEW_GAME_STATE')

        # Restaurar para no afectar otros tests
        manager.valid_states = current_states

    def test_ocp_dice_calculator_extensible_for_new_rules(self):
        """
        [OCP] Verifica que DiceMovesCalculator sea extensible para nuevas reglas
        sin modificar métodos existentes.
        """
        # Los métodos estáticos son extensibles por naturaleza
        result_normal = DiceMovesCalculator.calculate_available_moves(2, 5)
        result_doubles = DiceMovesCalculator.calculate_available_moves(3, 3)

        # Los resultados son predecibles
        self.assertEqual(result_normal, [2, 5])
        self.assertEqual(result_doubles, [3, 3, 3, 3])

        # Se pueden crear nuevas funciones sin modificar las existentes
        self.assertTrue(callable(DiceMovesCalculator.calculate_available_moves))
        self.assertTrue(callable(DiceMovesCalculator.is_doubles_roll))

    # --- DEPENDENCY INVERSION PRINCIPLE (DIP) TESTS ---
    def test_dip_pygame_ui_uses_manager_classes(self):
        """
        [DIP] Verifica que PygameUI usa las clases gestoras.
        """
        # Test indirecto: verificar que PygameUI puede usar las funcionalidades
        # sin verificar directamente los atributos privados problemáticos

        # Verificar que los gestores funcionan independientemente
        dice_calc = DiceMovesCalculator()
        state_mgr = GameStateManager()
        msg_mgr = MessageManager()

        # Test de funcionalidad
        moves = dice_calc.calculate_available_moves(5, 5)
        state = state_mgr.get_current_state()
        message = msg_mgr.get_start_message()

        self.assertEqual(moves, [5, 5, 5, 5])
        self.assertEqual(state, 'START_ROLL')
        self.assertIn("Presiona", message)

    def test_dip_classes_work_independently(self):
        """
        [DIP] Verifica que las clases gestoras funcionan independientemente.
        """
        # Test de DiceMovesCalculator independiente
        moves = DiceMovesCalculator.calculate_available_moves(5, 5)
        self.assertEqual(moves, [5, 5, 5, 5])

        # Test de GameStateManager independiente
        manager = GameStateManager()
        manager.change_state('AWAITING_ROLL')
        self.assertEqual(manager.get_current_state(), 'AWAITING_ROLL')

        # Test de MessageManager independiente
        message = MessageManager.get_doubles_roll_message("negro", 5, moves)
        # Cambiar de "DOBLES" a "dobles"
        self.assertIn("dobles", message)


    # --- INTEGRATION TEST FOR SOLID PRINCIPLES ---
    def test_solid_integration_all_principles_work_together(self):
        """
        [SOLID] Test de integración que verifica que todos los principios SOLID
        trabajen juntos correctamente.
        """
        # SRP: Cada clase maneja su responsabilidad específica
        dice_moves = DiceMovesCalculator.calculate_available_moves(5, 5)
        game_state = GameStateManager()
        message = MessageManager.get_doubles_roll_message("negro", 5, dice_moves)

        # OCP: Las clases son extensibles
        self.assertEqual(dice_moves, [5, 5, 5, 5])
        self.assertEqual(game_state.get_current_state(), 'START_ROLL')

        # DIP: Las abstracciones funcionan independientemente
        # Cambiar de "DOBLES" a "dobles"
        self.assertIn("dobles", message)
        self.assertIn("5", message)

        # ISP: Interfaces específicas
        self.assertTrue(callable(DiceMovesCalculator.calculate_available_moves))
        self.assertTrue(callable(game_state.change_state))
        self.assertTrue(callable(MessageManager.get_start_message))

        # Todo funciona en conjunto
        self.assertIsInstance(dice_moves, list)
        self.assertIsInstance(message, str)
        self.assertIsInstance(game_state.get_current_state(), str)

    def test_solid_architecture_separation_of_concerns(self):
        """
        [SRP] Verifica que la arquitectura mantenga separación de responsabilidades.
        """
        # DiceMovesCalculator: Solo cálculos de dados
        self.assertEqual(DiceMovesCalculator.calculate_available_moves(1, 1), [1, 1, 1, 1])
        self.assertEqual(DiceMovesCalculator.calculate_available_moves(2, 4), [2, 4])

        # GameStateManager: Solo manejo de estados
        state_manager = GameStateManager()
        self.assertEqual(state_manager.get_current_state(), 'START_ROLL')
        state_manager.change_state('AWAITING_ROLL')
        self.assertEqual(state_manager.get_current_state(), 'AWAITING_ROLL')

        # MessageManager: Solo generación de mensajes
        msg1 = MessageManager.get_start_message()
        msg2 = MessageManager.get_doubles_roll_message("blanco", 6, [6, 6, 6, 6])

        self.assertNotEqual(msg1, msg2)
        self.assertIn("Presiona", msg1)
        # Cambiar de "DOBLES" a "dobles"
        self.assertIn("dobles", msg2)
        self.assertIn("blanco", msg2.lower())


# --- TESTS PARA DICE MOVES CALCULATOR ---
class TestDiceMovesCalculator(unittest.TestCase):
    """
    Tests unitarios para la clase DiceMovesCalculator.
    Verifica el cumplimiento del principio SRP.
    
    Principios SOLID verificados:
        - SRP: La clase DiceMovesCalculator solo tiene la
          responsabilidad de lógica relacionada con los dados
          (cálculo de movimientos, detección de dobles).
    """

    def test_calculate_normal_moves(self):
        """Verifica el cálculo correcto para dados normales.
        
        Principio SRP: Prueba una responsabilidad específica (cálculo
        de movimientos normales) de la clase.
        """
        moves = DiceMovesCalculator.calculate_available_moves(2, 5)
        self.assertEqual(moves, [2, 5])

    def test_calculate_doubles_moves(self):
        """Verifica el cálculo correcto para dobles.
        
        Principio SRP: Prueba una responsabilidad específica (cálculo
        de movimientos dobles) de la clase.
        """
        moves = DiceMovesCalculator.calculate_available_moves(4, 4)
        self.assertEqual(moves, [4, 4, 4, 4])

    def test_is_doubles_roll_true(self):
        """Verifica detección correcta de dobles.
        
        Principio SRP: Prueba una responsabilidad específica (detección
        de dobles) de la clase.
        """
        result = DiceMovesCalculator.is_doubles_roll(6, 6)
        self.assertTrue(result)

    def test_is_doubles_roll_false(self):
        """Verifica detección correcta de no-dobles.
        
        Principio SRP: Prueba una responsabilidad específica (detección
        de no-dobles) de la clase.
        """
        result = DiceMovesCalculator.is_doubles_roll(3, 5)
        self.assertFalse(result)

    def test_edge_cases_doubles(self):
        """Verifica casos extremos para dobles.
        
        Principio LSP: Verifica que la lógica de dobles es consistente
        para todos los valores posibles (1-6).
        """
        # Todos los valores posibles de dobles
        for i in range(1, 7):
            moves = DiceMovesCalculator.calculate_available_moves(i, i)
            self.assertEqual(moves, [i, i, i, i])
            self.assertTrue(DiceMovesCalculator.is_doubles_roll(i, i))



# --- TESTS PARA GAME STATE MANAGER ---
class TestGameStateManager(unittest.TestCase):
    """
    Tests unitarios para la clase GameStateManager.
    Verifica el cumplimiento del principio SRP y validación de estados.
    
    Principios SOLID verificados:
        - SRP: La clase GameStateManager solo tiene la responsabilidad
          de gestionar y validar el estado actual del juego.
    """

    def setUp(self):
        """Configura un GameStateManager para cada test.
        
        Principio SRP: Aísla la instancia del manager para cada test.
        """
        self.manager = GameStateManager()

    def test_initial_state(self):
        """Verifica que el estado inicial sea correcto.
        
        Principio SRP: Prueba una responsabilidad específica (estado inicial)
        del GameStateManager.
        """
        self.assertEqual(self.manager.get_current_state(), 'START_ROLL')

    def test_valid_state_changes(self):
        """Verifica que los cambios de estado válidos funcionen.
        
        Principio SRP: Prueba la responsabilidad de cambiar y reportar
        estados válidos.
        """
        valid_states = ['START_ROLL', 'AWAITING_ROLL', 'AWAITING_PIECE_SELECTION']

        for state in valid_states:
            self.manager.change_state(state)
            self.assertEqual(self.manager.get_current_state(), state)

    def test_invalid_state_change_raises_error(self):
        """Verifica que estados inválidos generen error.
        
        Principio LSP: El manager maneja consistentemente una entrada
        inválida (lanzando una excepción).
        """
        with self.assertRaises(ValueError):
            self.manager.change_state('INVALID_STATE')

    def test_state_persistence(self):
        """Verifica que el estado se mantenga hasta el próximo cambio.
        
        Principio SRP: Prueba que el manager mantiene correctamente
        el estado interno.
        """
        self.manager.change_state('AWAITING_ROLL')
        self.assertEqual(self.manager.get_current_state(), 'AWAITING_ROLL')

        # Verificar que no cambia automáticamente
        self.assertEqual(self.manager.get_current_state(), 'AWAITING_ROLL')



# --- TESTS PARA MESSAGE MANAGER ---
class TestMessageManager(unittest.TestCase):
    """
    Tests unitarios para la clase MessageManager.
    Verifica el cumplimiento del principio SRP para generación de mensajes.
    
    Principios SOLID verificados:
        - SRP: La clase MessageManager solo tiene la responsabilidad
          de crear strings de mensajes para el usuario.
    """

    def test_start_message(self):
        """Verifica el mensaje de inicio.
        
        Principio SRP: Prueba la generación de un mensaje específico,
        confirmando la responsabilidad única de la clase.
        """
        message = MessageManager.get_start_message()
        self.assertIn("Presiona 'R'", message)
        self.assertIn("empieza", message)

    def test_roll_winner_message_negro(self):
        """Verifica el mensaje cuando gana negro.
        
        Principio SRP: Prueba la generación de un mensaje específico.
        """
        message = MessageManager.get_roll_winner_message("negro", 5, 3)
        self.assertIn("Negro (5)", message)
        self.assertIn("Blanco (3)", message)
        self.assertIn("gana", message)

    def test_roll_winner_message_blanco(self):
        """Verifica el mensaje cuando gana blanco.
        
        Principio SRP: Prueba la generación de un mensaje específico.
        """
        message = MessageManager.get_roll_winner_message("blanco", 6, 2)
        self.assertIn("Blanco (6)", message)
        self.assertIn("Negro (2)", message)
        self.assertIn("gana", message)

    def test_doubles_roll_message(self):
        """Verifica el mensaje específico para dobles.
        
        Principio SRP: Prueba la generación de un mensaje específico.
        """
        message = MessageManager.get_doubles_roll_message("negro", 4, [4, 4, 4, 4])
        self.assertIn("dobles", message)
        self.assertIn("Negro", message)
        self.assertIn("4", message)
        self.assertIn("4 movimientos", message)

    def test_normal_roll_message(self):
        """Verifica el mensaje para tirada normal.
        
        Principio SRP: Prueba la generación de un mensaje específico.
        """
        message = MessageManager.get_normal_roll_message("blanco", [2, 6])
        self.assertIn("Turno de blanco", message)
        self.assertIn("[2, 6]", message)

    def test_move_completed_message_remaining(self):
        """Verifica mensaje cuando quedan movimientos.
        
        Principio SRP: Prueba la generación de un mensaje específico.
        """
        message = MessageManager.get_move_completed_message(2, [3, 5])
        self.assertIn("Te quedan 2 dados", message)
        self.assertIn("[3, 5]", message)

    def test_move_completed_message_finished(self):
        """Verifica mensaje cuando se completa el turno.
        
        Principio SRP: Prueba la generación de un mensaje específico.
        """
        message = MessageManager.get_move_completed_message(0, [])
        self.assertEqual(message, "Turno completado.")

    def test_dice_not_available_message(self):
        """Verifica mensaje cuando no se tiene el dado necesario.
        
        Principio SRP: Prueba la generación de un mensaje específico.
        """
        message = MessageManager.get_dice_not_available_message(4, [2, 6])
        self.assertIn("No tienes el dado 4 disponible", message)
        self.assertIn("[2, 6]", message)

class TestPygameUICoverageExtension(unittest.TestCase):
    """
    Tests adicionales para aumentar cobertura de PygameUI.
    Se enfoca en métodos y escenarios no cubiertos en los tests existentes.
    
    SOLID: SRP - Cada test verifica un aspecto específico de funcionalidad.
    """

    @classmethod
    def setUpClass(cls):
        """Configura entorno sin pantalla.
        
        Principio SRP: Centraliza la configuración de Pygame para la suite.
        """
        os.environ["SDL_VIDEODRIVER"] = "dummy"
        pygame.init()

    def setUp(self):
        """Crea instancia de PygameUI para cada test.
        
        Principio SRP: Aísla la instancia de UI para cada test.
        """
        with patch('pygame.display.set_mode', return_value=pygame.Surface((1600, 900))), \
             patch('pygame.font.Font'):
            self.ui = PygameUI()

    # --- Tests para BarManager ---

    def test_bar_manager_remove_piece_no_pieces(self):
        """Test que remove_piece_from_bar retorna False cuando no hay fichas.
        
        Principio SRP: Verifica una responsabilidad específica de BarManager
        (manejar la remoción de fichas cuando está vacía).
        """
        result = self.ui.__bar_manager__.remove_piece_from_bar("negro")
        self.assertFalse(result)

    def test_bar_manager_remove_piece_success(self):
        """Test que remove_piece_from_bar retorna True y remueve correctamente.
        
        Principio SRP: Verifica la responsabilidad de BarManager
        (manejar la remoción de fichas).
        """
        self.ui.__bar_manager__.add_piece_to_bar("negro")
        result = self.ui.__bar_manager__.remove_piece_from_bar("negro")
        self.assertTrue(result)
        self.assertEqual(self.ui.__bar_manager__.get_pieces_count("negro"), 0)

    def test_bar_manager_add_invalid_color(self):
        """Test que agregar color inválido genera error.
        
        Principio LSP: El BarManager maneja consistentemente una
        entrada inválida (lanzando excepción).
        """
        with self.assertRaises(ValueError):
            self.ui.__bar_manager__.add_piece_to_bar("rojo")

    def test_bar_manager_get_bar_state_returns_copy(self):
        """Test que get_bar_state retorna copia, no referencia.
        
        Principio SRP: Verifica que el manager protege su estado
        interno (encapsulación) al reportarlo.
        """
        self.ui.__bar_manager__.add_piece_to_bar("negro")
        state = self.ui.__bar_manager__.get_bar_state()
        state["negro"] = 999
        self.assertEqual(self.ui.__bar_manager__.get_pieces_count("negro"), 1)

    # --- Tests para CaptureValidator ---

    def test_capture_validator_can_capture_empty_point(self):
        """Test que can_capture_piece retorna False si punto vacío.
        
        Principio SRP: Verifica una responsabilidad específica de CaptureValidator
        (lógica de captura, caso vacío).
        """
        result = CaptureValidator.can_capture_piece(None, "negro")
        self.assertFalse(result)

    def test_capture_validator_can_capture_same_color(self):
        """Test que no puede capturar ficha del mismo color.
        
        Principio SRP: Verifica la lógica de captura (caso mismo color).
        """
        result = CaptureValidator.can_capture_piece(("negro", 1), "negro")
        self.assertFalse(result)

    def test_capture_validator_can_capture_single_opponent(self):
        """Test que puede capturar ficha solitaria del oponente.
        
        Principio SRP: Verifica la lógica de captura (caso captura válida).
        """
        result = CaptureValidator.can_capture_piece(("blanco", 1), "negro")
        self.assertTrue(result)

    def test_capture_validator_cannot_capture_multiple_opponents(self):
        """Test que no puede capturar múltiples fichas oponentes.
        
        Principio SRP: Verifica la lógica de captura (caso bloqueo).
        """
        result = CaptureValidator.can_capture_piece(("blanco", 2), "negro")
        self.assertFalse(result)

    def test_capture_validator_is_move_blocked_empty(self):
        """Test que punto vacío no está bloqueado.
        
        Principio SRP: Verifica la lógica de bloqueo (caso vacío).
        """
        result = CaptureValidator.is_move_blocked(None, "negro")
        self.assertFalse(result)

    def test_capture_validator_is_move_blocked_same_color(self):
        """Test que mismo color no bloquea.
        
        Principio SRP: Verifica la lógica de bloqueo (caso mismo color).
        """
        result = CaptureValidator.is_move_blocked(("negro", 5), "negro")
        self.assertFalse(result)

    def test_capture_validator_is_move_blocked_multiple_opponents(self):
        """Test que 2+ fichas oponentes bloquean.
        
        Principio SRP: Verifica la lógica de bloqueo (caso bloqueo real).
        """
        result = CaptureValidator.is_move_blocked(("blanco", 2), "negro")
        self.assertTrue(result)

    # --- Tests para BarMovementRules ---

    def test_bar_movement_rules_entry_point_negro(self):
        """Test cálculo de punto de entrada para negro.
        
        Principio SRP: Verifica una responsabilidad específica de BarMovementRules
        (cálculo de punto de entrada para 'negro').
        """
        self.assertEqual(BarMovementRules.get_entry_point("negro", 3), 3)
        self.assertEqual(BarMovementRules.get_entry_point("negro", 6), 6)

    def test_bar_movement_rules_entry_point_blanco(self):
        """Test cálculo de punto de entrada para blanco.
        
        Principio SRP: Verifica la lógica de entrada desde barra (para 'blanco').
        """
        self.assertEqual(BarMovementRules.get_entry_point("blanco", 3), 22)
        self.assertEqual(BarMovementRules.get_entry_point("blanco", 6), 19)

    def test_bar_movement_rules_must_enter_true(self):
        """Test que detecta cuando debe mover desde barra.
        
        Principio SRP: Verifica la lógica de "debe entrar" (caso positivo).
        """
        self.ui.__bar_manager__.add_piece_to_bar("negro")
        result = BarMovementRules.must_enter_from_bar_first(
            self.ui.__bar_manager__, "negro")
        self.assertTrue(result)

    def test_bar_movement_rules_must_enter_false(self):
        """Test que no requiere entrada cuando barra vacía.
        
        Principio SRP: Verifica la lógica de "debe entrar" (caso negativo).
        """
        result = BarMovementRules.must_enter_from_bar_first(
            self.ui.__bar_manager__, "negro")
        self.assertFalse(result)

    # --- Tests para métodos de PygameUI no cubiertos ---

    def test_switch_player_negro_to_blanco(self):
        """Test cambio de jugador negro a blanco.
        
        Principio SRP: Prueba la responsabilidad de __switch_player
        de alternar correctamente el jugador actual.
        """
        self.ui.__current_player__ = "negro"
        self.ui._PygameUI__switch_player()
        self.assertEqual(self.ui.__current_player__, "blanco")

    def test_switch_player_blanco_to_negro(self):
        """Test cambio de jugador blanco a negro.
        
        Principio SRP: Prueba la responsabilidad de __switch_player
        de alternar correctamente el jugador actual.
        """
        self.ui.__current_player__ = "blanco"
        self.ui._PygameUI__switch_player()
        self.assertEqual(self.ui.__current_player__, "negro")

    def test_calculate_dice_needed_from_bar_negro(self):
        """Test cálculo de dado desde barra para negro.
        
        Principio SRP: Verifica la responsabilidad de la UI de *calcular*
        el dado necesario para un movimiento (caso barra 'negro').
        """
        self.ui.__current_player__ = "negro"
        # Cuando origen es 0 (barra) y destino es 5, para negro el dado es simplemente el destino
        result = self.ui._PygameUI__calculate_dice_needed(0, 5)
        self.assertEqual(result, 5)

    def test_calculate_dice_needed_from_bar_blanco(self):
        """Test cálculo de dado desde barra para blanco.
        
        Principio SRP: Verifica el cálculo de dado necesario (caso barra 'blanco').
        """
        self.ui.__current_player__ = "blanco"
        # Para blanco desde barra: 25 - destino
        result = self.ui._PygameUI__calculate_dice_needed(0, 22)
        self.assertEqual(result, 3)

    def test_calculate_dice_needed_normal_move(self):
        """Test cálculo de dado para movimiento normal.
        
        Principio SRP: Verifica el cálculo de dado necesario (caso normal).
        """
        # Movimiento normal es abs(origen - destino)
        result = self.ui._PygameUI__calculate_dice_needed(5, 10)
        self.assertEqual(result, 5)

    def test_is_valid_direction_negro_forward(self):
        """Test que negro mueve hacia números mayores.
        
        Principio SRP: Prueba la responsabilidad de __is_valid_direction
        de validar la dirección del movimiento para 'negro' (válido).
        """
        self.ui.__current_player__ = "negro"
        # Negro va de menor a mayor (10 -> 15)
        result = self.ui._PygameUI__is_valid_direction(10, 15)
        self.assertTrue(result)

    def test_is_valid_direction_negro_backward_invalid(self):
        """Test que negro no puede mover hacia atrás.
        
        Principio SRP: Prueba la validación de dirección para 'negro' (inválido).
        """
        self.ui.__current_player__ = "negro"
        # Negro NO puede ir de mayor a menor (15 -> 10)
        result = self.ui._PygameUI__is_valid_direction(15, 10)
        self.assertFalse(result)

    def test_is_valid_direction_blanco_backward(self):
        """Test que blanco mueve hacia números menores.
        
        Principio SRP: Prueba la validación de dirección para 'blanco' (válido).
        """
        self.ui.__current_player__ = "blanco"
        # Blanco va de mayor a menor (20 -> 15)
        result = self.ui._PygameUI__is_valid_direction(20, 15)
        self.assertTrue(result)

    def test_is_valid_direction_blanco_forward_invalid(self):
        """Test que blanco no puede mover hacia adelante.
        
        Principio SRP: Prueba la validación de dirección para 'blanco' (inválido).
        """
        self.ui.__current_player__ = "blanco"
        # Blanco NO puede ir de menor a mayor (10 -> 15)
        result = self.ui._PygameUI__is_valid_direction(10, 15)
        self.assertFalse(result)

    def test_get_point_from_mouse_pos_outside_board(self):
        """Test que click fuera del tablero retorna None.
        
        Principio LSP: Verifica el comportamiento consistente de
        __get_point_from_mouse_pos en un caso límite (fuera del tablero).
        """
        result = self.ui._PygameUI__get_point_from_mouse_pos((10, 10))
        self.assertIsNone(result)

    def test_get_point_from_mouse_pos_bar_area(self):
        """Test que click en barra retorna 0.
        
        Principio LSP: Verifica el comportamiento consistente de
        __get_point_from_mouse_pos en un caso límite (barra).
        """
        result = self.ui._PygameUI__get_point_from_mouse_pos((790, 450))
        self.assertEqual(result, 0)

    def test_bearing_off_validator_get_destination_negro(self):
        """Test destino ficticio para bearing off negro.
        
        Principio SRP: Verifica una responsabilidad específica de
        BearingOffValidator (definir el destino de 'bearing off' para 'negro').
        """
        result = self.ui.__bearing_off_validator__.get_bearing_off_destination("negro")
        self.assertEqual(result, 25)

    def test_bearing_off_validator_get_destination_blanco(self):
        """Test destino ficticio para bearing off blanco.
        
        Principio SRP: Verifica la responsabilidad de BearingOffValidator
        (definir el destino de 'bearing off' para 'blanco').
        """
        result = self.ui.__bearing_off_validator__.get_bearing_off_destination("blanco")
        self.assertEqual(result, 0)

    def test_bearing_off_validator_is_bearing_off_move_negro(self):
        """Test detección de intento de bearing off para negro.
        
        Principio SRP: Verifica la responsabilidad de BearingOffValidator
        de identificar un movimiento como 'bearing off' (caso 'negro').
        """
        result = self.ui.__bearing_off_validator__.is_bearing_off_move("negro", 23, 26)
        self.assertTrue(result)

    def test_bearing_off_validator_is_bearing_off_move_blanco(self):
        """Test detección de intento de bearing off para blanco.
        
        Principio SRP: Verifica la identificación de 'bearing off' (caso 'blanco').
        """
        result = self.ui.__bearing_off_validator__.is_bearing_off_move("blanco", 2, 0)
        self.assertTrue(result)

    def test_bearing_off_validator_not_bearing_off_normal_move(self):
        """Test que movimiento normal no es bearing off.
        
        Principio SRP: Verifica la identificación de 'bearing off' (caso negativo).
        """
        result = self.ui.__bearing_off_validator__.is_bearing_off_move("negro", 10, 15)
        self.assertFalse(result)

    # --- Tests para execute_move con capturas ---

    def test_execute_move_with_capture(self):
        """Test ejecución de movimiento con captura.
        
        Principio DIP: La UI (__execute_move) orquesta el movimiento,
        delegando la lógica de captura al Board y BarManager.
        """
        self.ui.__current_player__ = "negro"
        self.ui.__available_moves__ = [5]
        
        # Limpiar tablero y configurar escenario
        for i in range(1, 25):
            try:
                estado = self.ui.__board__.obtener_estado_punto(i)
                if estado:
                    self.ui.__board__.remover_ficha(i, estado[1])
            except:
                pass
        
        self.ui.__board__.colocar_ficha(10, "negro", 1)
        self.ui.__board__.colocar_ficha(15, "blanco", 1)

        self.ui._PygameUI__execute_move(10, 15)

        self.assertEqual(self.ui.__bar_manager__.get_pieces_count("blanco"), 1)

    def test_execute_move_from_bar_to_board(self):
        """Test movimiento desde barra al tablero.
        
        Principio DIP: La UI orquesta el movimiento, delegando la lógica
        de "salir de la barra" al BarManager y al Board.
        """
        self.ui.__current_player__ = "negro"
        self.ui.__available_moves__ = [3]
        self.ui.__bar_manager__.add_piece_to_bar("negro")
        
        # Limpiar punto destino
        try:
            estado = self.ui.__board__.obtener_estado_punto(3)
            if estado:
                self.ui.__board__.remover_ficha(3, estado[1])
        except:
            pass

        self.ui._PygameUI__execute_move(0, 3)

        self.assertFalse(self.ui.__bar_manager__.has_pieces_on_bar("negro"))

    def test_execute_move_removes_dice_from_available(self):
        """Test que execute_move remueve dado usado.
        
        Principio SRP: Verifica la responsabilidad de __execute_move
        de actualizar el estado interno (dados disponibles).
        """
        self.ui.__current_player__ = "negro"
        self.ui.__available_moves__ = [2, 5]
        
        # Limpiar y configurar
        for i in range(1, 25):
            try:
                estado = self.ui.__board__.obtener_estado_punto(i)
                if estado:
                    self.ui.__board__.remover_ficha(i, estado[1])
            except:
                pass
        
        self.ui.__board__.colocar_ficha(10, "negro", 1)

        self.ui._PygameUI__execute_move(10, 12)

        self.assertEqual(self.ui.__available_moves__, [5])

    def test_execute_move_last_dice_ends_turn(self):
        """Test que usar último dado termina turno.
        
        Principio SRP: Verifica la responsabilidad de __execute_move
        de gestionar el fin de turno cuando se acaban los dados.
        """
        self.ui.__current_player__ = "negro"
        self.ui.__available_moves__ = [3]
        
        # Limpiar y configurar
        for i in range(1, 25):
            try:
                estado = self.ui.__board__.obtener_estado_punto(i)
                if estado:
                    self.ui.__board__.remover_ficha(i, estado[1])
            except:
                pass
        
        self.ui.__board__.colocar_ficha(10, "negro", 1)

        self.ui._PygameUI__execute_move(10, 13)

        self.assertEqual(self.ui.__current_player__, "blanco")

    # --- Tests para validación de movimientos desde barra ---

    def test_validate_move_from_bar_no_pieces(self):
        """Test validación falla si no hay fichas en barra.
        
        Principio DIP: La UI (__validate_and_report_move) depende de
        BarManager para validar un movimiento desde la barra (caso sin fichas).
        """
        self.ui.__current_player__ = "negro"
        self.ui.__available_moves__ = [3]

        result = self.ui._PygameUI__validate_and_report_move(0, 3)

        self.assertFalse(result)
        self.assertIn("No tienes fichas en la barra", self.ui.__message__)

    def test_validate_move_from_bar_wrong_dice(self):
        """Test validación falla con dado incorrecto desde barra.
        
        Principio DIP: La UI valida el dado contra la lista de
        movimientos disponibles (lógica interna, pero informada por Dice).
        """
        self.ui.__current_player__ = "negro"
        self.ui.__available_moves__ = [5]
        self.ui.__bar_manager__.add_piece_to_bar("negro")

        result = self.ui._PygameUI__validate_and_report_move(0, 3)

        self.assertFalse(result)
        self.assertIn("No tienes dado", self.ui.__message__)

    def test_validate_move_from_bar_blocked_destination(self):
        """Test validación falla si destino bloqueado desde barra.
        
        Principio DIP: La UI depende de las reglas del Board
        (via CaptureValidator) para saber si el destino está bloqueado.
        """
        self.ui.__current_player__ = "negro"
        self.ui.__available_moves__ = [3]
        self.ui.__bar_manager__.add_piece_to_bar("negro")
        
        # Limpiar y bloquear destino
        try:
            estado = self.ui.__board__.obtener_estado_punto(3)
            if estado:
                self.ui.__board__.remover_ficha(3, estado[1])
        except:
            pass
        self.ui.__board__.colocar_ficha(3, "blanco", 2)

        result = self.ui._PygameUI__validate_and_report_move(0, 3)

        self.assertFalse(result)
        self.assertIn("bloqueado", self.ui.__message__)

    def test_validate_move_must_enter_from_bar_first(self):
        """Test que debe mover desde barra antes de tablero.
        
        Principio DIP: La UI depende de BarMovementRules (via
        MovementValidator) para forzar la entrada desde la barra.
        """
        self.ui.__current_player__ = "negro"
        self.ui.__available_moves__ = [3]
        self.ui.__bar_manager__.add_piece_to_bar("negro")
        
        # Limpiar y colocar ficha en tablero
        for i in range(1, 25):
            try:
                estado = self.ui.__board__.obtener_estado_punto(i)
                if estado:
                    self.ui.__board__.remover_ficha(i, estado[1])
            except:
                pass
        self.ui.__board__.colocar_ficha(10, "negro", 1)

        result = self.ui._PygameUI__validate_and_report_move(10, 13)

        self.assertFalse(result)
        self.assertIn("desde la barra", self.ui.__message__)

    # --- Tests para attempt_piece_selection con barra ---

    def test_attempt_piece_selection_bar_with_pieces(self):
        """Test selección de barra cuando tiene fichas.
        
        Principio SRP: Verifica la responsabilidad de la UI de manejar
        la selección de la barra (un punto 'especial') cuando es válido.
        """
        self.ui.__current_player__ = "negro"
        self.ui.__available_moves__ = [3]
        self.ui.__game_state_manager__.change_state('AWAITING_PIECE_SELECTION')
        self.ui.__bar_manager__.add_piece_to_bar("negro")

        self.ui._PygameUI__attempt_piece_selection(0)

        self.assertEqual(self.ui.__selected_point__, 0)
        self.assertIn("barra seleccionada", self.ui.__message__)

    def test_attempt_piece_selection_bar_without_pieces(self):
        """Test selección de barra sin fichas.
        
        Principio SRP: Verifica el manejo de selección de la barra
        (caso inválido, sin fichas).
        """
        self.ui.__current_player__ = "negro"
        self.ui.__game_state_manager__.change_state('AWAITING_PIECE_SELECTION')

        self.ui._PygameUI__attempt_piece_selection(0)

        self.assertIsNone(self.ui.__selected_point__)
        self.assertIn("No tienes fichas en la barra", self.ui.__message__)

    def test_attempt_piece_selection_must_move_from_bar(self):
        """Test mensaje cuando debe mover desde barra primero.
        
        Principio DIP: La UI consulta a BarMovementRules y
        reporta al usuario, cumpliendo su SRP de interfaz.
        """
        self.ui.__current_player__ = "negro"
        self.ui.__available_moves__ = [3]
        self.ui.__game_state_manager__.change_state('AWAITING_PIECE_SELECTION')
        self.ui.__bar_manager__.add_piece_to_bar("negro")
        
        # Limpiar y colocar ficha
        for i in range(1, 25):
            try:
                estado = self.ui.__board__.obtener_estado_punto(i)
                if estado:
                    self.ui.__board__.remover_ficha(i, estado[1])
            except:
                pass
        self.ui.__board__.colocar_ficha(10, "negro", 1)

        self.ui._PygameUI__attempt_piece_selection(10)

        self.assertIn("desde la barra", self.ui.__message__)

    # --- Tests para draw methods ---

    @patch("pygame.draw.circle")
    def test_draw_bar_pieces_negro(self, mock_circle):
        """Test dibujado de fichas negras en barra.
        
        Principio SRP: Verifica la responsabilidad única de
        __draw_bar_pieces de dibujar fichas (caso 'negro').
        """
        self.ui.__screen__ = pygame.Surface((1600, 900))
        self.ui.__bar_manager__.add_piece_to_bar("negro")
        self.ui.__bar_manager__.add_piece_to_bar("negro")

        self.ui._PygameUI__draw_bar_pieces()

        # 2 fichas + 2 bordes = 4 círculos
        self.assertEqual(mock_circle.call_count, 4)

    @patch("pygame.draw.circle")
    def test_draw_bar_pieces_blanco(self, mock_circle):
        """Test dibujado de fichas blancas en barra.
        
        Principio SRP: Verifica la responsabilidad de __draw_bar_pieces
        (caso 'blanco').
        """
        self.ui.__screen__ = pygame.Surface((1600, 900))
        self.ui.__bar_manager__.add_piece_to_bar("blanco")

        self.ui._PygameUI__draw_bar_pieces()

        # 1 ficha + 1 borde = 2 círculos
        self.assertEqual(mock_circle.call_count, 2)

    @patch("pygame.draw.circle")
    def test_draw_bar_pieces_more_than_8_shows_count(self, mock_circle):
        """Test que más de 8 fichas muestra contador.
        
        Principio LSP: Verifica que el método de dibujo __draw_bar_pieces
        maneja consistentemente un caso límite (muchas fichas).
        """
        self.ui.__screen__ = pygame.Surface((1600, 900))
        for _ in range(10):
            self.ui.__bar_manager__.add_piece_to_bar("negro")

        self.ui._PygameUI__draw_bar_pieces()

        # Máximo 8 fichas visibles + 8 bordes = 16 círculos
        self.assertEqual(mock_circle.call_count, 16)

    def test_draw_bearing_off_zones_not_active(self):
        """Test que zonas de bearing off no se dibujan si no puede sacar.
        
        Principio LSP: Verifica que __draw_bearing_off_zones
        se comporta correctamente (no dibuja) cuando el estado no lo permite.
        """
        self.ui.__screen__ = pygame.Surface((1600, 900))
        self.ui.__current_player__ = "negro"
        
        # Limpiar y colocar ficha fuera de casa
        for i in range(1, 25):
            try:
                estado = self.ui.__board__.obtener_estado_punto(i)
                if estado:
                    self.ui.__board__.remover_ficha(i, estado[1])
            except:
                pass
        self.ui.__board__.colocar_ficha(10, "negro", 1)

        try:
            self.ui._PygameUI__draw_bearing_off_zones()
        except Exception as e:
            self.fail(f"draw_bearing_off_zones falló: {e}")

    def test_draw_bearing_off_zones_wrong_state(self):
        """Test que zonas no se dibujan en estado incorrecto.
        
        Principio LSP: Verifica que el método de dibujo se
        comporta correctamente (no dibuja) en un estado de juego incorrecto.
        """
        self.ui.__screen__ = pygame.Surface((1600, 900))
        self.ui.__current_player__ = "negro"
        self.ui.__game_state_manager__.change_state('AWAITING_ROLL')

        try:
            self.ui._PygameUI__draw_bearing_off_zones()
        except Exception as e:
            self.fail(f"draw_bearing_off_zones falló: {e}")

    @patch("pygame.draw.circle")
    def test_draw_pips_value_1(self, mock_circle):
        """Test dibujado de pips para dado valor 1.
        
        Principio SRP: Verifica la responsabilidad de __draw_pips
        de dibujar el número correcto de pips (caso 1).
        """
        self.ui.__screen__ = pygame.Surface((1600, 900))
        rect = pygame.Rect(100, 100, 80, 80)

        self.ui._PygameUI__draw_pips(rect, 1)

        self.assertEqual(mock_circle.call_count, 1)

    @patch("pygame.draw.circle")
    def test_draw_pips_value_6(self, mock_circle):
        """Test dibujado de pips para dado valor 6.
        
        Principio SRP: Verifica la responsabilidad de __draw_pips
        de dibujar el número correcto de pips (caso 6).
        """
        self.ui.__screen__ = pygame.Surface((1600, 900))
        rect = pygame.Rect(100, 100, 80, 80)

        self.ui._PygameUI__draw_pips(rect, 6)

        self.assertEqual(mock_circle.call_count, 6)

    def test_draw_dice_without_rolls(self):
        """Test que draw_message funciona sin dados.
        
        Principio LSP: Verifica que __draw_message (que también
        dibuja dados) se comporta establemente cuando __dice_rolls__ está vacío.
        """
        # Configurar surface real y font mockeado
        self.ui.__screen__ = pygame.Surface((1600, 900))
        
        # Mock del font que retorna surface real
        mock_font = Mock()
        mock_surface = pygame.Surface((200, 50))
        mock_font.render.return_value = mock_surface
        self.ui.__font__ = mock_font
        
        self.ui.__dice_rolls__ = []
        
        try:
            self.ui._PygameUI__draw_message()
            # Si llegamos aquí, el test pasa
        except Exception as e:
            self.fail(f"draw_message falló: {e}")

    @patch("pygame.draw.rect")
    def test_draw_dice_with_doubles_highlight(self, mock_rect):
        """Test que dados dobles tienen highlight visual.
        
        Principio LSP: Verifica que __draw_dice altera su
        comportamiento (dibuja un highlight) consistentemente
        cuando __is_doubles_roll__ es True.
        """
        self.ui.__screen__ = pygame.Surface((1600, 900))
        self.ui.__dice_rolls__ = [5, 5]
        self.ui.__is_doubles_roll__ = True

        self.ui._PygameUI__draw_dice()

        # Verificar que se llamó rect para los bordes highlight
        self.assertGreater(mock_rect.call_count, 2)

if __name__ == "__main__":
    unittest.main()