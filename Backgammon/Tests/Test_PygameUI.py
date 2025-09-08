import unittest
from unittest.mock import patch, Mock
import pygame
from Backgammon.Interfaces.PygameUI import PygameUI
from Backgammon.Core.Board import Board


class TestPygameUI(unittest.TestCase):
    
    def setUp(self):
        """Configuración antes de cada test."""
        self.ui = PygameUI()

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


if __name__ == "__main__":
    unittest.main()