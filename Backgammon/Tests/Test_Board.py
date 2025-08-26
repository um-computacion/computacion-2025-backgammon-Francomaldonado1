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
        self.assertEqual(representacion.count("vacío"), 24)

    def test_mover_ficha_a_punto_vacio(self):
        """Mover una ficha a un punto vacío debe colocarla allí correctamente."""
        self.tablero.colocar_ficha(5, "rojo", 2)
        self.tablero.mover_ficha(5, 10, "rojo")
        self.assertEqual(self.tablero.obtener_estado_punto(5), ["rojo", 1])
        self.assertEqual(self.tablero.obtener_estado_punto(10), ["rojo", 1])

    def test_mover_ficha_apilar_mismo_color(self):
        """Mover una ficha a un punto con fichas del mismo color debe apilarlas."""
        self.tablero.colocar_ficha(8, "azul", 3)
        self.tablero.colocar_ficha(15, "azul", 2)
        self.tablero.mover_ficha(8, 15, "azul")
        self.assertEqual(self.tablero.obtener_estado_punto(8), ["azul", 2])
        self.assertEqual(self.tablero.obtener_estado_punto(15), ["azul", 3])

    def test_mover_ficha_comer_contraria(self):
        """Mover una ficha a un punto con UNA ficha contraria debe comerla y enviarla a la barra."""
        self.tablero.colocar_ficha(12, "rojo", 1)
        self.tablero.colocar_ficha(18, "azul", 1)
        self.tablero.mover_ficha(12, 18, "rojo")
        self.assertTrue(self.tablero.esta_vacio(12))
        self.assertEqual(self.tablero.obtener_estado_punto(18), ["rojo", 1])
        self.assertEqual(self.tablero.get_barra(), {"azul": 1})

    def test_mover_ficha_bloqueado_por_multiples_contrarias(self):
        """Intentar mover a un punto con 2+ fichas contrarias debe dar error."""
        self.tablero.colocar_ficha(6, "rojo", 1)
        self.tablero.colocar_ficha(14, "azul", 2)
        with self.assertRaises(ValueError) as context:
            self.tablero.mover_ficha(6, 14, "rojo")
        self.assertIn("bloqueado", str(context.exception))
        self.assertEqual(self.tablero.obtener_estado_punto(6), ["rojo", 1])
        self.assertEqual(self.tablero.obtener_estado_punto(14), ["azul", 2])

    def test_error_mover_desde_punto_vacio(self):
        """Intentar mover desde un punto vacío debe dar error."""
        with self.assertRaises(ValueError) as context:
            self.tablero.mover_ficha(7, 13, "rojo")
        self.assertIn("No hay fichas del color indicado en el origen", str(context.exception))

    def test_error_mover_color_incorrecto(self):
        """Intentar mover una ficha de color diferente al especificado debe dar error."""
        self.tablero.colocar_ficha(9, "azul", 2)
        with self.assertRaises(ValueError) as context:
            self.tablero.mover_ficha(9, 16, "rojo")
        self.assertIn("No hay fichas del color indicado en el origen", str(context.exception))

    def test_mover_ultima_ficha_del_punto(self):
        """Mover la última ficha de un punto debe dejarlo vacío."""
        self.tablero.colocar_ficha(4, "rojo", 1)
        self.tablero.mover_ficha(4, 11, "rojo")
        self.assertTrue(self.tablero.esta_vacio(4))
        self.assertEqual(self.tablero.obtener_estado_punto(11), ["rojo", 1])

    def test_enviar_a_barra_color_nuevo(self):
        """Enviar una ficha a la barra cuando no hay fichas de ese color debe crear la entrada."""
        self.tablero.enviar_a_barra("verde")
        self.assertEqual(self.tablero.get_barra(), {"verde": 1})

    def test_enviar_a_barra_color_existente(self):
        """Enviar una ficha a la barra cuando ya hay fichas de ese color debe incrementar la cantidad."""
        self.tablero.enviar_a_barra("azul")
        self.tablero.enviar_a_barra("azul")
        self.tablero.enviar_a_barra("rojo")
        self.assertEqual(self.tablero.get_barra(), {"azul": 2, "rojo": 1})

    def test_enviar_a_barra_multiples_colores(self):
        """Se pueden enviar fichas de diferentes colores a la barra."""
        self.tablero.enviar_a_barra("blanco")
        self.tablero.enviar_a_barra("negro")
        self.tablero.enviar_a_barra("blanco")
        esperado = {"blanco": 2, "negro": 1}
        self.assertEqual(self.tablero.get_barra(), esperado)

    def test_sacar_ficha_color_nuevo(self):
        """Enviar una ficha a la casa cuando no hay fichas de ese color debe crear la entrada."""
        self.tablero.sacar_ficha("amarillo")
        self.assertEqual(self.tablero.get_casa(), {"amarillo": 1})

    def test_sacar_ficha_color_existente(self):
        """Enviar una ficha a la casa cuando ya hay fichas de ese color debe incrementar la cantidad."""
        self.tablero.sacar_ficha("negro")
        self.tablero.sacar_ficha("negro")
        self.tablero.sacar_ficha("blanco")
        self.assertEqual(self.tablero.get_casa(), {"negro": 2, "blanco": 1})

    def test_sacar_ficha_multiples_colores(self):
        """Se pueden sacar fichas de diferentes colores a la casa."""
        self.tablero.sacar_ficha("rojo")
        self.tablero.sacar_ficha("azul")
        self.tablero.sacar_ficha("rojo")
        self.tablero.sacar_ficha("azul")
        self.tablero.sacar_ficha("verde")
        esperado = {"rojo": 2, "azul": 2, "verde": 1}
        self.assertEqual(self.tablero.get_casa(), esperado)

    def test_integracion_mover_comer_y_barra(self):
        """Test de integración: mover ficha, comer contraria y verificar que va a la barra."""
        self.tablero.colocar_ficha(1, "blanco", 2)
        self.tablero.colocar_ficha(7, "negro", 1)
        self.tablero.mover_ficha(1, 7, "blanco")
        self.assertEqual(self.tablero.obtener_estado_punto(1), ["blanco", 1])
        self.assertEqual(self.tablero.obtener_estado_punto(7), ["blanco", 1])
        self.assertEqual(self.tablero.get_barra(), {"negro": 1})


if __name__ == "__main__":
    unittest.main()
