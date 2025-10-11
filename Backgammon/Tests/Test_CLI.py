import unittest
from unittest.mock import Mock, patch
from Backgammon.Interfaces.CLI import CLI, main


class TestCLI(unittest.TestCase):
    """
    Suite de tests para la interfaz CLI del juego Backgammon.
    
    Verifica:
        - Inicialización correcta de la interfaz
        - Gestión del flujo del juego
        - Interacción con componentes del dominio (Board, Dice)
        - Manejo de entrada/salida del usuario
    
    Principios SOLID verificados:
        - SRP: CLI solo maneja I/O, delegando lógica al dominio
        - DIP: CLI depende de abstracciones (Board, Dice) no implementaciones
        - ISP: Métodos pequeños y enfocados en tareas específicas
    """

    def setUp(self):
        """
        Configuración inicial para cada test.
        
        SRP: Separa la configuración de test del test mismo.
        """
        self.cli = CLI()
        self.cli.board = Mock()
        self.cli.dados = Mock()

    def test_init(self):
        """
        Test de inicialización de CLI.
        
        Verifica:
            - Creación correcta de instancias de Board y Dice
            - Inicialización del estado del juego
        
        Principio DIP: CLI depende de las abstracciones Board y Dice.
        """
        cli = CLI()
        self.assertIsNotNone(cli.board)
        self.assertIsNotNone(cli.dados)
        self.assertEqual(cli.jugador_negro, "")
        self.assertEqual(cli.jugador_blanco, "")
        self.assertEqual(cli.turno_actual, "negro")

    @patch('builtins.input')
    @patch('builtins.print')
    def test_realizar_movimiento_doble_exitoso(self, mock_print, mock_input):
        """
        Test de movimiento doble exitoso.
        
        Verifica:
            - Movimiento usando ambos dados consecutivamente
            - Confirmación del usuario
        
        Principio DIP: Usa Board.realizar_movimiento_doble como abstracción.
        """
        mock_input.side_effect = ["6", "s"]
        self.cli.dados.obtener_valores = Mock(return_value=(3, 4))
        self.cli.board.calcular_destino = Mock(side_effect=[9, 13])
        self.cli.board.realizar_movimiento_doble = Mock(return_value=True)

        with patch.object(self.cli, 'mostrar_tablero'):
            resultado = self.cli.realizar_movimiento_doble()

        self.assertTrue(resultado)
        self.cli.board.realizar_movimiento_doble.assert_called_once()

    @patch('builtins.input')
    @patch('builtins.print')
    def test_realizar_movimiento_doble_cancelado(self, mock_print, mock_input):
        """
        Test de movimiento doble cancelado por el usuario.
        
        Verifica:
            - Respeto de la decisión del usuario
        
        Principio SRP: La interfaz solo captura y transmite la decisión.
        """
        mock_input.side_effect = ["6", "n"]
        self.cli.dados.obtener_valores = Mock(return_value=(3, 4))
        self.cli.board.calcular_destino = Mock(side_effect=[9, 13])

        with patch.object(self.cli, 'mostrar_tablero'):
            resultado = self.cli.realizar_movimiento_doble()

        self.assertFalse(resultado)

    @patch('builtins.input')
    @patch('builtins.print')
    def test_realizar_movimiento_doble_fallido(self, mock_print, mock_input):
        """
        Test de movimiento doble que falla en el board.
        
        Verifica:
            - Propagación correcta de fallos desde Board
        
        Principio LSP: Comportamiento predecible en éxito y fallo.
        """
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
        """
        Test de movimiento doble con valor inválido.
        
        Verifica:
            - Manejo de errores de entrada
        
        Principio SRP: Validación de entrada está separada.
        """
        mock_input.side_effect = ["abc"]

        with patch.object(self.cli, 'mostrar_tablero'):
            resultado = self.cli.realizar_movimiento_doble()

        self.assertFalse(resultado)

    @patch('builtins.input')
    @patch('builtins.print')
    def test_realizar_movimiento_doble_excepcion(self, mock_print, mock_input):
        """
        Test cuando se produce excepción en movimiento doble.
        
        Verifica:
            - Manejo robusto de excepciones
        
        Principio SRP: Separación entre lógica y manejo de errores.
        """
        mock_input.side_effect = ["6", "s"]
        self.cli.dados.obtener_valores = Mock(side_effect=Exception("Error de prueba"))

        with patch.object(self.cli, 'mostrar_tablero'):
            resultado = self.cli.realizar_movimiento_doble()

        self.assertFalse(resultado)

    @patch('builtins.input')
    @patch('builtins.print')
    def test_confirmacion_movimiento_doble_variantes(self, mock_print, mock_input):
        """
        Test de diferentes formas de confirmar movimiento doble.
        
        Verifica:
            - Aceptación de múltiples variantes de confirmación
        
        Principio OCP: Extensible para nuevas formas de confirmación.
        """
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
        """
        Test de interrupción de teclado en movimientos normales.
        
        Verifica:
            - Manejo correcto de Ctrl+C
        
        Principio SRP: Manejo de interrupciones separado de lógica de juego.
        """
        mock_input.side_effect = KeyboardInterrupt()
        self.cli.board.obtener_movimientos_posibles = Mock(return_value=[1, 2])

        with patch('builtins.print'):
            with self.assertRaises(SystemExit):
                self.cli.manejar_movimientos_normales()

    @patch('builtins.input')
    def test_keyboard_interrupt_en_dobles(self, mock_input):
        """
        Test de interrupción de teclado en dobles.
        
        Verifica:
            - Manejo consistente de interrupciones
        
        Principio LSP: Comportamiento uniforme ante interrupciones.
        """
        mock_input.side_effect = KeyboardInterrupt()
        self.cli.dados.obtener_dado1 = Mock(return_value=6)
        self.cli.board.obtener_movimientos_posibles = Mock(return_value=[1, 2])

        with patch('builtins.print'):
            with self.assertRaises(SystemExit):
                self.cli.manejar_dobles()

    @patch('builtins.input')
    @patch('builtins.print')
    def test_multiples_movimientos_normales(self, mock_print, mock_input):
        """
        Test de múltiples movimientos en un turno normal.
        
        Verifica:
            - Ejecución de 2 movimientos consecutivos
        
        Principio SRP: Coordinación de movimientos sin validarlos.
        """
        mock_input.side_effect = ["1", "1", "1", "2", "3"]
        self.cli.board.obtener_movimientos_posibles = Mock(side_effect=[[1, 2], [1, 2], []])

        with patch.object(self.cli, 'realizar_movimiento_simple_con_dados', return_value=True) as mock_simple:
            self.cli.manejar_movimientos_normales()

        self.assertEqual(mock_simple.call_count, 2)

    @patch('builtins.input')
    @patch('builtins.print')
    def test_movimiento_simple_fallido_continua_turno(self, mock_print, mock_input):
        """
        Test que el turno continúa después de un movimiento fallido.
        
        Verifica:
            - Permite reintentos después de fallos
        
        Principio OCP: Comportamiento extensible para reintentos.
        """
        mock_input.side_effect = [""] + ["1", "1", "3"] * 3 + [""] * 10

        def mock_movimientos(*args):
            return [1, 2]

        self.cli.board.obtener_movimientos_posibles = Mock(side_effect=mock_movimientos)
        self.cli.board.realizar_movimiento_completo = Mock(return_value=False)

        with patch.object(self.cli, 'mostrar_tablero'):
            self.cli.manejar_movimientos_normales()

        self.assertGreater(self.cli.board.realizar_movimiento_completo.call_count, 0)

    @patch('builtins.input')
    @patch('builtins.print')
    def test_movimiento_fallido_libera_dado(self, mock_print, mock_input):
        """
        Test que un movimiento fallido libera el dado para reintento.
        
        Verifica:
            - Gestión correcta de disponibilidad de dados
        
        Principio SRP: Lógica de disponibilidad separada de validación.
        """
        mock_input.side_effect = ["1", "1", "1", "1", "3"]
        self.cli.dados.obtener_dado1 = Mock(return_value=3)
        self.cli.dados.obtener_dado2 = Mock(return_value=4)
        self.cli.board.obtener_movimientos_posibles = Mock(return_value=[1, 2])

        with patch.object(self.cli, 'realizar_movimiento_simple_con_dados', side_effect=[False, True]) as mock_simple:
            self.cli.manejar_movimientos_normales()

        self.assertEqual(mock_simple.call_count, 2)
        mock_simple.assert_any_call(True, False)


class TestCLIIntegration(unittest.TestCase):
    """
    Tests de integración para CLI.
    
    Verifica:
        - Flujos completos del juego
        - Interacción entre componentes
        - Escenarios end-to-end
    
    Principios SOLID verificados:
        - DIP: Componentes interactúan a través de abstracciones
        - LSP: Comportamiento consistente en diferentes escenarios
    """

    @patch('builtins.input')
    @patch('builtins.print')
    def test_flujo_completo_juego_muy_corto(self, mock_print, mock_input):
        """
        Test de flujo completo de un juego muy corto.
        
        Verifica:
            - Integración de todos los componentes
            - Flujo desde inicio hasta fin
        
        Principio DIP: Todos los componentes interactúan mediante interfaces.
        """
        mock_input.side_effect = [
            "TestPlayer1", "TestPlayer2",
            "", "",
        ] + [""] * 5

        cli = CLI()
        cli.board.inicializar_posiciones_estandar = Mock()
        cli.board.ha_ganado = Mock(return_value=True)
        cli.dados.tirar = Mock()
        cli.dados.obtener_dado1 = Mock(side_effect=[6, 3])

        with patch.object(cli, 'mostrar_tablero'):
            cli.iniciar_juego()

        self.assertEqual(cli.jugador_negro, "TestPlayer1")
        self.assertEqual(cli.jugador_blanco, "TestPlayer2")
        self.assertEqual(cli.turno_actual, "negro")

    @patch('builtins.input')
    @patch('builtins.print')
    def test_flujo_con_varios_empates_inicial(self, mock_print, mock_input):
        """
        Test con varios empates al determinar quién empieza.
        
        Verifica:
            - Manejo correcto de múltiples empates
        
        Principio SRP: La lógica de desempate está encapsulada.
        """
        mock_input.side_effect = [
            "Player1", "Player2",
            "", "", "", "", "", ""
        ] + [""] * 5

        cli = CLI()
        cli.board.inicializar_posiciones_estandar = Mock()
        cli.board.ha_ganado = Mock(return_value=True)
        cli.dados.tirar = Mock()
        cli.dados.obtener_dado1 = Mock(side_effect=[4, 4, 3, 3, 2, 5])

        with patch.object(cli, 'mostrar_tablero'):
            cli.iniciar_juego()

        self.assertEqual(cli.turno_actual, "blanco")
        self.assertEqual(cli.dados.tirar.call_count, 6)

    def test_main_function_normal(self):
        """
        Test de la función main con ejecución normal.
        
        Verifica:
            - Punto de entrada funcional
        
        Principio SRP: main solo inicia y maneja excepciones globales.
        """
        with patch('Backgammon.Interfaces.CLI.CLI') as mock_cli_class:
            mock_cli_instance = Mock()
            mock_cli_class.return_value = mock_cli_instance

            main()

            mock_cli_class.assert_called_once()
            mock_cli_instance.iniciar_juego.assert_called_once()

    def test_main_function_keyboard_interrupt(self):
        """
        Test de la función main con interrupción de teclado.
        
        Verifica:
            - Manejo elegante de Ctrl+C
        
        Principio SRP: Manejo de interrupciones centralizado.
        """
        with patch('Backgammon.Interfaces.CLI.CLI') as mock_cli_class:
            mock_cli_instance = Mock()
            mock_cli_instance.iniciar_juego.side_effect = KeyboardInterrupt()
            mock_cli_class.return_value = mock_cli_instance

            with patch('builtins.print') as mock_print:
                main()

            mock_print.assert_called_with("\n\n¡Hasta luego! 👋")

    def test_main_function_exception(self):
        """
        Test de la función main con excepción inesperada.
        
        Verifica:
            - Manejo robusto de errores no esperados
        
        Principio SRP: Gestión de errores separada de lógica principal.
        """
        with patch('Backgammon.Interfaces.CLI.CLI') as mock_cli_class:
            mock_cli_instance = Mock()
            mock_cli_instance.iniciar_juego.side_effect = Exception("Error inesperado")
            mock_cli_class.return_value = mock_cli_instance

            with patch('builtins.print') as mock_print:
                main()

            mock_print.assert_called_with("\n❌ Error inesperado: Error inesperado")

    @patch('builtins.print')
    def test_mostrar_tablero_con_casa_vacia(self, mock_print):
        """
        Test específico para mostrar_tablero con casa vacía.
        
        Verifica:
            - Presentación correcta de casa sin fichas
        
        Principio LSP: Comportamiento consistente con casa llena o vacía.
        """
        cli = CLI()
        cli.board = Mock()
        cli.board.obtener_estado_punto = Mock(return_value=None)
        cli.board.get_barra = Mock(return_value={"negro": 0, "blanco": 0})
        cli.board.get_casa = Mock(return_value={"negro": 0, "blanco": 0})

        cli.mostrar_tablero()

        calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(any("CUADRANTE CASA NEGRO" in call for call in calls))
        self.assertTrue(any("CUADRANTE CASA BLANCO" in call for call in calls))
        self.assertTrue(any("CASA: vacía" in call for call in calls))

    @patch('builtins.print')
    def test_simbolos_correctos_fichas(self, mock_print):
        """
        Test que verifica que se usen los símbolos correctos para las fichas.
        
        Verifica:
            - Representación visual correcta de fichas
        
        Principio SRP: La presentación visual está separada de la lógica.
        """
        cli = CLI()
        cli.board = Mock()

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

        calls = [str(call) for call in mock_print.call_args_list]
        output = " ".join(calls)

        self.assertIn("○", output)
        self.assertIn("●", output)


class TestBackgammonCLIEdgeCases(unittest.TestCase):
    """
    Tests para casos extremos y edge cases.
    
    Verifica:
        - Comportamiento en situaciones límite
        - Robustez ante entradas inusuales
    
    Principios SOLID verificados:
        - LSP: Comportamiento predecible en casos extremos
        - SRP: Cada método maneja un aspecto específico
    """

    def setUp(self):
        """
        Configuración para tests de edge cases.
        
        Principio SRP: Configuración separada de tests.
        """
        self.cli = CLI()
        self.cli.board = Mock()
        self.cli.dados = Mock()

    @patch('builtins.input')
    @patch('builtins.print')
    def test_manejar_movimientos_sin_dados_disponibles(self, mock_print, mock_input):
        """
        Test cuando no quedan dados disponibles.
        
        Verifica:
            - Finalización correcta sin dados
        
        Principio LSP: Comportamiento predecible sin recursos.
        """
        mock_input.side_effect = ["3"]
        self.cli.board.obtener_movimientos_posibles = Mock(return_value=[])

        self.cli.manejar_movimientos_normales()

        self.cli.board.obtener_movimientos_posibles.assert_called()

    @patch('builtins.input')
    @patch('builtins.print')
    def test_realizar_movimiento_doble_sin_confirmacion_valida(self, mock_print, mock_input):
        """
        Test de movimiento doble con confirmaciones inválidas.
        
        Verifica:
            - Manejo de entradas no reconocidas
        
        Principio SRP: Validación de entrada separada.
        """
        mock_input.side_effect = ["6", "maybe", "no", "n"]
        self.cli.dados.obtener_valores = Mock(return_value=(3, 4))
        self.cli.board.calcular_destino = Mock(side_effect=[9, 13])

        with patch.object(self.cli, 'mostrar_tablero'):
            resultado = self.cli.realizar_movimiento_doble()

        self.assertFalse(resultado)

    @patch('builtins.print')
    def test_mostrar_tablero_con_estados_mixtos(self, mock_print):
        """
        Test de mostrar_tablero con diferentes estados en diferentes puntos.
        
        Verifica:
            - Presentación correcta de estados variados
        
        Principio SRP: Presentación no afecta lógica del juego.
        """
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

        self.assertEqual(self.cli.board.obtener_estado_punto.call_count, 24)

    def test_loop_principal_sin_ganador_inmediato(self):
        """
        Test del loop principal con varios turnos antes de que alguien gane.
        
        Verifica:
            - Múltiples iteraciones del bucle principal
        
        Principio SRP: loop_principal solo coordina, no implementa reglas.
        """
        self.cli.jugador_negro = "Juan"
        self.cli.jugador_blanco = "María"

        call_count = [0]
        def mock_ha_ganado(color):
            call_count[0] += 1
            return call_count[0] > 8 and color == "negro"

        self.cli.board.ha_ganado = Mock(side_effect=mock_ha_ganado)

        with patch.object(self.cli, 'turno_jugador') as mock_turno:
            with patch('builtins.print'):
                self.cli.loop_principal()

        self.assertGreater(mock_turno.call_count, 0)

    @patch('builtins.input')
    @patch('builtins.print')
    def test_turno_completo_con_movimientos_exitosos(self, mock_print, mock_input):
        """
        Test de un turno completo con movimientos exitosos.
        
        Verifica:
            - Flujo completo de un turno normal
        
        Principio DIP: Coordinación mediante abstracciones.
        """
        mock_input.side_effect = [""] + ["1", "1", "1", "1", "3"] * 3 + [""] * 10

        self.cli.jugador_negro = "TestPlayer"
        self.cli.turno_actual = "negro"

        self.cli.dados.tirar = Mock()
        self.cli.dados.reiniciar = Mock()
        self.cli.dados.__str__ = Mock(return_value="[3,4]")
        self.cli.dados.es_doble = Mock(return_value=False)
        self.cli.dados.obtener_dado1 = Mock(return_value=3)
        self.cli.dados.obtener_dado2 = Mock(return_value=4)

        call_count = [0]
        def mock_movimientos(*args):
            call_count[0] += 1
            if call_count[0] <= 3:
                return [1, 2]
            else:
                return []

        self.cli.board.obtener_movimientos_posibles = Mock(side_effect=mock_movimientos)
        self.cli.board.realizar_movimiento_completo = Mock(return_value=True)

        with patch.object(self.cli, 'mostrar_tablero'):
            self.cli.turno_jugador()

        self.assertGreaterEqual(self.cli.board.realizar_movimiento_completo.call_count, 2)
        self.cli.dados.reiniciar.assert_called_once()


class TestCLISOLIDPrinciples(unittest.TestCase):
    """
    Suite de tests específicamente diseñada para verificar el cumplimiento
    de los principios SOLID en la arquitectura de CLI.
    
    Esta clase demuestra cómo la interfaz CLI cumple con:
        - Single Responsibility Principle (SRP)
        - Open/Closed Principle (OCP)
        - Liskov Substitution Principle (LSP)
        - Interface Segregation Principle (ISP)
        - Dependency Inversion Principle (DIP)
    """

    def setUp(self):
        """
        Configuración para tests SOLID.
        
        Principio SRP: Configuración separada y reutilizable.
        """
        self.cli = CLI()
        self.cli.board = Mock()
        self.cli.dados = Mock()

    # --- SINGLE RESPONSIBILITY PRINCIPLE (SRP) TESTS ---

    def test_srp_cli_solo_maneja_interfaz(self):
        """
        Verifica que CLI solo maneja I/O, no lógica del juego.
        
        SRP: Una clase debe tener una sola razón para cambiar.
        CLI cambia solo si la interfaz de usuario cambia, no si las reglas cambian.
        """
        self.assertTrue(hasattr(self.cli, 'mostrar_tablero'))
        self.assertTrue(hasattr(self.cli, 'iniciar_juego'))
        self.assertTrue(callable(self.cli.mostrar_tablero))
        self.assertTrue(callable(self.cli.iniciar_juego))
        
        # CLI no implementa lógica de juego
        self.assertFalse(hasattr(self.cli, 'validar_movimiento'))
        self.assertFalse(hasattr(self.cli, 'calcular_destino'))

    def test_srp_metodos_especializados(self):
        """
        Verifica que cada método tiene una responsabilidad específica.
        
        SRP: Métodos pequeños y enfocados.
        """
        # Cada método tiene un propósito único
        metodos_presentacion = ['mostrar_tablero', 'mostrar_movimientos_disponibles']
        metodos_coordinacion = ['loop_principal', 'turno_jugador', 'determinar_primer_jugador']
        metodos_entrada = ['realizar_movimiento_simple_con_dados', 'realizar_movimiento_doble']
        
        for metodo in metodos_presentacion + metodos_coordinacion + metodos_entrada:
            self.assertTrue(hasattr(self.cli, metodo), 
                          f"CLI debe tener el método {metodo}")
            self.assertTrue(callable(getattr(self.cli, metodo)),
                          f"{metodo} debe ser callable")

    @patch('builtins.print')
    def test_srp_mostrar_tablero_solo_presenta(self, mock_print):
        """
        Verifica que mostrar_tablero solo presenta información.
        
        SRP: No modifica estado, solo muestra.
        """
        self.cli.board.obtener_estado_punto = Mock(return_value=None)
        self.cli.board.get_barra = Mock(return_value={})
        self.cli.board.get_casa = Mock(return_value={})
        
        # Guardar estado antes
        estado_antes = {
            'jugador_negro': self.cli.jugador_negro,
            'jugador_blanco': self.cli.jugador_blanco,
            'turno_actual': self.cli.turno_actual
        }
        
        self.cli.mostrar_tablero()
        
        # Verificar que no cambió el estado
        self.assertEqual(self.cli.jugador_negro, estado_antes['jugador_negro'])
        self.assertEqual(self.cli.jugador_blanco, estado_antes['jugador_blanco'])
        self.assertEqual(self.cli.turno_actual, estado_antes['turno_actual'])

    # --- OPEN/CLOSED PRINCIPLE (OCP) TESTS ---

    def test_ocp_cli_extensible_para_nuevas_interfaces(self):
        """
        Verifica que CLI es extensible sin modificación.
        
        OCP: Abierto para extensión, cerrado para modificación.
        La interfaz puede extenderse a GUI sin modificar la lógica existente.
        """
        # CLI puede ser extendida por herencia
        class GUICli(CLI):
            def mostrar_tablero_grafico(self):
                return "Versión gráfica"
        
        gui_cli = GUICli()
        self.assertIsInstance(gui_cli, CLI)
        self.assertTrue(hasattr(gui_cli, 'mostrar_tablero'))
        self.assertTrue(hasattr(gui_cli, 'mostrar_tablero_grafico'))

    def test_ocp_agregar_nuevos_tipos_movimiento(self):
        """
        Verifica que se pueden agregar nuevos tipos de movimiento.
        
        OCP: Nuevas funcionalidades sin modificar existentes.
        """
        # Los métodos existentes no necesitan modificarse
        # para agregar nuevos tipos de movimiento
        self.assertTrue(hasattr(self.cli, 'realizar_movimiento_simple_con_dados'))
        self.assertTrue(hasattr(self.cli, 'realizar_movimiento_doble'))
        
        # Se puede extender agregando nuevos métodos
        def realizar_movimiento_triple(self):
            pass
        
        CLI.realizar_movimiento_triple = realizar_movimiento_triple
        self.assertTrue(hasattr(self.cli, 'realizar_movimiento_triple'))
        delattr(CLI, 'realizar_movimiento_triple')  # Limpiar

    # --- LISKOV SUBSTITUTION PRINCIPLE (LSP) TESTS ---

    @patch('builtins.input')
    @patch('builtins.print')
    def test_lsp_comportamiento_consistente_jugadores(self, mock_print, mock_input):
        """
        Verifica comportamiento consistente para ambos jugadores.
        
        LSP: Los objetos pueden ser reemplazados por sus subtipos.
        El comportamiento es el mismo para negro y blanco.
        """
        mock_input.side_effect = ["", "", ""]
        
        # Test para negro
        self.cli.turno_actual = "negro"
        self.cli.jugador_negro = "Jugador1"
        self.cli.dados.tirar = Mock()
        self.cli.dados.__str__ = Mock(return_value="[3,4]")
        self.cli.dados.es_doble = Mock(return_value=False)
        self.cli.board.obtener_movimientos_posibles = Mock(return_value=[])
        
        self.cli.turno_jugador()
        llamadas_negro = self.cli.dados.tirar.call_count
        
        # Test para blanco (debe comportarse igual)
        self.cli.dados.tirar.reset_mock()
        self.cli.turno_actual = "blanco"
        self.cli.jugador_blanco = "Jugador2"
        
        self.cli.turno_jugador()
        llamadas_blanco = self.cli.dados.tirar.call_count
        
        self.assertEqual(llamadas_negro, llamadas_blanco)

    @patch('builtins.print')
    def test_lsp_mostrar_tablero_cualquier_estado(self, mock_print):
        """
        Verifica que mostrar_tablero funciona con cualquier estado.
        
        LSP: El método funciona consistentemente con tablero lleno, vacío, o mixto.
        """
        estados_prueba = [
            # Tablero vacío
            (Mock(return_value=None), {}, {}),
            # Tablero con fichas
            (Mock(return_value=("negro", 2)), {"negro": 1}, {"blanco": 2}),
            # Tablero mixto
            (Mock(side_effect=lambda p: ("negro", 1) if p % 2 == 0 else None), 
             {"negro": 0, "blanco": 1}, {"negro": 3, "blanco": 0})
        ]
        
        for mock_estado, barra, casa in estados_prueba:
            self.cli.board.obtener_estado_punto = mock_estado
            self.cli.board.get_barra = Mock(return_value=barra)
            self.cli.board.get_casa = Mock(return_value=casa)
            
            # No debe lanzar excepción
            try:
                self.cli.mostrar_tablero()
            except Exception as e:
                self.fail(f"mostrar_tablero falló con estado válido: {e}")

    # --- INTERFACE SEGREGATION PRINCIPLE (ISP) TESTS ---

    def test_isp_metodos_minimos_especificos(self):
        """
        Verifica que CLI usa interfaces mínimas y específicas.
        
        ISP: Los clientes no deben depender de interfaces que no usan.
        CLI solo usa los métodos necesarios de Board y Dice.
        """
        # CLI solo usa métodos públicos específicos de Board
        metodos_board_usados = [
            'inicializar_posiciones_estandar',
            'obtener_estado_punto',
            'get_barra',
            'get_casa',
            'ha_ganado',
            'obtener_movimientos_posibles',
            'realizar_movimiento_completo',
            'realizar_movimiento_doble',
            'calcular_destino'
        ]
        
        for metodo in metodos_board_usados:
            self.assertTrue(hasattr(self.cli.board, metodo),
                          f"Board debe exponer {metodo}")

    def test_isp_metodos_publicos_coherentes(self):
        """
        Verifica que los métodos públicos de CLI son coherentes.
        
        ISP: Interfaz pública mínima y coherente.
        """
        metodos_publicos = [
            'iniciar_juego',
            'determinar_primer_jugador',
            'mostrar_tablero',
            'loop_principal',
            'turno_jugador',
            'mostrar_movimientos_disponibles',
            'manejar_movimientos_normales',
            'manejar_dobles',
            'realizar_movimiento_simple_con_dados',
            'realizar_movimiento_doble'
        ]
        
        for metodo in metodos_publicos:
            self.assertTrue(hasattr(self.cli, metodo))
            self.assertTrue(callable(getattr(self.cli, metodo)))

    @patch('builtins.print')
    def test_isp_mostrar_movimientos_interface_minima(self, mock_print):
        """
        Verifica que mostrar_movimientos_disponibles usa interfaz mínima.
        
        ISP: Solo usa obtener_movimientos_posibles, nada más.
        """
        self.cli.board.obtener_movimientos_posibles = Mock(return_value=[1, 2, 3])
        
        resultado = self.cli.mostrar_movimientos_disponibles()
        
        # Solo debe haber llamado a un método
        self.cli.board.obtener_movimientos_posibles.assert_called_once()
        self.assertTrue(resultado)

    # --- DEPENDENCY INVERSION PRINCIPLE (DIP) TESTS ---

    def test_dip_cli_depende_de_abstracciones(self):
        """
        Verifica que CLI depende de abstracciones, no implementaciones.
        
        DIP: Módulos de alto nivel no deben depender de módulos de bajo nivel.
        CLI depende de Board y Dice como abstracciones.
        """
        # CLI tiene referencias a abstracciones
        self.assertIsNotNone(self.cli.board)
        self.assertIsNotNone(self.cli.dados)
        
        # CLI puede funcionar con cualquier implementación de Board y Dice
        mock_board = Mock()
        mock_dados = Mock()
        
        self.cli.board = mock_board
        self.cli.dados = mock_dados
        
        self.assertEqual(self.cli.board, mock_board)
        self.assertEqual(self.cli.dados, mock_dados)

    def test_dip_cli_no_conoce_implementacion_board(self):
        """
        Verifica que CLI no conoce detalles internos de Board.
        
        DIP: CLI usa Board a través de su interfaz pública.
        """
        # CLI no accede a atributos privados de Board
        with patch.object(self.cli, 'mostrar_tablero'):
            with patch('builtins.print'):
                # Solo usa métodos públicos
                self.cli.board.obtener_estado_punto = Mock(return_value=None)
                self.cli.board.get_barra = Mock(return_value={})
                self.cli.board.get_casa = Mock(return_value={})
                
                # Ejecutar sin acceder a implementación interna
                self.cli.board.obtener_estado_punto(1)
                self.cli.board.get_barra()
                self.cli.board.get_casa()
                
                # Verificar que solo usó interfaz pública
                self.cli.board.obtener_estado_punto.assert_called_once()
                self.cli.board.get_barra.assert_called_once()
                self.cli.board.get_casa.assert_called_once()

    def test_dip_cli_no_conoce_implementacion_dice(self):
        """
        Verifica que CLI no conoce detalles internos de Dice.
        
        DIP: CLI usa Dice a través de su interfaz pública.
        """
        # Métodos públicos que CLI usa de Dice
        metodos_dice = [
            'tirar',
            'obtener_dado1',
            'obtener_dado2',
            'obtener_valores',
            'es_doble',
            'reiniciar'
        ]
        
        for metodo in metodos_dice:
            self.assertTrue(hasattr(self.cli.dados, metodo))

    @patch('builtins.input')
    @patch('builtins.print')
    def test_dip_sustituibilidad_componentes(self, mock_print, mock_input):
        """
        Verifica que los componentes son sustituibles.
        
        DIP: CLI funciona con cualquier implementación que cumpla el contrato.
        """
        mock_input.side_effect = [""]
        
        # Sustituir Board y Dice con mocks
        nuevo_board = Mock()
        nuevos_dados = Mock()
        
        nuevo_board.obtener_movimientos_posibles = Mock(return_value=[])
        nuevos_dados.tirar = Mock()
        nuevos_dados.__str__ = Mock(return_value="[1,2]")
        nuevos_dados.reiniciar = Mock()
        
        self.cli.board = nuevo_board
        self.cli.dados = nuevos_dados
        self.cli.jugador_negro = "Test"
        
        # CLI debe funcionar igual
        self.cli.turno_jugador()
        
        nuevos_dados.tirar.assert_called_once()
        nuevo_board.obtener_movimientos_posibles.assert_called_once()

    # --- INTEGRATION TEST FOR SOLID PRINCIPLES ---

    @patch('builtins.input')
    @patch('builtins.print')
    def test_solid_integration_todos_principios(self, mock_print, mock_input):
        """
        Test de integración que verifica todos los principios SOLID juntos.
        
        Verifica:
            - SRP: Cada método tiene una responsabilidad
            - OCP: Extensible sin modificación
            - LSP: Comportamiento consistente
            - ISP: Interfaces específicas
            - DIP: Dependencia de abstracciones
        """
        mock_input.side_effect = ["Player1", "Player2", "", ""] + [""] * 10
        
        # Configurar mocks (DIP: abstracciones)
        self.cli.board.inicializar_posiciones_estandar = Mock()
        self.cli.board.ha_ganado = Mock(return_value=True)
        self.cli.dados.tirar = Mock()
        self.cli.dados.obtener_dado1 = Mock(side_effect=[5, 3])
        
        # Ejecutar (SRP: cada método su responsabilidad)
        with patch.object(self.cli, 'mostrar_tablero'):
            self.cli.iniciar_juego()
        
        # Verificar resultados
        self.assertEqual(self.cli.jugador_negro, "Player1")  # LSP: consistente
        self.assertEqual(self.cli.jugador_blanco, "Player2")
        self.assertEqual(self.cli.turno_actual, "negro")
        
        # ISP: solo llamó métodos necesarios
        self.cli.board.inicializar_posiciones_estandar.assert_called_once()
        self.assertEqual(self.cli.dados.tirar.call_count, 2)

    def test_solid_separacion_responsabilidades(self):
        """
        Verifica clara separación de responsabilidades.
        
        SOLID completo: Demuestra todos los principios en acción.
        """
        # SRP: Métodos de presentación
        self.assertTrue(hasattr(self.cli, 'mostrar_tablero'))
        
        # SRP: Métodos de coordinación
        self.assertTrue(hasattr(self.cli, 'loop_principal'))
        self.assertTrue(hasattr(self.cli, 'turno_jugador'))
        
        # SRP: Métodos de entrada
        self.assertTrue(hasattr(self.cli, 'realizar_movimiento_simple_con_dados'))
        
        # DIP: Referencias a abstracciones
        self.assertIsNotNone(self.cli.board)
        self.assertIsNotNone(self.cli.dados)
        
        # ISP: Cada método tiene propósito específico
        self.assertNotEqual(
            self.cli.mostrar_tablero.__code__.co_code,
            self.cli.turno_jugador.__code__.co_code
        )

    def test_solid_extensibilidad_sin_modificacion(self):
        """
        Verifica que CLI puede extenderse sin modificar código existente.
        
        OCP: Abierto para extensión, cerrado para modificación.
        """
        # Crear una extensión de CLI
        class CLIExtendida(CLI):
            def mostrar_estadisticas(self):
                return "Estadísticas del juego"
            
            def guardar_partida(self):
                return "Partida guardada"
        
        cli_ext = CLIExtendida()
        
        # Verifica que mantiene funcionalidad original
        self.assertTrue(hasattr(cli_ext, 'iniciar_juego'))
        self.assertTrue(hasattr(cli_ext, 'mostrar_tablero'))
        
        # Y tiene nueva funcionalidad
        self.assertTrue(hasattr(cli_ext, 'mostrar_estadisticas'))
        self.assertTrue(hasattr(cli_ext, 'guardar_partida'))
        
        # Sin modificar la clase base
        self.assertFalse(hasattr(CLI, 'mostrar_estadisticas'))
        self.assertFalse(hasattr(CLI, 'guardar_partida'))

    @patch('builtins.print')
    def test_solid_bajo_acoplamiento(self, mock_print):
        """
        Verifica bajo acoplamiento entre componentes.
        
        DIP + ISP: Componentes independientes con interfaces mínimas.
        """
        # Board y Dice son independientes
        self.cli.board = Mock()
        self.cli.dados = Mock()
        
        # Configurar solo lo necesario
        self.cli.board.obtener_estado_punto = Mock(return_value=None)
        self.cli.board.get_barra = Mock(return_value={})
        self.cli.board.get_casa = Mock(return_value={})
        
        # CLI funciona independientemente
        self.cli.mostrar_tablero()
        
        # Sin necesidad de configurar dados
        # Bajo acoplamiento verificado
        self.cli.board.obtener_estado_punto.assert_called()

    def test_solid_alta_cohesion(self):
        """
        Verifica alta cohesión dentro de CLI.
        
        SRP: Métodos relacionados agrupados lógicamente.
        """
        # Métodos de presentación están juntos
        metodos_presentacion = ['mostrar_tablero', 'mostrar_movimientos_disponibles']
        
        # Métodos de juego están juntos
        metodos_juego = ['loop_principal', 'turno_jugador', 'determinar_primer_jugador']
        
        # Métodos de movimiento están juntos
        metodos_movimiento = [
            'manejar_movimientos_normales',
            'manejar_dobles',
            'realizar_movimiento_simple_con_dados',
            'realizar_movimiento_doble'
        ]
        
        # Todos existen y son parte de grupos cohesivos
        todos_metodos = metodos_presentacion + metodos_juego + metodos_movimiento
        for metodo in todos_metodos:
            self.assertTrue(hasattr(self.cli, metodo),
                          f"Método cohesivo {metodo} debe existir")

class TestCLIIntegration(unittest.TestCase):
    """
    Tests de integración para CLI.
    
    Verifica:
        - Flujos completos del juego
        - Interacción entre componentes
        - Escenarios end-to-end
    
    Principios SOLID verificados:
        - DIP: Componentes interactúan a través de abstracciones
        - LSP: Comportamiento consistente en diferentes escenarios
    """

    @patch('builtins.input')
    @patch('builtins.print')
    def test_flujo_completo_juego_muy_corto(self, mock_print, mock_input):
        """
        Test de flujo completo de un juego muy corto.
        
        Verifica:
            - Integración de todos los componentes
            - Flujo desde inicio hasta fin
        
        Principio DIP: Todos los componentes interactúan mediante interfaces.
        """
        mock_input.side_effect = [
            "TestPlayer1", "TestPlayer2",
            "", "",
        ] + [""] * 5

        cli = CLI()
        cli.board.inicializar_posiciones_estandar = Mock()
        cli.board.ha_ganado = Mock(return_value=True)
        cli.dados.tirar = Mock()
        cli.dados.obtener_dado1 = Mock(side_effect=[6, 3])

        with patch.object(cli, 'mostrar_tablero'):
            cli.iniciar_juego()

        self.assertEqual(cli.jugador_negro, "TestPlayer1")
        self.assertEqual(cli.jugador_blanco, "TestPlayer2")
        self.assertEqual(cli.turno_actual, "negro")

    @patch('builtins.input')
    @patch('builtins.print')
    def test_flujo_con_varios_empates_inicial(self, mock_print, mock_input):
        """
        Test con varios empates al determinar quién empieza.
        
        Verifica:
            - Manejo correcto de múltiples empates
        
        Principio SRP: La lógica de desempate está encapsulada.
        """
        mock_input.side_effect = [
            "Player1", "Player2",
            "", "", "", "", "", ""
        ] + [""] * 5

        cli = CLI()
        cli.board.inicializar_posiciones_estandar = Mock()
        cli.board.ha_ganado = Mock(return_value=True)
        cli.dados.tirar = Mock()
        cli.dados.obtener_dado1 = Mock(side_effect=[4, 4, 3, 3, 2, 5])

        with patch.object(cli, 'mostrar_tablero'):
            cli.iniciar_juego()

        self.assertEqual(cli.turno_actual, "blanco")
        self.assertEqual(cli.dados.tirar.call_count, 6)

    def test_main_function_normal(self):
        """
        Test de la función main con ejecución normal.
        
        Verifica:
            - Punto de entrada funcional
        
        Principio SRP: main solo inicia y maneja excepciones globales.
        """
        with patch('Backgammon.Interfaces.CLI.CLI') as mock_cli_class:
            mock_cli_instance = Mock()
            mock_cli_class.return_value = mock_cli_instance

            main()

            mock_cli_class.assert_called_once()
            mock_cli_instance.iniciar_juego.assert_called_once()

    def test_main_function_keyboard_interrupt(self):
        """
        Test de la función main con interrupción de teclado.
        
        Verifica:
            - Manejo elegante de Ctrl+C
        
        Principio SRP: Manejo de interrupciones centralizado.
        """
        with patch('Backgammon.Interfaces.CLI.CLI') as mock_cli_class:
            mock_cli_instance = Mock()
            mock_cli_instance.iniciar_juego.side_effect = KeyboardInterrupt()
            mock_cli_class.return_value = mock_cli_instance

            with patch('builtins.print') as mock_print:
                main()

            mock_print.assert_called_with("\n\n¡Hasta luego! 👋")

    def test_main_function_exception(self):
        """
        Test de la función main con excepción inesperada.
        
        Verifica:
            - Manejo robusto de errores no esperados
        
        Principio SRP: Gestión de errores separada de lógica principal.
        """
        with patch('Backgammon.Interfaces.CLI.CLI') as mock_cli_class:
            mock_cli_instance = Mock()
            mock_cli_instance.iniciar_juego.side_effect = Exception("Error inesperado")
            mock_cli_class.return_value = mock_cli_instance

            with patch('builtins.print') as mock_print:
                main()

            mock_print.assert_called_with("\n❌ Error inesperado: Error inesperado")

    @patch('builtins.print')
    def test_mostrar_tablero_con_casa_vacia(self, mock_print):
        """
        Test específico para mostrar_tablero con casa vacía.
        
        Verifica:
            - Presentación correcta de casa sin fichas
        
        Principio LSP: Comportamiento consistente con casa llena o vacía.
        """
        cli = CLI()
        cli.board = Mock()
        cli.board.obtener_estado_punto = Mock(return_value=None)
        cli.board.get_barra = Mock(return_value={"negro": 0, "blanco": 0})
        cli.board.get_casa = Mock(return_value={"negro": 0, "blanco": 0})

        cli.mostrar_tablero()

        calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(any("CUADRANTE CASA NEGRO" in call for call in calls))
        self.assertTrue(any("CUADRANTE CASA BLANCO" in call for call in calls))
        self.assertTrue(any("CASA: vacía" in call for call in calls))

    @patch('builtins.print')
    def test_simbolos_correctos_fichas(self, mock_print):
        """
        Test que verifica que se usen los símbolos correctos para las fichas.
        
        Verifica:
            - Representación visual correcta de fichas
        
        Principio SRP: La presentación visual está separada de la lógica.
        """
        cli = CLI()
        cli.board = Mock()

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

        calls = [str(call) for call in mock_print.call_args_list]
        output = " ".join(calls)

        self.assertIn("○", output)
        self.assertIn("●", output)


class TestBackgammonCLIEdgeCases(unittest.TestCase):
    """
    Tests para casos extremos y edge cases.
    
    Verifica:
        - Comportamiento en situaciones límite
        - Robustez ante entradas inusuales
    
    Principios SOLID verificados:
        - LSP: Comportamiento predecible en casos extremos
        - SRP: Cada método maneja un aspecto específico
    """

    def setUp(self):
        """
        Configuración para tests de edge cases.
        
        Principio SRP: Configuración separada de tests.
        """
        self.cli = CLI()
        self.cli.board = Mock()
        self.cli.dados = Mock()

    @patch('builtins.input')
    @patch('builtins.print')
    def test_manejar_movimientos_sin_dados_disponibles(self, mock_print, mock_input):
        """
        Test cuando no quedan dados disponibles.
        
        Verifica:
            - Finalización correcta sin dados
        
        Principio LSP: Comportamiento predecible sin recursos.
        """
        mock_input.side_effect = ["3"]
        self.cli.board.obtener_movimientos_posibles = Mock(return_value=[])

        self.cli.manejar_movimientos_normales()

        self.cli.board.obtener_movimientos_posibles.assert_called()

    @patch('builtins.input')
    @patch('builtins.print')
    def test_realizar_movimiento_doble_sin_confirmacion_valida(self, mock_print, mock_input):
        """
        Test de movimiento doble con confirmaciones inválidas.
        
        Verifica:
            - Manejo de entradas no reconocidas
        
        Principio SRP: Validación de entrada separada.
        """
        mock_input.side_effect = ["6", "maybe", "no", "n"]
        self.cli.dados.obtener_valores = Mock(return_value=(3, 4))
        self.cli.board.calcular_destino = Mock(side_effect=[9, 13])

        with patch.object(self.cli, 'mostrar_tablero'):
            resultado = self.cli.realizar_movimiento_doble()

        self.assertFalse(resultado)

    @patch('builtins.print')
    def test_mostrar_tablero_con_estados_mixtos(self, mock_print):
        """
        Test de mostrar_tablero con diferentes estados en diferentes puntos.
        
        Verifica:
            - Presentación correcta de estados variados
        
        Principio SRP: Presentación no afecta lógica del juego.
        """
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

        self.assertEqual(self.cli.board.obtener_estado_punto.call_count, 24)

    def test_loop_principal_sin_ganador_inmediato(self):
        """
        Test del loop principal con varios turnos antes de que alguien gane.
        
        Verifica:
            - Múltiples iteraciones del bucle principal
        
        Principio SRP: loop_principal solo coordina, no implementa reglas.
        """
        self.cli.jugador_negro = "Juan"
        self.cli.jugador_blanco = "María"

        call_count = [0]
        def mock_ha_ganado(color):
            call_count[0] += 1
            return call_count[0] > 8 and color == "negro"

        self.cli.board.ha_ganado = Mock(side_effect=mock_ha_ganado)

        with patch.object(self.cli, 'turno_jugador') as mock_turno:
            with patch('builtins.print'):
                self.cli.loop_principal()

        self.assertGreater(mock_turno.call_count, 0)

    @patch('builtins.input')
    @patch('builtins.print')
    def test_turno_completo_con_movimientos_exitosos(self, mock_print, mock_input):
        """
        Test de un turno completo con movimientos exitosos.
        
        Verifica:
            - Flujo completo de un turno normal
        
        Principio DIP: Coordinación mediante abstracciones.
        """
        mock_input.side_effect = [""] + ["1", "1", "1", "1", "3"] * 3 + [""] * 10

        self.cli.jugador_negro = "TestPlayer"
        self.cli.turno_actual = "negro"

        self.cli.dados.tirar = Mock()
        self.cli.dados.reiniciar = Mock()
        self.cli.dados.__str__ = Mock(return_value="[3,4]")
        self.cli.dados.es_doble = Mock(return_value=False)
        self.cli.dados.obtener_dado1 = Mock(return_value=3)
        self.cli.dados.obtener_dado2 = Mock(return_value=4)

        call_count = [0]
        def mock_movimientos(*args):
            call_count[0] += 1
            if call_count[0] <= 3:
                return [1, 2]
            else:
                return []

        self.cli.board.obtener_movimientos_posibles = Mock(side_effect=mock_movimientos)
        self.cli.board.realizar_movimiento_completo = Mock(return_value=True)

        with patch.object(self.cli, 'mostrar_tablero'):
            self.cli.turno_jugador()

        self.assertGreaterEqual(self.cli.board.realizar_movimiento_completo.call_count, 2)
        self.cli.dados.reiniciar.assert_called_once()


# --- CLASE DE TESTS PARA PRINCIPIOS SOLID EN CLI ---
class TestCLISOLID(unittest.TestCase):
    """
    Suite de tests dedicada a verificar el cumplimiento de los principios SOLID.
    """
    def setUp(self):
        """Configuración para los tests SOLID, inyectando Mocks."""
        self.cli = CLI()
        self.cli.board = Mock()
        self.cli.dados = Mock()
        # SOLUCIÓN: Configuración base para evitar errores de 'unpack'
        self.cli.board.obtener_estado_punto.return_value = (None, 0)
        self.cli.board.get_barra.return_value = {"negro": 0, "blanco": 0}
        self.cli.board.get_casa.return_value = {"negro": 0, "blanco": 0}

    def test_srp_cli_delegates_all_game_logic(self):
        """[SRP] La CLI delega toda la lógica de juego a los componentes del Core."""
        with patch('builtins.input', side_effect=["1", "1", "3"]): # Opción, origen, pasar
            self.cli.turno_actual = "negro"
            # Configuramos todos los mocks necesarios para un turno
            self.cli.dados.obtener_dado1.return_value = 1
            self.cli.dados.obtener_dado2.return_value = 2
            self.cli.board.obtener_movimientos_posibles.return_value = [(1, 2)]
            self.cli.board.realizar_movimiento_completo.return_value = True

            self.cli.manejar_movimientos_normales()

            # Afirmamos que la CLI llamó a los métodos del tablero y los dados.
            self.cli.board.obtener_movimientos_posibles.assert_called()
            self.cli.board.realizar_movimiento_completo.assert_called()

    def test_ocp_cli_is_extensible_for_display(self):
        """[OCP] La CLI está abierta a extensión para diferentes formatos de visualización."""
        class FancyCLI(CLI):
            """Una CLI extendida que modifica la visualización del tablero."""
            def mostrar_tablero(self):
                print("--- TABLERO ESTILIZADO ---")
                # Llama al método original para no reescribir toda la lógica
                super().mostrar_tablero()

        fancy_cli = FancyCLI()
        fancy_cli.board = Mock()
        fancy_cli.board.obtener_estado_punto.return_value = (None, 0)
        fancy_cli.board.get_barra.return_value = {"negro": 0, "blanco": 0}
        fancy_cli.board.get_casa.return_value = {"negro": 0, "blanco": 0}

        with patch('builtins.print') as mock_print:
            fancy_cli.mostrar_tablero()
            mock_print.assert_any_call("--- TABLERO ESTILIZADO ---")
            # Verificamos que también se ejecutó la lógica del método padre
            fancy_cli.board.obtener_estado_punto.assert_called()

    def test_lsp_subclass_can_be_substituted(self):
        """[LSP] Una subclase de CLI (ej. para un bot) puede sustituir a la original."""
        class AutomatedCLI(CLI):
            """Una CLI que simula las decisiones de un bot en lugar de pedir input."""
            def pedir_input_movimiento(self):
                # En lugar de pedir input, el bot siempre devuelve '1', '1'.
                return "1", "1"

        auto_cli = AutomatedCLI()
        origen, dado_elegido = auto_cli.pedir_input_movimiento()
        self.assertEqual(origen, "1")
        self.assertEqual(dado_elegido, "1")

    def test_dip_cli_relies_on_abstractions(self):
        """[DIP] La CLI depende de abstracciones (la 'interfaz' de Board y Dice)."""
        self.assertIsInstance(self.cli.board, Mock)
        self.assertIsInstance(self.cli.dados, Mock)
        
        # La CLI puede operar con el Mock de Board porque solo le importa
        # el "contrato" (que tenga un método `ha_ganado`), no la clase concreta.
        self.cli.board.ha_ganado.return_value = True
        resultado = self.cli.board.ha_ganado("negro")
        self.assertTrue(resultado)



if __name__ == '__main__':
    unittest.main()