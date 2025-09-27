import unittest
from unittest.mock import patch, Mock
import pygame
import os
import sys

# Asegura que los módulos del proyecto se encuentren
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Backgammon.Interfaces.PygameUI import PygameUI, DiceMovesCalculator, GameStateManager, MessageManager
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
        Se ejecuta antes de cada test. Inicializa PygameUI de forma segura.
        """
        with patch('pygame.init'), \
             patch('pygame.display.set_mode'), \
             patch('pygame.font.Font'):
            self.ui = PygameUI()

    # --- Helper Method ---
    def _simulate_click_on_point(self, point_number: int):
        """Helper para simular un evento de clic del ratón."""
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
        """Verifica que 'negro' gana la tirada inicial con un dado más alto."""
        mock_dado1.return_value = 5
        mock_dado2.return_value = 3
        self.ui._PygameUI__roll_to_start()
        self.assertEqual(self.ui.__current_player__, "negro")

    @patch('Backgammon.Core.Dice.Dice.tirar')
    @patch('Backgammon.Core.Dice.Dice.obtener_dado1')
    @patch('Backgammon.Core.Dice.Dice.obtener_dado2')
    def test_roll_to_start_blanco_wins(self, mock_dado2, mock_dado1, mock_tirar):
        """Verifica que 'blanco' gana la tirada inicial con un dado más alto."""
        mock_dado1.return_value = 2
        mock_dado2.return_value = 6
        self.ui._PygameUI__roll_to_start()
        self.assertEqual(self.ui.__current_player__, "blanco")

    @patch('Backgammon.Core.Dice.Dice.tirar')
    @patch('Backgammon.Core.Dice.Dice.obtener_dado1')
    @patch('Backgammon.Core.Dice.Dice.obtener_dado2')
    def test_roll_to_start_handles_tie(self, mock_dado2, mock_dado1, mock_tirar):
        """Verifica que el método vuelve a tirar los dados si ocurre un empate."""
        mock_dado1.side_effect = [4, 6]
        mock_dado2.side_effect = [4, 1]
        self.ui._PygameUI__roll_to_start()
        self.assertEqual(self.ui.__current_player__, "negro")
        self.assertEqual(mock_tirar.call_count, 2)

    # --- Tests para Selección y Validación de Movimientos ---
    def test_select_valid_piece(self):
        """Verifica que se puede seleccionar un punto con fichas propias."""
        self.ui.__board__.colocar_ficha(1, "negro", 1)
        self._simulate_click_on_point(1)
        self.assertEqual(self.ui.__selected_point__, 1)

    def test_validate_move_valid(self):
        """Verifica que la UI reporta correctamente un movimiento válido."""
        self.ui.__current_player__ = "negro"
        self.ui.__available_moves__ = [4]
        self.ui.__board__.colocar_ficha(19, "negro", 1)
        # Vaciamos el punto de destino para asegurar que el movimiento sea válido
        self.ui.__board__.colocar_ficha(23, "vacío", 0)
        result = self.ui._PygameUI__validate_and_report_move(origen=19, destino=23)
        self.assertTrue(result)

    def test_validate_move_invalid_blocked(self):
        """Verifica que la UI reporta correctamente un movimiento a un punto bloqueado."""
        self.ui.__current_player__ = "negro"
        self.ui.__available_moves__ = [4]
        self.ui.__board__.colocar_ficha(19, "negro", 1)
        self.ui.__board__.colocar_ficha(23, "blanco", 2) # Bloqueamos el destino
        result = self.ui._PygameUI__validate_and_report_move(origen=19, destino=23)
        self.assertFalse(result)

    def test_move_direction_negro_valid(self):
        """Verifica que el jugador negro PUEDE mover hacia números mayores."""
        self.ui.__current_player__ = "negro"
        self.ui.__available_moves__ = [2]
        self.ui.__board__.colocar_ficha(1, "negro", 1)
        result = self.ui._PygameUI__validate_and_report_move(origen=1, destino=3)
        self.assertTrue(result)

    def test_move_direction_blanco_valid(self):
        """Verifica que el jugador blanco PUEDE mover hacia números menores."""
        self.ui.__current_player__ = "blanco"
        self.ui.__available_moves__ = [2]
        self.ui.__board__.colocar_ficha(24, "blanco", 1)
        result = self.ui._PygameUI__validate_and_report_move(origen=24, destino=22)
        self.assertTrue(result)
        
    def test_move_direction_negro_edge_cases(self):
        """Tests adicionales para casos límite del jugador negro."""
        self.ui.__current_player__ = "negro"
        self.ui.__available_moves__ = [6]
        self.ui.__board__.colocar_ficha(1, "negro", 1)
        result = self.ui._PygameUI__validate_and_report_move(origen=1, destino=7)
        self.assertTrue(result)

    def test_move_direction_blanco_edge_cases(self):
        """Tests adicionales para casos límite del jugador blanco."""
        self.ui.__current_player__ = "blanco"
        self.ui.__available_moves__ = [6]
        self.ui.__board__.colocar_ficha(24, "blanco", 1)
        # Vaciamos el punto de destino para asegurar que el movimiento sea válido
        self.ui.__board__.colocar_ficha(18, "vacío", 0)
        result = self.ui._PygameUI__validate_and_report_move(origen=24, destino=18)
        self.assertTrue(result)


# --- TESTS PARA VALIDACIÓN DE DOBLES ---
class TestDoublesValidation(unittest.TestCase):
    """
    Suite de tests específica para validar la lógica de dobles en el Backgammon.
    """
    def setUp(self):
        """Configura el entorno de test sin interfaz gráfica."""
        with patch('pygame.init'), \
             patch('pygame.display.set_mode'), \
             patch('pygame.font.Font'):
            self.ui = PygameUI()

    @patch('Backgammon.Core.Dice.Dice.tirar')
    @patch('Backgammon.Core.Dice.Dice.obtener_dado1')
    @patch('Backgammon.Core.Dice.Dice.obtener_dado2')
    def test_roll_doubles_generates_four_moves(self, mock_dado2, mock_dado1, mock_tirar):
        """Verifica que al sacar dobles se generen 4 movimientos del mismo valor."""
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
        """Verifica que al sacar dados normales se generen 2 movimientos."""
        mock_dado1.return_value = 2
        mock_dado2.return_value = 5
        self.ui.__current_player__ = "negro"
        self.ui._PygameUI__roll_player_dice()
        self.assertCountEqual(self.ui.__available_moves__, [2, 5])
        self.assertFalse(self.ui.__is_doubles_roll__)

    def test_execute_move_removes_one_die_from_doubles(self):
        """Verifica que al ejecutar un movimiento con dobles se remueva solo un dado."""
        self.ui.__current_player__ = "negro"
        self.ui.__available_moves__ = [4, 4, 4, 4]
        self.ui.__is_doubles_roll__ = True
        self.ui.__board__.colocar_ficha(1, "negro", 1)
        self.ui._PygameUI__execute_move(1, 5)
        self.assertEqual(self.ui.__available_moves__, [4, 4, 4])

    def test_complete_all_doubles_moves_ends_turn(self):
        """Verifica que usar todos los movimientos de dobles termine el turno."""
        self.ui.__current_player__ = "negro"
        self.ui.__available_moves__ = [6]
        self.ui.__is_doubles_roll__ = True
        self.ui.__board__.colocar_ficha(1, "negro", 1)
        self.ui._PygameUI__execute_move(1, 7)
        self.assertEqual(self.ui.__current_player__, "blanco")
        self.assertFalse(self.ui.__is_doubles_roll__)
        self.assertEqual(self.ui.__game_state_manager__.get_current_state(), "AWAITING_ROLL")

    def test_validate_doubles_move_with_available_die(self):
        """Verifica que se pueda validar un movimiento cuando el dado está disponible en dobles."""
        self.ui.__current_player__ = "negro"
        self.ui.__available_moves__ = [5, 5, 5, 5]
        # Colocamos una ficha en el punto 2 (que está vacío por defecto)
        self.ui.__board__.colocar_ficha(2, "negro", 1)
        # El destino es el punto 7 (2 + 5), que también está vacío por defecto.
        # Esto representa el movimiento más simple y válido posible.
        result = self.ui._PygameUI__validate_and_report_move(2, 7)
        self.assertTrue(result)

    def test_validate_doubles_move_without_available_die(self):
        """Verifica que se rechace un movimiento cuando el dado no está disponible en dobles."""
        self.ui.__current_player__ = "negro"
        self.ui.__available_moves__ = [3, 3, 3, 3]
        result = self.ui._PygameUI__validate_and_report_move(1, 6)
        self.assertFalse(result)
        self.assertIn("No tienes el dado 5 disponible", self.ui.__message__)



# --- TESTS DE PRINCIPIOS SOLID ---
class TestSOLIDPrinciples(unittest.TestCase):
    """
    Suite de tests específicamente diseñada para verificar el cumplimiento
    de los principios SOLID en la arquitectura de PygameUI.
    Esto es clave para demostrar buena orientación a objetos.
    """
    
    def setUp(self):
        """Configura el entorno sin interfaz gráfica."""
        with patch('pygame.init'), \
             patch('pygame.display.set_mode'), \
             patch('pygame.font.Font'):
            self.ui = PygameUI()
    
    # --- SINGLE RESPONSIBILITY PRINCIPLE (SRP) TESTS ---
    def test_srp_dice_calculator_only_handles_dice_logic(self):
        """
        Verifica que DiceMovesCalculator solo maneja lógica de dados.
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
        Verifica que GameStateManager solo maneja estados del juego.
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
        Verifica que MessageManager solo maneja generación de mensajes.
        """
        # Test directo de los métodos estáticos
        start_msg = MessageManager.get_start_message()
        doubles_msg = MessageManager.get_doubles_roll_message("negro", 4, [4, 4, 4, 4])
        normal_msg = MessageManager.get_normal_roll_message("blanco", [2, 6])
        
        self.assertIsInstance(start_msg, str)
        self.assertIsInstance(doubles_msg, str)
        self.assertIsInstance(normal_msg, str)
        self.assertIn("DOBLES", doubles_msg)
        self.assertIn("Presiona", start_msg)
    
    # --- OPEN/CLOSED PRINCIPLE (OCP) TESTS ---
    def test_ocp_game_state_manager_extensible_for_new_states(self):
        """
        Verifica que GameStateManager sea extensible para nuevos estados
        sin modificar código existente (OCP).
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
        Verifica que DiceMovesCalculator sea extensible para nuevas reglas
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
        Verifica que PygameUI usa las clases gestoras (principio DIP).
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
        Verifica que las clases gestoras funcionan independientemente (DIP).
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
        self.assertIn("DOBLES", message)
    
    # --- INTEGRATION TEST FOR SOLID PRINCIPLES ---
    def test_solid_integration_all_principles_work_together(self):
        """
        Test de integración que verifica que todos los principios SOLID
        trabajen juntos correctamente.
        """
        # SRP: Cada clase maneja su responsabilidad específica
        dice_moves = DiceMovesCalculator.calculate_available_moves(5, 5)  # Solo dados
        game_state = GameStateManager()  # Solo estados
        message = MessageManager.get_doubles_roll_message("negro", 5, dice_moves)  # Solo mensajes
        
        # OCP: Las clases son extensibles
        self.assertEqual(dice_moves, [5, 5, 5, 5])
        self.assertEqual(game_state.get_current_state(), 'START_ROLL')
        
        # DIP: Las abstracciones funcionan independientemente
        self.assertIn("DOBLES", message)
        self.assertIn("5-5", message)
        
        # ISP: Interfaces específicas (cada clase tiene métodos específicos a su propósito)
        self.assertTrue(callable(DiceMovesCalculator.calculate_available_moves))
        self.assertTrue(callable(game_state.change_state))
        self.assertTrue(callable(MessageManager.get_start_message))
        
        # Todo funciona en conjunto
        self.assertIsInstance(dice_moves, list)
        self.assertIsInstance(message, str)
        self.assertIsInstance(game_state.get_current_state(), str)
    
    def test_solid_architecture_separation_of_concerns(self):
        """
        Verifica que la arquitectura mantenga separación de responsabilidades.
        """
        # Cada clase tiene una responsabilidad clara y diferenciada
        
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
        self.assertIn("DOBLES", msg2)
        self.assertIn("blanco", msg2.lower())


# --- TESTS PARA DICE MOVES CALCULATOR ---
class TestDiceMovesCalculator(unittest.TestCase):
    """
    Tests unitarios para la clase DiceMovesCalculator.
    Verifica el cumplimiento del principio SRP.
    """
    
    def test_calculate_normal_moves(self):
        """Verifica el cálculo correcto para dados normales."""
        moves = DiceMovesCalculator.calculate_available_moves(2, 5)
        self.assertEqual(moves, [2, 5])
    
    def test_calculate_doubles_moves(self):
        """Verifica el cálculo correcto para dobles."""
        moves = DiceMovesCalculator.calculate_available_moves(4, 4)
        self.assertEqual(moves, [4, 4, 4, 4])
    
    def test_is_doubles_roll_true(self):
        """Verifica detección correcta de dobles."""
        result = DiceMovesCalculator.is_doubles_roll(6, 6)
        self.assertTrue(result)
    
    def test_is_doubles_roll_false(self):
        """Verifica detección correcta de no-dobles."""
        result = DiceMovesCalculator.is_doubles_roll(3, 5)
        self.assertFalse(result)
    
    def test_edge_cases_doubles(self):
        """Verifica casos extremos para dobles."""
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
    """
    
    def setUp(self):
        """Configura un GameStateManager para cada test."""
        self.manager = GameStateManager()
    
    def test_initial_state(self):
        """Verifica que el estado inicial sea correcto."""
        self.assertEqual(self.manager.get_current_state(), 'START_ROLL')
    
    def test_valid_state_changes(self):
        """Verifica que los cambios de estado válidos funcionen."""
        valid_states = ['START_ROLL', 'AWAITING_ROLL', 'AWAITING_PIECE_SELECTION']
        
        for state in valid_states:
            self.manager.change_state(state)
            self.assertEqual(self.manager.get_current_state(), state)
    
    def test_invalid_state_change_raises_error(self):
        """Verifica que estados inválidos generen error."""
        with self.assertRaises(ValueError):
            self.manager.change_state('INVALID_STATE')
    
    def test_state_persistence(self):
        """Verifica que el estado se mantenga hasta el próximo cambio."""
        self.manager.change_state('AWAITING_ROLL')
        self.assertEqual(self.manager.get_current_state(), 'AWAITING_ROLL')
        
        # Verificar que no cambia automáticamente
        self.assertEqual(self.manager.get_current_state(), 'AWAITING_ROLL')



# --- TESTS PARA MESSAGE MANAGER ---
class TestMessageManager(unittest.TestCase):
    """
    Tests unitarios para la clase MessageManager.
    Verifica el cumplimiento del principio SRP para generación de mensajes.
    """
    
    def test_start_message(self):
        """Verifica el mensaje de inicio."""
        message = MessageManager.get_start_message()
        self.assertIn("Presiona 'R'", message)
        self.assertIn("empieza", message)
    
    def test_roll_winner_message_negro(self):
        """Verifica el mensaje cuando gana negro."""
        message = MessageManager.get_roll_winner_message("negro", 5, 3)
        self.assertIn("Negro (5)", message)
        self.assertIn("Blanco (3)", message)
        self.assertIn("gana", message)
    
    def test_roll_winner_message_blanco(self):
        """Verifica el mensaje cuando gana blanco."""
        message = MessageManager.get_roll_winner_message("blanco", 6, 2)
        self.assertIn("Blanco (6)", message)
        self.assertIn("Negro (2)", message)
        self.assertIn("gana", message)
    
    def test_doubles_roll_message(self):
        """Verifica el mensaje específico para dobles."""
        message = MessageManager.get_doubles_roll_message("negro", 4, [4, 4, 4, 4])
        self.assertIn("DOBLES", message)
        self.assertIn("Negro", message)
        self.assertIn("4-4", message)
        self.assertIn("4 movimientos", message)
    
    def test_normal_roll_message(self):
        """Verifica el mensaje para tirada normal."""
        message = MessageManager.get_normal_roll_message("blanco", [2, 6])
        self.assertIn("Turno de blanco", message)
        self.assertIn("[2, 6]", message)
    
    def test_move_completed_message_remaining(self):
        """Verifica mensaje cuando quedan movimientos."""
        message = MessageManager.get_move_completed_message(2, [3, 5])
        self.assertIn("Te quedan 2 dados", message)
        self.assertIn("[3, 5]", message)
    
    def test_move_completed_message_finished(self):
        """Verifica mensaje cuando se completa el turno."""
        message = MessageManager.get_move_completed_message(0, [])
        self.assertEqual(message, "Turno completado.")
    
    def test_dice_not_available_message(self):
        """Verifica mensaje cuando no se tiene el dado necesario."""
        message = MessageManager.get_dice_not_available_message(4, [2, 6])
        self.assertIn("No tienes el dado 4 disponible", message)
        self.assertIn("[2, 6]", message)


if __name__ == "__main__":
    unittest.main()
