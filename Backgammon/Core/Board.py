from Backgammon.Core.Dice import Dice


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

    def inicializar_posiciones_estandar(self) -> None:
        """
        Coloca las fichas en sus posiciones iniciales estándar del Backgammon.
        
        Posiciones iniciales:
        - Negro: 2 en punto 1, 5 en punto 12, 3 en punto 17, 5 en punto 19
        - Blanco: 2 en punto 24, 5 en punto 13, 3 en punto 8, 5 en punto 6

        Returns:
            None
        """
        # Limpiar tablero
        self.__puntos__ = [None] * 24
        self.__barra__ = {}
        self.__casa__ = {}
        
        # Fichas negras
        self.colocar_ficha(1, "negro", 2)   # Posición inicial negro
        self.colocar_ficha(12, "negro", 5)
        self.colocar_ficha(17, "negro", 3)
        self.colocar_ficha(19, "negro", 5)
        
        # Fichas blancas
        self.colocar_ficha(24, "blanco", 2)  # Posición inicial blanco
        self.colocar_ficha(13, "blanco", 5)
        self.colocar_ficha(8, "blanco", 3)
        self.colocar_ficha(6, "blanco", 5)

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

    def calcular_destino(self, origen: int, movimiento: int, color: str) -> int:
        """
        Calcula el punto de destino basado en el origen, movimiento y color del jugador.
        
        Args:
            origen (int): Punto de origen (1 a 24, o 0 para barra).
            movimiento (int): Valor del dado (1 a 6).
            color (str): Color del jugador ('negro' o 'blanco').
            
        Returns:
            int: Punto de destino (1 a 24, o 25/0 para casa).
            
        Raises:
            ValueError: Si el movimiento resulta fuera del tablero.
        """
        if color == "negro":
            # Negro avanza de 1 hacia 24
            destino = origen + movimiento
            if destino > 24:
                return 25  # Fuera del tablero (casa)
            return destino
        else:  # color == "blanco"
            # Blanco avanza de 24 hacia 1
            destino = origen - movimiento
            if destino < 1:
                return 0   # Fuera del tablero (casa)
            return destino

    def mover_desde_barra(self, color: str, movimiento: int) -> bool:
        """
        Intenta mover una ficha desde la barra al tablero.
        
        Args:
            color (str): Color de la ficha a mover.
            movimiento (int): Valor del dado para el movimiento.
            
        Returns:
            bool: True si el movimiento fue exitoso, False si no es posible.
        """
        # Verificar si hay fichas en la barra
        if self.__barra__.get(color, 0) == 0:
            return False
            
        # Calcular punto de entrada
        if color == "negro":
            destino = movimiento  # Negro entra desde punto 1
        else:  # blanco
            destino = 25 - movimiento  # Blanco entra desde punto 24
            
        # Verificar si el movimiento es válido
        if not self.es_movimiento_valido_a_punto(destino, color):
            return False
            
        # Realizar el movimiento
        self.__barra__[color] -= 1
        if self.__barra__[color] == 0:
            del self.__barra__[color]
            
        # Si hay una ficha contraria, comerla
        estado_destino = self.obtener_estado_punto(destino)
        if estado_destino is not None and estado_destino[0] != color:
            self.remover_ficha(destino, 1)
            self.enviar_a_barra(estado_destino[0])
            
        self.colocar_ficha(destino, color, 1)
        return True

    def es_movimiento_valido_a_punto(self, punto: int, color: str) -> bool:
        """
        Verifica si es válido mover a un punto específico.
        
        Args:
            punto (int): Punto de destino (1 a 24).
            color (str): Color de la ficha que se mueve.
            
        Returns:
            bool: True si el movimiento es válido, False si está bloqueado.
        """
        if punto < 1 or punto > 24:
            return False
            
        estado = self.obtener_estado_punto(punto)
        if estado is None:
            return True  # Punto vacío
            
        color_destino, cantidad = estado
        if color_destino == color:
            return True  # Mismo color, se puede apilar
            
        # Ficha contraria: solo se puede si hay una sola
        return cantidad == 1

    def puede_sacar_fichas(self, color: str) -> bool:
        """
        Verifica si un jugador puede comenzar a sacar fichas (todas en el cuarto final).
        
        Args:
            color (str): Color del jugador.
            
        Returns:
            bool: True si puede sacar fichas, False en caso contrario.
        """
        # No puede sacar si tiene fichas en la barra
        if self.__barra__.get(color, 0) > 0:
            return False
            
        if color == "negro":
            # Negro debe tener todas las fichas en puntos 19-24
            for i in range(1, 19):
                estado = self.obtener_estado_punto(i)
                if estado is not None and estado[0] == color:
                    return False
        else:  # blanco
            # Blanco debe tener todas las fichas en puntos 1-6
            for i in range(7, 25):
                estado = self.obtener_estado_punto(i)
                if estado is not None and estado[0] == color:
                    return False
                    
        return True

    def realizar_movimiento_completo(self, color, dados, origen, usar_dado1=False, usar_dado2=False):
        """
        Realiza un movimiento completo usando uno de los dados disponibles.
        
        Args:
            color (str): Color del jugador.
            dados (Dice): Objeto dados con la tirada actual.
            origen (int): Punto de origen (0 para barra, 1-24 para puntos del tablero).
            usar_dado1 (bool): True para usar dado1, False para usar dado2.
            
        Returns:
            bool: True si el movimiento fue exitoso, False en caso contrario.
        """
        if not dados.han_sido_tirados():
            return False
            
        movimiento = dados.obtener_dado1() if usar_dado1 else dados.obtener_dado2()
        
        # Movimiento desde la barra
        if origen == 0:
            return self.mover_desde_barra(color, movimiento)
            
        # Movimiento normal en el tablero
        estado_origen = self.obtener_estado_punto(origen)
        if estado_origen is None or estado_origen[0] != color:
            return False
            
        destino = self.calcular_destino(origen, movimiento, color)
        
        # Sacar fichas (destino fuera del tablero)
        if (destino <= 0 and color == "blanco") or (destino >= 25 and color == "negro"):
            if not self.puede_sacar_fichas(color):
                return False
            self.remover_ficha(origen, 1)
            self.sacar_ficha(color)
            return True
            
        # Movimiento normal dentro del tablero
        if not self.es_movimiento_valido_a_punto(destino, color):
            return False
            
        return self.mover_ficha(origen, destino, color)
    
    def realizar_movimiento_doble(self, color: str, dados: Dice, origen: int) -> bool:
        """
        Mueve una sola ficha usando ambos dados consecutivamente.
    
        Args:
        color (str): Color del jugador.
        dados (Dice): Objeto dados con la tirada actual.
        origen (int): Punto de origen.
        
        Returns:
        bool: True si ambos movimientos fueron exitosos, False en caso contrario.
        """
        # Validar que se pueda hacer el primer movimiento
        # Hacer movimiento temporal 
        # Validar que se pueda hacer el segundo movimiento
        # Si ambos son válidos, ejecutar
        # Si no, deshacer cambios

    def obtener_movimientos_posibles(self, color: str, dados: Dice) -> list[int]:
        """
        Devuelve una lista de puntos desde los cuales el jugador puede mover.
        
        Args:
            color (str): Color del jugador.
            dados (Dice): Objeto dados con la tirada actual.
            
        Returns:
            list[int]: Lista de puntos válidos para mover (incluye 0 si puede mover desde barra).
        """
        if not dados.han_sido_tirados():
            return []
            
        movimientos_posibles = []
        dado1, dado2 = dados.obtener_valores()
        
        # Si hay fichas en la barra, solo puede mover desde ahí
        if self.__barra__.get(color, 0) > 0:
            if color == "negro":
                destino1 = dado1
                destino2 = dado2
            else:  # blanco
                destino1 = 25 - dado1
                destino2 = 25 - dado2
                
            if (self.es_movimiento_valido_a_punto(destino1, color) or 
                self.es_movimiento_valido_a_punto(destino2, color)):
                movimientos_posibles.append(0)
            return movimientos_posibles
            
        # Verificar movimientos desde cada punto del tablero
        for punto in range(1, 25):
            estado = self.obtener_estado_punto(punto)
            if estado is not None and estado[0] == color:
                destino1 = self.calcular_destino(punto, dado1, color)
                destino2 = self.calcular_destino(punto, dado2, color)
                
                # Verificar si puede sacar fichas
                puede_sacar = self.puede_sacar_fichas(color)
                
                movimiento_valido = False
                
                # Verificar dado1
                if (destino1 <= 0 and color == "blanco" and puede_sacar) or \
                   (destino1 >= 25 and color == "negro" and puede_sacar) or \
                   (1 <= destino1 <= 24 and self.es_movimiento_valido_a_punto(destino1, color)):
                    movimiento_valido = True
                    
                # Verificar dado2
                if not movimiento_valido:
                    if (destino2 <= 0 and color == "blanco" and puede_sacar) or \
                       (destino2 >= 25 and color == "negro" and puede_sacar) or \
                       (1 <= destino2 <= 24 and self.es_movimiento_valido_a_punto(destino2, color)):
                        movimiento_valido = True
                        
                if movimiento_valido:
                    movimientos_posibles.append(punto)
                    
        return movimientos_posibles

    def tiene_fichas_en_barra(self, color: str) -> bool:
        """
        Verifica si un jugador tiene fichas en la barra.
        
        Args:
            color (str): Color del jugador.
            
        Returns:
            bool: True si tiene fichas en la barra, False en caso contrario.
        """
        return self.__barra__.get(color, 0) > 0

    def ha_ganado(self, color: str) -> bool:
        """
        Verifica si un jugador ha ganado (todas sus fichas están en casa).
        
        Args:
            color (str): Color del jugador.
            
        Returns:
            bool: True si ha ganado, False en caso contrario.
        """
        return self.__casa__.get(color, 0) == 15

    def mover_ficha(self, origen: int, destino: int, color: str) -> bool:
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

        Returns:
            bool: True si el movimiento fue exitoso, False en caso contrario.
        """
        # 1. Origen vacío
        if not self.__puntos__[origen]:
         raise ValueError("No hay fichas en el punto de origen")

        # 2. Ficha de otro color
        if self.__puntos__[origen][-1].color != color:
         raise ValueError("No se puede mover una ficha del color contrario")

        # 3. Bloqueo por fichas contrarias
        if len(self.__puntos__[destino]) >= 2 and self.__puntos__[destino][-1].color != color:
         raise ValueError("Movimiento inválido: punto bloqueado por el rival")

        # Validar origen ANTES de hacer cualquier cambio
        estado_origen = self.obtener_estado_punto(origen)
        if estado_origen is None or estado_origen[0] != color:
            return False

        # Validar destino ANTES de hacer cualquier cambio
        estado_destino = self.obtener_estado_punto(destino)
        if estado_destino is not None:
            color_destino, cantidad_destino = estado_destino
            if color_destino != color and cantidad_destino > 1:
                return False

        # Solo ahora hacer los cambios (todas las validaciones pasaron)
        self.remover_ficha(origen, 1)

        if estado_destino is None:
            # Punto vacío → colocar ficha
            self.colocar_ficha(destino, color, 1)
        else:
            color_destino, cantidad_destino = estado_destino
            if color_destino == color:
                # Mismo color → apilar
                self.colocar_ficha(destino, color, 1)
            else:  # color_destino != color and cantidad_destino == 1
                # Comer ficha contraria (ya validamos que es solo 1)
                self.remover_ficha(destino, 1)
                self.enviar_a_barra(color_destino)
                self.colocar_ficha(destino, color, 1)
                
        return True

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
                
        # Agregar información de barra y casa
        if self.__barra__:
            estado.append(f"Barra: {self.__barra__}")
        if self.__casa__:
            estado.append(f"Casa: {self.__casa__}")
            
        return "\n".join(estado)