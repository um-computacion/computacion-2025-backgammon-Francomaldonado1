class Board:
    """
    Tablero de Backgammon con 24 puntos, barra y casa.
    """

    def __init__(self):
        """
        Inicializa un tablero vacío de Backgammon.

        Returns:
            None
        """
        self.__puntos__ = [None] * 24   # Cada punto podrá contener (color, cantidad)
        self.__barra__ = {}             # {color: cantidad}
        self.__casa__ = {}              # {color: cantidad}

    def colocar_ficha(self, punto: int, color: str, cantidad: int = 1) -> None:
        """
        Coloca fichas en un punto específico del tablero.

        Args:
            punto (int): Número del punto (1 a 24).
            color (str): Color de las fichas.
            cantidad (int): Número de fichas a colocar.

        Returns:
            None

        Raises:
            ValueError: Si se intenta mezclar fichas de distinto color en el mismo punto.
        """
        if self.__puntos__[punto - 1] is None:
            self.__puntos__[punto - 1] = [color, cantidad]
        else:
            mismo_color, cant_actual = self.__puntos__[punto - 1]
            if mismo_color == color:
                self.__puntos__[punto - 1][1] += cantidad
            else:
                raise ValueError("No se pueden mezclar fichas de distinto color en el mismo punto.")

    def remover_ficha(self, punto: int, cantidad: int = 1) -> None:
        """
        Quita fichas de un punto específico.

        Args:
            punto (int): Número del punto (1 a 24).
            cantidad (int): Número de fichas a quitar.

        Returns:
            None

        Raises:
            ValueError: Si no hay fichas suficientes o el punto está vacío.
        """
        if self.__puntos__[punto - 1] is None:
            raise ValueError("No hay fichas en este punto.")
        
        color, cant_actual = self.__puntos__[punto - 1]
        if cant_actual < cantidad:
            raise ValueError("No hay suficientes fichas para quitar.")
        
        self.__puntos__[punto - 1][1] -= cantidad
        if self.__puntos__[punto - 1][1] == 0:
            self.__puntos__[punto - 1] = None

    def obtener_estado_punto(self, punto: int):
        """
        Devuelve el estado de un punto.

        Args:
            punto (int): Número del punto (1 a 24).

        Returns:
            tuple | None: (color, cantidad) si hay fichas, o None si está vacío.
        """
        return self.__puntos__[punto - 1]

    def esta_vacio(self, punto: int) -> bool:
        """
        Indica si un punto está vacío.

        Args:
            punto (int): Número del punto (1 a 24).

        Returns:
            bool: True si está vacío, False en caso contrario.
        """
        return self.__puntos__[punto - 1] is None

    def __str__(self) -> str:
        """
        Devuelve una representación en texto del tablero.

        Returns:
            str: Estado del tablero en formato legible.
        """
        estado = []
        for i, punto in enumerate(self.__puntos__, start=1):
            if punto is None:
                estado.append(f"{i}: vacío")
            else:
                color, cant = punto
                estado.append(f"{i}: {cant} {color}")
        return "\n".join(estado)
