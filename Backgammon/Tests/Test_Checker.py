import unittest
from Backgammon.Core.Checker import Checker


class TestChecker(unittest.TestCase):

    def setUp(self):
        """Configura un entorno básico para cada test."""
        self.ficha_blanca = Checker("blanco", 5)
        self.ficha_negra = Checker("negro")

    def test_creacion_ficha_con_posicion(self):
        """Verifica que una ficha se cree correctamente con posición inicial."""
        self.assertEqual(self.ficha_blanca.obtener_color(), "blanco")
        self.assertEqual(self.ficha_blanca.obtener_posicion(), 5)
        self.assertFalse(self.ficha_blanca.esta_fuera())

    def test_creacion_ficha_sin_posicion(self):
        """Verifica que una ficha sin posición inicial esté fuera del tablero."""
        self.assertEqual(self.ficha_negra.obtener_color(), "negro")
        self.assertIsNone(self.ficha_negra.obtener_posicion())
        self.assertTrue(self.ficha_negra.esta_fuera())

    def test_establecer_posicion(self):
        """Verifica que se pueda actualizar la posición de la ficha."""
        self.ficha_negra.establecer_posicion(12)
        self.assertEqual(self.ficha_negra.obtener_posicion(), 12)
        self.assertFalse(self.ficha_negra.esta_fuera())

    def test_establecer_posicion_fuera(self):
        """Verifica que se pueda poner la ficha fuera del tablero."""
        self.ficha_blanca.establecer_posicion(None)
        self.assertIsNone(self.ficha_blanca.obtener_posicion())
        self.assertTrue(self.ficha_blanca.esta_fuera())

    def test_str(self):
        """Verifica la representación en string de la ficha."""
        self.assertEqual(str(self.ficha_blanca), "Ficha(color=blanco, posicion=5)")
        self.assertEqual(str(self.ficha_negra), "Ficha(color=negro, posicion=None)")


if __name__ == "__main__":
    unittest.main()
