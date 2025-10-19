import os
import sys
from typing import Tuple, Optional, List
import pygame
import math
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Backgammon.Core.Board import Board  # pylint: disable=wrong-import-position
from Backgammon.Core.Dice import Dice  # pylint: disable=wrong-import-position


class DiceMovesCalculator:
    """Calcula movimientos disponibles basados en los dados.
      Rol: 
      - Componente de cálculo puro que transforma tiradas de dados en movimientos.
    
    Principios SOLID:
        - SRP: Cada método tiene una única responsabilidad de cálculo específica.
        - OCP: Puede extenderse con nuevas reglas de dados sin modificar las existentes.
        - ISP: Interfaz mínima con dos métodos públicos específicos."""

    @staticmethod
    def calculate_available_moves(dice_roll1: int, dice_roll2: int) -> List[int]:
        """
        Calcula los movimientos disponibles.
        SRP: Su única responsabilidad es calcular los movimientos.
        OCP: La lógica puede extenderse sin modificar el método.
        """
        if dice_roll1 == dice_roll2:
            return [dice_roll1] * 4
        return [dice_roll1, dice_roll2]

    @staticmethod
    def is_doubles_roll(dice_roll1: int, dice_roll2: int) -> bool:
        """
        Determina si la tirada es dobles.
        SRP: Su única responsabilidad es verificar si la tirada es doble.
        ISP: Método mínimo y específico.
        """
        return dice_roll1 == dice_roll2

class GameStateManager:
    """Gestiona los estados del juego.
    Rol:
        - Componente de control de flujo que valida transiciones de estado.
    
    Principios SOLID:
        - SRP: Solo gestiona estados, no implementa lógica asociada a cada estado.
        - OCP: Nuevos estados pueden agregarse sin modificar la lógica existente.
        - DIP: Los clientes dependen de métodos públicos, no de implementación interna."""

    def __init__(self):
        """
        Inicializa el gestor de estados del juego.
        SRP: Inicializa el estado del juego.
        OCP: Estados válidos pueden modificarse sin cambiar métodos.
        """
        self.current_state = 'START_ROLL'
        self.valid_states = {'START_ROLL', 'AWAITING_ROLL', 'AWAITING_PIECE_SELECTION', 'AWAITING_SKIP_CONFIRMATION'}

    def change_state(self, new_state: str) -> None:
        """
        Cambia el estado del juego con validación.
        SRP: Cambia el estado del juego.
        OCP: Se pueden añadir más estados sin modificar la lógica existente.
        """
        if new_state in self.valid_states:
            self.current_state = new_state
        else:
            raise ValueError(f"Estado inválido: {new_state}")

    def get_current_state(self) -> str:
        """
        Obtiene el estado actual.
        SRP: Su única responsabilidad es devolver el estado actual.
        ISP: Método mínimo de consulta.
        """
        return self.current_state


class MessageManager:
    """
    Genera mensajes apropiados para el estado del juego.
    
    Rol:
        - Componente de presentación que centraliza la generación de mensajes.
    
    Principios SOLID:
        - SRP: Centraliza la creación de todos los mensajes de la UI.
        - OCP: Nuevos mensajes pueden agregarse sin modificar existentes.
        - ISP: Cada método genera un tipo específico de mensaje.
    """

    @staticmethod
    def get_start_message() -> str:
        """
        Mensaje para el inicio del juego.
        
        Principios SOLID:
            - SRP: Genera únicamente el mensaje de inicio.
            - ISP: Método específico sin parámetros innecesarios.
        """
        return "Presiona 'R' para decidir quién empieza."

    @staticmethod
    def get_roll_winner_message(winner: str, winner_roll: int, loser_roll: int) -> str:
        """
        Mensaje cuando alguien gana la tirada inicial.
        
        Principios SOLID:
            - SRP: Formatea mensaje de ganador de tirada inicial.
            - ISP: Parámetros mínimos necesarios para el mensaje.
        """
        winner_display = winner.capitalize()
        loser_display = "Blanco" if winner == "negro" else "Negro"
        return (f"{winner_display} ({winner_roll}) gana a {loser_display} "
                f"({loser_roll}). Presiona 'R' para tirar tus dados.")

    @staticmethod
    def get_awaiting_roll_message(current_player: str) -> str:
        """
        Mensaje cuando el jugador debe tirar dados.
        
        Principios SOLID:
            - SRP: Genera mensaje específico para espera de tirada.
            - ISP: Interfaz mínima con un solo parámetro.
        """
        return f"Turno de {current_player}. Presiona 'R' para tirar los dados."

    @staticmethod
    def get_doubles_roll_message(current_player: str, dice_value: int,
                                available_moves: List[int]) -> str:
        """
        Mensaje cuando se sacan dobles.
        
        Principios SOLID:
            - SRP: Formatea mensaje específico para tirada de dobles.
            - ISP: Parámetros específicos del contexto de dobles.
        """
        moves_count = len(available_moves)
        return f"{current_player.capitalize()} sacó dobles de {dice_value}! Tienes {moves_count} movimientos de {dice_value}. Elige ficha."

    @staticmethod
    def get_normal_roll_message(current_player: str, available_moves: List[int]) -> str:
        """
        Mensaje para tirada normal.
        
        Principios SOLID:
            - SRP: Genera mensaje para tirada normal (no dobles).
            - ISP: Interfaz específica para contexto normal.
        """
        dice_str = ', '.join(map(str, available_moves))
        return f"Turno de {current_player}. Dados: [{dice_str}]. Elige una ficha para mover."

    @staticmethod
    def get_piece_selected_message(point: int, available_moves: List[int]) -> str:
        """
        Mensaje cuando se selecciona una ficha.
        
        Principios SOLID:
            - SRP: Formatea mensaje de selección de pieza.
            - ISP: Parámetros mínimos para el contexto.
        """
        dice_str = ', '.join(map(str, available_moves))
        return f"Ficha en punto {point} seleccionada. Dados disponibles: [{dice_str}]. Elige destino."

    @staticmethod
    def get_move_completed_message(remaining_moves: int, available_moves: List[int]) -> str:
        """
        Mensaje cuando se completa un movimiento.
        
        Principios SOLID:
            - SRP: Genera mensaje post-movimiento con estado actualizado.
            - OCP: Maneja caso de turno completo sin modificar lógica base.
        """
        if remaining_moves == 0:
            return "Turno completado."
        dice_str = ', '.join(map(str, available_moves))
        return f"Movimiento realizado. Te quedan {remaining_moves} dados: [{dice_str}]. Elige ficha."

    @staticmethod
    def get_invalid_piece_message(point: int) -> str:
        """
        Mensaje cuando se selecciona una ficha inválida.
        
        Principios SOLID:
            - SRP: Formatea error específico de selección inválida.
            - ISP: Parámetro mínimo necesario.
        """
        return f"No tienes fichas en el punto {point}. Elige una válida."

    @staticmethod
    def get_invalid_move_message() -> str:
        """
        Mensaje para movimiento inválido.
        
        Principios SOLID:
            - SRP: Mensaje genérico de error de movimiento.
            - ISP: Sin parámetros, mensaje fijo.
        """
        return "Movimiento inválido. Vuelve a elegir una ficha."

    @staticmethod
    def get_invalid_direction_message() -> str:
        """
        Mensaje para dirección incorrecta.
        
        Principios SOLID:
            - SRP: Error específico de dirección.
            - ISP: Mensaje fijo sin parámetros.
        """
        return "Movimiento inválido (dirección incorrecta)."

    @staticmethod
    def get_dice_not_available_message(dice_needed: int, available_moves: List[int]) -> str:
        """
        Mensaje cuando no se tiene el dado necesario.
        
        Principios SOLID:
            - SRP: Formatea error de dado no disponible.
            - ISP: Parámetros específicos para este error.
        """
        return f"No tienes el dado {dice_needed} disponible. Dados: {available_moves}."

    @staticmethod
    def get_blocked_move_message(origin: int, destination: int) -> str:
        """
        Mensaje para movimiento bloqueado.
        
        Principios SOLID:
            - SRP: Error específico de bloqueo.
            - ISP: Parámetros mínimos (origen y destino).
        """
        return f"Movimiento de {origin} a {destination} bloqueado o inválido."
    
    @staticmethod
    def get_no_moves_available_message(player: str, reason: str) -> str:
        """
        Mensaje cuando no hay movimientos disponibles.
        
        Principios SOLID:
            - SRP: Formatea mensaje de sin movimientos con razón.
            - ISP: Parámetros específicos del contexto.
        """
        return f"¡{player.capitalize()} no puede mover! {reason} Presiona 'R' para continuar."
    
    @staticmethod
    def get_bearing_off_available_message(player: str, home_count: int) -> str:
        """
        Mensaje cuando puede hacer bearing off.
        
        Principios SOLID:
            - SRP: Mensaje específico de disponibilidad de bearing off.
            - ISP: Parámetros necesarios para el contexto.
        """
        return f"{player.capitalize()}: Puedes sacar fichas ({home_count}/15). Click fuera del tablero."

    @staticmethod
    def get_cannot_bear_off_message() -> str:
        """
        Mensaje cuando intenta bearing off pero no puede.
        
        Principios SOLID:
            - SRP: Error específico de bearing off no permitido.
            - ISP: Mensaje fijo, sin parámetros.
        """
        return "No puedes sacar. Tienes fichas fuera del cuadrante casa."

    @staticmethod
    def get_bearing_off_success_message(player: str, home_count: int, remaining_moves: int) -> str:
        """
        Mensaje cuando saca una ficha exitosamente.
        
        Principios SOLID:
            - SRP: Formatea éxito de bearing off con estado.
            - OCP: Maneja caso de turno completo sin modificar base.
        """
        if remaining_moves > 0:
            return f"¡Ficha sacada! ({home_count}/15) Te quedan {remaining_moves} dados."
        return f"Ficha sacada ({home_count}/15). Turno completado."

    @staticmethod
    def get_victory_message(player: str) -> str:
        """
        Mensaje de victoria.
        
        Principios SOLID:
            - SRP: Genera únicamente mensaje de victoria.
            - ISP: Parámetro mínimo (jugador ganador).
        """
        return f"🎉 ¡{player.upper()} GANA EL JUEGO! 🎉"

class MovementValidator:
    """
    Valida si un jugador tiene movimientos disponibles.
    
    Rol:
        - Componente de validación que verifica disponibilidad de movimientos.
    
    Principios SOLID:
        - SRP: Orquesta validaciones pero delega lógica específica.
        - DIP: Recibe Board y BarManager por inyección, no crea instancias.
        - ISP: Interfaz pública mínima con métodos específicos.
    """

    def __init__(self, board, bar_manager):
        """
        Inicializa el validador con sus dependencias.
        
        Principios SOLID:
            - DIP: Recibe las dependencias (Board, BarManager) por inyección.
            - SRP: Solo inicializa referencias, no implementa lógica.
        """
        self.board = board
        self.bar_manager = bar_manager

    def has_any_valid_move(self, player: str, available_moves: list) -> bool:
        """
        Verifica si el jugador tiene algún movimiento válido disponible.
        
        Principios SOLID:
            - SRP: Su responsabilidad es orquestar las validaciones para un movimiento estándar.
            - DIP: Depende de abstracciones de reglas (Board, BarManager), no de su implementación.
            - ISP: Llama solo a métodos necesarios de cada dependencia.
        """
        # Primero verificar si debe mover desde la barra
        if self.bar_manager.has_pieces_on_bar(player):
            return self._can_enter_from_bar(player, available_moves)
        
        # Si no hay fichas en la barra, verificar movimientos desde el tablero
        return self._can_move_from_board(player, available_moves)
    

    def _can_enter_from_bar(self, player: str, available_moves: list) -> bool:
        """
        Verifica si el jugador puede entrar desde la barra con alguno de los dados.
        
        Principios SOLID:
            - SRP: Valida únicamente entrada desde barra.
            - DIP: Usa Board para verificar estado sin conocer implementación.
        """
        for dice_value in set(available_moves):  # usar set para evitar repetidos
            entry_point = self._get_entry_point(player, dice_value)
            destination_state = self.board.obtener_estado_punto(entry_point)
            
            # Puede entrar si está vacío, tiene fichas propias, o tiene solo 1 ficha enemiga
            if destination_state is None:
                return True
            
            dest_color, dest_count = destination_state
            if dest_color == player or dest_count == 1:
                return True
        
        return False

    def _can_move_from_board(self, player: str, available_moves: list) -> bool:
        """
        Verifica si el jugador puede mover alguna ficha del tablero.
        
        Principios SOLID:
            - SRP: Valida únicamente movimientos desde tablero.
            - DIP: Usa Board para obtener estado sin implementación interna.
        """
        for point_num in range(1, 25):
            point_state = self.board.obtener_estado_punto(point_num)
            
            # Si el punto tiene fichas del jugador actual
            if point_state and point_state[0] == player:
                # Verificar si puede mover con alguno de los dados disponibles
                for dice_value in set(available_moves):
                    destination = self._calculate_destination(player, point_num, dice_value)
                    
                    # Verificar que el destino sea válido
                    if 1 <= destination <= 24:
                        if self._is_move_possible(destination, player):
                            return True
        
        return False

    def _is_move_possible(self, destination: int, player: str) -> bool:
        """
        Verifica si un destino específico es accesible para el jugador.
        
        Principios SOLID:
            - SRP: Valida únicamente accesibilidad de destino.
            - ISP: Método privado específico, no expuesto públicamente.
        """
        destination_state = self.board.obtener_estado_punto(destination)
        
        if destination_state is None:
            return True
        
        dest_color, dest_count = destination_state
        
        # Accesible si: tiene fichas propias, o tiene solo 1 ficha enemiga (captura)
        return dest_color == player or dest_count == 1

    def _calculate_destination(self, player: str, origin: int, dice_value: int) -> int:
        """
        Calcula el punto de destino basado en el origen y el valor del dado.
        
        Principios SOLID:
            - SRP: Cálculo puro de destino sin validación.
            - ISP: Método privado específico.
        """
        if player == "negro":
            return origin + dice_value
        else:
            return origin - dice_value

    def _get_entry_point(self, player: str, dice_value: int) -> int:
        """
        Calcula el punto de entrada desde la barra.
        
        Principios SOLID:
            - SRP: Cálculo específico de entrada desde barra.
            - ISP: Método privado enfocado.
        """
        if player == "negro":
            return dice_value
        else:
            return 25 - dice_value

    def get_blocked_reason(self, player: str, available_moves: list) -> str:
        """
        Obtiene una descripción del por qué el jugador no puede mover.
        
        Principios SOLID:
            - SRP: Genera descripción de bloqueo sin modificar estado.
            - ISP: Método público específico para obtener razón.
        """
        if self.bar_manager.has_pieces_on_bar(player):
            return ("No puedes entrar desde la barra. Todos los puntos de entrada "
                   "están bloqueados por el oponente.")
        else:
            return ("No tienes movimientos válidos. Todas tus fichas están bloqueadas "
                   "por el oponente.")


class BarManager:
    """
    Gestiona la lógica de la barra central.
    
    Rol:
        - Componente de estado que mantiene fichas capturadas.
    
    Principios SOLID:
        - SRP: Solo gestiona estado de la barra, no reglas de movimiento.
        - OCP: Operaciones nuevas pueden agregarse sin modificar existentes.
        - Encapsulamiento: Protege estado interno mediante atributo privado.
    """

    def __init__(self):
        """
        Inicializa el gestor de barra.
        
        Principios SOLID:
            - SRP: Solo inicializa el estado de la barra.
            - Encapsulamiento: Usa atributo privado para proteger estado.
        """
        self.__bar_pieces__ = {"negro": 0, "blanco": 0}

    def add_piece_to_bar(self, color: str) -> None:
        """
        Agrega una ficha a la barra.
        
        Principios SOLID:
            - SRP: Única operación de agregar con validación.
            - ISP: Método específico para agregar.
        """
        if color in self.__bar_pieces__:
            self.__bar_pieces__[color] += 1
        else:
            raise ValueError(f"Color inválido: {color}")

    def remove_piece_from_bar(self, color: str) -> bool:
        """
        Remueve una ficha de la barra.
        
        Principios SOLID:
            - SRP: Única operación de remover con validación.
            - ISP: Método específico para remover.
        """
        if color in self.__bar_pieces__ and self.__bar_pieces__[color] > 0:
            self.__bar_pieces__[color] -= 1
            return True
        return False

    def get_pieces_count(self, color: str) -> int:
        """
        Obtiene el número de fichas en la barra.
        
        Principios SOLID:
            - SRP: Consulta pura sin modificar estado.
            - ISP: Método mínimo de consulta.
        """
        return self.__bar_pieces__.get(color, 0)

    def has_pieces_on_bar(self, color: str) -> bool:
        """
        Verifica si un jugador tiene fichas en la barra.
        
        Principios SOLID:
            - SRP: Verificación específica de existencia.
            - ISP: Método booleano específico.
        """
        return self.get_pieces_count(color) > 0

    def get_bar_state(self) -> dict:
        """
        Obtiene el estado completo de la barra.
        
        Principios SOLID:
            - SRP: Consulta de estado completo.
            - Encapsulamiento: Retorna copia, no referencia interna.
        """
        return self.__bar_pieces__.copy()


class CaptureValidator:
    """
    Valida y determina capturas.
    
    Rol:
        - Componente de validación de reglas de captura.
    
    Principios SOLID:
        - SRP: Métodos estáticos que validan condiciones específicas.
        - ISP: Interfaz mínima con dos métodos especializados.
        - OCP: Nuevas reglas pueden agregarse sin modificar existentes.
    """

    @staticmethod
    def can_capture_piece(destination_state: tuple, attacking_color: str) -> bool:
        """
        Determina si se puede capturar una ficha.
        
        Principios SOLID:
            - SRP: Validación pura de condición de captura.
            - ISP: Método específico sin efectos secundarios.
        """
        if destination_state is None:
            return False
        destination_color, destination_count = destination_state
        return destination_color != attacking_color and destination_count == 1

    @staticmethod
    def is_move_blocked(destination_state: tuple, attacking_color: str) -> bool:
        """
        Determina si un movimiento está bloqueado.
        
        Principios SOLID:
            - SRP: Validación específica de bloqueo.
            - ISP: Método específico complementario a can_capture_piece.
        """
        if destination_state is None:
            return False
        destination_color, destination_count = destination_state
        return destination_color != attacking_color and destination_count > 1


class BarMovementRules:
    """Define las reglas para movimientos desde la barra."""

    @staticmethod
    def get_entry_point(color: str, dice_value: int) -> int:
        """Calcula el punto de entrada desde la barra."""
        if color == "negro":
            return dice_value
        return 25 - dice_value

    @staticmethod
    def must_enter_from_bar_first(bar_manager: 'BarManager', color: str) -> bool:
        """Determina si el jugador debe mover desde la barra."""
        return bar_manager.has_pieces_on_bar(color)
    
class BearingOffValidator:
    """
    Valida y gestiona las reglas de bearing off (sacar fichas a casa).
    
    Rol:
        - Componente especializado en validación de reglas de bearing off.
    
    Principios SOLID:
        - SRP: Cada método valida un aspecto específico de bearing off.
        - DIP: Depende de Board mediante inyección, no crea instancias.
        - ISP: Métodos específicos para cada tipo de validación.
    """

    def __init__(self, board):
        """
        Inicializa el validador con su dependencia.
        
        Principios SOLID:
            - DIP: Recibe Board por inyección.
            - SRP: Solo inicializa referencia.
        """
        self.board = board

    def can_bear_off(self, player: str) -> bool:
        """
        Verifica si un jugador puede empezar a sacar fichas.
        Solo puede hacerlo si todas sus fichas están en su cuadrante casa.
        
        Principios SOLID:
            - SRP: Valida únicamente condición de bearing off permitido.
            - DIP: Usa Board sin conocer implementación interna.
            - ISP: Método específico que retorna booleano.
        """
        if player == "negro":
            home_quadrant = range(19, 25)  # 19-24 (último cuadrante)
            other_points = range(1, 19)
        else:  # blanco
            home_quadrant = range(1, 7)  # 1-6 (último cuadrante)
            other_points = range(7, 25)

        for point in other_points:
            state = self.board.obtener_estado_punto(point)
            if state and state[0] == player:
                return False
        return True

    def is_bearing_off_move(self, player: str, origin: int, destination: int) -> bool:
        """
        Determina si un movimiento es un intento de bearing off.
        
        Principios SOLID:
            - SRP: Verifica únicamente si es intento de bearing off.
            - ISP: Método específico sin efectos secundarios.
        """
        if player == "negro":
            return destination > 24
        else:  # blanco
            return destination < 1

    def validate_bearing_off_move(self, player: str, origin: int, 
                                  dice_value: int) -> tuple[bool, str]:
        """
        Valida un movimiento de bearing off según las reglas.
        
        Reglas:
        1. El jugador debe tener todas sus fichas en el cuadrante casa
        2. El dado debe coincidir exactamente con la posición de la ficha
        3. Si el dado es mayor y no hay fichas en posiciones superiores, es válido
        
        Principios SOLID:
            - SRP: Valida reglas complejas de bearing off en un solo lugar.
            - ISP: Retorna tupla específica (validez, mensaje).
            - OCP: Reglas pueden extenderse sin modificar estructura.
        """
        # 1. Verificar que puede hacer bearing off
        if not self.can_bear_off(player):
            return False, "No puedes sacar fichas. Tienes fichas fuera del cuadrante casa."

        # 2. Verificar que la ficha está en el cuadrante casa
        if player == "negro":
            home_quadrant = range(19, 25)
            position = 25 - origin  # Distancia a la salida
        else:
            home_quadrant = range(1, 7)
            position = origin  # Distancia a la salida

        if origin not in home_quadrant:
            return False, "La ficha no está en tu cuadrante casa."

        # 3. Verificar reglas del dado
        if dice_value == position:
            # Dado exacto - siempre válido
            return True, ""
        elif dice_value > position:
            # Dado mayor - solo válido si no hay fichas en posiciones superiores
            if not self._has_pieces_in_higher_positions(player, origin):
                return True, ""
            else:
                return False, f"Necesitas dado {position} o mover fichas superiores primero."
        else:
            # Dado menor - nunca válido para bearing off
            return False, f"Necesitas al menos dado {position} para sacar esta ficha."

    def _has_pieces_in_higher_positions(self, player: str, origin: int) -> bool:
        """
        Verifica si hay fichas en posiciones más altas que el origen.
        
        Principios SOLID:
            - SRP: Verificación específica de posiciones superiores.
            - ISP: Método privado enfocado.
        """
        if player == "negro":
            # Negro (19-24): más alejado = menor número
            higher_points = range(19, origin)
        else:
            # Blanco (1-6): más alejado = mayor número
            higher_points = range(origin + 1, 7)

        for point in higher_points:
            state = self.board.obtener_estado_punto(point)
            if state and state[0] == player:
                return True

        return False

    def get_bearing_off_destination(self, player: str) -> int:
        """
        Obtiene el punto de destino ficticio para bearing off.
        Usado para calcular movimientos fuera del tablero.
        
        Principios SOLID:
            - SRP: Cálculo específico de destino ficticio.
            - ISP: Método específico sin efectos secundarios.
        """
        return 25 if player == "negro" else 0

class HomeManager:
    """
    Gestiona las fichas que han salido del tablero (en casa).
    
    Rol:
        - Componente de estado que mantiene conteo de fichas en casa.
    
    Principios SOLID:
        - SRP: Solo gestiona conteo de fichas en casa, no implementa bearing off.
        - OCP: Operaciones nuevas pueden agregarse sin modificar existentes.
        - Encapsulamiento: Protege estado interno mediante atributo privado.
    """

    def __init__(self):
        """
        Inicializa el gestor de casa.
        
        Principios SOLID:
            - SRP: Solo inicializa el estado de casa.
            - Encapsulamiento: Usa atributo privado.
        """
        self.__home_pieces__ = {"negro": 0, "blanco": 0}

    def add_piece_to_home(self, color: str) -> None:
        """
        Agrega una ficha a casa.
        
        Principios SOLID:
            - SRP: Única operación de agregar con validación.
            - ISP: Método específico para agregar.
        """
        if color in self.__home_pieces__:
            self.__home_pieces__[color] += 1
        else:
            raise ValueError(f"Color inválido: {color}")

    def get_pieces_count(self, color: str) -> int:
        """
        Obtiene el número de fichas en casa.
        
        Principios SOLID:
            - SRP: Consulta pura sin modificar estado.
            - ISP: Método mínimo de consulta.
        """
        return self.__home_pieces__.get(color, 0)

    def get_home_state(self) -> dict:
        """
        Obtiene el estado completo de casa.
        
        Principios SOLID:
            - SRP: Consulta de estado completo.
            - Encapsulamiento: Retorna copia, no referencia interna.
        """
        return self.__home_pieces__.copy()

    def has_won(self, color: str) -> bool:
        """
        Verifica si un jugador ha ganado (15 fichas en casa).
        
        Principios SOLID:
            - SRP: Verifica únicamente condición de victoria.
            - ISP: Método booleano específico.
        """
        return self.__home_pieces__.get(color, 0) == 15
    
class PygameUI:
    """
    Interfaz gráfica principal del juego de Backgammon.
    
    Rol:
        - Capa de presentación visual que comunica al usuario con el dominio del juego.
        - Coordina la visualización, entrada de usuario y lógica de turnos.
    
    Principios SOLID:
        - SRP: Inicializa y coordina todos los componentes de la UI sin implementar
          reglas de negocio (delegadas a clases especializadas).
        - OCP: Puede extenderse agregando nuevos gestores sin modificar el núcleo.
        - DIP: Depende de abstracciones como Board, Dice, y gestores especializados,
          no de implementaciones concretas.
    """

    def __init__(self, board_width: int = 1600, board_height: int = 900):
        """
        Inicializa la interfaz gráfica y todos sus componentes.
        
        Principios SOLID:
            - SRP: Solo inicializa componentes, no implementa lógica de juego.
            - DIP: Inyecta dependencias (Board, Dice, gestores) mediante composición.
            - ISP: Utiliza interfaces específicas de cada gestor sin acoplamiento excesivo.
        """
        pygame.init()  # pylint: disable=no-member
        self.__screen__ = pygame.display.set_mode((board_width, board_height))
        pygame.display.set_caption("Backgammon")
        self.__clock__ = pygame.time.Clock()
        self.__running__ = True
        self.__game_state_manager__ = GameStateManager()
        self.__dice_calculator__ = DiceMovesCalculator()
        self.__message_manager__ = MessageManager()
        self.__bar_manager__ = BarManager()
        self.__capture_validator__ = CaptureValidator()
        self.__dice__ = Dice()
        self.__dice_rolls__ = []
        self.__available_moves__ = []
        self.__current_player__ = None
        self.__font__ = pygame.font.Font(None, 45)
        self.__message__ = self.__message_manager__.get_start_message()
        self.__is_doubles_roll__ = False
        self.__board__ = Board()
        self.__board__.inicializar_posiciones_estandar()
        self.__movement_validator__ = MovementValidator(self.__board__, self.__bar_manager__)
        self.__selected_point__: Optional[int] = None
        self.__bearing_off_validator__ = BearingOffValidator(self.__board__)
        self.__home_manager__ = HomeManager()
        self.__white__ = (255, 255, 255)
        self.__black__ = (0, 0, 0)
        self.__brown_light__ = (222, 184, 135)
        self.__brown_dark__ = (139, 69, 19)
        self.__board_border__ = (101, 67, 33)
        self.__bar_color__ = (101, 67, 33)
        self.__checker_white__ = (240, 240, 240)
        self.__checker_black__ = (40, 40, 40)
        self.__checker_border__ = (0, 0, 0)
        self.__dice_color__ = (250, 250, 250)
        self.__pip_color__ = (0, 0, 0)
        self.__doubles_highlight__ = (255, 215, 0)
        self.__capture_highlight__ = (255, 0, 0)
        self.__board_margin__ = 50
        self.__board_width__ = 1500
        self.__board_height__ = 800
        self.__bar_width__ = 80

    def run(self) -> None:
        """
        Inicia el bucle principal del juego.
        
        Principios SOLID:
            - SRP: Su única responsabilidad es mantener el ciclo de vida del juego.
            - OCP: Puede extenderse el ciclo sin modificar este método base.
        """
        while self.__running__:
            self.__handle_events()
            self.__update()
            self.__draw()
            self.__clock__.tick(60)
        pygame.quit()  # pylint: disable=no-member
        sys.exit()

    def __handle_events(self) -> None:
        """
        Gestiona las entradas del usuario (teclado y mouse).
        
        Principios SOLID:
            - SRP: Solo maneja eventos de entrada, delega acciones a métodos especializados.
            - OCP: Nuevos eventos pueden agregarse sin modificar eventos existentes.
            - ISP: Separa eventos por tipo (teclado, mouse) para interfaces específicas.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # pylint: disable=no-member
                self.__running__ = False
            elif event.type == pygame.KEYDOWN:  # pylint: disable=no-member
                if event.key == pygame.K_ESCAPE:  # pylint: disable=no-member
                    self.__running__ = False
                if event.key == pygame.K_r:  # pylint: disable=no-member
                    self.__handle_roll_request()
            elif (event.type == pygame.MOUSEBUTTONDOWN and  # pylint: disable=no-member
                  event.button == 1):
                if (self.__game_state_manager__.get_current_state() ==
                        'AWAITING_PIECE_SELECTION'):
                    self.__handle_piece_selection(pygame.mouse.get_pos())

    def __handle_roll_request(self) -> None:
        """
        Maneja las solicitudes de tirada de dados según el estado actual.
        
        Principios SOLID:
            - SRP: Delega a métodos especializados según el estado del juego.
            - OCP: Estados nuevos pueden agregarse sin modificar lógica existente.
            - DIP: Depende de GameStateManager para determinar flujo.
        """
        current_state = self.__game_state_manager__.get_current_state()
        if current_state == 'START_ROLL':
            self.__roll_to_start()
        elif current_state == 'AWAITING_ROLL':
            self.__roll_player_dice()
        elif current_state == 'AWAITING_SKIP_CONFIRMATION':
            self.__end_turn()

    def __handle_piece_selection(self, mouse_pos: Tuple[int, int]) -> None:
        """
        Maneja la selección de fichas y destinos mediante clicks del mouse.
        
        Principios SOLID:
            - SRP: Coordina selección de origen/destino, delega validación a otros métodos.
            - DIP: Usa métodos abstractos de cálculo sin conocer detalles de implementación.
        """
        clicked_point = self.__get_point_from_mouse_pos(mouse_pos)
        if clicked_point is None:
            return
        if self.__selected_point__ is None:
            self.__attempt_piece_selection(clicked_point)
        else:
            self.__attempt_move(self.__selected_point__, clicked_point)
            self.__selected_point__ = None


    def __attempt_piece_selection(self, point: int) -> None:
        """
        Intenta seleccionar una ficha en un punto específico.
        
        Principios SOLID:
            - SRP: Valida selección de pieza y actualiza mensajes al usuario.
            - DIP: Usa BarManager y Board para verificar estado sin implementar lógica interna.
            - ISP: Llama solo a métodos necesarios de cada dependencia.
        """
        # Click en la barra
        if point == 0:
            if self.__bar_manager__.has_pieces_on_bar(self.__current_player__):
                self.__selected_point__ = 0
                self.__message__ = (f"Ficha en la barra seleccionada. Dados: "
                                f"{self.__available_moves__}. Elige punto de entrada.")
            else:
                self.__message__ = "No tienes fichas en la barra."
            return
        
        # Verificar si debe mover desde la barra primero
        if BarMovementRules.must_enter_from_bar_first(self.__bar_manager__,
                                                    self.__current_player__):
            self.__message__ = ("Debes mover primero desde la barra. "
                            "Haz clic en el centro del tablero.")
            return
        
        # Click en punto normal
        estado_punto = self.__board__.obtener_estado_punto(point)
        if estado_punto and estado_punto[0] == self.__current_player__:
            self.__selected_point__ = point
            
            # Verificar si REALMENTE puede sacar esta ficha específica
            can_bear_off_this_piece = False
            if self.__bearing_off_validator__.can_bear_off(self.__current_player__):
                # Verificar si está en home quadrant
                if self.__current_player__ == "negro":
                    in_home = 19 <= point <= 24
                else:
                    in_home = 1 <= point <= 6
                
                if in_home:
                    # Verificar si tiene algún dado válido para sacar ESTA ficha
                    dice_needed = self.__calculate_bearing_off_dice(point)
                    for dice_value in self.__available_moves__:
                        is_valid, _ = self.__bearing_off_validator__.validate_bearing_off_move(
                            self.__current_player__, point, dice_value)
                        if is_valid:
                            can_bear_off_this_piece = True
                            break
            
            # Mensaje apropiado
            if can_bear_off_this_piece:
                home_count = self.__home_manager__.get_pieces_count(self.__current_player__)
                casa_name = "CASA NEGRO" if self.__current_player__ == "negro" else "CASA BLANCO"
                self.__message__ = f"¡Puede sacar! ({home_count}/15) Click en {casa_name}"
            else:
                dice_str = ', '.join(map(str, self.__available_moves__))
                self.__message__ = f"Punto {point} seleccionado. Dados: [{dice_str}]. Elige destino."
        else:
            self.__message__ = "No tienes fichas en esta posición. Elige una válida."

    def __attempt_move(self, origen: int, destino: int) -> None:
        """
        Intenta realizar un movimiento desde origen a destino.
        
        Principios SOLID:
            - SRP: Coordina validación y ejecución, pero delega cada tarea a métodos especializados.
            - OCP: Bearing off es una extensión sin modificar movimientos normales.
            - DIP: Depende de validadores abstractos (BearingOffValidator).
        """
        # Verificar si es un intento de bearing off
        if self.__bearing_off_validator__.is_bearing_off_move(
                self.__current_player__, origen, destino):
            self.__attempt_bearing_off(origen, destino)
            return
        
        # Validar el movimiento ANTES de ejecutarlo
        if not self.__validate_and_report_move(origen, destino):
            # Ya hay mensaje de error
            return
        
        # Si pasó la validación, ejecutar
        self.__execute_move(origen, destino)


    def __attempt_bearing_off(self, origen: int, destino: int) -> None:
        """
        Intenta realizar bearing off (sacar fichas del tablero).
        
        Principios SOLID:
            - SRP: Gestiona solo la lógica de bearing off, no movimientos normales.
            - DIP: Usa BearingOffValidator y HomeManager sin conocer su implementación.
            - LSP: Puede sustituir movimientos normales cuando corresponde.
        """
        # Calcular dado necesario
        dice_needed = self.__calculate_bearing_off_dice(origen)
        
        # Verificar que el dado esté disponible
        if dice_needed not in self.__available_moves__:
            available_str = ', '.join(map(str, self.__available_moves__))
            self.__message__ = f"Necesitas dado {dice_needed}. Tienes: {available_str}"
            return
        
        # Validar según las reglas de bearing off
        is_valid, error_msg = self.__bearing_off_validator__.validate_bearing_off_move(
            self.__current_player__, origen, dice_needed)
        
        if not is_valid:
            self.__message__ = error_msg
            return
        
        # Ejecutar bearing off
        try:
            self.__board__.remover_ficha(origen, 1)
            self.__home_manager__.add_piece_to_home(self.__current_player__)
            self.__available_moves__.remove(dice_needed)
            
            # Verificar victoria
            if self.__home_manager__.has_won(self.__current_player__):
                self.__message__ = f"🎉 ¡{self.__current_player__.upper()} GANA! 🎉"
                return
            
            remaining_moves = len(self.__available_moves__)
            home_count = self.__home_manager__.get_pieces_count(self.__current_player__)
            
            if remaining_moves == 0:
                self.__end_turn()
            else:
                # Verificar movimientos válidos
                has_moves = (
                    self.__movement_validator__.has_any_valid_move(
                        self.__current_player__, self.__available_moves__) or
                    self.__has_valid_bearing_off_moves()
                )
                
                if not has_moves:
                    self.__message__ = "Sin movimientos válidos. Presiona 'R'."
                    self.__game_state_manager__.change_state('AWAITING_SKIP_CONFIRMATION')
                else:
                    dice_str = ', '.join(map(str, self.__available_moves__))
                    self.__message__ = f"¡Ficha sacada! ({home_count}/15) Dados: [{dice_str}]"
                    
        except Exception as e:
            self.__message__ = "Error al sacar ficha."

    def __calculate_bearing_off_dice(self, origen: int) -> int:
        """
        Calcula qué dado se necesita para bearing off desde un punto.
        
        Principios SOLID:
            - SRP: Cálculo específico para bearing off.
            - ISP: Método mínimo enfocado en una operación.
        """
        if self.__current_player__ == "negro":
            return 25 - origen
        else:
            return origen



    def __execute_bearing_off(self, origen: int, dice_used: int) -> None:
        """
        Ejecuta un bearing off validado.
        
        Principios SOLID:
            - SRP: Solo ejecuta, asume que la validación ya ocurrió.
            - DIP: Usa Board y HomeManager mediante interfaces públicas.
        """
        try:
            # Remover la ficha del tablero
            self.__board__.remover_ficha(origen, 1)
            
            # Agregar a casa
            self.__home_manager__.add_piece_to_home(self.__current_player__)
            
            # Remover el dado usado
            self.__available_moves__.remove(dice_used)
            
            # Verificar victoria
            if self.__home_manager__.has_won(self.__current_player__):
                self.__message__ = f"¡{self.__current_player__.upper()} GANA!"
                self.__game_state_manager__.change_state('GAME_OVER')
                return
            
            remaining_moves = len(self.__available_moves__)
            home_count = self.__home_manager__.get_pieces_count(self.__current_player__)
            
            if remaining_moves == 0:
                self.__message__ = f"Ficha sacada ({home_count}/15). Turno terminado."
                self.__end_turn()
            else:
                # Verificar movimientos válidos
                has_moves = (self.__movement_validator__.has_any_valid_move(
                    self.__current_player__, self.__available_moves__) or
                    self.__has_valid_bearing_off_moves())
                
                if not has_moves:
                    self.__message__ = "Sin movimientos válidos. Presiona 'R'."
                    self.__game_state_manager__.change_state('AWAITING_SKIP_CONFIRMATION')
                else:
                    dice_str = ', '.join(map(str, self.__available_moves__))
                    self.__message__ = f"¡Sacaste 1! ({home_count}/15) Dados: [{dice_str}]"
                    
        except Exception as e:
            self.__message__ = "Error al sacar ficha. Intenta de nuevo."


    def __has_valid_bearing_off_moves(self) -> bool:
        """
        Verifica si hay movimientos válidos de bearing off disponibles.
        
        Principios SOLID:
            - SRP: Verificación específica de bearing off.
            - DIP: Usa BearingOffValidator para reglas de negocio.
        """
        if not self.__bearing_off_validator__.can_bear_off(self.__current_player__):
            return False
        
        if self.__current_player__ == "negro":
            home_quadrant = range(19, 25)
        else:
            home_quadrant = range(1, 7)
        
        for point in home_quadrant:
            state = self.__board__.obtener_estado_punto(point)
            if state and state[0] == self.__current_player__:
                for dice_value in set(self.__available_moves__):
                    is_valid, _ = self.__bearing_off_validator__.validate_bearing_off_move(
                        self.__current_player__, point, dice_value)
                    if is_valid:
                        return True
        
        return False
    

    def __execute_move(self, origen: int, destino: int) -> None:
        """
        Ejecuta un movimiento previamente validado.
        
        Principios SOLID:
            - SRP: Solo ejecuta movimientos, no valida (validación ya hecha).
            - DIP: Interactúa con Board, BarManager y CaptureValidator sin detalles internos.
            - OCP: Capturas son una extensión que no modifica movimientos base.
        """
        # El movimiento ya fue validado en __validate_and_report_move
        # Aquí solo ejecutamos
        
        dado_usado = self.__calculate_dice_needed(origen, destino)
        destination_state = self.__board__.obtener_estado_punto(destino)
        capture_occurred = False
        captured_color = None

        # Procesar captura si existe
        if (destination_state is not None and 
            self.__capture_validator__.can_capture_piece(destination_state,
                                                        self.__current_player__)):
            captured_color = destination_state[0]
            capture_occurred = True
            
            try:
                self.__board__.remover_ficha(destino, 1)
            except TypeError:
                self.__board__.remover_ficha(destino)
            
            self.__bar_manager__.add_piece_to_bar(captured_color)

        # Ejecutar el movimiento
        try:
            if origen == 0:  # Desde la barra
                # Primero colocar, luego remover de barra
                self.__board__.colocar_ficha(destino, self.__current_player__, 1)
                self.__bar_manager__.remove_piece_from_bar(self.__current_player__)
            else:  # Movimiento normal
                self.__board__.mover_ficha(origen, destino, self.__current_player__)
            
            # Remover el dado usado
            self.__available_moves__.remove(dado_usado)
            
            # Actualizar estado
            remaining_moves = len(self.__available_moves__)
            
            if remaining_moves == 0:
                self.__end_turn()
            else:
                # Verificar si quedan movimientos válidos
                has_valid_moves = (
                    self.__movement_validator__.has_any_valid_move(
                        self.__current_player__, self.__available_moves__) or
                    self.__has_valid_bearing_off_moves()
                )
                
                if not has_valid_moves:
                    self.__message__ = "Sin movimientos válidos. Presiona 'R'."
                    self.__game_state_manager__.change_state('AWAITING_SKIP_CONFIRMATION')
                elif capture_occurred:
                    dice_str = ', '.join(map(str, self.__available_moves__))
                    self.__message__ = f"¡Captura! Dados: [{dice_str}]. Elige ficha."
                else:
                    self.__message__ = self.__message_manager__.get_move_completed_message(
                        remaining_moves, self.__available_moves__)
                        
        except Exception as e:
            # Si algo falla, restaurar estado
            if capture_occurred and captured_color:
                self.__bar_manager__.remove_piece_from_bar(captured_color)
                try:
                    self.__board__.colocar_ficha(destino, captured_color, 1)
                except:
                    pass
            
            self.__message__ = "Error al ejecutar movimiento."


    def __end_turn(self) -> None:
        """
        Termina el turno actual y prepara el siguiente.
        
        Principios SOLID:
            - SRP: Solo gestiona transición de turnos, limpia estado.
            - DIP: Usa GameStateManager para cambiar estados.
        """
        self.__switch_player()
        self.__game_state_manager__.change_state('AWAITING_ROLL')
        self.__dice_rolls__ = []
        self.__available_moves__ = []
        self.__is_doubles_roll__ = False
        self.__selected_point__ = None  # Limpiar selección al cambiar turno
        self.__message__ = self.__message_manager__.get_awaiting_roll_message(
            self.__current_player__)

    def __switch_player(self) -> None:
        """
        Cambia al siguiente jugador.
        
        Principios SOLID:
            - SRP: Su única responsabilidad es alternar jugadores.
            - ISP: Método mínimo y específico.
        """
        self.__current_player__ = "blanco" if self.__current_player__ == "negro" else "negro"

    def __roll_to_start(self) -> None:
        """
        Realiza la tirada inicial para determinar quién comienza.
        
        Principios SOLID:
            - SRP: Gestiona solo la lógica de tirada inicial.
            - DIP: Usa Dice y MessageManager sin implementar reglas internas.
        """
        self.__dice__.tirar()
        roll1 = self.__dice__.obtener_dado1()
        roll2 = self.__dice__.obtener_dado2()
        while roll1 == roll2:
            self.__dice__.tirar()
            roll1 = self.__dice__.obtener_dado1()
            roll2 = self.__dice__.obtener_dado2()
        self.__dice_rolls__ = [roll1, roll2]
        if roll1 > roll2:
            self.__current_player__ = "negro"
            self.__message__ = self.__message_manager__.get_roll_winner_message(
                "negro", roll1, roll2)
        else:
            self.__current_player__ = "blanco"
            self.__message__ = self.__message_manager__.get_roll_winner_message(
                "blanco", roll2, roll1)
        self.__game_state_manager__.change_state('AWAITING_ROLL')

    def __roll_player_dice(self) -> None:
        """
        El jugador tira los dados en su turno.
        
        Principios SOLID:
            - SRP: Coordina tirada, cálculo de movimientos y validación de disponibilidad.
            - DIP: Depende de Dice, DiceMovesCalculator y MovementValidator.
            - OCP: Dobles son manejados sin modificar flujo normal.
        """
        self.__dice__.tirar()
        dado1 = self.__dice__.obtener_dado1()
        dado2 = self.__dice__.obtener_dado2()
        self.__dice_rolls__ = [dado1, dado2]
        self.__available_moves__ = self.__dice_calculator__.calculate_available_moves(dado1, dado2)
        self.__is_doubles_roll__ = self.__dice_calculator__.is_doubles_roll(dado1, dado2)
        
        # Verificar si el jugador tiene movimientos disponibles
        if not self.__movement_validator__.has_any_valid_move(
                self.__current_player__, self.__available_moves__):
            if self.__bar_manager__.has_pieces_on_bar(self.__current_player__):
                self.__message__ = f"{self.__current_player__.capitalize()}: No puedes entrar desde la barra. Presiona 'R' para saltar turno."
            else:
                self.__message__ = f"{self.__current_player__.capitalize()}: Todas tus fichas están bloqueadas. Presiona 'R' para saltar turno."
            self.__game_state_manager__.change_state('AWAITING_SKIP_CONFIRMATION')
            return
        
        # Si hay movimientos disponibles, continuar normalmente
        self.__game_state_manager__.change_state('AWAITING_PIECE_SELECTION')
        if self.__is_doubles_roll__:
            self.__message__ = self.__message_manager__.get_doubles_roll_message(
                self.__current_player__, dado1, self.__available_moves__)
        else:
            self.__message__ = self.__message_manager__.get_normal_roll_message(
                self.__current_player__, self.__available_moves__)

    def __validate_and_report_move(self, origen: int, destino: int) -> bool:
        """
        Valida un movimiento completo y reporta errores al usuario.
        
        Principios SOLID:
            - SRP: Solo valida movimientos, no los ejecuta.
            - DIP: Usa BarManager, Board y CaptureValidator para validar.
            - ISP: Llama solo a métodos de validación necesarios.
        """
        # Verificar si debe mover desde la barra primero
        if (origen != 0 and BarMovementRules.must_enter_from_bar_first(
                self.__bar_manager__, self.__current_player__)):
            self.__message__ = "Debes mover primero desde la barra."
            return False
        
        # Movimiento desde la barra
        if origen == 0:
            if not self.__bar_manager__.has_pieces_on_bar(self.__current_player__):
                self.__message__ = "No tienes fichas en la barra."
                return False
            
            dado_necesario = (destino if self.__current_player__ == "negro" else 25 - destino)
            if dado_necesario not in self.__available_moves__:
                self.__message__ = f"No tienes dado {dado_necesario}. Disponibles: {self.__available_moves__}"
                return False
            
            destination_state = self.__board__.obtener_estado_punto(destino)
            if self.__capture_validator__.is_move_blocked(destination_state,
                                                        self.__current_player__):
                self.__message__ = f"Punto {destino} bloqueado (2+ fichas rivales)."
                return False
            return True
        
        # VALIDACIÓN CRÍTICA: Verificar dirección correcta
        if not self.__is_valid_direction(origen, destino):
            self.__message__ = "Dirección incorrecta. Negro va hacia arriba, Blanco hacia abajo."
            return False
        
        # Calcular dado necesario
        dado_necesario = self.__calculate_dice_needed(origen, destino)
        if dado_necesario not in self.__available_moves__:
            self.__message__ = f"No tienes dado {dado_necesario}. Disponibles: {self.__available_moves__}"
            return False
        
        # Verificar si el destino está bloqueado
        destination_state = self.__board__.obtener_estado_punto(destino)
        if self.__capture_validator__.is_move_blocked(destination_state, self.__current_player__):
            self.__message__ = f"Punto {destino} bloqueado (2+ fichas rivales)."
            return False
        
        return True

    def __calculate_dice_needed(self, origen: int, destino: int) -> int:
        """
        Calcula qué dado se necesita para un movimiento.
        
        Principios SOLID:
            - SRP: Cálculo puro sin efectos secundarios.
            - ISP: Método pequeño y específico.
        """
        if origen == 0:
            return destino if self.__current_player__ == "negro" else 25 - destino
        return abs(origen - destino)

    def __is_valid_direction(self, origen: int, destino: int) -> bool:
        """
        Verifica si el movimiento va en la dirección correcta para el jugador.
        
        Principios SOLID:
            - SRP: Solo verifica dirección, no otras validaciones.
            - ISP: Método específico y reutilizable.
        """
        if self.__current_player__ == "negro":
            return destino > origen
        return destino < origen

    def __get_point_from_mouse_pos(self, mouse_pos: Tuple[int, int]) -> Optional[int]:
        """
        Calcula en qué punto del tablero se hizo click.
        
        Principios SOLID:
            - SRP: Solo traduce coordenadas de pantalla a puntos lógicos.
            - OCP: Zonas de bearing off son extensiones sin modificar cálculos base.
            - ISP: Retorna información mínima (número de punto).
        """
        mx, my = mouse_pos
        side_width = (self.__board_width__ - self.__bar_width__) // 2
        point_width = side_width // 6
        bar_x_start = self.__board_margin__ + side_width
        bar_x_end = bar_x_start + self.__bar_width__
        
        # Verificar que el click esté dentro del área del tablero
        if not (self.__board_margin__ <= mx <= self.__board_margin__ + self.__board_width__ and
                self.__board_margin__ <= my <= self.__board_margin__ + self.__board_height__):
            return None
        
        # Click en la barra
        if (bar_x_start <= mx <= bar_x_end):
            return 0
        
        # Mitad superior del tablero
        if self.__board_margin__ < my < self.__board_margin__ + self.__board_height__ // 2:
            # Cuadrante superior derecho (puntos 1-6)
            start_x_top_right = self.__board_margin__ + side_width + self.__bar_width__
            if start_x_top_right < mx < self.__board_margin__ + self.__board_width__:
                point_idx = (self.__board_margin__ + self.__board_width__ - mx) // point_width
                if 0 <= point_idx < 6:
                    return point_idx + 1
            
            # Cuadrante superior izquierdo (puntos 7-12)
            start_x_top_left = self.__board_margin__
            if start_x_top_left < mx < self.__board_margin__ + side_width:
                # Detectar bearing off blanco
                if (self.__current_player__ == "blanco" and 
                    self.__bearing_off_validator__.can_bear_off(self.__current_player__) and
                    self.__game_state_manager__.get_current_state() == 'AWAITING_PIECE_SELECTION'):
                    return 0  # Bearing off blanco
                
                point_idx = (mx - start_x_top_left) // point_width
                if 0 <= point_idx < 6:
                    return 12 - point_idx
        
        # Mitad inferior del tablero
        elif (self.__board_margin__ + self.__board_height__ // 2 < my, self.__board_margin__ + self.__board_height__): 
            
            # Cuadrante inferior izquierdo (puntos 13-18)
            start_x_bottom_left = self.__board_margin__
            if start_x_bottom_left < mx < self.__board_margin__ + side_width:
                # Detectar bearing off negro
                if (self.__current_player__ == "negro" and 
                    self.__bearing_off_validator__.can_bear_off(self.__current_player__) and
                    self.__game_state_manager__.get_current_state() == 'AWAITING_PIECE_SELECTION'):
                    return 25  # Bearing off negro
                
                point_idx = (mx - start_x_bottom_left) // point_width
                if 0 <= point_idx < 6:
                    return 13 + point_idx
            
            # Cuadrante inferior derecho (puntos 19-24)
            start_x_bottom_right = self.__board_margin__ + side_width + self.__bar_width__
            if start_x_bottom_right < mx < self.__board_margin__ + self.__board_width__:
                point_idx = (self.__board_margin__ + self.__board_width__ - mx) // point_width
                if 0 <= point_idx < 6:
                    return 24 - point_idx
        
        return None

    def __update(self) -> None:
        """
        Actualiza la lógica del juego cada frame.
        
        Principios SOLID:
            - SRP: Placeholder para actualizaciones futuras.
            - OCP: Puede extenderse con animaciones sin modificar estructura.
        """
        pass

    def __draw_bar_pieces(self) -> None:
        """
        Dibuja las fichas capturadas en la barra central.
        
        Principios SOLID:
            - SRP: Solo renderiza fichas de la barra.
            - DIP: Usa BarManager para obtener estado sin implementar lógica.
        """
        bar_x = self.__board_margin__ + (self.__board_width__ // 2) - (self.__bar_width__ // 2)
        bar_center_x = bar_x + (self.__bar_width__ // 2)
        checker_radius = 20
        negro_count = self.__bar_manager__.get_pieces_count("negro")
        if negro_count > 0:
            start_y = self.__board_margin__ + 50
            for i in range(min(negro_count, 8)):
                ficha_y = start_y + (i * checker_radius * 1.5)
                pygame.draw.circle(self.__screen__, self.__checker_black__,
                                 (bar_center_x, int(ficha_y)), checker_radius)
                pygame.draw.circle(self.__screen__, self.__checker_border__,
                                 (bar_center_x, int(ficha_y)), checker_radius, 2)
            if negro_count > 8:
                font_small = pygame.font.Font(None, 20)
                count_text = font_small.render(str(negro_count), True, self.__white__)
                text_rect = count_text.get_rect(center=(bar_center_x, start_y + 200))
                self.__screen__.blit(count_text, text_rect)
        blanco_count = self.__bar_manager__.get_pieces_count("blanco")
        if blanco_count > 0:
            start_y = self.__board_margin__ + self.__board_height__ - 50
            for i in range(min(blanco_count, 8)):
                ficha_y = start_y - (i * checker_radius * 1.5)
                pygame.draw.circle(self.__screen__, self.__checker_white__,
                                 (bar_center_x, int(ficha_y)), checker_radius)
                pygame.draw.circle(self.__screen__, self.__checker_border__,
                                 (bar_center_x, int(ficha_y)), checker_radius, 2)
            if blanco_count > 8:
                font_small = pygame.font.Font(None, 20)
                count_text = font_small.render(str(blanco_count), True, self.__black__)
                text_rect = count_text.get_rect(center=(bar_center_x, start_y - 200))
                self.__screen__.blit(count_text, text_rect)

    def __draw_home_pieces(self) -> None:
        """
        Dibuja el contador de fichas que han salido del tablero (casa).
        
        Principios SOLID:
            - SRP: Renderiza solo información de fichas en casa.
            - DIP: Usa HomeManager sin conocer detalles internos.
        """
        font_small = pygame.font.Font(None, 30)
    
        # Fichas negras en casa (ABAJO a la izquierda, cerca de su zona de bearing off)
        negro_count = self.__home_manager__.get_pieces_count("negro")
        if negro_count > 0:
            text = f"Casa Negro: {negro_count}/15"
            color = self.__white__ if negro_count < 15 else (0, 255, 0)
            text_surface = font_small.render(text, True, color)
            x = 50  # Esquina izquierda
            y = self.__screen__.get_height() - 80  # Abajo
            self.__screen__.blit(text_surface, (x, y))
        
        # Fichas blancas en casa (ARRIBA a la izquierda, cerca de su zona de bearing off)
        blanco_count = self.__home_manager__.get_pieces_count("blanco")
        if blanco_count > 0:
            text = f"Casa Blanco: {blanco_count}/15"
            color = self.__white__ if blanco_count < 15 else (0, 255, 0)
            text_surface = font_small.render(text, True, color)
            x = 50  # Esquina izquierda
            y = 30  # Arriba
            self.__screen__.blit(text_surface, (x, y))
        
    def __draw_bearing_off_zones(self) -> None:
        """
        Dibuja las zonas visuales de bearing off cuando están activas.
        
        Principios SOLID:
            - SRP: Renderiza solo zonas de bearing off con efectos visuales.
            - OCP: Extensión visual que no modifica renderizado base.
            - DIP: Usa BearingOffValidator para determinar visibilidad.
        """
        # Solo mostrar si el jugador actual PUEDE hacer bearing off
        if not self.__bearing_off_validator__.can_bear_off(self.__current_player__):
            return
        
        # Solo mostrar en estado de selección
        if self.__game_state_manager__.get_current_state() != 'AWAITING_PIECE_SELECTION':
            return
        
        # Configuración de dimensiones
        side_width = (self.__board_width__ - self.__bar_width__) // 2
        point_width = side_width // 6
        
        # Efecto pulsante para llamar la atención
        import math
        import time
        pulse = int(40 * abs(math.sin(time.time() * 2.5)))
        
        font_large = pygame.font.Font(None, 50)
        font_small = pygame.font.Font(None, 30)
        
        if self.__current_player__ == "negro":
            # Casa Negro: cuadrante 13-18 (inferior izquierdo)
            # Dibujar rectángulo horizontal que cubre los 6 puntos
            start_x = self.__board_margin__
            start_y = self.__board_margin__ + (self.__board_height__ // 2) + 10
            zone_width = side_width
            zone_height = (self.__board_height__ // 2) - 20
            
            zone_rect = pygame.Rect(start_x, start_y, zone_width, zone_height)
            
            # Color base marrón oscuro con efecto pulsante
            base_color = (101, 67, 33)
            highlight_color = (101 + pulse, 67 + pulse, 33 + pulse)
            
            # Dibujar fondo
            pygame.draw.rect(self.__screen__, highlight_color, zone_rect, border_radius=15)
            
            # Borde verde brillante pulsante
            border_color = (0, 200 + (pulse // 2), 0)
            pygame.draw.rect(self.__screen__, border_color, zone_rect, 6, border_radius=15)
            
            # Textos centrados
            text1 = font_large.render("🏠 CASA NEGRO", True, (255, 255, 255))
            text2 = font_small.render("Click aquí para sacar fichas", True, (200, 255, 200))
            
            # Cantidad de fichas en casa
            home_count = self.__home_manager__.get_pieces_count("negro")
            text3 = font_small.render(f"Fichas en casa: {home_count}/15", True, (255, 215, 0))
            
            # Centrar textos verticalmente
            center_y = zone_rect.centery
            self.__screen__.blit(text1, (zone_rect.centerx - text1.get_width() // 2, 
                                        center_y - 60))
            self.__screen__.blit(text2, (zone_rect.centerx - text2.get_width() // 2, 
                                        center_y - 10))
            self.__screen__.blit(text3, (zone_rect.centerx - text3.get_width() // 2, 
                                        center_y + 30))
            
        else:  # blanco
            # Casa Blanco: cuadrante 7-12 (superior izquierdo)
            start_x = self.__board_margin__
            start_y = self.__board_margin__ + 10
            zone_width = side_width
            zone_height = (self.__board_height__ // 2) - 20
            
            zone_rect = pygame.Rect(start_x, start_y, zone_width, zone_height)
            
            # Color base marrón oscuro con efecto pulsante
            base_color = (101, 67, 33)
            highlight_color = (101 + pulse, 67 + pulse, 33 + pulse)
            
            # Dibujar fondo
            pygame.draw.rect(self.__screen__, highlight_color, zone_rect, border_radius=15)
            
            # Borde verde brillante pulsante
            border_color = (0, 200 + (pulse // 2), 0)
            pygame.draw.rect(self.__screen__, border_color, zone_rect, 6, border_radius=15)
            
            # Textos centrados
            text1 = font_large.render("🏠 CASA BLANCO", True, (255, 255, 255))
            text2 = font_small.render("Click aquí para sacar fichas", True, (200, 255, 200))
            
            # Cantidad de fichas en casa
            home_count = self.__home_manager__.get_pieces_count("blanco")
            text3 = font_small.render(f"Fichas en casa: {home_count}/15", True, (255, 215, 0))
            
            # Centrar textos verticalmente
            center_y = zone_rect.centery
            self.__screen__.blit(text1, (zone_rect.centerx - text1.get_width() // 2, 
                                        center_y - 60))
            self.__screen__.blit(text2, (zone_rect.centerx - text2.get_width() // 2, 
                                        center_y - 10))
            self.__screen__.blit(text3, (zone_rect.centerx - text3.get_width() // 2, 
                                        center_y + 30))
            
    def __draw(self) -> None:
        """
        Dibuja todos los elementos visuales del juego.
        
        Principios SOLID:
            - SRP: Coordina renderizado, delega cada elemento a métodos especializados.
            - OCP: Nuevos elementos visuales pueden agregarse sin modificar existentes.
            - ISP: Llama solo a métodos de dibujo necesarios.
        """
        self.__screen__.fill((139, 69, 19))
        
            # Primero dibujar tablero
        self.__draw_backgammon_board()
        
        # DESPUÉS dibujar bearing off zones (para que queden ENCIMA)
        self.__draw_bearing_off_zones()
        
        # Luego el resto
        self.__draw_checkers()
        self.__draw_bar_pieces()
        self.__draw_home_pieces()  
        self.__draw_message()
        if self.__dice_rolls__:
            self.__draw_dice()
        self.__draw_available_moves()
        pygame.display.flip()

    def __draw_available_moves(self) -> None:
        """
        Dibuja los movimientos disponibles en pantalla.
        
        Principios SOLID:
            - SRP: Solo renderiza información de dados disponibles.
            - ISP: Método específico de visualización de estado.
        """
        if not self.__available_moves__:
            return
        font_small = pygame.font.Font(None, 35)
        
        # Mensaje compacto
        if self.__is_doubles_roll__:
            moves_text = f"¡DOBLES! Tienes {len(self.__available_moves__)} movimientos"
            text_color = self.__doubles_highlight__
        else:
            moves_text = f"Dados disponibles: {', '.join(map(str, self.__available_moves__))}"
            text_color = self.__white__
        
        text_surface = font_small.render(moves_text, True, text_color)
        text_rect = text_surface.get_rect()
        # Posicionar en la parte inferior
        text_rect.center = (self.__screen__.get_width() // 2, 
                        self.__screen__.get_height() - 30)
        self.__screen__.blit(text_surface, text_rect)

    def __draw_message(self) -> None:
        """
        Renderiza el mensaje de estado del juego.
        
        Principios SOLID:
            - SRP: Solo renderiza mensajes, no genera contenido.
            - ISP: Método específico de renderizado de texto.
        """
        # Determinar color del texto
        current_state = self.__game_state_manager__.get_current_state()
        
        if current_state == 'AWAITING_SKIP_CONFIRMATION':
            # Rojo para indicar que no puede mover
            text_color = (255, 100, 100)
        elif self.__is_doubles_roll__ and "DOBLES" in self.__message__:
            text_color = self.__doubles_highlight__
        else:
            text_color = self.__white__
        
        text_surface = self.__font__.render(self.__message__, True, text_color)
        text_rect = text_surface.get_rect(center=(self.__screen__.get_width() // 2, 30))
        self.__screen__.blit(text_surface, text_rect)

            
    def __draw_dice(self) -> None:
        """
        Dibuja los dos dados con sus valores actuales.
        
        Principios SOLID:
            - SRP: Coordina renderizado de dados, delega pips a método específico.
            - OCP: Efectos visuales (dobles) son extensiones.
        """
        dice_size = 80
        margin = 20
        x1 = (self.__board_margin__ + (self.__board_width__ / 2) -
              self.__bar_width__ - dice_size - margin)
        x2 = self.__board_margin__ + (self.__board_width__ / 2) + self.__bar_width__ + margin
        y_pos = (self.__screen__.get_height() / 2) - (dice_size / 2)
        dice_rect1 = pygame.Rect(x1, y_pos, dice_size, dice_size)
        dice_rect2 = pygame.Rect(x2, y_pos, dice_size, dice_size)
        pygame.draw.rect(self.__screen__, self.__dice_color__, dice_rect1, border_radius=10)
        pygame.draw.rect(self.__screen__, self.__dice_color__, dice_rect2, border_radius=10)
        if self.__is_doubles_roll__:
            pygame.draw.rect(self.__screen__, self.__doubles_highlight__, dice_rect1, 5,
                           border_radius=10)
            pygame.draw.rect(self.__screen__, self.__doubles_highlight__, dice_rect2, 5,
                           border_radius=10)
        self.__draw_pips(dice_rect1, self.__dice_rolls__[0])
        self.__draw_pips(dice_rect2, self.__dice_rolls__[1])

    def __draw_pips(self, rect: pygame.Rect, number: int) -> None:
        """
        Dibuja los puntos (pips) en la cara de un dado.
        
        Principios SOLID:
            - SRP: Renderiza solo los pips de un valor específico.
            - ISP: Método mínimo y reutilizable.
        """
        pip_radius = 8
        margin = 20
        positions = {
            1: [rect.center],
            2: [(rect.left + margin, rect.top + margin),
                (rect.right - margin, rect.bottom - margin)],
            3: [(rect.left + margin, rect.top + margin), rect.center,
                (rect.right - margin, rect.bottom - margin)],
            4: [(rect.left + margin, rect.top + margin), (rect.right - margin, rect.top + margin),
                (rect.left + margin, rect.bottom - margin),
                (rect.right - margin, rect.bottom - margin)],
            5: [(rect.left + margin, rect.top + margin), (rect.right - margin, rect.top + margin),
                rect.center, (rect.left + margin, rect.bottom - margin),
                (rect.right - margin, rect.bottom - margin)],
            6: [(rect.left + margin, rect.top + margin), (rect.right - margin, rect.top + margin),
                (rect.left + margin, rect.centery), (rect.right - margin, rect.centery),
                (rect.left + margin, rect.bottom - margin),
                (rect.right - margin, rect.bottom - margin)]
        }
        if number in positions:
            for pos in positions[number]:
                pygame.draw.circle(self.__screen__, self.__pip_color__, pos, pip_radius)

    def __draw_backgammon_board(self) -> None:
        """
        Dibuja el tablero principal de Backgammon.
        
        Principios SOLID:
            - SRP: Solo dibuja la estructura base del tablero.
            - ISP: Método específico de renderizado de tablero.
        """
        board_rect = pygame.Rect(self.__board_margin__, self.__board_margin__, self.__board_width__, self.__board_height__)
        pygame.draw.rect(self.__screen__, self.__brown_light__, board_rect)
        pygame.draw.rect(self.__screen__, self.__board_border__, board_rect, 5)
        
        bar_x = self.__board_margin__ + (self.__board_width__ // 2) - (self.__bar_width__ // 2)
        bar_rect = pygame.Rect(bar_x, self.__board_margin__, self.__bar_width__, self.__board_height__)
        pygame.draw.rect(self.__screen__, self.__bar_color__, bar_rect)
        pygame.draw.rect(self.__screen__, self.__black__, bar_rect, 3)
        
        self.__draw_points()
        
    def __draw_points(self) -> None:
        """
        Dibuja los 24 puntos triangulares del tablero.
        
        Principios SOLID:
            - SRP: Renderiza solo los puntos, no fichas ni otros elementos.
            - ISP: Método enfocado en una tarea visual específica.
        """
        side_width = (self.__board_width__ - self.__bar_width__) // 2
        point_width = side_width // 6
        point_height = 320
        
        # Cuadrante superior derecho (puntos 1-6)
        start_x_top_right = self.__board_margin__ + side_width + self.__bar_width__
        for i in range(6):
            x = start_x_top_right + ((5 - i) * point_width) 
            y = self.__board_margin__
            color = self.__brown_light__ if i % 2 == 0 else self.__brown_dark__
            self.__draw_triangle_point(x, y, point_width, point_height, color, pointing_down=True)
            
        # Cuadrante superior izquierdo (puntos 7-12)
        start_x_top_left = self.__board_margin__
        for i in range(6):
            x = start_x_top_left + i * point_width
            y = self.__board_margin__
            color = self.__brown_light__ if i % 2 == 0 else self.__brown_dark__
            self.__draw_triangle_point(x, y, point_width, point_height, color, pointing_down=True)
            
        # Cuadrante inferior izquierdo (puntos 13-18)
        for i in range(6):
            x = start_x_top_left + i * point_width
            y = self.__board_margin__ + self.__board_height__ - point_height
            color = self.__brown_dark__ if i % 2 == 0 else self.__brown_light__
            self.__draw_triangle_point(x, y, point_width, point_height, color, pointing_down=False)
            
        # Cuadrante inferior derecho (puntos 19-24)
        for i in range(6):
            x = start_x_top_right + ((5 - i) * point_width)
            y = self.__board_margin__ + self.__board_height__ - point_height
            color = self.__brown_dark__ if i % 2 == 0 else self.__brown_light__
            self.__draw_triangle_point(x, y, point_width, point_height, color, pointing_down=False)

    def __draw_triangle_point(self, x: int, y: int, width: int, height: int, 
                            color: Tuple[int, int, int], pointing_down: bool = True) -> None:
        """
        Dibuja un único punto triangular.
        
        Principios SOLID:
            - SRP: Renderiza un solo triángulo con parámetros dados.
            - OCP: Puede reutilizarse para distintos estilos sin modificación.
            - ISP: Interfaz mínima con parámetros esenciales.
        """
        if pointing_down:
            points = [(x + width // 2, y + height), (x, y), (x + width, y)]
        else:
            points = [(x + width // 2, y), (x, y + height), (x + width, y + height)]
        pygame.draw.polygon(self.__screen__, color, points)
        pygame.draw.polygon(self.__screen__, self.__black__, points, 2)
    
    def __draw_checkers(self) -> None:
        """
        Dibuja todas las fichas en el tablero.
        
        Principios SOLID:
            - SRP: Coordina dibujo de fichas, delega pilas a método especializado.
            - DIP: Usa Board para obtener estado sin conocer implementación interna.
        """
        checker_radius = 25
        for point_num in range(1, 25):
            point_data = self.__board__.obtener_estado_punto(point_num)
            if point_data:
                color, cantidad = point_data
                point_x, point_y = self.__get_point_screen_position(point_num)
                self.__draw_checker_stack(point_x, point_y, color, cantidad, point_num, checker_radius)
    
    def __get_point_screen_position(self, point_num: int) -> Tuple[int, int]:
        """
        Calcula la posición en pantalla de un punto lógico.
        
        Principios SOLID:
            - SRP: Solo traduce puntos lógicos a coordenadas visuales.
            - ISP: Retorna información mínima necesaria.
        """
        side_width = (self.__board_width__ - self.__bar_width__) // 2
        point_width = side_width // 6
        checker_radius = 25

        if 1 <= point_num <= 6:
            start_x = self.__board_margin__ + side_width + self.__bar_width__
            x = start_x + ((6 - point_num) * point_width) + (point_width // 2)
            y = self.__board_margin__ + checker_radius
        elif 7 <= point_num <= 12:
            start_x = self.__board_margin__
            x = start_x + ((12 - point_num) * point_width) + (point_width // 2)
            y = self.__board_margin__ + checker_radius
        elif 13 <= point_num <= 18:
            start_x = self.__board_margin__
            x = start_x + ((point_num - 13) * point_width) + (point_width // 2)
            y = self.__board_margin__ + self.__board_height__ - checker_radius
        else:
            start_x = self.__board_margin__ + side_width + self.__bar_width__
            x = start_x + ((point_num - 19) * point_width) + (point_width // 2)
            y = self.__board_margin__ + self.__board_height__ - checker_radius
        return x, y

    def __draw_checker_stack(self, x: int, y: int, color: str, cantidad: int, 
                           point_num: int, radius: int) -> None:
        """
        Dibuja una pila de fichas en una posición específica.
        
        Principios SOLID:
            - SRP: Renderiza una pila completa de fichas.
            - ISP: Parámetros específicos sin exceso de información.
        """
        checker_color = self.__checker_white__ if color == "blanco" else self.__checker_black__
        going_down = 1 <= point_num <= 12
        
        for i in range(min(cantidad, 10)):
            if going_down:
                ficha_y = y + i * (radius * 1.2)
            else:
                ficha_y = y - i * (radius * 1.2)
            pygame.draw.circle(self.__screen__, checker_color, (x, int(ficha_y)), radius)
            pygame.draw.circle(self.__screen__, self.__checker_border__, (x, int(ficha_y)), radius, 2)


if __name__ == "__main__":
    game = PygameUI()
    game.run()