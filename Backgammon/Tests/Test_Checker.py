import unittest
from Backgammon.Core.Checker import Checker


class TestCheckerFunctionality(unittest.TestCase):
    """Tests de funcionalidad completa para Checker."""
    
    def test_crear_checker_con_posicion(self):
        """
        Verifica creación correcta con posición inicial.
        
        SOLID: SRP - Constructor simple que solo inicializa estado.
        """
        ficha = Checker('blanco', 5)
        self.assertEqual(ficha.obtener_color(), 'blanco')
        self.assertEqual(ficha.obtener_posicion(), 5)
        self.assertFalse(ficha.esta_fuera())
    
    def test_crear_checker_sin_posicion(self):
        """
        Verifica creación correcta sin posición (ficha fuera del tablero).
        
        SOLID: SRP - Manejo simple de estado None.
        """
        ficha = Checker('negro')
        self.assertEqual(ficha.obtener_color(), 'negro')
        self.assertIsNone(ficha.obtener_posicion())
        self.assertTrue(ficha.esta_fuera())
    
    def test_establecer_posicion_valida(self):
        """
        Verifica que se puede actualizar la posición.
        
        SOLID: SRP - Modificación de estado sin lógica compleja.
        """
        ficha = Checker('blanco')
        ficha.establecer_posicion(12)
        self.assertEqual(ficha.obtener_posicion(), 12)
        self.assertFalse(ficha.esta_fuera())
    
    def test_establecer_posicion_fuera(self):
        """
        Verifica que se puede poner ficha fuera del tablero.
        
        SOLID: SRP - Permite representar todos los estados posibles.
        """
        ficha = Checker('negro', 10)
        ficha.establecer_posicion(None)
        self.assertIsNone(ficha.obtener_posicion())
        self.assertTrue(ficha.esta_fuera())
    
    def test_establecer_posicion_limites(self):
        """
        Verifica posiciones en límites del tablero.
        
        SOLID: ISP - Interfaz simple no impone validaciones innecesarias.
        """
        ficha = Checker('blanco')
        
        # Límite inferior
        ficha.establecer_posicion(1)
        self.assertEqual(ficha.obtener_posicion(), 1)
        
        # Límite superior
        ficha.establecer_posicion(24)
        self.assertEqual(ficha.obtener_posicion(), 24)
    
    def test_str_representation(self):
        """
        Verifica representación en string.
        
        SOLID: ISP - Proporciona interfaz mínima para debugging.
        """
        ficha1 = Checker('blanco', 5)
        ficha2 = Checker('negro', None)
        
        self.assertIn('blanco', str(ficha1))
        self.assertIn('5', str(ficha1))
        self.assertIn('negro', str(ficha2))
        self.assertIn('None', str(ficha2))
    
    def test_multiple_changes_posicion(self):
        """
        Verifica cambios múltiples de posición.
        
        SOLID: SRP - Estado mutable sin efectos secundarios.
        """
        ficha = Checker('blanco', 1)
        
        for pos in [5, 10, 15, 20, None, 3]:
            ficha.establecer_posicion(pos)
            self.assertEqual(ficha.obtener_posicion(), pos)
    
    def test_color_inmutable(self):
        """
        Verifica que el color no cambia después de creación.
        
        SOLID: SRP - Identidad de ficha es inmutable.
        """
        ficha = Checker('negro', 5)
        color_inicial = ficha.obtener_color()
        
        # Cambiar posición no afecta color
        ficha.establecer_posicion(10)
        self.assertEqual(ficha.obtener_color(), color_inicial)


class TestCheckerSOLID(unittest.TestCase):
    """Tests específicos de principios SOLID para Checker."""
    
    def test_srp_single_responsibility(self):
        """
        SRP: Checker solo representa una ficha (color y posición).
        
        Verifica que NO tiene:
        - Lógica de movimiento
        - Validación de reglas
        - Dependencias de tablero
        """
        ficha = Checker('blanco', 5)
        
        # Solo tiene métodos de estado
        public_methods = [m for m in dir(ficha) if not m.startswith('_')]
        expected = {'obtener_color', 'obtener_posicion', 
                   'establecer_posicion', 'esta_fuera'}
        
        self.assertTrue(expected.issubset(set(public_methods)))
        
        # NO tiene métodos de lógica
        self.assertFalse(hasattr(ficha, 'mover'))
        self.assertFalse(hasattr(ficha, 'validar'))
        self.assertFalse(hasattr(ficha, 'puede_mover'))
    
    def test_isp_minimal_interface(self):
        """
        ISP: Interfaz mínima sin métodos innecesarios.
        
        Los clientes solo dependen de lo esencial.
        """
        ficha = Checker('negro', 10)
        
        # Interfaz completa y mínima
        self.assertTrue(callable(ficha.obtener_color))
        self.assertTrue(callable(ficha.obtener_posicion))
        self.assertTrue(callable(ficha.establecer_posicion))
        self.assertTrue(callable(ficha.esta_fuera))
        
        # Sin métodos superfluos
        self.assertFalse(hasattr(ficha, 'calcular_destino'))
        self.assertFalse(hasattr(ficha, 'obtener_jugador'))
    
    def test_ocp_extensible_sin_modificacion(self):
        """
        OCP: Puede extenderse sin modificar la clase base.
        
        Ejemplo: Crear SpecialChecker con poderes especiales.
        """
        class PowerChecker(Checker):
            def __init__(self, color, posicion, poder):
                super().__init__(color, posicion)
                self.poder = poder
            
            def usar_poder(self):
                return f"Usando poder: {self.poder}"
        
        ficha_especial = PowerChecker('blanco', 5, 'salto_doble')
        
        # Mantiene funcionalidad base
        self.assertEqual(ficha_especial.obtener_color(), 'blanco')
        self.assertEqual(ficha_especial.obtener_posicion(), 5)
        
        # Agrega funcionalidad nueva
        self.assertEqual(ficha_especial.usar_poder(), "Usando poder: salto_doble")
    
    def test_lsp_subtypes_substitutable(self):
        """
        LSP: Subtipos pueden sustituir al tipo base.
        
        Cualquier subclase funciona donde se espera Checker.
        """
        class GoldenChecker(Checker):
            def vale_doble(self):
                return True
        
        def procesar_ficha(ficha: Checker) -> str:
            return f"{ficha.obtener_color()} en {ficha.obtener_posicion()}"
        
        ficha_normal = Checker('blanco', 3)
        ficha_oro = GoldenChecker('negro', 7)
        
        # Ambas funcionan con la misma función
        resultado1 = procesar_ficha(ficha_normal)
        resultado2 = procesar_ficha(ficha_oro)
        
        self.assertIn('blanco', resultado1)
        self.assertIn('negro', resultado2)
    
    def test_dip_no_dependencies(self):
        """
        DIP: Checker no depende de implementaciones concretas.
        
        Es una clase de dominio puro sin dependencias.
        """
        ficha = Checker('blanco', 5)
        
        # No tiene dependencias inyectadas
        attrs = [a for a in dir(ficha) if not a.startswith('__')]
        
        # No debe tener referencias a Board, Player, Game, etc.
        attrs_lower = [a.lower() for a in attrs]
        self.assertNotIn('board', attrs_lower)
        self.assertNotIn('player', attrs_lower)
        self.assertNotIn('game', attrs_lower)
        self.assertNotIn('dice', attrs_lower)


if __name__ == "__main__":
    unittest.main()
