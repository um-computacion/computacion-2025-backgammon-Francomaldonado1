class Checker:
    """
    Ficha de Backgammon con color y posición.
    """

    def __init__(self, color: str, posicion: int | None = None):
        """
        Crea una ficha.

        Args:
            color (str): Color de la ficha (por ejemplo, 'blanco' o 'negro').
            posicion (int | None): Punto del tablero (1 a 24) o None si está fuera.

        Returns:
            None
        """
        self.__color__ = color
        self.__posicion__ = posicion

    def obtener_color(self) -> str:
        """
        Devuelve el color de la ficha.

        Args:
            None

        Returns:
            str: Color actual de la ficha.
        """
        return self.__color__

    def obtener_posicion(self) -> int | None:
        """
        Devuelve la posición actual de la ficha.

        Args:
            None

        Returns:
            int | None: Número de punto (1 a 24) o None si está fuera del tablero.
        """
        return self.__posicion__

    def establecer_posicion(self, nueva_posicion: int | None) -> None:
        """
        Actualiza la posición de la ficha.

        Args:
            nueva_posicion (int | None): Nuevo punto (1 a 24) o None si queda fuera.

        Returns:
            None
        """
        self.__posicion__ = nueva_posicion

    def esta_fuera(self) -> bool:
        """
        Indica si la ficha está fuera del tablero.

        Args:
            None

        Returns:
            bool: True si la ficha no tiene posición (None), False en caso contrario.
        """
        return self.__posicion__ is None

    def __str__(self) -> str:
        """
        Devuelve una representación legible de la ficha.

        Args:
            None

        Returns:
            str: Descripción con color y posición.
        """
        return f"Ficha(color={self.__color__}, posicion={self.__posicion__})"
