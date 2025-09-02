import unittest
from unittest.mock import Mock, patch, MagicMock
import io
import sys
from Backgammon.Interfaces.CLI import BackgammonCLI, main


class TestBackgammonCLI(unittest.TestCase):
    """
    Tests para la interfaz CLI de Backgammon.
    """
    
    def setUp(self):
        """Configuración inicial para cada test."""
        self.cli = BackgammonCLI()
        self.cli.board = Mock()
        self.cli.dados = Mock()
    
    def test_init(self):
        """Test de inicialización de BackgammonCLI."""
        cli = BackgammonCLI()
        self.assertIsNotNone(cli.board)
        self.assertIsNotNone(cli.dados)
        self.assertEqual(cli.jugador_negro, "")
        self.assertEqual(cli.jugador_blanco, "")
        self.assertEqual(cli.turno_actual, "negro")
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_iniciar_juego_con_nombres_personalizados(self, mock_print, mock_input):
        """Test de inicialización del juego con nombres personalizados."""
        # Configurar mocks
        mock_input.side_effect = ["Juan", "María", ""]  # Último input para parar el loop
        self.cli.board.inicializar_posiciones_estandar = Mock()
        self.cli.board.ha_ganado = Mock(return_value=True)  # Para terminar el loop rápidamente
        
        with patch.object(self.cli, 'mostrar_tablero'):
            self.cli.iniciar_juego()
        
        self.assertEqual(self.cli.jugador_negro, "Juan")
        self.assertEqual(self.cli.jugador_blanco, "María")
        self.cli.board.inicializar_posiciones_estandar.assert_called_once()
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_iniciar_juego_nombres_vacios(self, mock_print, mock_input):
        """Test con nombres vacíos (usa nombres por defecto)."""
        mock_input.side_effect = ["", "", ""]
        self.cli.board.inicializar_posiciones_estandar = Mock()
        self.cli.board.ha_ganado = Mock(return_value=True)
        
        with patch.object(self.cli, 'mostrar_tablero'):
            self.cli.iniciar_juego()
        
        self.assertEqual(self.cli.jugador_negro, "Jugador Negro")
        self.assertEqual(self.cli.jugador_blanco, "Jugador Blanco")
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_iniciar_juego_nombres_con_espacios(self, mock_print, mock_input):
        """Test con nombres que tienen espacios al inicio y final."""
        mock_input.side_effect = ["  Juan  ", "  María  ", ""]
        self.cli.board.inicializar_posiciones_estandar = Mock()
        self.cli.board.ha_ganado = Mock(return_value=True)
        
        with patch.object(self.cli, 'mostrar_tablero'):
            self.cli.iniciar_juego()
        
        self.assertEqual(self.cli.jugador_negro, "Juan")
        self.assertEqual(self.cli.jugador_blanco, "María")
    
    @patch('builtins.print')
    def test_mostrar_tablero_completo(self, mock_print):
        """Test de visualización completa del tablero."""
        # Configurar mock del board
        def mock_obtener_estado(punto):
            if punto == 1:
                return ("negro", 2)
            elif punto == 6:
                return ("blanco", 5)
            else:
                return None
        
        self.cli.board.obtener_estado_punto = Mock(side_effect=mock_obtener_estado)
        self.cli.board.get_barra = Mock(return_value={"negro": 1, "blanco": 0})
        self.cli.board.get_casa = Mock(return_value={"negro": 3, "blanco": 2})
        
        self.cli.mostrar_tablero()
        
        # Verificar que se llamaron los métodos correctos
        self.assertEqual(self.cli.board.obtener_estado_punto.call_count, 24)  # 24 puntos
        self.cli.board.get_barra.assert_called_once()
        self.cli.board.get_casa.assert_called_once()
    
    @patch('builtins.print')
    def test_mostrar_tablero_vacio(self, mock_print):
        """Test de visualización del tablero vacío."""
        self.cli.board.obtener_estado_punto = Mock(return_value=None)
        self.cli.board.get_barra = Mock(return_value={})
        self.cli.board.get_casa = Mock(return_value={})
        
        self.cli.mostrar_tablero()
        
        self.assertEqual(self.cli.board.obtener_estado_punto.call_count, 24)
    
    @patch('builtins.print')
    def test_mostrar_tablero_barra_con_fichas(self, mock_print):
        """Test de visualización con fichas en la barra."""
        self.cli.board.obtener_estado_punto = Mock(return_value=None)
        self.cli.board.get_barra = Mock(return_value={"negro": 2, "blanco": 1})
        self.cli.board.get_casa = Mock(return_value={})
        
        self.cli.mostrar_tablero()
        
        # Verificar que se muestran las fichas en barra
        calls = [str(call) for call in mock_print.call_args_list]
        barra_calls = [call for call in calls if "BARRA" in call]
        self.assertTrue(len(barra_calls) > 0)
    
    def test_loop_principal_ganador_negro(self):
        """Test del loop principal cuando gana el jugador negro."""
        self.cli.jugador_negro = "Juan"
        self.cli.board.ha_ganado = Mock(side_effect=[False, True])  # Gana en el segundo turno
        
        with patch.object(self.cli, 'turno_jugador') as mock_turno:
            with patch('builtins.print') as mock_print:
                self.cli.loop_principal()
        
        mock_turno.assert_called_once()
        self.cli.board.ha_ganado.assert_called()
    
    def test_loop_principal_ganador_blanco(self):
        """Test del loop principal cuando gana el jugador blanco."""
        self.cli.jugador_blanco = "María"
        self.cli.board.ha_ganado = Mock(side_effect=lambda color: color == "blanco")
        
        with patch.object(self.cli, 'turno_jugador') as mock_turno:
            with patch('builtins.print') as mock_print:
                self.cli.loop_principal()
        
        self.cli.board.ha_ganado.assert_called()
    
    def test_loop_principal_cambio_turnos(self):
        """Test del cambio de turnos en el loop principal."""
        self.cli.board.ha_ganado = Mock(side_effect=[False, False, True])  # Gana en el tercer turno
        
        with patch.object(self.cli, 'turno_jugador') as mock_turno:
            with patch('builtins.print'):
                self.cli.loop_principal()
        
        # Debería haber 2 turnos antes de ganar
        self.assertEqual(mock_turno.call_count, 2)
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_turno_jugador_sin_movimientos_posibles(self, mock_print, mock_input):
        """Test de turno cuando no hay movimientos posibles."""
        mock_input.return_value = ""
        self.cli.jugador_negro = "Juan"
        self.cli.dados.tirar = Mock()
        self.cli.dados.reiniciar = Mock()
        self.cli.dados.__str__ = Mock(return_value="[3,4]")
        self.cli.board.obtener_movimientos_posibles = Mock(return_value=[])
        
        self.cli.turno_jugador()
        
        self.cli.dados.tirar.assert_called_once()
        self.cli.dados.reiniciar.assert_called_once()
        self.cli.board.obtener_movimientos_posibles.assert_called_once()
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_turno_jugador_con_dobles(self, mock_print, mock_input):
        """Test de turno con dados dobles."""
        mock_input.return_value = ""
        self.cli.jugador_negro = "Juan"
        self.cli.dados.tirar = Mock()
        self.cli.dados.reiniciar = Mock()
        self.cli.dados.__str__ = Mock(return_value="[6,6]")
        self.cli.dados.es_doble = Mock(return_value=True)
        self.cli.board.obtener_movimientos_posibles = Mock(return_value=[1, 2, 3])
        
        with patch.object(self.cli, 'manejar_dobles') as mock_dobles:
            self.cli.turno_jugador()
        
        mock_dobles.assert_called_once()
        self.cli.dados.reiniciar.assert_called_once()
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_turno_jugador_movimientos_normales(self, mock_print, mock_input):
        """Test de turno con movimientos normales (no dobles)."""
        mock_input.return_value = ""
        self.cli.jugador_blanco = "María"
        self.cli.turno_actual = "blanco"
        self.cli.dados.tirar = Mock()
        self.cli.dados.reiniciar = Mock()
        self.cli.dados.__str__ = Mock(return_value="[3,4]")
        self.cli.dados.es_doble = Mock(return_value=False)
        self.cli.board.obtener_movimientos_posibles = Mock(return_value=[1, 2, 3])
        
        with patch.object(self.cli, 'manejar_movimientos_normales') as mock_normales:
            self.cli.turno_jugador()
        
        mock_normales.assert_called_once()
        self.cli.dados.reiniciar.assert_called_once()
    
    def test_mostrar_movimientos_disponibles_con_movimientos(self):
        """Test cuando hay movimientos disponibles."""
        self.cli.board.obtener_movimientos_posibles = Mock(return_value=[1, 2, 0])
        
        with patch('builtins.print') as mock_print:
            resultado = self.cli.mostrar_movimientos_disponibles()
        
        self.assertTrue(resultado)
        self.cli.board.obtener_movimientos_posibles.assert_called_once()
    
    def test_mostrar_movimientos_disponibles_sin_movimientos(self):
        """Test cuando no hay movimientos disponibles."""
        self.cli.board.obtener_movimientos_posibles = Mock(return_value=[])
        
        with patch('builtins.print'):
            resultado = self.cli.mostrar_movimientos_disponibles()
        
        self.assertFalse(resultado)
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_manejar_movimientos_normales_opcion_1(self, mock_print, mock_input):
        """Test de movimientos normales eligiendo opción 1 (movimiento simple)."""
        mock_input.side_effect = ["1", "3"]  # Opción 1, luego pasar turno
        self.cli.board.obtener_movimientos_posibles = Mock(side_effect=[[1, 2, 3], []])
        
        with patch.object(self.cli, 'realizar_movimiento_simple', return_value=True) as mock_simple:
            self.cli.manejar_movimientos_normales()
        
        mock_simple.assert_called_once()
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_manejar_movimientos_normales_opcion_2(self, mock_print, mock_input):
        """Test de movimientos normales eligiendo opción 2 (movimiento doble)."""
        mock_input.side_effect = ["2"]
        self.cli.board.obtener_movimientos_posibles = Mock(return_value=[1, 2, 3])
        
        with patch.object(self.cli, 'realizar_movimiento_doble', return_value=True) as mock_doble:
            self.cli.manejar_movimientos_normales()
        
        mock_doble.assert_called_once()
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_manejar_movimientos_normales_pasar_turno(self, mock_print, mock_input):
        """Test de movimientos normales eligiendo pasar turno."""
        mock_input.side_effect = ["3"]
        self.cli.board.obtener_movimientos_posibles = Mock(return_value=[1, 2, 3])
        
        self.cli.manejar_movimientos_normales()
        
        # No debería llamar a ningún método de movimiento
        self.cli.board.obtener_movimientos_posibles.assert_called_once()
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_manejar_movimientos_normales_opcion_invalida(self, mock_print, mock_input):
        """Test con opción inválida seguida de opción válida."""
        mock_input.side_effect = ["999", "3"]  # Opción inválida, luego pasar
        self.cli.board.obtener_movimientos_posibles = Mock(return_value=[1, 2, 3])
        
        self.cli.manejar_movimientos_normales()
        
        # Debería haber mostrado error y luego ejecutado pasar turno
        mock_print.assert_called()
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_manejar_movimientos_normales_sin_movimientos_posibles(self, mock_print, mock_input):
        """Test cuando no hay movimientos posibles durante el turno."""
        mock_input.side_effect = ["1"]
        self.cli.board.obtener_movimientos_posibles = Mock(return_value=[])
        
        self.cli.manejar_movimientos_normales()
        
        # Debería terminar inmediatamente
        self.cli.board.obtener_movimientos_posibles.assert_called_once()
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_manejar_dobles_exitoso(self, mock_print, mock_input):
        """Test de manejo de dobles con movimientos exitosos."""
        mock_input.side_effect = ["1", "1", "2"]  # Hacer 2 movimientos, luego pasar
        self.cli.dados.obtener_dado1 = Mock(return_value=6)
        self.cli.board.obtener_movimientos_posibles = Mock(side_effect=[[1, 2], [1, 2], []])
        
        with patch.object(self.cli, 'realizar_movimiento_simple', return_value=True) as mock_simple:
            self.cli.manejar_dobles()
        
        self.assertEqual(mock_simple.call_count, 2)
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_manejar_dobles_sin_movimientos(self, mock_print, mock_input):
        """Test de dobles cuando no hay movimientos posibles."""
        self.cli.dados.obtener_dado1 = Mock(return_value=6)
        self.cli.board.obtener_movimientos_posibles = Mock(return_value=[])
        
        self.cli.manejar_dobles()
        
        self.cli.board.obtener_movimientos_posibles.assert_called_once()
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_manejar_dobles_pasar_turno(self, mock_print, mock_input):
        """Test de dobles eligiendo pasar turno."""
        mock_input.side_effect = ["2"]  # Pasar turno
        self.cli.dados.obtener_dado1 = Mock(return_value=6)
        self.cli.board.obtener_movimientos_posibles = Mock(return_value=[1, 2])
        
        self.cli.manejar_dobles()
        
        self.cli.board.obtener_movimientos_posibles.assert_called_once()
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_realizar_movimiento_simple_exitoso(self, mock_print, mock_input):
        """Test de movimiento simple exitoso."""
        mock_input.side_effect = ["1", "1"]  # Desde punto 1, usar dado 1
        self.cli.dados.es_doble = Mock(return_value=False)
        self.cli.dados.obtener_dado1 = Mock(return_value=3)
        self.cli.dados.obtener_dado2 = Mock(return_value=4)
        self.cli.board.realizar_movimiento_completo = Mock(return_value=True)
        
        with patch.object(self.cli, 'mostrar_tablero'):
            resultado = self.cli.realizar_movimiento_simple()
        
        self.assertTrue(resultado)
        self.cli.board.realizar_movimiento_completo.assert_called_once_with(
            self.cli.turno_actual, self.cli.dados, 1, True, False
        )
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_realizar_movimiento_simple_desde_barra(self, mock_print, mock_input):
        """Test de movimiento simple desde la barra."""
        mock_input.side_effect = ["0", "2"]  # Desde barra, usar dado 2
        self.cli.dados.es_doble = Mock(return_value=False)
        self.cli.dados.obtener_dado1 = Mock(return_value=3)
        self.cli.dados.obtener_dado2 = Mock(return_value=4)
        self.cli.board.realizar_movimiento_completo = Mock(return_value=True)
        
        with patch.object(self.cli, 'mostrar_tablero'):
            resultado = self.cli.realizar_movimiento_simple()
        
        self.assertTrue(resultado)
        self.cli.board.realizar_movimiento_completo.assert_called_once_with(
            self.cli.turno_actual, self.cli.dados, 0, False, True
        )
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_realizar_movimiento_simple_con_dobles(self, mock_print, mock_input):
        """Test de movimiento simple cuando hay dobles."""
        mock_input.side_effect = ["6"]  # Solo punto de origen
        self.cli.dados.es_doble = Mock(return_value=True)
        self.cli.board.realizar_movimiento_completo = Mock(return_value=True)
        
        with patch.object(self.cli, 'mostrar_tablero'):
            resultado = self.cli.realizar_movimiento_simple()
        
        self.assertTrue(resultado)
        self.cli.board.realizar_movimiento_completo.assert_called_once_with(
            self.cli.turno_actual, self.cli.dados, 6, True, False
        )
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_realizar_movimiento_simple_fallido(self, mock_print, mock_input):
        """Test de movimiento simple que falla."""
        mock_input.side_effect = ["1", "1"]
        self.cli.dados.es_doble = Mock(return_value=False)
        self.cli.dados.obtener_dado1 = Mock(return_value=3)
        self.cli.dados.obtener_dado2 = Mock(return_value=4)
        self.cli.board.realizar_movimiento_completo = Mock(return_value=False)
        
        resultado = self.cli.realizar_movimiento_simple()
        
        self.assertFalse(resultado)
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_realizar_movimiento_simple_dado_invalido(self, mock_print, mock_input):
        """Test con selección de dado inválida."""
        mock_input.side_effect = ["1", "999"]
        self.cli.dados.es_doble = Mock(return_value=False)
        self.cli.dados.obtener_dado1 = Mock(return_value=3)
        self.cli.dados.obtener_dado2 = Mock(return_value=4)
        
        resultado = self.cli.realizar_movimiento_simple()
        
        self.assertFalse(resultado)
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_realizar_movimiento_simple_valor_invalido(self, mock_print, mock_input):
        """Test con valor no numérico."""
        mock_input.side_effect = ["abc"]
        
        resultado = self.cli.realizar_movimiento_simple()
        
        self.assertFalse(resultado)
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_realizar_movimiento_simple_excepcion(self, mock_print, mock_input):
        """Test cuando se produce una excepción."""
        mock_input.side_effect = ["1", "1"]
        self.cli.dados.es_doble = Mock(return_value=False)
        self.cli.dados.obtener_dado1 = Mock(return_value=3)
        self.cli.dados.obtener_dado2 = Mock(return_value=4)
        self.cli.board.realizar_movimiento_completo = Mock(side_effect=Exception("Error de prueba"))
        
        resultado = self.cli.realizar_movimiento_simple()
        
        self.assertFalse(resultado)
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_realizar_movimiento_doble_exitoso(self, mock_print, mock_input):
        """Test de movimiento doble exitoso."""
        mock_input.side_effect = ["6", "s"]
        self.cli.dados.obtener_valores = Mock(return_value=(3, 4))
        self.cli.board.calcular_destino = Mock(side_effect=[9, 13])  # 6→9→13
        self.cli.board.realizar_movimiento_doble = Mock(return_value=True)
        
        with patch.object(self.cli, 'mostrar_tablero'):
            resultado = self.cli.realizar_movimiento_doble()
        
        self.assertTrue(resultado)
        self.cli.board.realizar_movimiento_doble.assert_called_once()
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_realizar_movimiento_doble_cancelado(self, mock_print, mock_input):
        """Test de movimiento doble cancelado por el usuario."""
        mock_input.side_effect = ["6", "n"]
        self.cli.dados.obtener_valores = Mock(return_value=(3, 4))
        self.cli.board.calcular_destino = Mock(side_effect=[9, 13])
        
        resultado = self.cli.realizar_movimiento_doble()
        
        self.assertFalse(resultado)
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_realizar_movimiento_doble_fallido(self, mock_print, mock_input):
        """Test de movimiento doble que falla en el board."""
        mock_input.side_effect = ["6", "si"]
        self.cli.dados.obtener_valores = Mock(return_value=(3, 4))
        self.cli.board.calcular_destino = Mock(side_effect=[9, 13])
        self.cli.board.realizar_movimiento_doble = Mock(return_value=False)
        
        resultado = self.cli.realizar_movimiento_doble()
        
        self.assertFalse(resultado)
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_realizar_movimiento_doble_valor_invalido(self, mock_print, mock_input):
        """Test de movimiento doble con valor inválido."""
        mock_input.side_effect = ["abc"]
        
        resultado = self.cli.realizar_movimiento_doble()
        
        self.assertFalse(resultado)
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_realizar_movimiento_doble_excepcion(self, mock_print, mock_input):
        """Test cuando se produce excepción en movimiento doble."""
        mock_input.side_effect = ["6", "s"]
        self.cli.dados.obtener_valores = Mock(side_effect=Exception("Error de prueba"))
        
        resultado = self.cli.realizar_movimiento_doble()
        
        self.assertFalse(resultado)
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_confirmacion_movimiento_doble_variantes(self, mock_print, mock_input):
        """Test de diferentes formas de confirmar movimiento doble."""
        confirmaciones_validas = ["s", "si", "sí", "y", "yes"]
        
        for confirmacion in confirmaciones_validas:
            with self.subTest(confirmacion=confirmacion):
                mock_input.side_effect = ["6", confirmacion]
                self.cli.dados.obtener_valores = Mock(return_value=(3, 4))
                self.cli.board.calcular_destino = Mock(side_effect=[9, 13])
                self.cli.board.realizar_movimiento_doble = Mock(return_value=True)
                
                with patch.object(self.cli, 'mostrar_tablero'):
                    resultado = self.cli.realizar_movimiento_doble()
                
                self.assertTrue(resultado)
    
    @patch('builtins.input')
    def test_keyboard_interrupt_en_movimientos_normales(self, mock_input):
        """Test de interrupción de teclado en movimientos normales."""
        mock_input.side_effect = KeyboardInterrupt()
        self.cli.board.obtener_movimientos_posibles = Mock(return_value=[1, 2])
        
        with patch('builtins.print'):
            with self.assertRaises(SystemExit):
                self.cli.manejar_movimientos_normales()
    
    @patch('builtins.input')
    def test_keyboard_interrupt_en_dobles(self, mock_input):
        """Test de interrupción de teclado en dobles."""
        mock_input.side_effect = KeyboardInterrupt()
        self.cli.dados.obtener_dado1 = Mock(return_value=6)
        self.cli.board.obtener_movimientos_posibles = Mock(return_value=[1, 2])
        
        with patch('builtins.print'):
            with self.assertRaises(SystemExit):
                self.cli.manejar_dobles()
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_multiples_movimientos_normales(self, mock_print, mock_input):
        """Test de múltiples movimientos en un turno normal."""
        mock_input.side_effect = ["1", "1", "1"]  # Dos movimientos simples, luego sin más movimientos
        self.cli.board.obtener_movimientos_posibles = Mock(side_effect=[[1, 2], [1, 2], []])
        
        with patch.object(self.cli, 'realizar_movimiento_simple', return_value=True) as mock_simple:
            self.cli.manejar_movimientos_normales()
        
        self.assertEqual(mock_simple.call_count, 2)
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_movimiento_simple_fallido_continua_turno(self, mock_print, mock_input):
        """Test que el turno continúa después de un movimiento fallido."""
        mock_input.side_effect = ["1", "1", "3"]  # Movimiento fallido, luego pasar
        self.cli.dados.es_doble = Mock(return_value=False)
        self.cli.dados.obtener_dado1 = Mock(return_value=3)
        self.cli.dados.obtener_dado2 = Mock(return_value=4)
        self.cli.board.obtener_movimientos_posibles = Mock(return_value=[1, 2])
        self.cli.board.realizar_movimiento_completo = Mock(return_value=False)
        
        self.cli.manejar_movimientos_normales()
        
        # Debería haber intentado el movimiento
        self.cli.board.realizar_movimiento_completo.assert_called_once()

if __name__ == "__main__":
    unittest.main()
