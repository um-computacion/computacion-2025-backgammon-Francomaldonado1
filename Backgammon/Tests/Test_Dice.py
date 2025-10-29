import unittest
from unittest.mock import patch
from Backgammon.Core.Dice import Dice


class TestDiceFunctionality(unittest.TestCase):
    """Tests de funcionalidad completa para Dice."""
    
    def setUp(self):
        """Crea instancia de dados para cada test."""
        self.dados = Dice()
    
    def test_inicializacion_sin_valores(self):
        """
        Verifica inicialización correcta sin tirada.
        
        SOLID: SRP - Estado inicial consistente.
        """
        self.assertIsNone(self.dados.obtener_dado1())
        self.assertIsNone(self.dados.obtener_dado2())
        self.assertEqual(self.dados.obtener_valores(), (None, None))
        self.assertFalse(self.dados.han_sido_tirados())
    
    @patch('random.randint')
    def test_tirar_genera_valores_validos(self, mock_randint):
        """
        Verifica que tirar genera valores entre 1 y 6.
        
        SOLID: SRP - Solo genera números aleatorios.
        """
        mock_randint.side_effect = [3, 5]
        self.dados.tirar()
        
        self.assertEqual(self.dados.obtener_dado1(), 3)
        self.assertEqual(self.dados.obtener_dado2(), 5)
        self.assertEqual(self.dados.obtener_valores(), (3, 5))
        self.assertTrue(self.dados.han_sido_tirados())
    
    @patch('random.randint')
    def test_es_doble_detecta_correctamente(self, mock_randint):
        """
        Verifica detección correcta de dobles.
        
        SOLID: SRP - Comparación simple sin lógica de juego.
        """
        # Caso doble
        mock_randint.side_effect = [4, 4]
        self.dados.tirar()
        self.assertTrue(self.dados.es_doble())
        
        # Caso no doble
        self.dados.reiniciar()
        mock_randint.side_effect = [2, 6]
        self.dados.tirar()
        self.assertFalse(self.dados.es_doble())
    
    def test_es_doble_sin_tirar_error(self):
        """
        Verifica error al consultar doble sin tirar.
        
        SOLID: ISP - Validación de estado apropiada.
        """
        with self.assertRaises(ValueError) as context:
            self.dados.es_doble()
        self.assertIn("No se han tirado", str(context.exception))
    
    @patch('random.randint')
    def test_reiniciar_vuelve_estado_inicial(self, mock_randint):
        """
        Verifica que reiniciar restaura estado inicial.
        
        SOLID: SRP - Gestión simple de estado.
        """
        mock_randint.side_effect = [5, 5]
        self.dados.tirar()
        self.assertTrue(self.dados.han_sido_tirados())
        
        self.dados.reiniciar()
        self.assertIsNone(self.dados.obtener_dado1())
        self.assertIsNone(self.dados.obtener_dado2())
        self.assertFalse(self.dados.han_sido_tirados())
    
    @patch('random.randint')
    def test_str_representation_todos_estados(self, mock_randint):
        """
        Verifica representación string en todos los estados.
        
        SOLID: ISP - Interfaz para debugging.
        """
        # Sin tirar
        self.assertEqual(str(self.dados), "Dados sin tirar")
        
        # Tirada normal
        mock_randint.side_effect = [2, 5]
        self.dados.tirar()
        self.assertEqual(str(self.dados), "Dados: 2, 5")
        
        # Dobles
        self.dados.reiniciar()
        mock_randint.side_effect = [6, 6]
        self.dados.tirar()
        self.assertIn("¡Doble!", str(self.dados))
    
    @patch('random.randint')
    def test_tiradas_multiples_sobrescriben(self, mock_randint):
        """
        Verifica que tiradas múltiples sobrescriben valores.
        
        SOLID: SRP - Comportamiento predecible.
        """
        mock_randint.side_effect = [1, 2, 3, 4]
        
        self.dados.tirar()
        self.assertEqual(self.dados.obtener_valores(), (1, 2))
        
        self.dados.tirar()
        self.assertEqual(self.dados.obtener_valores(), (3, 4))
    
    def test_set_dados_para_test(self):
        """
        Verifica método de inyección para testing.
        
        SOLID: DIP - Permite testing sin dependencias de random.
        """
        self.dados.set_dados_para_test(4, 6)
        
        self.assertEqual(self.dados.obtener_dado1(), 4)
        self.assertEqual(self.dados.obtener_dado2(), 6)
        self.assertTrue(self.dados.han_sido_tirados())
        self.assertFalse(self.dados.es_doble())
    
    @patch('random.randint')
    def test_todos_valores_posibles(self, mock_randint):
        """
        Verifica que genera todos los valores de 1 a 6.
        
        SOLID: SRP - Cobertura completa del comportamiento.
        """
        for valor1 in range(1, 7):
            for valor2 in range(1, 7):
                self.dados.reiniciar()
                mock_randint.side_effect = [valor1, valor2]
                self.dados.tirar()
                
                self.assertEqual(self.dados.obtener_dado1(), valor1)
                self.assertEqual(self.dados.obtener_dado2(), valor2)
    
    @patch('random.randint')
    def test_todos_dobles_posibles(self, mock_randint):
        """
        Verifica detección de dobles para todos los valores.
        
        SOLID: SRP - Cobertura exhaustiva.
        """
        for valor in range(1, 7):
            self.dados.reiniciar()
            mock_randint.side_effect = [valor, valor]
            self.dados.tirar()
            
            self.assertTrue(self.dados.es_doble())
            self.assertEqual(self.dados.obtener_dado1(), valor)
            self.assertEqual(self.dados.obtener_dado2(), valor)


class TestDiceSOLID(unittest.TestCase):
    """Tests específicos de principios SOLID para Dice."""
    
    def setUp(self):
        """Crea instancia para cada test."""
        self.dados = Dice()
    
    def test_srp_only_generates_random_numbers(self):
        """
        SRP: Dice solo genera números aleatorios.
        
        NO calcula movimientos disponibles.
        NO valida reglas de backgammon.
        """
        # Solo tiene métodos de generación
        essential_methods = {
            'tirar', 'obtener_dado1', 'obtener_dado2',
            'obtener_valores', 'es_doble', 'han_sido_tirados',
            'reiniciar', 'set_dados_para_test'
        }
        
        public_methods = [m for m in dir(self.dados) if not m.startswith('_')]
        
        for method in essential_methods:
            self.assertIn(method, public_methods)
        
        # NO tiene lógica de backgammon
        self.assertFalse(hasattr(self.dados, 'calcular_movimientos'))
        self.assertFalse(hasattr(self.dados, 'validar_movimiento'))
        self.assertFalse(hasattr(self.dados, 'contar_movimientos_dobles'))
    
    def test_isp_focused_interface(self):
        """
        ISP: Interfaz enfocada en generación de números.
        
        No mezcla responsabilidades de dados con reglas de juego.
        """
        self.dados.set_dados_para_test(3, 5)
        
        # Puede obtener valores
        self.assertEqual(self.dados.obtener_dado1(), 3)
        self.assertEqual(self.dados.obtener_dado2(), 5)
        
        # Puede consultar si es doble
        self.assertFalse(self.dados.es_doble())
        
        # Pero NO interpreta qué hacer con esos valores
        self.assertFalse(hasattr(self.dados, 'aplicar_regla_dobles'))
    
    def test_ocp_extensible_for_variants(self):
        """
        OCP: Puede extenderse para dados especiales.
        
        Ejemplo: Dados cargados sin modificar base.
        """
        class LoadedDice(Dice):
            def __init__(self, valor_fijo):
                super().__init__()
                self.valor_fijo = valor_fijo
            
            def tirar(self):
                # --- CORRECCIÓN AQUÍ ---
                # Accedemos directamente a los atributos __dado1__ y __dado2__
                # sin la sintaxis de "name mangling".
                self.__dado1__ = self.valor_fijo
                self.__dado2__ = self.valor_fijo
        
        dados_cargados = LoadedDice(6)
        dados_cargados.tirar()
        
        self.assertEqual(dados_cargados.obtener_dado1(), 6)
        self.assertEqual(dados_cargados.obtener_dado2(), 6)
        self.assertTrue(dados_cargados.es_doble())
    
    def test_lsp_variants_substitutable(self):
        """
        LSP: Variantes de Dice pueden sustituir a Dice.
        
        Mantienen el mismo contrato.
        """
        class FairDice(Dice):
            pass
        
        def usar_dados(dados: Dice) -> bool:
            dados.tirar()
            return dados.han_sido_tirados()
        
        dados_normal = Dice()
        dados_fair = FairDice()
        
        # Ambos funcionan igual
        self.assertTrue(usar_dados(dados_normal))
        self.assertTrue(usar_dados(dados_fair))
    
    def test_dip_no_dependencies_on_game_rules(self):
        """
        DIP: Dice no depende de reglas de backgammon.
        
        Completamente independiente del dominio.
        """
        self.dados.set_dados_para_test(5, 5)
        
        # Solo reporta que es doble
        self.assertTrue(self.dados.es_doble())
        
        # NO sabe que dobles = 4 movimientos en backgammon
        # Esa lógica está en DiceMovesCalculator
        attrs = [a for a in dir(self.dados) if not a.startswith('__')]
        attrs_lower = [a.lower() for a in attrs]
        
        self.assertNotIn('movimientos', ' '.join(attrs_lower))
        self.assertNotIn('backgammon', ' '.join(attrs_lower))
    
    def test_dip_testable_without_mocks(self):
        """
        DIP: Testing simple sin mocks por su independencia.
        
        set_dados_para_test permite inyección de dependencias.
        """
        self.dados.set_dados_para_test(3, 6)
        
        # Testing directo sin mocks
        self.assertEqual(self.dados.obtener_dado1(), 3)
        self.assertEqual(self.dados.obtener_dado2(), 6)
        self.assertFalse(self.dados.es_doble())

if __name__ == "__main__":
    unittest.main()

