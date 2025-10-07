"""Clase Dice para manejo de dados."""
import random

class Dice:
    """
    Dados de Backgammon para generar tiradas de dos dados de seis caras.
    
    PRINCIPIOS SOLID:
    - SRP: Responsabilidad única - Generar números aleatorios para dados
    - DIP: Sin dependencias - No depende de reglas de backgammon
    - OCP: Extensible - Permite crear dados con diferentes comportamientos
    
    DECISIÓN DE DISEÑO:
    No calcula movimientos disponibles (responsabilidad de DiceMovesCalculator).
    No valida movimientos (responsabilidad de MovementValidator).
    Ver justificacion.md para la separación de responsabilidades.
    """

    def __init__(self):
        """Inicializa los dados sin valores."""
        self.__dado1__ = None
        self.__dado2__ = None

    def tirar(self) -> None:
        """
        Tira ambos dados y guarda los valores obtenidos.
        
        SRP: Solo genera números aleatorios, no interpreta resultados.
        """
        self.__dado1__ = random.randint(1, 6)
        self.__dado2__ = random.randint(1, 6)

    def obtener_valores(self) -> tuple[int, int]:
        """Devuelve los valores actuales de ambos dados."""
        return (self.__dado1__, self.__dado2__)

    def obtener_dado1(self) -> int | None:
        """Devuelve el valor del primer dado."""
        return self.__dado1__

    def obtener_dado2(self) -> int | None:
        """Devuelve el valor del segundo dado."""
        return self.__dado2__

    def es_doble(self) -> bool:
        """
        Indica si la tirada actual es un doble.
        
        SRP: Comparación simple sin lógica de movimientos.
        La interpretación de qué hacer con dobles es responsabilidad externa.
        
        Raises:
            ValueError: Si no se han tirado los dados todavía.
        """
        if self.__dado1__ is None or self.__dado2__ is None:
            raise ValueError("No se han tirado los dados todavía.")
        return self.__dado1__ == self.__dado2__

    def han_sido_tirados(self) -> bool:
        """
        Indica si los dados ya han sido tirados.
        
        ISP: Método simple de consulta sin efectos secundarios.
        """
        return self.__dado1__ is not None and self.__dado2__ is not None

    def reiniciar(self) -> None:
        """
        Reinicia los dados para una nueva tirada.
        
        SRP: Gestión simple de estado interno.
        """
        self.__dado1__ = None
        self.__dado2__ = None

    def __str__(self) -> str:
        """Devuelve una representación legible de la tirada actual."""
        if not self.han_sido_tirados():
            return "Dados sin tirar"
        resultado = f"Dados: {self.__dado1__}, {self.__dado2__}"
        if self.es_doble():
            resultado += " (¡Doble!)"
        return resultado

    def set_dados_para_test(self, dado1: int, dado2: int) -> None:
        """
        Setea valores de dados manualmente (solo para tests).
        
        DIP: Permite inyección de valores para testing sin romper encapsulación.
        """
        self.__dado1__ = dado1
        self.__dado2__ = dado2