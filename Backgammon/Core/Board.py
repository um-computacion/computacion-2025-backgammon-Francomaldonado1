"""Clase Board para el tablero de Backgammon."""
import copy
from Backgammon.Core.Dice import Dice


class Board:
    """
    Tablero de Backgammon con 24 puntos, barra y casa.
    """

    def __init__(self):
        """
        Inicializa un tablero vacío de Backgammon.
        SRP: Crea estructuras de datos para puntos, barra y casa sin lógica de reglas.
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
        SRP: Configura estado inicial del tablero sin aplicar lógica de juego.
        OCP: Permite redefinir esta configuración en variantes personalizadas.
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
        SRP: Manipula el estado del tablero sin verificar reglas globales.
        LSP: Método genérico compatible con subclases que amplíen reglas.
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
            mismo_color, _ = self.__puntos__[punto - 1]
            if mismo_color == color:
                self.__puntos__[punto - 1][1] += cantidad
            else:
                raise ValueError(
                 "No se pueden mezclar fichas de distinto color en el mismo punto."
                )

    def remover_ficha(self, punto: int, cantidad: int = 1) -> None:
        """
        Quita fichas de un punto específico.
        SRP: Responsabilidad limitada al manejo del estado interno.
        Args:
            punto (int): Número del punto (1 a 24).
            cantidad (int, optional): Número de fichas a quitar. Por defecto 1.

        Raises:
            ValueError: Si el punto está vacío o no hay fichas suficientes.
        """
        if self.__puntos__[punto - 1] is None:
            raise ValueError("No hay fichas en este punto.")

        _ , cant_actual = self.__puntos__[punto - 1]
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
        SRP: Cálculo puro sin efectos secundarios.
        OCP: Permite redefinir sentido del movimiento en variantes.
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
    
        # Blanco avanza de 24 hacia 1
        destino = origen - movimiento
        if destino < 1:
                return 0   # Fuera del tablero (casa)
        return destino

    def mover_desde_barra(self, color: str, movimiento: int) -> bool:
        """
        Intenta mover una ficha desde la barra al tablero.
        SRP: Gestiona reglas específicas de reincorporación.
        OCP: Permite adaptar reglas en subclases (por ejemplo, doble dado).
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
        SRP: Evalúa accesibilidad sin modificar estado.
        ISP: Parte de la interfaz pública del tablero.
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
        SRP: Evalúa condición de fin de partida.
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

    def debug_estado_jugador(self, color: str) -> str:
        """
        Devuelve información de debugging sobre el estado de un jugador.

        Args:
            color (str): Color del jugador.

        Returns:
            str: Información de debugging.
        """
        puntos_con_fichas = []
        for i in range(1, 25):
            estado = self.obtener_estado_punto(i)
            if estado is not None and estado[0] == color:
                puntos_con_fichas.append(f"{i}: {estado[1]} fichas")

        barra = self.__barra__.get(color, 0)
        casa = self.__casa__.get(color, 0)
        puede_sacar = self.puede_sacar_fichas(color)

        return (
        f"Color {color}: Puntos={puntos_con_fichas},"
        f"Barra={barra}, Casa={casa}, PuedeSacar={puede_sacar}"
        )

    def realizar_movimiento_completo(self, color: str, dados: Dice, 
            origen: int, usar_dado1: bool = True, usar_dado2: bool = False) -> bool:
        """
        Realiza un movimiento completo usando uno de los dados disponibles.
        Implementa las reglas correctas de bearing off.
        SRP: Coordina submétodos sin manejar interfaz ni estado externo.
        DIP: Usa `Dice` como abstracción (no genera tiradas directamente).
        Args:
            color (str): Color del jugador.
            dados (Dice): Objeto dados con la tirada actual.
            origen (int): Punto de origen (0 para barra, 1-24 para puntos del tablero).
            usar_dado1 (bool): True para usar dado1, False en caso contrario.
            usar_dado2 (bool): True para usar dado2, False en caso contrario.

        Returns:
            bool: True si el movimiento fue exitoso, False en caso contrario.
        """
        if not dados.han_sido_tirados():
            return False

        # Determinar qué dado usar
        if usar_dado2:
            movimiento = dados.obtener_dado2()
        else:
            movimiento = dados.obtener_dado1()

        # Movimiento desde la barra
        if origen == 0:
            return self.mover_desde_barra(color, movimiento)

        # Movimiento normal en el tablero
        estado_origen = self.obtener_estado_punto(origen)
        if estado_origen is None or estado_origen[0] != color:
            return False

        destino = self.calcular_destino(origen, movimiento, color)

        # BEARING OFF - Sacar fichas (destino fuera del tablero)
        if (destino <= 0 and color == "blanco") or (destino >= 25 and color == "negro"):
            # Verificar si puede sacar fichas
            if not self.puede_sacar_fichas(color):
                return False

            # NUEVA LÓGICA: Verificar reglas exactas de bearing off
            if not self._es_bearing_off_valido(color, origen, movimiento):
                return False

            # Realizar el bearing off
            self.remover_ficha(origen, 1)
            self.sacar_ficha(color)
            return True

        # Movimiento normal dentro del tablero
        if not self.es_movimiento_valido_a_punto(destino, color):
            return False

        return self._mover_ficha_bool(origen, destino, color)


    def _es_bearing_off_valido(self, color: str, origen: int, movimiento: int) -> bool:
        """
        Verifica si un bearing off (sacar ficha) es válido según las reglas del backgammon.

        Reglas:
        1) Se puede sacar con el valor exacto del dado.
        2) EXCEPCIÓN: Si el dado es mayor, 
        solo es válido si NO hay fichas en posiciones más lejanas al borne
        (es decir, más atrás dentro del cuadrante casa).

        Convenciones del tablero usadas aquí (consistentes con el resto del código):
        - NEGRO avanza hacia 25 y su casa es 19..24 (sale en 25)
        - BLANCO avanza hacia 0 y su casa es 1..6   (sale en 0)
        """
        if color == "negro":
            # Debe estar en casa 19..24
            if origen < 19 or origen > 24:
                return False

            # Distancia exacta hasta salir
            posicion_relativa = 25 - origen  # 24->1, 23->2, ..., 19->6

            # Regla 1: dado exacto
            if movimiento == posicion_relativa:
                return True

            # Regla 2: dado mayor solo si no hay fichas "más atrás" (19..origen-1)
            if movimiento > posicion_relativa:
                return not self._hay_fichas_en_posiciones_mas_altas(color, origen)

            # Dado menor nunca saca
            return False

        else:  # color == "blanco"
            # Debe estar en casa 1..6
            if origen < 1 or origen > 6:
                return False

            # Distancia exacta hasta salir
            posicion_relativa = origen  # 1->1, 2->2, ..., 6->6

            # Regla 1: dado exacto
            if movimiento == posicion_relativa:
                return True

            # Regla 2: dado mayor solo si no hay fichas "más atrás" (origen+1..6)
            if movimiento > posicion_relativa:
                return not self._hay_fichas_en_posiciones_mas_altas(color, origen)

            # Dado menor nunca saca
            return False


    def _hay_fichas_en_posiciones_mas_altas(self, color: str, origen: int) -> bool:
        """
        Indica si hay fichas del color en posiciones MÁS LEJANAS AL BORNE.
        Para NEGRO (casa 19..24): "más atrás" son puntos con índice MENOR (19..origen-1).
        Para BLANCO (casa 1..6): "más atrás" son puntos con índice MAYOR (origen+1..6).
        """
        if color == "negro":
            puntos_a_revisar = range(19, origen)  # 19..origen-1
        else:  # blanco
            puntos_a_revisar = range(origen + 1, 7)  # origen+1..6

        for punto in puntos_a_revisar:
            estado = self.obtener_estado_punto(punto)
            if estado is not None and estado[0] == color and estado[1] > 0:
                return True
        return False



    # MÉTODO AUXILIAR ADICIONAL para facilitar debugging y testing
    def _debug_bearing_off(self, color: str, origen: int, movimiento: int) -> str:
        """
        Devuelve una descripción legible del chequeo de bearing off para debugging.
        """
        if color == "negro":
            cuadrante_casa = list(range(19, 25))
            posicion_relativa = 25 - origen
            fuera_de_casa = origen not in range(19, 25)
            hay_atras = self._hay_fichas_en_posiciones_mas_altas(color, origen)
        else:
            cuadrante_casa = list(range(1, 7))
            posicion_relativa = origen
            fuera_de_casa = origen not in range(1, 7)
            hay_atras = self._hay_fichas_en_posiciones_mas_altas(color, origen)

        if fuera_de_casa:
            return f"❌ Ficha no está en cuadrante casa. Origen: {origen}, Casa: {cuadrante_casa}"

        if movimiento == posicion_relativa:
            return f"✅ Valor exacto. Dado: {movimiento}, Distancia: {posicion_relativa}"

        if movimiento > posicion_relativa:
            if hay_atras:
                return (f"❌ Dado mayor ({movimiento}) pero HAY fichas más atrás en la casa. "
                        f"Distancia desde {origen}: {posicion_relativa}")
            else:
                return (f"✅ Dado mayor ({movimiento}) y NO hay fichas más atrás. "
                        f"Distancia desde {origen}: {posicion_relativa}")

        return f"❌ Dado menor ({movimiento}) que la distancia {posicion_relativa} desde {origen}"

        
    def _realizar_paso_movimiento_doble(self, origen: int, destino: int, color: str, movimiento: int) -> bool:
        """
        Ejecuta un paso dentro de un movimiento doble, con validación de bearing off.
        """
        
        # Caso 1: Sacar fichas (destino fuera del tablero)
        if (destino <= 0 and color == "blanco") or (destino >= 25 and color == "negro"):
            # 1a. Verificar si puede sacar fichas
            if not self.puede_sacar_fichas(color):
                return False

            # 1b. Verificar reglas exactas de bearing off
            if not self._es_bearing_off_valido(color, origen, movimiento):
                return False

            # 1c. Realizar el bearing off
            self.remover_ficha(origen, 1)
            self.sacar_ficha(color)
            return True

        # Caso 2: Destino dentro de rango válido
        if 1 <= destino <= 24:
            # 2a. Movimiento normal dentro del tablero (con validación de bloqueo/comer)
            if not self.es_movimiento_valido_a_punto(destino, color):
                return False
            
            # 2b. Ejecutar el movimiento
            return self._mover_ficha_bool(origen, destino, color)
        
        # Caso 3: Destino fuera de rango (como destino intermedio en el bearing off)
        return False

    def realizar_movimiento_simple(self, origen: int, destino: int, color: str) -> bool:
        """
        Realiza un movimiento simple de un punto a otro, manejando casos especiales.

        Args:
            origen (int): Punto de origen (1 a 24).
            destino (int): Punto de destino (puede ser fuera del tablero).
            color (str): Color de la ficha.

        Returns:
            bool: True si el movimiento fue exitoso, False en caso contrario.
        """
        # Verificar que hay ficha del color en origen
        estado_origen = self.obtener_estado_punto(origen)
        if estado_origen is None or estado_origen[0] != color:
            return False

        # Caso 1: Sacar fichas (destino fuera del tablero)
        if (destino <= 0 and color == "blanco") or (destino >= 25 and color == "negro"):
            if not self.puede_sacar_fichas(color):
                return False
            self.remover_ficha(origen, 1)
            self.sacar_ficha(color)
            return True

        # Caso 2: Destino fuera de rango válido
        if destino < 1 or destino > 24:
            return False

        # Caso 3: Movimiento normal dentro del tablero
        if not self.es_movimiento_valido_a_punto(destino, color):
            return False

        return self._mover_ficha_bool(origen, destino, color)

    def _mover_ficha_bool(self, origen: int, destino: int, color: str) -> bool:
        """
        Versión de mover_ficha que retorna bool en lugar de lanzar excepciones.

        Args:
            origen (int): Punto de origen (1 a 24).
            destino (int): Punto de destino (1 a 24).
            color (str): Color de la ficha que se mueve.

        Returns:
            bool: True si el movimiento fue exitoso, False en caso contrario.
        """
        # Validar origen
        estado_origen = self.obtener_estado_punto(origen)
        if estado_origen is None or estado_origen[0] != color:
            return False

        # Validar destino
        estado_destino = self.obtener_estado_punto(destino)
        if estado_destino is not None:
            color_destino, cantidad_destino = estado_destino
            if color_destino != color and cantidad_destino > 1:
                return False

        # Realizar el movimiento
        try:
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
                    # Comer ficha contraria
                    self.remover_ficha(destino, 1)
                    self.enviar_a_barra(color_destino)
                    self.colocar_ficha(destino, color, 1)

            return True
        except ValueError:
            return False


    def obtener_movimientos_posibles(self, color: str, dados: Dice) -> list[int]:
        """
        Devuelve una lista de puntos desde los cuales el jugador puede mover.
        
        SRP: Consulta de estado sin modificar tablero.
        ISP: Parte esencial de la interfaz pública.

        Args:
            color (str): Color del jugador.
            dados (Dice): Objeto dados con la tirada actual.

        Returns:
            list[int]: Lista de puntos válidos para mover
             (incluye 0 si puede mover desde barra).
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

        SRP: Lógica pura de verificación.

        Args:
            color (str): Color del jugador.

        Returns:
            bool: True si ha ganado, False en caso contrario.
        """
        return self.__casa__.get(color, 0) == 15

    def mover_ficha(self, origen: int, destino: int, color: str) -> None:
        """
        Mueve una ficha de un punto a otro.

        Reglas:
        - Si el destino está vacío, se coloca la ficha.
        - Si el destino tiene fichas del mismo color, se apila.
        - Si el destino tiene UNA sola ficha del color contrario,
          se la come y se envía a la barra.
        - Si el destino tiene 2+ fichas del color contrario, el movimiento no es válido.

        Args:
            origen (int): Punto de origen (1 a 24).
            destino (int): Punto de destino (1 a 24).
            color (str): Color de la ficha que se mueve.

        Raises:
            ValueError: Si el movimiento no es válido.
        """
        # Validar origen ANTES de hacer cualquier cambio
        estado_origen = self.obtener_estado_punto(origen)
        if estado_origen is None or estado_origen[0] != color:
            raise ValueError("No hay fichas del color indicado en el origen.")

        # Validar destino ANTES de hacer cualquier cambio
        estado_destino = self.obtener_estado_punto(destino)
        if estado_destino is not None:
            color_destino, cantidad_destino = estado_destino
            if color_destino != color and cantidad_destino > 1:
                raise ValueError("El destino está bloqueado por fichas contrarias.")

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
    

    def obtener_estado_dict(self) -> dict:
        """
        Exporta el estado actual del tablero a un diccionario serializable (JSON).
        SRP: Única responsabilidad de empaquetar el estado interno.
        """
        return {
            "puntos": self.__puntos__,
            "barra": self.__barra__,
            "casa": self.__casa__
        }

    def cargar_estado_dict(self, estado: dict) -> None:
        """
        Carga el estado del tablero desde un diccionario (JSON).
        SRP: Única responsabilidad de desempaquetar y aplicar estado.
        """
        try:
            # Usamos .get() para cargar de forma segura,
            # proveyendo valores por defecto si la clave no existe
            self.__puntos__ = estado.get("puntos", [None] * 24)
            self.__barra__ = estado.get("barra", {})
            self.__casa__ = estado.get("casa", {})
        except Exception as e:
            print(f"Error grave al cargar estado del tablero: {e}")
            # Si el estado está muy corrupto, restaurar al inicio
            self.inicializar_posiciones_estandar()


    def __str__(self) -> str:
        """
        Devuelve una representación en texto del tablero.

        ISP: Permite inspeccionar el estado para debugging o CLI.
        
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
