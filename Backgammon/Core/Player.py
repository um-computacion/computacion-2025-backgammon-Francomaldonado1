"""Clase Player."""
from Backgammon.Core.Checker import Checker
from Backgammon.Core.Dice import Dice

class Player:
    """
    Representa a un jugador de Backgammon.
    """

    def __init__(self, nombre: str, color: str):
        """
        Inicializa un jugador con su nombre, color y 15 fichas.

        Args:
            nombre (str): Nombre del jugador.
            color (str): Color de sus fichas ('blanco' o 'negro').
        """
        self.__nombre__ = nombre
        self.__color__ = color
        self.__fichas__ = [Checker(color) for _ in range(15)]
        self.__dados__ = Dice()  # Cada jugador tiene sus dados propios

    def obtener_nombre(self) -> str:
        """Devuelve el nombre del jugador."""
        return self.__nombre__

    def obtener_color(self) -> str:
        """Devuelve el color del jugador ('blanco' o 'negro')."""
        return self.__color__

    def obtener_fichas(self) -> list[Checker]:
        """Devuelve la lista de fichas del jugador."""
        return self.__fichas__

    def obtener_dados(self) -> Dice:
        """Devuelve el objeto dados del jugador."""
        return self.__dados__

    def __str__(self) -> str:
        return f"Jugador(nombre={self.__nombre__}, color={self.__color__})"
