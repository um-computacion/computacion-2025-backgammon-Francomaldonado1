class Board:
    """
    Tablero de Backgammon con 24 puntos, barra y casa.
    """

    def __init__(self):
        """
        Inicializa un tablero vacío de Backgammon.

        Attributes:
            __puntos__ (list): Lista de 24 puntos, cada uno con [color, cantidad] o None.
            __barra__ (dict): Diccionario {color: cantidad} de fichas enviadas a la barra.
            __casa__ (dict): Diccionario {color: cantidad} de fichas enviadas a la casa.
        """
        self.__puntos__ = [None] * 24
        self.__barra__ = {}
        self.__casa__ = {}

    def colocar_ficha(self, punto: int, color: str, cantidad: int = 1) -> None:
        """
        Coloca fichas en un punto específico del tablero.

        Args:
            punto (int): Número del punto (1 a 24).
            color (str): Color de las fichas.
            cantidad (int, optional): Número de fichas a colocar. Por defecto 1.

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
            cantidad (int, optional): Número de fichas a quitar. Por defecto 1.

        Raises:
            ValueError: Si el punto está vacío o no hay fichas suficientes.
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
            list | None: [color, cantidad] si hay fichas, o None si está vacío.
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

    def mover_ficha(self, origen: int, destino: int, color: str) -> None:
     """
    Mueve una ficha de un punto a otro.

    Reglas:
    - Si el destino está vacío, se coloca la ficha.
    - Si el destino tiene fichas del mismo color, se apila.
    - Si el destino tiene UNA sola ficha del color contrario, se la come y se envía a la barra.
    - Si el destino tiene 2+ fichas del color contrario, el movimiento no es válido.

    Args:
        origen (int): Punto de origen (1 a 24).
        destino (int): Punto de destino (1 a 24).
        color (str): Color de la ficha que se mueve.

    Raises:
        ValueError: Si el movimiento no es válido.
      """
     estado_origen = self.obtener_estado_punto(origen)
     if estado_origen is None or estado_origen[0] != color:
        raise ValueError("No hay fichas del color indicado en el origen.")

     estado_destino = self.obtener_estado_punto(destino)
     if estado_destino is None:
        # Punto vacío → movimiento válido
        self.remover_ficha(origen, 1)
        self.colocar_ficha(destino, color, 1)
     else:
        color_destino, cantidad_destino = estado_destino
        if color_destino == color:
            # Misma color → apilar
            self.remover_ficha(origen, 1)
            self.colocar_ficha(destino, color, 1)
        elif cantidad_destino == 1:
            # Comer ficha contraria
            self.remover_ficha(origen, 1)
            self.remover_ficha(destino, 1)
            self.enviar_a_barra(color_destino)
            self.colocar_ficha(destino, color, 1)
        else:
            # Bloqueado
            raise ValueError("El destino está bloqueado por fichas contrarias.")


    def enviar_a_barra(self, color: str) -> None:
        """
        Envía una ficha a la barra.

        Args:
            color (str): Color de la ficha.

        Returns:
            None
        """
        self.__barra__[color] = self.__barra__.get(color, 0) + 1

    def sacar_ficha(self, color: str) -> None:
        """
        Envía una ficha a la casa del jugador.

        Args:
            color (str): Color de la ficha.

        Returns:
            None
        """
        self.__casa__[color] = self.__casa__.get(color, 0) + 1

    # ----- Getters para tests -----
    def get_barra(self) -> dict:
        """
        Devuelve el estado de la barra.

        Returns:
            dict: Diccionario {color: cantidad} de fichas en la barra.
        """
        return self.__barra__

    def get_casa(self) -> dict:
        """
        Devuelve el estado de la casa.

        Returns:
            dict: Diccionario {color: cantidad} de fichas en la casa.
        """
        return self.__casa__

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
