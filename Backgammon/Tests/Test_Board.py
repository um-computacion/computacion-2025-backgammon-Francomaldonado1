import unittest
from Backgammon.Core.Board import Board
from Backgammon.Core.Dice import Dice
from Backgammon.Core.Player import Player

class TestBoardFunctionality(unittest.TestCase):
    """Tests de funcionalidad completa para Board."""
    
    def setUp(self):
        """Crea tablero limpio para cada test."""
        self.tablero = Board()
    
    # --- Tests de Inicialización ---
    
    def test_inicializacion_tablero_vacio(self):
        """
        Verifica que el tablero inicia vacío.
        
        SOLID: SRP - Constructor simple que inicializa estructuras.
        """
        for i in range(1, 25):
            self.assertTrue(self.tablero.esta_vacio(i))
            self.assertIsNone(self.tablero.obtener_estado_punto(i))
    
    def test_inicializacion_estandar_correcta(self):
        """
        Verifica configuración inicial estándar del backgammon.
        
        SOLID: OCP - Configuración extensible para variantes.
        """
        self.tablero.inicializar_posiciones_estandar()
        
        # Fichas negras
        self.assertEqual(self.tablero.obtener_estado_punto(1), ["negro", 2])
        self.assertEqual(self.tablero.obtener_estado_punto(12), ["negro", 5])
        self.assertEqual(self.tablero.obtener_estado_punto(17), ["negro", 3])
        self.assertEqual(self.tablero.obtener_estado_punto(19), ["negro", 5])
        
        # Fichas blancas
        self.assertEqual(self.tablero.obtener_estado_punto(24), ["blanco", 2])
        self.assertEqual(self.tablero.obtener_estado_punto(13), ["blanco", 5])
        self.assertEqual(self.tablero.obtener_estado_punto(8), ["blanco", 3])
        self.assertEqual(self.tablero.obtener_estado_punto(6), ["blanco", 5])
    
    # --- Tests de Colocación de Fichas ---
    
    def test_colocar_ficha_punto_vacio(self):
        """
        Verifica colocación en punto vacío.
        
        SOLID: SRP - Operación simple de modificación de estado.
        """
        self.tablero.colocar_ficha(1, "negro", 1)
        self.assertEqual(self.tablero.obtener_estado_punto(1), ["negro", 1])
    
    def test_colocar_fichas_mismo_color_apila(self):
        """
        Verifica que fichas del mismo color se apilan.
        
        SOLID: SRP - Lógica de apilamiento simple.
        """
        self.tablero.colocar_ficha(5, "blanco", 2)
        self.tablero.colocar_ficha(5, "blanco", 3)
        self.assertEqual(self.tablero.obtener_estado_punto(5), ["blanco", 5])
    
    def test_colocar_fichas_colores_diferentes_error(self):
        """
        Verifica error al mezclar colores.
        
        SOLID: ISP - Validación apropiada de reglas básicas.
        """
        self.tablero.colocar_ficha(10, "negro", 1)
        with self.assertRaises(ValueError) as context:
            self.tablero.colocar_ficha(10, "blanco", 1)
        self.assertIn("No se pueden mezclar", str(context.exception))
    
    # --- Tests de Remoción de Fichas ---
    
    def test_remover_fichas_parcial(self):
        """
        Verifica remoción parcial de fichas.
        
        SOLID: SRP - Modificación de estado controlada.
        """
        self.tablero.colocar_ficha(8, "negro", 5)
        self.tablero.remover_ficha(8, 3)
        self.assertEqual(self.tablero.obtener_estado_punto(8), ["negro", 2])
    
    def test_remover_todas_fichas_punto_vacio(self):
        """
        Verifica que remover todas las fichas vacía el punto.
        
        SOLID: SRP - Estado consistente después de operación.
        """
        self.tablero.colocar_ficha(12, "blanco", 2)
        self.tablero.remover_ficha(12, 2)
        self.assertTrue(self.tablero.esta_vacio(12))
        self.assertIsNone(self.tablero.obtener_estado_punto(12))
    
    def test_remover_de_punto_vacio_error(self):
        """
        Verifica error al remover de punto vacío.
        
        SOLID: ISP - Validación de precondiciones.
        """
        with self.assertRaises(ValueError) as context:
            self.tablero.remover_ficha(3, 1)
        self.assertIn("No hay fichas", str(context.exception))
    
    def test_remover_mas_fichas_que_existentes_error(self):
        """
        Verifica error al remover más fichas de las disponibles.
        
        SOLID: ISP - Protección de invariantes.
        """
        self.tablero.colocar_ficha(20, "negro", 2)
        with self.assertRaises(ValueError) as context:
            self.tablero.remover_ficha(20, 5)
        self.assertIn("No hay suficientes", str(context.exception))
    
    # --- Tests de Movimiento de Fichas ---
    
    def test_mover_ficha_punto_vacio(self):
        """
        Verifica movimiento a punto vacío.
        
        SOLID: SRP - Coordinación de operaciones básicas.
        """
        self.tablero.colocar_ficha(5, "negro", 2)
        self.tablero.mover_ficha(5, 10, "negro")
        
        self.assertEqual(self.tablero.obtener_estado_punto(5), ["negro", 1])
        self.assertEqual(self.tablero.obtener_estado_punto(10), ["negro", 1])
    
    def test_mover_ficha_apilar_mismo_color(self):
        """
        Verifica apilamiento al mover a punto con mismo color.
        
        SOLID: SRP - Lógica de apilamiento consistente.
        """
        self.tablero.colocar_ficha(8, "blanco", 3)
        self.tablero.colocar_ficha(15, "blanco", 2)
        self.tablero.mover_ficha(8, 15, "blanco")
        
        self.assertEqual(self.tablero.obtener_estado_punto(8), ["blanco", 2])
        self.assertEqual(self.tablero.obtener_estado_punto(15), ["blanco", 3])
    
    def test_mover_ficha_captura_contraria(self):
        """
        Verifica captura de ficha contraria solitaria.
        
        SOLID: SRP - Lógica de captura bien definida.
        """
        self.tablero.colocar_ficha(12, "negro", 1)
        self.tablero.colocar_ficha(18, "blanco", 1)
        self.tablero.mover_ficha(12, 18, "negro")
        
        self.assertTrue(self.tablero.esta_vacio(12))
        self.assertEqual(self.tablero.obtener_estado_punto(18), ["negro", 1])
        self.assertEqual(self.tablero.get_barra(), {"blanco": 1})
    
    def test_mover_ficha_punto_bloqueado_error(self):
        """
        Verifica error al mover a punto bloqueado (2+ fichas contrarias).
        
        SOLID: ISP - Validación de reglas de bloqueo.
        """
        self.tablero.colocar_ficha(6, "negro", 1)
        self.tablero.colocar_ficha(14, "blanco", 2)
        
        with self.assertRaises(ValueError) as context:
            self.tablero.mover_ficha(6, 14, "negro")
        self.assertIn("bloqueado", str(context.exception))
    
    def test_mover_desde_punto_vacio_error(self):
        """
        Verifica error al mover desde punto vacío.
        
        SOLID: ISP - Validación de origen.
        """
        with self.assertRaises(ValueError) as context:
            self.tablero.mover_ficha(7, 13, "negro")
        self.assertIn("No hay fichas del color indicado en el origen", str(context.exception))
    
    def test_mover_color_incorrecto_error(self):
        """
        Verifica error al intentar mover ficha de otro color.
        
        SOLID: ISP - Validación de pertenencia.
        """
        self.tablero.colocar_ficha(9, "blanco", 2)
        
        with self.assertRaises(ValueError) as context:
            self.tablero.mover_ficha(9, 16, "negro")
        self.assertIn("No hay fichas del color indicado en el origen", str(context.exception))
    
    # --- Tests de Barra ---
    
    def test_enviar_a_barra_color_nuevo(self):
        """
        Verifica envío de ficha a barra (color nuevo).
        
        SOLID: SRP - Gestión de barra independiente.
        """
        self.tablero.enviar_a_barra("negro")
        self.assertEqual(self.tablero.get_barra(), {"negro": 1})
    
    def test_enviar_a_barra_color_existente(self):
        """
        Verifica envío múltiple a barra.
        
        SOLID: SRP - Acumulación correcta en barra.
        """
        self.tablero.enviar_a_barra("blanco")
        self.tablero.enviar_a_barra("blanco")
        self.tablero.enviar_a_barra("negro")
        
        self.assertEqual(self.tablero.get_barra(), {"blanco": 2, "negro": 1})
    
    def test_tiene_fichas_en_barra(self):
        """
        Verifica detección de fichas en barra.
        
        SOLID: ISP - Consulta simple de estado.
        """
        self.assertFalse(self.tablero.tiene_fichas_en_barra("negro"))
        
        self.tablero.enviar_a_barra("negro")
        self.assertTrue(self.tablero.tiene_fichas_en_barra("negro"))
    
    def test_mover_desde_barra_exitoso(self):
        """
        Verifica movimiento exitoso desde barra.
        
        SOLID: SRP - Lógica de reincorporación.
        """
        self.tablero.enviar_a_barra("negro")
        exito = self.tablero.mover_desde_barra("negro", 3)
        
        self.assertTrue(exito)
        self.assertEqual(self.tablero.obtener_estado_punto(3), ["negro", 1])
        self.assertFalse(self.tablero.tiene_fichas_en_barra("negro"))
    
    def test_mover_desde_barra_punto_bloqueado(self):
        """
        Verifica fallo al mover desde barra a punto bloqueado.
        
        SOLID: ISP - Validación de destino.
        """
        self.tablero.enviar_a_barra("blanco")
        self.tablero.colocar_ficha(22, "negro", 2)
        
        exito = self.tablero.mover_desde_barra("blanco", 3)
        
        self.assertFalse(exito)
        self.assertTrue(self.tablero.tiene_fichas_en_barra("blanco"))
    
    # --- Tests de Casa (Bearing Off) ---
    
    def test_sacar_ficha_a_casa(self):
        """
        Verifica envío de ficha a casa.
        
        SOLID: SRP - Gestión de casa independiente.
        """
        self.tablero.sacar_ficha("negro")
        self.assertEqual(self.tablero.get_casa(), {"negro": 1})
    
    def test_sacar_multiples_fichas_casa(self):
        """
        Verifica acumulación en casa.
        
        SOLID: SRP - Contador de fichas en casa.
        """
        for _ in range(5):
            self.tablero.sacar_ficha("blanco")
        
        self.assertEqual(self.tablero.get_casa(), {"blanco": 5})
    
    def test_puede_sacar_fichas_todas_en_cuadrante(self):
        """
        Verifica detección correcta de posibilidad de bearing off.
        
        SOLID: ISP - Validación de condición de bearing off.
        """
        # Negro debe tener todas en 19-24
        self.tablero.colocar_ficha(19, "negro", 15)
        self.assertTrue(self.tablero.puede_sacar_fichas("negro"))
        
        # Blanco debe tener todas en 1-6
        self.tablero.colocar_ficha(1, "blanco", 15)
        self.assertTrue(self.tablero.puede_sacar_fichas("blanco"))
    
    def test_no_puede_sacar_fichas_fuera_cuadrante(self):
        """
        Verifica que no puede sacar si tiene fichas fuera del cuadrante.
        
        SOLID: ISP - Validación completa de bearing off.
        """
        self.tablero.colocar_ficha(19, "negro", 14)
        self.tablero.colocar_ficha(10, "negro", 1)  # Fuera del cuadrante
        
        self.assertFalse(self.tablero.puede_sacar_fichas("negro"))
    
    def test_no_puede_sacar_con_fichas_en_barra(self):
        """
        Verifica que no puede sacar si tiene fichas en barra.
        
        SOLID: ISP - Precondición de bearing off.
        """
        self.tablero.colocar_ficha(1, "blanco", 15)
        self.tablero.enviar_a_barra("blanco")
        
        self.assertFalse(self.tablero.puede_sacar_fichas("blanco"))
    
    def test_ha_ganado_15_fichas_casa(self):
        """
        Verifica detección de victoria.
        
        SOLID: SRP - Condición de victoria simple.
        """
        self.assertFalse(self.tablero.ha_ganado("negro"))
        
        for _ in range(15):
            self.tablero.sacar_ficha("negro")
        
        self.assertTrue(self.tablero.ha_ganado("negro"))
    
    # --- Tests de Cálculo de Destino ---
    
    def test_calcular_destino_negro(self):
        """
        Verifica cálculo correcto de destino para negro.
        
        SOLID: SRP - Cálculo puro sin efectos secundarios.
        """
        self.assertEqual(self.tablero.calcular_destino(5, 3, "negro"), 8)
        self.assertEqual(self.tablero.calcular_destino(22, 6, "negro"), 25)  # Sale
    
    def test_calcular_destino_blanco(self):
        """
        Verifica cálculo correcto de destino para blanco.
        
        SOLID: SRP - Lógica de dirección consistente.
        """
        self.assertEqual(self.tablero.calcular_destino(20, 3, "blanco"), 17)
        self.assertEqual(self.tablero.calcular_destino(3, 4, "blanco"), 0)  # Sale
    
    # --- Tests de Validación de Movimiento ---
    
    def test_es_movimiento_valido_punto_vacio(self):
        """
        Verifica que punto vacío es válido.
        
        SOLID: ISP - Consulta de estado simple.
        """
        self.assertTrue(self.tablero.es_movimiento_valido_a_punto(5, "negro"))
    
    def test_es_movimiento_valido_mismo_color(self):
        """
        Verifica que punto con mismo color es válido.
        
        SOLID: ISP - Lógica de apilamiento.
        """
        self.tablero.colocar_ficha(10, "blanco", 2)
        self.assertTrue(self.tablero.es_movimiento_valido_a_punto(10, "blanco"))
    
    def test_es_movimiento_valido_captura(self):
        """
        Verifica que puede capturar ficha solitaria.
        
        SOLID: ISP - Regla de captura.
        """
        self.tablero.colocar_ficha(15, "blanco", 1)
        self.assertTrue(self.tablero.es_movimiento_valido_a_punto(15, "negro"))
    
    def test_es_movimiento_invalido_bloqueado(self):
        """
        Verifica que punto bloqueado es inválido.
        
        SOLID: ISP - Regla de bloqueo.
        """
        self.tablero.colocar_ficha(18, "blanco", 2)
        self.assertFalse(self.tablero.es_movimiento_valido_a_punto(18, "negro"))
    
    # --- Tests de Integración con Dice ---
    
    def test_realizar_movimiento_completo_con_dados(self):
        """
        Verifica movimiento completo usando dados.
        
        SOLID: DIP - Usa Dice como abstracción.
        """
        dados = Dice()
        dados.set_dados_para_test(3, 5)
        
        self.tablero.colocar_ficha(5, "negro", 1)
        exito = self.tablero.realizar_movimiento_completo("negro", dados, 5, usar_dado1=True)
        
        self.assertTrue(exito)
        self.assertEqual(self.tablero.obtener_estado_punto(8), ["negro", 1])
    
    def test_realizar_movimiento_desde_barra_con_dados(self):
        """
        Verifica movimiento desde barra usando dados.
        
        SOLID: DIP - Integración con Dice.
        """
        dados = Dice()
        dados.set_dados_para_test(4, 2)
        
        self.tablero.enviar_a_barra("blanco")
        exito = self.tablero.realizar_movimiento_completo("blanco", dados, 0, usar_dado2=True)
        
        self.assertTrue(exito)
        self.assertEqual(self.tablero.obtener_estado_punto(23), ["blanco", 1])
    
    def test_obtener_movimientos_posibles(self):
        """
        Verifica obtención de puntos válidos para mover.
        
        SOLID: ISP - Consulta de movimientos disponibles.
        """
        dados = Dice()
        dados.set_dados_para_test(2, 3)
        
        self.tablero.colocar_ficha(5, "negro", 1)
        movimientos = self.tablero.obtener_movimientos_posibles("negro", dados)
        
        self.assertIn(5, movimientos)
    
    def test_obtener_movimientos_posibles_con_barra(self):
        """
        Verifica que solo puede mover desde barra si tiene fichas ahí.
        
        SOLID: ISP - Prioridad de movimientos desde barra.
        """
        dados = Dice()
        dados.set_dados_para_test(2, 3)
        
        self.tablero.enviar_a_barra("negro")
        movimientos = self.tablero.obtener_movimientos_posibles("negro", dados)
        
        self.assertEqual(movimientos, [0])


class TestBoardSOLID(unittest.TestCase):
    """Tests específicos de principios SOLID para Board."""
    
    def setUp(self):
        """Crea tablero para cada test."""
        self.tablero = Board()
    
    def test_srp_manages_board_state_only(self):
        """
        SRP: Board solo gestiona estado del tablero.
        
        NO renderiza, NO gestiona UI, NO maneja red.
        """
        # Tiene métodos de gestión de estado
        state_methods = [
            'colocar_ficha', 'remover_ficha', 'mover_ficha',
            'obtener_estado_punto', 'esta_vacio'
        ]
        
        for method in state_methods:
            self.assertTrue(hasattr(self.tablero, method))
        
        # NO tiene métodos de UI
        self.assertFalse(hasattr(self.tablero, 'draw'))
        self.assertFalse(hasattr(self.tablero, 'render'))
        self.assertFalse(hasattr(self.tablero, 'display'))
    
    def test_ocp_extensible_for_variants(self):
        """
        OCP: Board puede extenderse para variantes de backgammon.
        
        Ejemplo: Acey-Deucey con reglas diferentes.
        """
        class AceyDeuceyBoard(Board):
            def inicializar_posiciones_estandar(self):
                # Acey-Deucey empieza con tablero vacío
                pass
            
            def es_movimiento_especial_acey_deucey(self):
                return "Reglas especiales Acey-Deucey"
        
        tablero_variante = AceyDeuceyBoard()
        tablero_variante.inicializar_posiciones_estandar()
        
        # Mantiene API base
        self.assertTrue(hasattr(tablero_variante, 'colocar_ficha'))
        self.assertTrue(hasattr(tablero_variante, 'mover_ficha'))
        
        # Agrega funcionalidad nueva
        self.assertIn("Acey-Deucey", tablero_variante.es_movimiento_especial_acey_deucey())
    
    def test_lsp_variants_maintain_contract(self):
        """
        LSP: Variantes de Board mantienen el contrato base.
        
        Pueden sustituir a Board en cualquier contexto.
        """
        class NackgammonBoard(Board):
            pass
        
        def colocar_fichas_iniciales(board: Board):
            board.colocar_ficha(1, "negro", 2)
            return board.obtener_estado_punto(1)
        
        board_normal = Board()
        board_nack = NackgammonBoard()
        
        # Ambos funcionan igual
        resultado1 = colocar_fichas_iniciales(board_normal)
        resultado2 = colocar_fichas_iniciales(board_nack)
        
        self.assertEqual(resultado1, ["negro", 2])
        self.assertEqual(resultado2, ["negro", 2])
    
    def test_isp_focused_board_operations(self):
        """
        ISP: Board expone operaciones específicas de tablero.
        
        No mezcla con responsabilidades de otros componentes.
        """
        # Operaciones de tablero
        board_ops = [
            'colocar_ficha', 'remover_ficha', 'mover_ficha',
            'enviar_a_barra', 'sacar_ficha'
        ]
        
        for op in board_ops:
            self.assertTrue(hasattr(self.tablero, op))
        
        # NO tiene operaciones de jugador
        self.assertFalse(hasattr(self.tablero, 'crear_jugador'))
        self.assertFalse(hasattr(self.tablero, 'cambiar_turno'))
    
    def test_dip_depends_on_dice_abstraction(self):
        """
        DIP: Board depende de Dice (abstracción), no de implementación.
        
        Permite usar cualquier tipo de dado.
        """
        # Board acepta Dice como parámetro
        dados = Dice()
        dados.set_dados_para_test(3, 5)
        
        self.tablero.colocar_ficha(1, "negro", 1)
        exito = self.tablero.realizar_movimiento_completo("negro", dados, 1, usar_dado1=True)
        
        self.assertTrue(exito)


if __name__ == "__main__":
    unittest.main()
