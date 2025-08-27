import unittest
from Backgammon.Core.Player import Player
from Backgammon.Core.Checker import Checker
from Backgammon.Core.Dice import Dice


class TestPlayer(unittest.TestCase):

    def setUp(self):
        """Crea un jugador de prueba antes de cada test."""
        self.player = Player(nombre="Alice", color="blanco")

    def test_inicializacion_jugador(self):
        """El jugador debe inicializarse con nombre, color, 15 fichas y un objeto Dice."""
        self.assertEqual(self.player.obtener_nombre(), "Alice")
        self.assertEqual(self.player.obtener_color(), "blanco")

        # Debe tener exactamente 15 fichas
        fichas = self.player.obtener_fichas()
        self.assertEqual(len(fichas), 15)

        # Todas las fichas deben ser instancias de Checker y del mismo color
        for ficha in fichas:
            self.assertIsInstance(ficha, Checker)
            self.assertEqual(ficha.obtener_color(), "blanco")

        # Debe tener un objeto de tipo Dice
        self.assertIsInstance(self.player.obtener_dados(), Dice)

    def test_obtener_nombre(self):
        """Probar que se devuelve correctamente el nombre del jugador."""
        self.assertEqual(self.player.obtener_nombre(), "Alice")

    def test_obtener_color(self):
        """Probar que se devuelve correctamente el color del jugador."""
        self.assertEqual(self.player.obtener_color(), "blanco")

    def test_obtener_fichas(self):
        """Probar que obtener_fichas devuelve una lista de 15 Checkers del color correcto."""
        fichas = self.player.obtener_fichas()
        self.assertEqual(len(fichas), 15)
        self.assertTrue(all(isinstance(f, Checker) for f in fichas))
        self.assertTrue(all(f.obtener_color() == "blanco" for f in fichas))

    def test_obtener_dados(self):
        """Probar que obtener_dados devuelve un objeto de tipo Dice."""
        dados = self.player.obtener_dados()
        self.assertIsInstance(dados, Dice)

    def test_str(self):
        """Probar que la representación en string del jugador es la esperada."""
        representacion = str(self.player)
        self.assertIn("Alice", representacion)
        self.assertIn("blanco", representacion)


if __name__ == "__main__":
    unittest.main()
