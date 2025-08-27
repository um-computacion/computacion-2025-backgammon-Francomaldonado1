import unittest
from unittest.mock import patch
from Backgammon.Core.Dice import Dice


class TestDice(unittest.TestCase):
    def setUp(self):
        """Crea una instancia de dados antes de cada test."""
        self.dados = Dice()

    def test_inicializacion_sin_tirar(self):
        """Los dados deben iniciar sin valores hasta que se tiren."""
        self.assertIsNone(self.dados.obtener_dado1())
        self.assertIsNone(self.dados.obtener_dado2())
        self.assertEqual(self.dados.obtener_valores(), (None, None))
        self.assertFalse(self.dados.han_sido_tirados())

    def test_str_dados_sin_tirar(self):
        """La representación de dados sin tirar debe ser descriptiva."""
        resultado = str(self.dados)
        self.assertEqual(resultado, "Dados sin tirar")

    def test_error_es_doble_sin_tirar(self):
        """Consultar si es doble sin haber tirado debe dar error."""
        with self.assertRaises(ValueError) as context:
            self.dados.es_doble()
        
        self.assertIn("No se han tirado los dados todavía", str(context.exception))

    @patch('random.randint')
    def test_tirar_dados_valores_validos(self, mock_randint):
        """Tirar dados debe generar valores entre 1 y 6."""
        mock_randint.side_effect = [3, 5]  # Simular tirada de 3 y 5
        
        self.dados.tirar()
        
        self.assertEqual(self.dados.obtener_dado1(), 3)
        self.assertEqual(self.dados.obtener_dado2(), 5)
        self.assertEqual(self.dados.obtener_valores(), (3, 5))
        self.assertTrue(self.dados.han_sido_tirados())

    @patch('random.randint')
    def test_tirar_dados_doble(self, mock_randint):
        """Tirar dados iguales debe detectarse como doble."""
        mock_randint.side_effect = [4, 4]  # Simular doble 4
        
        self.dados.tirar()
        
        self.assertEqual(self.dados.obtener_dado1(), 4)
        self.assertEqual(self.dados.obtener_dado2(), 4)
        self.assertTrue(self.dados.es_doble())

    @patch('random.randint')
    def test_tirar_dados_no_doble(self, mock_randint):
        """Tirar dados diferentes no debe ser doble."""
        mock_randint.side_effect = [2, 6]  # Simular 2 y 6
        
        self.dados.tirar()
        
        self.assertEqual(self.dados.obtener_dado1(), 2)
        self.assertEqual(self.dados.obtener_dado2(), 6)
        self.assertFalse(self.dados.es_doble())

    @patch('random.randint')
    def test_str_dados_tirados_normal(self, mock_randint):
        """La representación de dados tirados debe mostrar los valores."""
        mock_randint.side_effect = [1, 3]
        
        self.dados.tirar()
        resultado = str(self.dados)
        
        self.assertEqual(resultado, "Dados: 1, 3")

    @patch('random.randint')
    def test_str_dados_tirados_doble(self, mock_randint):
        """La representación de dobles debe incluir indicador especial."""
        mock_randint.side_effect = [6, 6]
        
        self.dados.tirar()
        resultado = str(self.dados)
        
        self.assertEqual(resultado, "Dados: 6, 6 (¡Doble!)")

    @patch('random.randint')
    def test_reiniciar_dados(self, mock_randint):
        """Reiniciar debe volver los dados a estado inicial."""
        mock_randint.side_effect = [2, 4]
        
        # Tirar primero
        self.dados.tirar()
        self.assertTrue(self.dados.han_sido_tirados())
        
        # Reiniciar
        self.dados.reiniciar()
        
        self.assertIsNone(self.dados.obtener_dado1())
        self.assertIsNone(self.dados.obtener_dado2())
        self.assertEqual(self.dados.obtener_valores(), (None, None))
        self.assertFalse(self.dados.han_sido_tirados())
        self.assertEqual(str(self.dados), "Dados sin tirar")

    @patch('random.randint')
    def test_error_es_doble_despues_reiniciar(self, mock_randint):
        """Consultar si es doble después de reiniciar debe dar error."""
        mock_randint.side_effect = [5, 5]
        
        # Tirar y verificar que funciona
        self.dados.tirar()
        self.assertTrue(self.dados.es_doble())
        
        # Reiniciar y verificar que da error
        self.dados.reiniciar()
        with self.assertRaises(ValueError):
            self.dados.es_doble()

    @patch('random.randint')
    def test_tirar_multiple_veces(self, mock_randint):
        """Tirar múltiples veces debe actualizar los valores."""
        mock_randint.side_effect = [1, 2, 3, 4]  # Primera: 1,2  Segunda: 3,4
        
        # Primera tirada
        self.dados.tirar()
        self.assertEqual(self.dados.obtener_valores(), (1, 2))
        
        # Segunda tirada debe sobrescribir
        self.dados.tirar()
        self.assertEqual(self.dados.obtener_valores(), (3, 4))

    @patch('random.randint')
    def test_todos_los_valores_posibles_dobles(self, mock_randint):
        """Test que verifica dobles para todos los valores del 1 al 6."""
        for valor in range(1, 7):
            with self.subTest(valor=valor):
                mock_randint.side_effect = [valor, valor]
                
                self.dados.reiniciar()
                self.dados.tirar()
                
                self.assertTrue(self.dados.es_doble())
                self.assertEqual(self.dados.obtener_dado1(), valor)
                self.assertEqual(self.dados.obtener_dado2(), valor)

    @patch('random.randint')
    def test_valores_extremos(self, mock_randint):
        """Test con valores mínimos y máximos posibles."""
        # Mínimo: 1, 1
        mock_randint.side_effect = [1, 1]
        self.dados.tirar()
        self.assertEqual(self.dados.obtener_valores(), (1, 1))
        self.assertTrue(self.dados.es_doble())
        
        # Máximo: 6, 6
        mock_randint.side_effect = [6, 6]
        self.dados.tirar()
        self.assertEqual(self.dados.obtener_valores(), (6, 6))
        self.assertTrue(self.dados.es_doble())
        
        # Combinación extrema no doble: 1, 6
        mock_randint.side_effect = [1, 6]
        self.dados.tirar()
        self.assertEqual(self.dados.obtener_valores(), (1, 6))
        self.assertFalse(self.dados.es_doble())

    @patch('random.randint')
    def test_consistencia_han_sido_tirados(self, mock_randint):
        """El método han_sido_tirados debe ser consistente con el estado."""
        # Estado inicial
        self.assertFalse(self.dados.han_sido_tirados())
        
        # Después de tirar
        mock_randint.side_effect = [3, 3]
        self.dados.tirar()
        self.assertTrue(self.dados.han_sido_tirados())
        
        # Después de reiniciar
        self.dados.reiniciar()
        self.assertFalse(self.dados.han_sido_tirados())

    def test_integracion_flujo_completo(self):
        """Test de integración del flujo completo de uso."""
        # 1. Estado inicial
        self.assertFalse(self.dados.han_sido_tirados())
        
        # 2. Tirar dados (sin mock para probar randomness real)
        self.dados.tirar()
        self.assertTrue(self.dados.han_sido_tirados())
        
        # 3. Verificar que los valores están en rango válido
        dado1 = self.dados.obtener_dado1()
        dado2 = self.dados.obtener_dado2()
        self.assertIn(dado1, range(1, 7))
        self.assertIn(dado2, range(1, 7))
        
        # 4. Verificar que es_doble no da error
        es_doble = self.dados.es_doble()  # No debería dar error
        self.assertIsInstance(es_doble, bool)
        
        # 5. Reiniciar y volver al estado inicial
        self.dados.reiniciar()
        self.assertFalse(self.dados.han_sido_tirados())


if __name__ == "__main__":
    unittest.main()