import unittest
from unittest.mock import patch
import pygame
from Backgammon.Interfaces.PygameUI import PygameUI


class TestPygameUI(unittest.TestCase):
    def setUp(self):
        self.ui = PygameUI()

    def test_inicializacion(self):
        """El objeto debe inicializar con los atributos principales."""
        attrs = [
            "__screen__", "__clock__", "__running__",
            "__white__", "__black__", "__brown_light__",
            "__brown_dark__", "__board_border__", "__bar_color__"
        ]
        for attr in attrs:
            self.assertTrue(hasattr(self.ui, f"_PygameUI{attr}"))

    @patch("pygame.draw.polygon")
    def test_draw_triangle_point_down(self, mock_polygon):
        """Debe dibujar un triángulo apuntando hacia abajo."""
        self.ui._PygameUI__screen__ = pygame.Surface((1600, 900))
        self.ui._PygameUI__draw_triangle_point(10, 20, 30, 40, (255, 0, 0), pointing_down=True)
        self.assertTrue(mock_polygon.called)

    @patch("pygame.draw.polygon")
    def test_draw_triangle_point_up(self, mock_polygon):
        """Debe dibujar un triángulo apuntando hacia arriba."""
        self.ui._PygameUI__screen__ = pygame.Surface((1600, 900))
        self.ui._PygameUI__draw_triangle_point(10, 20, 30, 40, (0, 255, 0), pointing_down=False)
        self.assertTrue(mock_polygon.called)

    @patch("pygame.event.get")
    def test_handle_event_quit(self, mock_get):
        """El evento QUIT debe detener el loop."""
        self.ui._PygameUI__running__ = True
        mock_get.return_value = [pygame.event.Event(pygame.QUIT)]
        self.ui._PygameUI__handle_events()
        self.assertFalse(self.ui._PygameUI__running__)

    @patch("pygame.event.get")
    def test_handle_event_escape(self, mock_get):
        """Presionar ESC debe detener el loop."""
        self.ui._PygameUI__running__ = True
        mock_get.return_value = [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE)]
        self.ui._PygameUI__handle_events()
        self.assertFalse(self.ui._PygameUI__running__)


if __name__ == "__main__":
    unittest.main()
