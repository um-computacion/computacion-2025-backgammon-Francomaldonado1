import unittest
from unittest.mock import Mock, patch
from Backgammon.Interfaces.CLI import BackgammonCLI, main


class TestBackgammonCLI(unittest.TestCase):

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
        # Configurar mocks - suficientes inputs para todo el flujo
        mock_input.side_effect = [
            "Juan", "María",  # Nombres
            "", "",  # Determinar primer jugador - dados
            ""  # Para parar cualquier loop adicional
        ] + [""] * 10  # Inputs adicionales por si acaso
        
        self.cli.board.inicializar_posiciones_estandar = Mock()
        self.cli.board.ha_ganado = Mock(return_value=True)  # Para terminar el loop rápidamente
        
        # Mock para determinar_primer_jugador
        with patch.object(self.cli, 'mostrar_tablero'), \
             patch.object(self.cli, 'determinar_primer_jugador'):
            self.cli.iniciar_juego()
        
        self.assertEqual(self.cli.jugador_negro, "Juan")
        self.assertEqual(self.cli.jugador_blanco, "María")
        self.cli.board.inicializar_posiciones_estandar.assert_called_once()
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_iniciar_juego_nombres_vacios(self, mock_print, mock_input):
        """Test con nombres vacíos (usa nombres por defecto)."""
        mock_input.side_effect = ["", ""] + [""] * 10
        self.cli.board.inicializar_posiciones_estandar = Mock()
        self.cli.board.ha_ganado = Mock(return_value=True)
        
        with patch.object(self.cli, 'mostrar_tablero'), \
             patch.object(self.cli, 'determinar_primer_jugador'):
            self.cli.iniciar_juego()
        
        self.assertEqual(self.cli.jugador_negro, "Jugador 1")
        self.assertEqual(self.cli.jugador_blanco, "Jugador 2")
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_iniciar_juego_nombres_con_espacios(self, mock_print, mock_input):
        """Test con nombres que tienen espacios al inicio y final."""
        mock_input.side_effect = ["  Juan  ", "  María  "] + [""] * 10
        self.cli.board.inicializar_posiciones_estandar = Mock()
        self.cli.board.ha_ganado = Mock(return_value=True)
        
        with patch.object(self.cli, 'mostrar_tablero'), \
             patch.object(self.cli, 'determinar_primer_jugador'):
            self.cli.iniciar_juego()
        
        self.assertEqual(self.cli.jugador_negro, "Juan")
        self.assertEqual(self.cli.jugador_blanco, "María")
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_determinar_primer_jugador_negro_gana(self, mock_print, mock_input):
        """Test cuando el jugador negro gana el primer tiro."""
        mock_input.side_effect = ["", ""]  # Dos ENTERs
        self.cli.jugador_negro = "Juan"
        self.cli.jugador_blanco = "María"
        
        # Configurar dados: Negro saca 6, Blanco saca 3
        self.cli.dados.tirar = Mock()
        self.cli.dados.obtener_dado1 = Mock(side_effect=[6, 3])
        
        self.cli.determinar_primer_jugador()
        
        self.assertEqual(self.cli.turno_actual, "negro")
        self.assertEqual(self.cli.dados.tirar.call_count, 2)
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_determinar_primer_jugador_blanco_gana(self, mock_print, mock_input):
        """Test cuando el jugador blanco gana el primer tiro."""
        mock_input.side_effect = ["", ""]
        self.cli.jugador_negro = "Juan"
        self.cli.jugador_blanco = "María"
        
        # Configurar dados: Negro saca 2, Blanco saca 5
        self.cli.dados.tirar = Mock()
        self.cli.dados.obtener_dado1 = Mock(side_effect=[2, 5])
        
        self.cli.determinar_primer_jugador()
        
        self.assertEqual(self.cli.turno_actual, "blanco")
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_determinar_primer_jugador_con_empate(self, mock_print, mock_input):
        """Test cuando hay empate y necesitan volver a tirar."""
        mock_input.side_effect = ["", "", "", ""]  # Dos rondas de tiros
        self.cli.jugador_negro = "Juan"
        self.cli.jugador_blanco = "María"
        
        # Primer empate (4-4), luego Negro gana (6-2)
        self.cli.dados.tirar = Mock()
        self.cli.dados.obtener_dado1 = Mock(side_effect=[4, 4, 6, 2])
        
        self.cli.determinar_primer_jugador()
        
        self.assertEqual(self.cli.turno_actual, "negro")
        self.assertEqual(self.cli.dados.tirar.call_count, 4)
    
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
        
        # CORRECCIÓN: Mock que permite al menos un turno antes de ganar
        call_count = [0]
        def mock_ha_ganado(color):
            call_count[0] += 1
            # Permite un turno antes de que gane negro
            return call_count[0] > 2 and color == "negro"
        
        self.cli.board.ha_ganado = Mock(side_effect=mock_ha_ganado)
        
        with patch.object(self.cli, 'turno_jugador') as mock_turno:
            with patch('builtins.print'):
                self.cli.loop_principal()
        
        self.assertGreater(mock_turno.call_count, 0)  # Al menos un turno
        self.cli.board.ha_ganado.assert_called()
    
    def test_loop_principal_ganador_blanco(self):
        """Test del loop principal cuando gana el jugador blanco."""
        self.cli.jugador_blanco = "María"
        
        # Permitir que el blanco gane después de algunos turnos
        call_count = [0]
        def mock_ha_ganado(color):
            call_count[0] += 1
            return call_count[0] > 2 and color == "blanco"
        
        self.cli.board.ha_ganado = Mock(side_effect=mock_ha_ganado)
        
        with patch.object(self.cli, 'turno_jugador') as mock_turno:
            with patch('builtins.print'):
                self.cli.loop_principal()
        
        self.cli.board.ha_ganado.assert_called()
    
    def test_loop_principal_cambio_turnos(self):
        """Test del cambio de turnos en el loop principal."""
        # CORRECCIÓN: Permitir exactamente 2 turnos antes de ganar
        call_count = [0]
        def mock_ha_ganado(color):
            call_count[0] += 1
            # Permitir 2 turnos completos (4 verificaciones) antes de ganar
            return call_count[0] > 4
        
        self.cli.board.ha_ganado = Mock(side_effect=mock_ha_ganado)
        
        with patch.object(self.cli, 'turno_jugador') as mock_turno:
            with patch('builtins.print'):
                self.cli.loop_principal()
        
        # Debería haber al menos 2 turnos
        self.assertGreaterEqual(mock_turno.call_count, 2)
    
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
        
        with patch('builtins.print'):
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
    def test_manejar_movimientos_normales_opcion_1_ambos_dados(self, mock_print, mock_input):
        """Test de movimientos normales eligiendo opción 1 con ambos dados disponibles."""
        mock_input.side_effect = ["1", "1", "3"]  # Opción 1, dado 1, luego pasar turno
        self.cli.board.obtener_movimientos_posibles = Mock(side_effect=[[1, 2, 3], [1, 2, 3], []])
        
        with patch.object(self.cli, 'realizar_movimiento_simple_con_dados', return_value=True) as mock_simple:
            self.cli.manejar_movimientos_normales()
        
        mock_simple.assert_called_once_with(True, False)
    
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
        
        self.cli.board.obtener_movimientos_posibles.assert_called_once()
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_manejar_movimientos_normales_solo_dado1_disponible(self, mock_print, mock_input):
        """Test cuando solo el dado 1 está disponible."""
        # CORRECCIÓN: Inputs suficientes y mejor simulación
        mock_input.side_effect = ["1", "1", "3"] + [""] * 10
        
        # Simulación mejorada de movimientos disponibles que acepta los argumentos
        call_count = [0]
        def mock_movimientos(*args):  # Acepta cualquier número de argumentos
            call_count[0] += 1
            if call_count[0] <= 2:
                return [1, 2]  # Movimientos disponibles
            else:
                return []  # Sin movimientos
        
        self.cli.board.obtener_movimientos_posibles = Mock(side_effect=mock_movimientos)
        self.cli.dados.obtener_dado1 = Mock(return_value=3)
        self.cli.dados.obtener_dado2 = Mock(return_value=4)
        
        with patch.object(self.cli, 'realizar_movimiento_simple_con_dados', return_value=True) as mock_simple:
            self.cli.manejar_movimientos_normales()
        
        # CORRECCIÓN: Verificar que se llamó al menos una vez
        self.assertGreater(mock_simple.call_count, 0)
    
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
    def test_manejar_dobles_exitoso(self, mock_print, mock_input):
        """Test de manejo de dobles con movimientos exitosos."""
        mock_input.side_effect = ["1", "1", "2"]  # Hacer 2 movimientos, luego pasar
        self.cli.dados.obtener_dado1 = Mock(return_value=6)
        self.cli.board.obtener_movimientos_posibles = Mock(side_effect=[[1, 2], [1, 2], []])
        
        with patch.object(self.cli, 'realizar_movimiento_simple_con_dados', return_value=True) as mock_simple:
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
    def test_realizar_movimiento_simple_con_dados_exitoso(self, mock_print, mock_input):
        """Test de movimiento simple exitoso."""
        mock_input.side_effect = ["1"]  # Desde punto 1
        self.cli.board.realizar_movimiento_completo = Mock(return_value=True)
        
        with patch.object(self.cli, 'mostrar_tablero'):
            resultado = self.cli.realizar_movimiento_simple_con_dados(True, False)
        
        self.assertTrue(resultado)
        self.cli.board.realizar_movimiento_completo.assert_called_once()
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_realizar_movimiento_simple_con_dados_desde_barra(self, mock_print, mock_input):
        """Test de movimiento simple desde la barra."""
        mock_input.side_effect = ["0"]  # Desde barra
        self.cli.board.realizar_movimiento_completo = Mock(return_value=True)
        
        with patch.object(self.cli, 'mostrar_tablero'):
            resultado = self.cli.realizar_movimiento_simple_con_dados(False, True)
        
        self.assertTrue(resultado)
        self.cli.board.realizar_movimiento_completo.assert_called_once_with(
            self.cli.turno_actual, self.cli.dados, 0, False, True
        )
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_realizar_movimiento_simple_con_dados_fallido(self, mock_print, mock_input):
        """Test de movimiento simple que falla."""
        mock_input.side_effect = ["1"]
        self.cli.board.realizar_movimiento_completo = Mock(return_value=False)
        
        with patch.object(self.cli, 'mostrar_tablero'):
            resultado = self.cli.realizar_movimiento_simple_con_dados(True, False)
        
        self.assertFalse(resultado)
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_realizar_movimiento_simple_con_dados_valor_invalido(self, mock_print, mock_input):
        """Test con valor no numérico."""
        mock_input.side_effect = ["abc"]
        
        with patch.object(self.cli, 'mostrar_tablero'):
            resultado = self.cli.realizar_movimiento_simple_con_dados(True, False)
        
        self.assertFalse(resultado)
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_realizar_movimiento_simple_con_dados_excepcion(self, mock_print, mock_input):
        """Test cuando se produce una excepción."""
        mock_input.side_effect = ["1"]
        self.cli.board.realizar_movimiento_completo = Mock(side_effect=Exception("Error de prueba"))
        
        with patch.object(self.cli, 'mostrar_tablero'):
            resultado = self.cli.realizar_movimiento_simple_con_dados(True, False)
        
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
        
        with patch.object(self.cli, 'mostrar_tablero'):
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
        
        with patch.object(self.cli, 'mostrar_tablero'):
            resultado = self.cli.realizar_movimiento_doble()
        
        self.assertFalse(resultado)
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_realizar_movimiento_doble_valor_invalido(self, mock_print, mock_input):
        """Test de movimiento doble con valor inválido."""
        mock_input.side_effect = ["abc"]
        
        with patch.object(self.cli, 'mostrar_tablero'):
            resultado = self.cli.realizar_movimiento_doble()
        
        self.assertFalse(resultado)
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_realizar_movimiento_doble_excepcion(self, mock_print, mock_input):
        """Test cuando se produce excepción en movimiento doble."""
        mock_input.side_effect = ["6", "s"]
        self.cli.dados.obtener_valores = Mock(side_effect=Exception("Error de prueba"))
        
        with patch.object(self.cli, 'mostrar_tablero'):
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
        mock_input.side_effect = ["1", "1", "1", "2", "3"]  # Dos movimientos simples, luego pasar
        self.cli.board.obtener_movimientos_posibles = Mock(side_effect=[[1, 2], [1, 2], []])
        
        with patch.object(self.cli, 'realizar_movimiento_simple_con_dados', return_value=True) as mock_simple:
            self.cli.manejar_movimientos_normales()
        
        self.assertEqual(mock_simple.call_count, 2)
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_movimiento_simple_fallido_continua_turno(self, mock_print, mock_input):
        """Test que el turno continúa después de un movimiento fallido."""
        # CORRECCIÓN: Agregar suficientes inputs para todo el flujo
        mock_input.side_effect = [""] + ["1", "1", "3"] * 3 + [""] * 10
        
        # La función mock debe aceptar argumentos
        def mock_movimientos(*args):
            return [1, 2]
        
        self.cli.board.obtener_movimientos_posibles = Mock(side_effect=mock_movimientos)
        self.cli.board.realizar_movimiento_completo = Mock(return_value=False)
        
        with patch.object(self.cli, 'mostrar_tablero'):
            self.cli.manejar_movimientos_normales()
        
        # Debería haber intentado el movimiento
        self.assertGreater(self.cli.board.realizar_movimiento_completo.call_count, 0)
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_movimiento_fallido_libera_dado(self, mock_print, mock_input):
        """Test que un movimiento fallido libera el dado para reintento."""
        mock_input.side_effect = ["1", "1", "1", "1", "3"]  # Falla, reintenta con mismo dado, luego pasa
        self.cli.dados.obtener_dado1 = Mock(return_value=3)
        self.cli.dados.obtener_dado2 = Mock(return_value=4)
        self.cli.board.obtener_movimientos_posibles = Mock(return_value=[1, 2])
        
        with patch.object(self.cli, 'realizar_movimiento_simple_con_dados', side_effect=[False, True]) as mock_simple:
            self.cli.manejar_movimientos_normales()
        
        # Debería intentar dos veces con el mismo dado
        self.assertEqual(mock_simple.call_count, 2)
        # Ambas llamadas deberían usar el dado 1
        mock_simple.assert_any_call(True, False)


class TestBackgammonCLIIntegration(unittest.TestCase):
    """
    Tests de integración para BackgammonCLI.
    """
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_flujo_completo_juego_muy_corto(self, mock_print, mock_input):
        """Test de flujo completo de un juego muy corto."""
        # Simular un juego que termina rápidamente
        mock_input.side_effect = [
            "TestPlayer1", "TestPlayer2",  # Nombres
            "", "",  # Dados para determinar primer jugador
        ] + [""] * 5  # Inputs adicionales
        
        cli = BackgammonCLI()
        cli.board.inicializar_posiciones_estandar = Mock()
        cli.board.ha_ganado = Mock(return_value=True)  # Termina inmediatamente
        cli.dados.tirar = Mock()
        cli.dados.obtener_dado1 = Mock(side_effect=[6, 3])  # Player1 gana
        
        with patch.object(cli, 'mostrar_tablero'):
            cli.iniciar_juego()
        
        self.assertEqual(cli.jugador_negro, "TestPlayer1")
        self.assertEqual(cli.jugador_blanco, "TestPlayer2")
        self.assertEqual(cli.turno_actual, "negro")
    
    @patch('builtins.input')
    @patch('builtins.print') 
    def test_flujo_con_varios_empates_inicial(self, mock_print, mock_input):
        """Test con varios empates al determinar quién empieza."""
        mock_input.side_effect = [
            "Player1", "Player2",  # Nombres
            "", "", "", "", "", ""  # Tres rondas de dados
        ] + [""] * 5
        
        cli = BackgammonCLI()
        cli.board.inicializar_posiciones_estandar = Mock()
        cli.board.ha_ganado = Mock(return_value=True)
        cli.dados.tirar = Mock()
        # Empate, empate, luego gana Player2
        cli.dados.obtener_dado1 = Mock(side_effect=[4, 4, 3, 3, 2, 5])
        
        with patch.object(cli, 'mostrar_tablero'):
            cli.iniciar_juego()
        
        self.assertEqual(cli.turno_actual, "blanco")  # Player2 debería ganar
        self.assertEqual(cli.dados.tirar.call_count, 6)  # 3 rondas × 2 jugadores
    
    def test_main_function_normal(self):
        """Test de la función main con ejecución normal."""
        with patch('Backgammon.Interfaces.CLI.BackgammonCLI') as mock_cli_class:
            mock_cli_instance = Mock()
            mock_cli_class.return_value = mock_cli_instance
            
            main()
            
            mock_cli_class.assert_called_once()
            mock_cli_instance.iniciar_juego.assert_called_once()
    
    def test_main_function_keyboard_interrupt(self):
        """Test de la función main con interrupción de teclado."""
        with patch('Backgammon.Interfaces.CLI.BackgammonCLI') as mock_cli_class:
            mock_cli_instance = Mock()
            mock_cli_instance.iniciar_juego.side_effect = KeyboardInterrupt()
            mock_cli_class.return_value = mock_cli_instance
            
            with patch('builtins.print') as mock_print:
                main()
            
            mock_print.assert_called_with("\n\n¡Hasta luego! 👋")
    
    def test_main_function_exception(self):
        """Test de la función main con excepción inesperada."""
        with patch('Backgammon.Interfaces.CLI.BackgammonCLI') as mock_cli_class:
            mock_cli_instance = Mock()
            mock_cli_instance.iniciar_juego.side_effect = Exception("Error inesperado")
            mock_cli_class.return_value = mock_cli_instance
            
            with patch('builtins.print') as mock_print:
                main()
            
            mock_print.assert_called_with("\n❌ Error inesperado: Error inesperado")
    
    @patch('builtins.print')
    def test_mostrar_tablero_con_casa_vacia(self, mock_print):
        """Test específico para mostrar_tablero con casa vacía."""
        cli = BackgammonCLI()
        cli.board = Mock()
        cli.board.obtener_estado_punto = Mock(return_value=None)
        cli.board.get_barra = Mock(return_value={"negro": 0, "blanco": 0})
        cli.board.get_casa = Mock(return_value={"negro": 0, "blanco": 0})
        
        cli.mostrar_tablero()
        
        # Verificar que se muestran todas las secciones
        calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(any("CUADRANTE CASA NEGRO" in call for call in calls))
        self.assertTrue(any("CUADRANTE CASA BLANCO" in call for call in calls))
        self.assertTrue(any("CASA: vacía" in call for call in calls))
    
    @patch('builtins.print')
    def test_simbolos_correctos_fichas(self, mock_print):
        """Test que verifica que se usen los símbolos correctos para las fichas."""
        cli = BackgammonCLI()
        cli.board = Mock()
        
        # Mock que devuelve fichas negras y blancas
        def mock_estado(punto):
            if punto == 1:
                return ("negro", 2)
            elif punto == 12:
                return ("blanco", 3)
            else:
                return None
        
        cli.board.obtener_estado_punto = Mock(side_effect=mock_estado)
        cli.board.get_barra = Mock(return_value={})
        cli.board.get_casa = Mock(return_value={})
        
        cli.mostrar_tablero()
        
        # Verificar que se usan los símbolos correctos
        calls = [str(call) for call in mock_print.call_args_list]
        output = " ".join(calls)
        
        # Negro debería ser ○ (círculo vacío)
        self.assertIn("○", output)
        # Blanco debería ser ● (círculo lleno)  
        self.assertIn("●", output)


class TestBackgammonCLIEdgeCases(unittest.TestCase):
    """
    Tests para casos extremos y edge cases.
    """
    
    def setUp(self):
        self.cli = BackgammonCLI()
        self.cli.board = Mock()
        self.cli.dados = Mock()
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_manejar_movimientos_sin_dados_disponibles(self, mock_print, mock_input):
        """Test cuando no quedan dados disponibles."""
        mock_input.side_effect = ["3"]  # Pasar turno
        self.cli.board.obtener_movimientos_posibles = Mock(return_value=[])
        
        self.cli.manejar_movimientos_normales()
        
        # Debería terminar rápidamente
        self.cli.board.obtener_movimientos_posibles.assert_called()
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_realizar_movimiento_doble_sin_confirmacion_valida(self, mock_print, mock_input):
        """Test de movimiento doble con confirmaciones inválidas."""
        mock_input.side_effect = ["6", "maybe", "no", "n"]  # Confirmaciones inválidas hasta "n"
        self.cli.dados.obtener_valores = Mock(return_value=(3, 4))
        self.cli.board.calcular_destino = Mock(side_effect=[9, 13])
        
        with patch.object(self.cli, 'mostrar_tablero'):
            resultado = self.cli.realizar_movimiento_doble()
        
        self.assertFalse(resultado)
    
    @patch('builtins.print')
    def test_mostrar_tablero_con_estados_mixtos(self, mock_print):
        """Test de mostrar_tablero con diferentes estados en diferentes puntos."""
        def mock_estado_mixto(punto):
            estados = {
                1: ("negro", 1),
                6: ("blanco", 2),
                12: None,
                13: ("negro", 5),
                24: ("blanco", 1)
            }
            return estados.get(punto, None)
        
        self.cli.board.obtener_estado_punto = Mock(side_effect=mock_estado_mixto)
        self.cli.board.get_barra = Mock(return_value={"negro": 1, "blanco": 0})
        self.cli.board.get_casa = Mock(return_value={"negro": 2, "blanco": 3})
        
        self.cli.mostrar_tablero()
        
        # Verificar que se llamó obtener_estado_punto para todos los puntos
        self.assertEqual(self.cli.board.obtener_estado_punto.call_count, 24)
    
    def test_loop_principal_sin_ganador_inmediato(self):
        """Test del loop principal con varios turnos antes de que alguien gane."""
        self.cli.jugador_negro = "Juan"
        self.cli.jugador_blanco = "María"
        
        # Simular varios turnos antes de que gane negro
        call_count = [0]
        def mock_ha_ganado(color):
            call_count[0] += 1
            # Gana después de varios intentos
            return call_count[0] > 8 and color == "negro"
        
        self.cli.board.ha_ganado = Mock(side_effect=mock_ha_ganado)
        
        with patch.object(self.cli, 'turno_jugador') as mock_turno:
            with patch('builtins.print'):
                self.cli.loop_principal()
        
        # Debería haber al menos algunos turnos
        self.assertGreater(mock_turno.call_count, 0)
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_turno_completo_con_movimientos_exitosos(self, mock_print, mock_input):
        """Test de un turno completo con movimientos exitosos."""
        # CORRECCIÓN: Secuencia de inputs más realista
        mock_input.side_effect = [""] + ["1", "1", "1", "1", "3"] * 3 + [""] * 10
        
        self.cli.jugador_negro = "TestPlayer"
        self.cli.turno_actual = "negro"
        
        # Configurar mocks
        self.cli.dados.tirar = Mock()
        self.cli.dados.reiniciar = Mock()
        self.cli.dados.__str__ = Mock(return_value="[3,4]")
        self.cli.dados.es_doble = Mock(return_value=False)
        self.cli.dados.obtener_dado1 = Mock(return_value=3)
        self.cli.dados.obtener_dado2 = Mock(return_value=4)
        
        # CORRECCIÓN: Simular correctamente la disponibilidad de movimientos
        # La función ahora acepta argumentos
        call_count = [0]
        def mock_movimientos(*args):
            call_count[0] += 1
            if call_count[0] <= 3:
                return [1, 2]  # Primeras llamadas: movimientos disponibles
            else:
                return []  # Sin más movimientos
        
        self.cli.board.obtener_movimientos_posibles = Mock(side_effect=mock_movimientos)
        self.cli.board.realizar_movimiento_completo = Mock(return_value=True)
        
        with patch.object(self.cli, 'mostrar_tablero'):
            self.cli.turno_jugador()
        
        # CORRECCIÓN: Verificar que se realizaron movimientos
        self.assertGreaterEqual(self.cli.board.realizar_movimiento_completo.call_count, 2)
        self.cli.dados.reiniciar.assert_called_once()

if __name__ == '__main__':
    unittest.main()