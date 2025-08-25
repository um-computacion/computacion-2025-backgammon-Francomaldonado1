import unittest
from Backgammon.Core.Board import Board


class TestTablero(unittest.TestCase):
    def setUp(self):
        """Crea un tablero vacío antes de cada test."""
        self.tablero = Board()

    def test_inicializacion_vacia(self):
        """El tablero debe iniciar con todos los puntos vacíos."""
        for i in range(1, 25):
            self.assertTrue(self.tablero.esta_vacio(i))
            self.assertIsNone(self.tablero.obtener_estado_punto(i))

    def test_colocar_ficha_en_punto_vacio(self):
        """Colocar una ficha en un punto vacío debe registrarla correctamente."""
        self.tablero.colocar_ficha(1, "rojo", 1)
        estado = self.tablero.obtener_estado_punto(1)
        self.assertEqual(estado, ["rojo", 1])

    def test_agregar_fichas_mismo_color(self):
        """Se deben poder apilar fichas del mismo color en un punto."""
        self.tablero.colocar_ficha(5, "azul", 2)
        self.tablero.colocar_ficha(5, "azul", 3)
        estado = self.tablero.obtener_estado_punto(5)
        self.assertEqual(estado, ["azul", 5])

    def test_error_mezclar_colores(self):
        """Intentar colocar fichas de distinto color en un punto debe dar error."""
        self.tablero.colocar_ficha(10, "rojo", 1)
        with self.assertRaises(ValueError):
            self.tablero.colocar_ficha(10, "azul", 1)

    def test_remover_fichas_correctamente(self):
        """Remover fichas debe actualizar la cantidad en el punto."""
        self.tablero.colocar_ficha(8, "rojo", 3)
        self.tablero.remover_ficha(8, 2)
        estado = self.tablero.obtener_estado_punto(8)
        self.assertEqual(estado, ["rojo", 1])

    def test_remover_todas_las_fichas(self):
        """Si se quitan todas las fichas, el punto debe quedar vacío."""
        self.tablero.colocar_ficha(12, "azul", 2)
        self.tablero.remover_ficha(12, 2)
        self.assertTrue(self.tablero.esta_vacio(12))
        self.assertIsNone(self.tablero.obtener_estado_punto(12))

    def test_error_remover_de_punto_vacio(self):
        """Quitar fichas de un punto vacío debe dar error."""
        with self.assertRaises(ValueError):
            self.tablero.remover_ficha(3, 1)

    def test_error_remover_mas_de_lo_existente(self):
        """Quitar más fichas de las que hay debe dar error."""
        self.tablero.colocar_ficha(20, "rojo", 1)
        with self.assertRaises(ValueError):
            self.tablero.remover_ficha(20, 5)

    def test_str_tablero_vacio(self):
        """La representación de un tablero vacío debe mostrar 'vacío' en todos los puntos."""
        representacion = str(self.tablero)
        self.assertIn("1: vacío", representacion)
        self.assertIn("24: vacío", representacion)
        # Contamos que aparezca 24 veces la palabra vacío
        self.assertEqual(representacion.count("vacío"), 24)


if __name__ == "__main__":
    unittest.main()
