import unittest
from Backgammon.Core.Player import Player
from Backgammon.Core.Checker import Checker
from Backgammon.Core.Dice import Dice


class TestPlayerFunctionality(unittest.TestCase):
    """Tests de funcionalidad completa para Player."""
    
    def test_inicializacion_completa(self):
        """
        Verifica inicialización correcta del jugador.
        
        SOLID: SRP - Constructor inicializa recursos del jugador.
        """
        jugador = Player('Ana', 'blanco')
        
        self.assertEqual(jugador.obtener_nombre(), 'Ana')
        self.assertEqual(jugador.obtener_color(), 'blanco')
        
        # Debe tener 15 fichas
        fichas = jugador.obtener_fichas()
        self.assertEqual(len(fichas), 15)
        
        # Todas del mismo color
        for ficha in fichas:
            self.assertIsInstance(ficha, Checker)
            self.assertEqual(ficha.obtener_color(), 'blanco')
        
        # Debe tener dados
        dados = jugador.obtener_dados()
        self.assertIsInstance(dados, Dice)
    
    def test_fichas_independientes(self):
        """
        Verifica que cada ficha es una instancia independiente.
        
        SOLID: SRP - Gestión correcta de recursos.
        """
        jugador = Player('Carlos', 'negro')
        fichas = jugador.obtener_fichas()
        
        # Modificar una ficha no afecta a las demás
        fichas[0].establecer_posicion(5)
        fichas[1].establecer_posicion(10)
        
        self.assertEqual(fichas[0].obtener_posicion(), 5)
        self.assertEqual(fichas[1].obtener_posicion(), 10)
        self.assertIsNone(fichas[2].obtener_posicion())
    
    def test_dados_propios_jugador(self):
        """
        Verifica que cada jugador tiene sus propios dados.
        
        SOLID: DIP - Composición con Dice.
        """
        jugador1 = Player('J1', 'blanco')
        jugador2 = Player('J2', 'negro')
        
        dados1 = jugador1.obtener_dados()
        dados2 = jugador2.obtener_dados()
        
        # Son instancias diferentes
        self.assertIsNot(dados1, dados2)
        
        # Modificar uno no afecta al otro
        dados1.set_dados_para_test(3, 5)
        dados2.set_dados_para_test(6, 6)
        
        self.assertEqual(dados1.obtener_dado1(), 3)
        self.assertEqual(dados2.obtener_dado1(), 6)
    
    def test_str_representation(self):
        """
        Verifica representación en string.
        
        SOLID: ISP - Interfaz mínima para debugging.
        """
        jugador = Player('TestPlayer', 'blanco')
        repr_str = str(jugador)
        
        self.assertIn('TestPlayer', repr_str)
        self.assertIn('blanco', repr_str)
    
    def test_nombre_y_color_inmutables(self):
        """
        Verifica que nombre y color no cambian.
        
        SOLID: SRP - Identidad del jugador es estable.
        """
        jugador = Player('Jugador1', 'negro')
        
        nombre_inicial = jugador.obtener_nombre()
        color_inicial = jugador.obtener_color()
        
        # Usar dados no cambia identidad
        dados = jugador.obtener_dados()
        dados.tirar()
        
        self.assertEqual(jugador.obtener_nombre(), nombre_inicial)
        self.assertEqual(jugador.obtener_color(), color_inicial)


class TestPlayerSOLID(unittest.TestCase):
    """Tests específicos de principios SOLID para Player."""
    
    def test_srp_represents_player_identity_and_resources(self):
        """
        SRP: Player representa identidad y recursos.
        
        NO gestiona:
        - Turnos (GameStateManager)
        - Estrategia (Interfaz/IA)
        - Validación (Validators)
        """
        jugador = Player('Test', 'blanco')
        
        # Tiene métodos de identidad y recursos
        self.assertTrue(hasattr(jugador, 'obtener_nombre'))
        self.assertTrue(hasattr(jugador, 'obtener_color'))
        self.assertTrue(hasattr(jugador, 'obtener_fichas'))
        self.assertTrue(hasattr(jugador, 'obtener_dados'))
        
        # NO tiene lógica de juego
        self.assertFalse(hasattr(jugador, 'hacer_movimiento'))
        self.assertFalse(hasattr(jugador, 'calcular_estrategia'))
        self.assertFalse(hasattr(jugador, 'gestionar_turno'))
        self.assertFalse(hasattr(jugador, 'validar_movimiento'))
    
    def test_isp_minimal_interface_for_identity(self):
        """
        ISP: Interfaz mínima para identificación y recursos.
        
        No expone métodos innecesarios.
        """
        jugador = Player('Test', 'negro')
        
        # Métodos esenciales
        essential = {'obtener_nombre', 'obtener_color',
                    'obtener_fichas', 'obtener_dados'}
        
        public_methods = [m for m in dir(jugador) if not m.startswith('_')]
        
        for method in essential:
            self.assertIn(method, public_methods)
    
    def test_ocp_extensible_for_ai_player(self):
        """
        OCP: Puede extenderse para crear jugadores IA.
        
        Sin modificar Player base.
        """
        class AIPlayer(Player):
            def __init__(self, nombre, color, dificultad):
                super().__init__(nombre, color)
                self.dificultad = dificultad
            
            def calcular_mejor_movimiento(self, board):
                return f"Movimiento IA nivel {self.dificultad}"
        
        ia = AIPlayer('Bot', 'blanco', 'difícil')
        
        # Mantiene funcionalidad base
        self.assertEqual(ia.obtener_nombre(), 'Bot')
        self.assertEqual(ia.obtener_color(), 'blanco')
        self.assertEqual(len(ia.obtener_fichas()), 15)
        
        # Agrega funcionalidad
        self.assertIn('difícil', ia.calcular_mejor_movimiento(None))
    
    def test_ocp_extensible_for_remote_player(self):
        """
        OCP: Puede extenderse para jugadores remotos.
        
        Permite juego en red sin modificar Player.
        """
        class RemotePlayer(Player):
            def __init__(self, nombre, color, connection_id):
                super().__init__(nombre, color)
                self.connection_id = connection_id
            
            def send_move(self, move):
                return f"Sending {move} to {self.connection_id}"
        
        remoto = RemotePlayer('RemoteUser', 'negro', 'conn-abc123')
        
        self.assertEqual(remoto.obtener_nombre(), 'RemoteUser')
        self.assertEqual(remoto.connection_id, 'conn-abc123')
        self.assertIn('conn-abc123', remoto.send_move('1->5'))
    
    def test_lsp_subtypes_maintain_contract(self):
        """
        LSP: Subtipos de Player mantienen el contrato.
        
        Pueden sustituir a Player en cualquier contexto.
        """
        class EnhancedPlayer(Player):
            def get_stats(self):
                return {'wins': 0, 'losses': 0}
        
        def obtener_info(player: Player) -> str:
            return f"{player.obtener_nombre()} - {player.obtener_color()}"
        
        jugador_normal = Player('Normal', 'blanco')
        jugador_mejorado = EnhancedPlayer('Enhanced', 'negro')
        
        # Ambos funcionan igual con la función
        info1 = obtener_info(jugador_normal)
        info2 = obtener_info(jugador_mejorado)
        
        self.assertIn('Normal', info1)
        self.assertIn('Enhanced', info2)
    
    def test_dip_depends_on_abstractions(self):
        """
        DIP: Player depende de abstracciones (Checker, Dice).
        
        No de implementaciones concretas.
        """
        jugador = Player('Test', 'blanco')
        
        # Usa Checker (abstracción)
        fichas = jugador.obtener_fichas()
        self.assertIsInstance(fichas[0], Checker)
        
        # Usa Dice (abstracción)
        dados = jugador.obtener_dados()
        self.assertIsInstance(dados, Dice)
    
    def test_dip_composition_over_inheritance(self):
        """
        DIP: Usa composición (HAS-A) no herencia (IS-A).
        
        Player HAS-A Dice, no IS-A Dice.
        Player HAS-A Checkers, no IS-A Checker.
        """
        
        jugador = Player('Test', 'negro')
        
        # Composición: Player tiene dados
        self.assertTrue(hasattr(jugador, 'obtener_dados'))
        self.assertIsInstance(jugador.obtener_dados(), Dice)
        
        # No herencia: Player no es Dice ni Checker
        self.assertFalse(isinstance(jugador, Dice))
        self.assertFalse(isinstance(jugador, Checker))


if __name__ == "__main__":
    unittest.main()
