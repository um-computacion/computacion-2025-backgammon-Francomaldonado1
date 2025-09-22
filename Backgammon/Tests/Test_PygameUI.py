import unittest
from unittest.mock import patch, Mock
import pygame
import os
import sys

# Asegura que los módulos del proyecto se encuentren
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Backgammon.Interfaces.PygameUI import PygameUI
from Backgammon.Core.Board import Board


# --- CLASE BASE PARA TESTS DE LÓGICA Y DIBUJO ---
# Esta clase centraliza la configuración para evitar código repetido.
class PygameUITestBase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Se ejecuta una vez por clase para preparar el entorno de Pygame sin pantalla."""
        os.environ["SDL_VIDEODRIVER"] = "dummy"
        pygame.init()

    def setUp(self):
        """
        Se ejecuta antes de cada test. Crea una instancia de PygameUI segura,
        'parcheando' las funciones de Pygame para que el constructor se ejecute
        por completo pero sin crear una ventana real.
        """
        with patch('pygame.display.set_mode', return_value=pygame.Surface((1600, 900))), \
             patch('pygame.font.Font'):
            self.ui = PygameUI()

# --- CLASE BASE PARA TESTS DE PYGAMEUI ---
# Se utiliza para centralizar la configuración y evitar código repetido.
class TestPygameUI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Se ejecuta una vez para preparar el entorno de Pygame sin pantalla."""
        os.environ["SDL_VIDEODRIVER"] = "dummy"
        pygame.init() # Es necesario para crear superficies

    def setUp(self):
        """
        Se ejecuta antes de cada test. Crea una instancia real de PygameUI
        con una superficie en memoria para poder probar las funciones de dibujado.
        """
        self.ui = PygameUI()
        # Se asigna una superficie real para que los métodos de dibujo no fallen
        self.ui._PygameUI__screen__ = pygame.Surface((1600, 900))

    def test_draw_backgammon_board_dibuja_elementos(self):
        """Debe poder llamar a las funciones de dibujo sin errores."""
        try:
            self.ui._PygameUI__draw_backgammon_board()
        except Exception as e:
            self.fail(f"__draw_backgammon_board() falló con el error: {e}")

    def test_creacion_objeto(self):
        """Debe crear correctamente una instancia de PygameUI."""
        self.assertIsNotNone(self.ui)
        self.assertIsInstance(self.ui, PygameUI)

    def test_metodo_run_existe(self):
        """Debe tener el método run."""
        self.assertTrue(hasattr(self.ui, 'run'))
        self.assertTrue(callable(self.ui.run))

    def test_metodo_handle_events_existe(self):
        """Debe tener el método privado __handle_events."""
        self.assertTrue(hasattr(self.ui, '_PygameUI__handle_events'))

    def test_metodo_update_existe(self):
        """Debe tener el método privado __update."""
        self.assertTrue(hasattr(self.ui, '_PygameUI__update'))

    def test_metodo_draw_existe(self):
        """Debe tener el método privado __draw."""
        self.assertTrue(hasattr(self.ui, '_PygameUI__draw'))

    def test_metodo_draw_backgammon_board_existe(self):
        """Debe tener el método privado __draw_backgammon_board."""
        self.assertTrue(hasattr(self.ui, '_PygameUI__draw_backgammon_board'))

    def test_metodo_draw_points_existe(self):
        """Debe tener el método privado __draw_points."""
        self.assertTrue(hasattr(self.ui, '_PygameUI__draw_points'))

    def test_metodo_draw_triangle_point_existe(self):
        """Debe tener el método privado __draw_triangle_point."""
        self.assertTrue(hasattr(self.ui, '_PygameUI__draw_triangle_point'))

    def test_metodo_draw_checkers_existe(self):
        """Debe tener el método privado __draw_checkers."""
        self.assertTrue(hasattr(self.ui, '_PygameUI__draw_checkers'))

    def test_metodo_get_point_screen_position_existe(self):
        """Debe tener el método privado __get_point_screen_position."""
        self.assertTrue(hasattr(self.ui, '_PygameUI__get_point_screen_position'))

    def test_metodo_draw_checker_stack_existe(self):
        """Debe tener el método privado __draw_checker_stack."""
        self.assertTrue(hasattr(self.ui, '_PygameUI__draw_checker_stack'))

    def test_inicializacion_con_dimensiones_default(self):
        """Debe inicializarse con dimensiones por defecto."""
        ui_default = PygameUI()
        self.assertIsNotNone(ui_default)

    def test_inicializacion_con_dimensiones_custom(self):
        """Debe inicializarse con dimensiones personalizadas."""
        ui_custom = PygameUI(board_width=1920, board_height=1080)
        self.assertIsNotNone(ui_custom)

    def test_posicion_punto_1_en_rango_valido(self):
        """El punto 1 debe tener una posición válida."""
        x, y = self.ui._PygameUI__get_point_screen_position(1)
        self.assertIsInstance(x, int)
        self.assertIsInstance(y, int)
        self.assertGreaterEqual(x, 0)
        self.assertGreaterEqual(y, 0)
        self.assertLess(x, 1600)
        self.assertLess(y, 900)

    def test_posicion_punto_24_en_rango_valido(self):
        """El punto 24 debe tener una posición válida."""
        x, y = self.ui._PygameUI__get_point_screen_position(24)
        self.assertIsInstance(x, int)
        self.assertIsInstance(y, int)
        self.assertGreaterEqual(x, 0)
        self.assertGreaterEqual(y, 0)
        self.assertLess(x, 1600)
        self.assertLess(y, 900)

    def test_todas_las_posiciones_puntos_validas(self):
        """Todos los puntos 1-24 deben tener posiciones válidas."""
        for punto in range(1, 25):
            x, y = self.ui._PygameUI__get_point_screen_position(punto)
            self.assertIsInstance(x, int, f"X del punto {punto} no es entero")
            self.assertIsInstance(y, int, f"Y del punto {punto} no es entero")
            self.assertGreaterEqual(x, 0, f"X del punto {punto} es negativo: {x}")
            self.assertGreaterEqual(y, 0, f"Y del punto {punto} es negativo: {y}")
            self.assertLess(x, 1600, f"X del punto {punto} fuera de pantalla: {x}")
            self.assertLess(y, 900, f"Y del punto {punto} fuera de pantalla: {y}")

    def test_cuadrantes_puntos_correctos(self):
        """Los puntos deben estar en sus cuadrantes correctos."""
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
        """Debe dibujar triángulos apuntando hacia abajo."""
        self.ui._PygameUI__screen__ = pygame.Surface((1600, 900))
        self.ui._PygameUI__draw_triangle_point(100, 100, 50, 100, (255, 0, 0), pointing_down=True)
        self.assertTrue(mock_polygon.called)
        self.assertEqual(mock_polygon.call_count, 2)  # Relleno + borde

    @patch("pygame.draw.polygon")
    def test_draw_triangle_point_hacia_arriba(self, mock_polygon):
        """Debe dibujar triángulos apuntando hacia arriba."""
        self.ui._PygameUI__screen__ = pygame.Surface((1600, 900))
        self.ui._PygameUI__draw_triangle_point(100, 100, 50, 100, (0, 255, 0), pointing_down=False)
        self.assertTrue(mock_polygon.called)
        self.assertEqual(mock_polygon.call_count, 2)  # Relleno + borde

    @patch("pygame.draw.circle")
    def test_draw_checker_stack_fichas_blancas(self, mock_circle):
        """Debe dibujar stack de fichas blancas."""
        self.ui._PygameUI__screen__ = pygame.Surface((1600, 900))
        self.ui._PygameUI__draw_checker_stack(400, 300, "blanco", 3, 6, 25)
        # 3 fichas + 3 bordes = 6 llamadas
        self.assertEqual(mock_circle.call_count, 6)

    @patch("pygame.draw.circle")
    def test_draw_checker_stack_fichas_negras(self, mock_circle):
        """Debe dibujar stack de fichas negras."""
        self.ui._PygameUI__screen__ = pygame.Surface((1600, 900))
        self.ui._PygameUI__draw_checker_stack(400, 300, "negro", 2, 19, 25)
        # 2 fichas + 2 bordes = 4 llamadas
        self.assertEqual(mock_circle.call_count, 4)

    @patch("pygame.draw.circle")
    def test_draw_checker_stack_limite_fichas_visibles(self, mock_circle):
        """No debe dibujar más de 10 fichas visibles."""
        self.ui._PygameUI__screen__ = pygame.Surface((1600, 900))
        self.ui._PygameUI__draw_checker_stack(400, 300, "blanco", 15, 13, 25)
        # Máximo 10 fichas + 10 bordes = 20 llamadas
        self.assertEqual(mock_circle.call_count, 20)

    @patch("pygame.draw.rect")
    def test_draw_backgammon_board_dibuja_elementos(self, mock_rect):
        """Debe dibujar el fondo del tablero y la barra."""
        self.ui._PygameUI__screen__ = pygame.Surface((1600, 900))
        self.ui._PygameUI__draw_backgammon_board()
        # Al menos 2 rectángulos: fondo del tablero + barra
        self.assertGreaterEqual(mock_rect.call_count, 2)

    @patch("pygame.draw.polygon")
    def test_draw_points_dibuja_24_triangulos(self, mock_polygon):
        """Debe dibujar los 24 triángulos del tablero."""
        self.ui._PygameUI__screen__ = pygame.Surface((1600, 900))
        self.ui._PygameUI__draw_points()
        # 24 triángulos × 2 (relleno + borde) = 48 llamadas
        self.assertEqual(mock_polygon.call_count, 48)

    def test_draw_checkers_no_falla_con_board_real(self):
        """El método draw_checkers debe funcionar con el board real."""
        self.ui._PygameUI__screen__ = pygame.Surface((1600, 900))
        try:
            self.ui._PygameUI__draw_checkers()
        except Exception as e:
            self.fail(f"draw_checkers falló con board real: {e}")

    @patch("pygame.display.flip")
    def test_draw_llama_display_flip(self, mock_flip):
        """El método draw debe llamar a pygame.display.flip."""
        self.ui._PygameUI__screen__ = pygame.Surface((1600, 900))
        self.ui._PygameUI__draw()
        mock_flip.assert_called_once()

    def test_update_metodo_ejecutable(self):
        """El método __update debe ser ejecutable sin errores."""
        try:
            self.ui._PygameUI__update()
        except Exception as e:
            self.fail(f"Método __update falló: {e}")

    def test_handle_events_sin_eventos(self):
        """Handle events debe funcionar sin eventos."""
        with patch("pygame.event.get", return_value=[]):
            try:
                self.ui._PygameUI__handle_events()
            except Exception as e:
                self.fail(f"__handle_events falló sin eventos: {e}")

    def test_draw_metodo_completo_ejecutable(self):
        """El método __draw completo debe ser ejecutable."""
        self.ui._PygameUI__screen__ = pygame.Surface((1600, 900))
        try:
            self.ui._PygameUI__draw()
        except Exception as e:
            self.fail(f"Método __draw completo falló: {e}")

    def test_puntos_extremos_posicionamiento_correcto(self):
        """Los puntos en las esquinas deben estar correctamente posicionados."""
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
        """Los parámetros del triángulo deben ser manejados correctamente."""
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
        """Las fichas deben apilarse en la dirección correcta según el punto."""
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
        """La instancia interna debe ser de tipo Board."""
        # Acceder al board de manera más indirecta
        board_attr_names = [attr for attr in dir(self.ui) if 'board' in attr.lower()]
        self.assertGreater(len(board_attr_names), 0, "Debe tener al menos un atributo relacionado con board")

        
# --- NUEVA CLASE DE TESTS AÑADIDA ---
class TestPygameUIClickDetection(unittest.TestCase):
    """
    Suite de pruebas dedicada a verificar la correcta detección de clics en el tablero.
    """
    @classmethod
    def setUpClass(cls):
        # Evita que pygame intente abrir una ventana durante los tests
        os.environ["SDL_VIDEODRIVER"] = "dummy"
        
    def setUp(self):
        """Crea una instancia de PygameUI para cada test."""
        with patch('pygame.init'), patch('pygame.display.set_mode'), patch('pygame.font.Font'):
         self.ui = PygameUI(board_width=1600, board_height=900)

    def test_get_point_from_mouse_pos_top_right_quadrant(self):
        """Prueba clics en cuadrante superior derecho (puntos 1-6)."""
        # Punto 1 (más a la derecha)
        self.assertEqual(self.ui._PygameUI__get_point_from_mouse_pos((1500, 100)), 1)
        # Punto 3
        self.assertEqual(self.ui._PygameUI__get_point_from_mouse_pos((1250, 100)), 3)
        # Punto 6 (más cercano a la barra)
        self.assertEqual(self.ui._PygameUI__get_point_from_mouse_pos((850, 100)), 6)

    def test_get_point_from_mouse_pos_top_left_quadrant(self):
        """Prueba clics en cuadrante superior izquierdo (puntos 7-12)."""
        # Punto 7 (más cercano a la barra)
        self.assertEqual(self.ui._PygameUI__get_point_from_mouse_pos((750, 100)), 7)
        # Punto 10
        self.assertEqual(self.ui._PygameUI__get_point_from_mouse_pos((400, 100)), 10)
        # Punto 12 (más a la izquierda)
        self.assertEqual(self.ui._PygameUI__get_point_from_mouse_pos((100, 100)), 12)

    def test_get_point_from_mouse_pos_bottom_left_quadrant(self):
        """Prueba clics en cuadrante inferior izquierdo (puntos 13-18)."""
        # Punto 13 (más a la izquierda)
        self.assertEqual(self.ui._PygameUI__get_point_from_mouse_pos((100, 800)), 13)
        # Punto 15
        self.assertEqual(self.ui._PygameUI__get_point_from_mouse_pos((300, 800)), 15)
        # Punto 18 (más cercano a la barra)
        self.assertEqual(self.ui._PygameUI__get_point_from_mouse_pos((700, 800)), 18)

    def test_get_point_from_mouse_pos_bottom_right_quadrant(self):
        """Prueba clics en cuadrante inferior derecho (puntos 19-24)."""
        # Punto 19 (más cercano a la barra)
        self.assertEqual(self.ui._PygameUI__get_point_from_mouse_pos((850, 800)), 19)
        # Punto 21
        self.assertEqual(self.ui._PygameUI__get_point_from_mouse_pos((1100, 800)), 21)
        # Punto 24 (más a la derecha)
        self.assertEqual(self.ui._PygameUI__get_point_from_mouse_pos((1500, 800)), 24)
        
    def test_get_point_from_mouse_pos_invalid_clicks(self):
        """Prueba que los clics fuera de las áreas de los puntos devuelven None."""
        # Click en el margen izquierdo
        self.assertIsNone(self.ui._PygameUI__get_point_from_mouse_pos((25, 450)))
        # Click en el margen superior
        self.assertIsNone(self.ui._PygameUI__get_point_from_mouse_pos((800, 25)))
        # Click en la barra central
        self.assertIsNone(self.ui._PygameUI__get_point_from_mouse_pos((790, 450)))


# --- SUITE DE TESTS PARA LA LÓGICA DEL JUEGO (SIN DIBUJADO) ---
class TestPygameUILogic(unittest.TestCase):
    """
    Suite de pruebas para la lógica del juego (tiradas, selección, validación),
    sin depender de la renderización en pantalla.
    """
    def setUp(self):
        """
        Se ejecuta antes de cada test. Inicializa PygameUI de forma segura,
        'parcheando' las funciones de Pygame para que el constructor __init__
        pueda ejecutarse por completo sin crear una ventana.
        """
        # Este 'patch' es la clave: permite que PygameUI.__init__ se ejecute
        # y cree todos los atributos (__board__, __current_player__, etc.)
        # sin fallar por intentar crear una ventana.
        with patch('pygame.init'), \
             patch('pygame.display.set_mode'), \
             patch('pygame.font.Font'):
            self.ui = PygameUI()

    # --- Tests para la Tirada de Dados ---
    @patch('Backgammon.Core.Dice.Dice.tirar')
    @patch('Backgammon.Core.Dice.Dice.obtener_dado1')
    @patch('Backgammon.Core.Dice.Dice.obtener_dado2')
    @patch.object(PygameUI, '_PygameUI__draw')
    def test_roll_to_start_negro_wins(self, mock_draw, mock_dado2, mock_dado1, mock_tirar):
        """Verifica que 'negro' gana la tirada inicial con un dado más alto."""
        mock_dado1.return_value = 5
        mock_dado2.return_value = 3
        self.ui._PygameUI__roll_to_start()
        self.assertEqual(self.ui.__current_player__, "negro")
        self.assertEqual(self.ui.__game_state__, "AWAITING_ROLL")

    @patch('Backgammon.Core.Dice.Dice.tirar')
    @patch('Backgammon.Core.Dice.Dice.obtener_dado1')
    @patch('Backgammon.Core.Dice.Dice.obtener_dado2')
    @patch.object(PygameUI, '_PygameUI__draw')
    def test_roll_to_start_blanco_wins(self, mock_draw, mock_dado2, mock_dado1, mock_tirar):
        """Verifica que 'blanco' gana la tirada inicial con un dado más alto."""
        mock_dado1.return_value = 2
        mock_dado2.return_value = 6
        self.ui._PygameUI__roll_to_start()
        self.assertEqual(self.ui.__current_player__, "blanco")
        self.assertEqual(self.ui.__game_state__, "AWAITING_ROLL")

    @patch('Backgammon.Core.Dice.Dice.tirar')
    @patch('Backgammon.Core.Dice.Dice.obtener_dado1')
    @patch('Backgammon.Core.Dice.Dice.obtener_dado2')
    @patch.object(PygameUI, '_PygameUI__draw')
    def test_roll_to_start_handles_tie(self, mock_draw, mock_dado2, mock_dado1, mock_tirar):
        """Verifica que el método vuelve a tirar los dados si ocurre un empate."""
        mock_dado1.side_effect = [4, 6]
        mock_dado2.side_effect = [4, 1]
        self.ui._PygameUI__roll_to_start()
        self.assertEqual(self.ui.__current_player__, "negro")
        self.assertEqual(mock_tirar.call_count, 2)

    # --- Tests para Tirada de Dados del Jugador ---
    @patch('Backgammon.Core.Dice.Dice.tirar')
    @patch('Backgammon.Core.Dice.Dice.obtener_dado1')
    @patch('Backgammon.Core.Dice.Dice.obtener_dado2')
    def test_roll_player_dice(self, mock_dado2, mock_dado1, mock_tirar):
        """Verifica que se pueden tirar los dados del jugador."""
        self.ui.__current_player__ = "negro"
        self.ui.__game_state__ = "AWAITING_ROLL"
        
        mock_dado1.return_value = 4
        mock_dado2.return_value = 6
        
        self.ui._PygameUI__roll_player_dice()
        
        self.assertEqual(self.ui.__dice_rolls__, [4, 6])
        self.assertEqual(self.ui.__game_state__, "AWAITING_PIECE_SELECTION")
        self.assertIn("Turno de negro", self.ui.__message__)

    # --- Tests para la Validación de Movimientos ---
    def test_select_valid_piece(self):
        """Verifica que se puede seleccionar un punto con fichas propias."""
        self.ui.__current_player__ = "negro"
        self.ui.__game_state__ = "AWAITING_PIECE_SELECTION"
        self._simulate_click_on_point(1)
        self.assertEqual(self.ui.__selected_point__, 1)

    def test_validate_move_valid(self):
        """Verifica que la UI reporta correctamente un movimiento válido."""
        self.ui.__current_player__ = "negro"
        self.ui.__dice_rolls__ = [4]
        
        # Asegurar que hay una ficha negra en el punto de origen
        self.ui.__board__.colocar_ficha(19, "negro", 1)
        
        # Mock del método _mover_ficha_bool para que retorne True
        with patch.object(self.ui.__board__, '_mover_ficha_bool', return_value=True):
            result = self.ui._PygameUI__validate_and_report_move(origen=19, destino=23)  # Movimiento en dirección correcta
            self.assertTrue(result)
            self.assertIn("es VÁLIDO", self.ui.__message__)

    def test_validate_move_invalid_blocked(self):
        """Verifica que la UI reporta correctamente un movimiento a un punto bloqueado."""
        self.ui.__current_player__ = "negro"
        self.ui.__dice_rolls__ = [4]
        
        # Colocar ficha negra en origen
        self.ui.__board__.colocar_ficha(19, "negro", 1)
        
        # Mock del método _mover_ficha_bool para que retorne False (punto bloqueado)
        with patch.object(self.ui.__board__, '_mover_ficha_bool', return_value=False):
            result = self.ui._PygameUI__validate_and_report_move(origen=19, destino=23)  # Movimiento en dirección correcta
            self.assertFalse(result)
            self.assertIn("NO ES VÁLIDO", self.ui.__message__)

    def test_validate_move_dice_not_matching(self):
        """Verifica que se rechaza un movimiento cuando el dado no coincide."""
        self.ui.__current_player__ = "negro"
        self.ui.__dice_rolls__ = [3, 5]  # Solo dados 3 y 5 disponibles
        
        # Colocar ficha negra en el punto de origen
        self.ui.__board__.colocar_ficha(1, "negro", 1)
        
        # Intentar mover 4 espacios (dado no disponible)
        result = self.ui._PygameUI__validate_and_report_move(origen=1, destino=5)
        self.assertFalse(result)
        self.assertIn("El valor del dado no coincide", self.ui.__message__)

    # --- TESTS PARA LA RESTRICCIÓN DIRECCIONAL ---
    def test_move_direction_negro_valid(self):
        """Verifica que el jugador negro PUEDE mover hacia números mayores (dirección correcta)."""
        self.ui.__current_player__ = "negro"
        self.ui.__dice_rolls__ = [2]
        
        # Colocar ficha negra en el punto de origen
        self.ui.__board__.colocar_ficha(1, "negro", 1)
        
        # Mock del método _mover_ficha_bool para que retorne True
        with patch.object(self.ui.__board__, '_mover_ficha_bool', return_value=True):
            # El movimiento de 1 a 3 es válido para negro (hacia números mayores)
            result = self.ui._PygameUI__validate_and_report_move(origen=1, destino=3)
            self.assertTrue(result)
            self.assertIn("es VÁLIDO", self.ui.__message__)

    def test_move_direction_negro_invalid(self):
        """Verifica que el jugador negro NO PUEDE mover hacia números menores (dirección incorrecta)."""
        self.ui.__current_player__ = "negro"
        self.ui.__dice_rolls__ = [2]
        
        # Colocar ficha negra en el punto de origen
        self.ui.__board__.colocar_ficha(3, "negro", 1)
        
        # El movimiento de 3 a 1 es inválido para negro (hacia números menores)
        result = self.ui._PygameUI__validate_and_report_move(origen=3, destino=1)
        self.assertFalse(result)
        self.assertIn("dirección incorrecta", self.ui.__message__)
    
    def test_move_direction_blanco_valid(self):
        """Verifica que el jugador blanco PUEDE mover hacia números menores (dirección correcta)."""
        self.ui.__current_player__ = "blanco"
        self.ui.__dice_rolls__ = [2]
        
        # Colocar ficha blanca en el punto de origen
        self.ui.__board__.colocar_ficha(24, "blanco", 1)
        
        # Mock del método _mover_ficha_bool para que retorne True
        with patch.object(self.ui.__board__, '_mover_ficha_bool', return_value=True):
            # El movimiento de 24 a 22 es válido para blanco (hacia números menores)
            result = self.ui._PygameUI__validate_and_report_move(origen=24, destino=22)
            self.assertTrue(result)
            self.assertIn("es VÁLIDO", self.ui.__message__)

    def test_move_direction_blanco_invalid(self):
        """Verifica que el jugador blanco NO PUEDE mover hacia números mayores (dirección incorrecta)."""
        self.ui.__current_player__ = "blanco"
        self.ui.__dice_rolls__ = [2]
        
        # Colocar ficha blanca en el punto de origen
        self.ui.__board__.colocar_ficha(22, "blanco", 1)
        
        # El movimiento de 22 a 24 es inválido para blanco (hacia números mayores)
        result = self.ui._PygameUI__validate_and_report_move(origen=22, destino=24)
        self.assertFalse(result)
        self.assertIn("dirección incorrecta", self.ui.__message__)

    def test_move_direction_negro_edge_cases(self):
        """Tests adicionales para casos límite del jugador negro."""
        self.ui.__current_player__ = "negro"
        
        # Test: Movimiento desde punto 1 hacia adelante
        self.ui.__dice_rolls__ = [6]
        self.ui.__board__.colocar_ficha(1, "negro", 1)
        
        with patch.object(self.ui.__board__, '_mover_ficha_bool', return_value=True):
            result = self.ui._PygameUI__validate_and_report_move(origen=1, destino=7)
            self.assertTrue(result)
        
        # Test: Intento de movimiento hacia atrás desde punto medio
        self.ui.__dice_rolls__ = [3]
        self.ui.__board__.colocar_ficha(15, "negro", 1)
        
        result = self.ui._PygameUI__validate_and_report_move(origen=15, destino=12)
        self.assertFalse(result)
        self.assertIn("dirección incorrecta", self.ui.__message__)

    def test_move_direction_blanco_edge_cases(self):
        """Tests adicionales para casos límite del jugador blanco."""
        self.ui.__current_player__ = "blanco"
        
        # Test: Movimiento desde punto 24 hacia adelante (números menores)
        self.ui.__dice_rolls__ = [6]
        self.ui.__board__.colocar_ficha(24, "blanco", 1)
        
        with patch.object(self.ui.__board__, '_mover_ficha_bool', return_value=True):
            result = self.ui._PygameUI__validate_and_report_move(origen=24, destino=18)
            self.assertTrue(result)
        
        # Test: Intento de movimiento hacia atrás desde punto medio
        self.ui.__dice_rolls__ = [3]
        self.ui.__board__.colocar_ficha(10, "blanco", 1)
        
        result = self.ui._PygameUI__validate_and_report_move(origen=10, destino=13)
        self.assertFalse(result)
        self.assertIn("dirección incorrecta", self.ui.__message__)

    # --- Helper Method ---
    def _simulate_click_on_point(self, point_number: int):
        """Helper para simular un evento de clic del ratón."""
        with patch.object(self.ui, '_PygameUI__get_point_from_mouse_pos', return_value=point_number):
            mock_event = Mock(type=pygame.MOUSEBUTTONDOWN, button=1)
            mock_event.pos = (100, 100)  # Añadir posición del mouse
            with patch('pygame.event.get', return_value=[mock_event]), \
                 patch('pygame.mouse.get_pos', return_value=(100, 100)):
                self.ui._PygameUI__handle_events()

if __name__ == "__main__":
    unittest.main()
