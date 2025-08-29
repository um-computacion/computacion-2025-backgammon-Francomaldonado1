import random
class Dice:
    """
    Dados de Backgammon para generar tiradas de dos dados de seis caras.
    """

    def __init__(self):
        """
        Inicializa los dados sin valores.

        Returns:
            None
        """
        self.__dado1__ = None
        self.__dado2__ = None

    def tirar(self) -> None:
        """
        Tira ambos dados y guarda los valores obtenidos.

        Returns:
            None
        """
        self.__dado1__ = random.randint(1, 6)
        self.__dado2__ = random.randint(1, 6)

    def obtener_valores(self) -> tuple[int, int]:
        """
        Devuelve los valores actuales de ambos dados.

        Returns:
            tuple[int, int]: Valores del dado1 y dado2, o (None, None) si no se han tirado.
        """
        return (self.__dado1__, self.__dado2__)

    def obtener_dado1(self) -> int | None:
        """
        Devuelve el valor del primer dado.

        Returns:
            int | None: Valor del primer dado o None si no se ha tirado.
        """
        return self.__dado1__

    def obtener_dado2(self) -> int | None:
        """
        Devuelve el valor del segundo dado.

        Returns:
            int | None: Valor del segundo dado o None si no se ha tirado.
        """
        return self.__dado2__

    def es_doble(self) -> bool:
        """
        Indica si la tirada actual es un doble.

        Returns:
            bool: True si ambos dados tienen el mismo valor, False en caso contrario.
            
        Raises:
            ValueError: Si no se han tirado los dados todavía.
        """
        if self.__dado1__ is None or self.__dado2__ is None:
            raise ValueError("No se han tirado los dados todavía.")
        
        return self.__dado1__ == self.__dado2__

    def han_sido_tirados(self) -> bool:
        """
        Indica si los dados ya han sido tirados en esta instancia.

        Returns:
            bool: True si los dados tienen valores, False si están sin tirar.
        """
        return self.__dado1__ is not None and self.__dado2__ is not None

    def reiniciar(self) -> None:
        """
        Reinicia los dados para una nueva tirada.

        Returns:
            None
        """
        self.__dado1__ = None
        self.__dado2__ = None

    def __str__(self) -> str:
        """
        Devuelve una representación legible de la tirada actual.

        Returns:
            str: Descripción de los valores de los dados.
        """
        if not self.han_sido_tirados():
            return "Dados sin tirar"
        
        resultado = f"Dados: {self.__dado1__}, {self.__dado2__}"
        if self.es_doble():
            resultado += " (¡Doble!)"
        
        return resultado