import os
import sys
from typing import Tuple, Optional, List
import pygame

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Backgammon.Core.Board import Board  # pylint: disable=wrong-import-position
from Backgammon.Core.Dice import Dice  # pylint: disable=wrong-import-position


class DiceMovesCalculator:
    """Calcula movimientos disponibles basados en los dados."""

    @staticmethod
    def calculate_available_moves(dice_roll1: int, dice_roll2: int) -> List[int]:
        """Calcula los movimientos disponibles."""
        if dice_roll1 == dice_roll2:
            return [dice_roll1] * 4
        return [dice_roll1, dice_roll2]

    @staticmethod
    def is_doubles_roll(dice_roll1: int, dice_roll2: int) -> bool:
        """Determina si la tirada es dobles."""
        return dice_roll1 == dice_roll2


class GameStateManager:
    """Gestiona los estados del juego."""

    def __init__(self):
        self.current_state = 'START_ROLL'
        self.valid_states = {'START_ROLL', 'AWAITING_ROLL', 'AWAITING_PIECE_SELECTION', 'AWAITING_SKIP_CONFIRMATION'}

    def change_state(self, new_state: str) -> None:
        """Cambia el estado del juego con validación."""
        if new_state in self.valid_states:
            self.current_state = new_state
        else:
            raise ValueError(f"Estado inválido: {new_state}")

    def get_current_state(self) -> str:
        """Obtiene el estado actual."""
        return self.current_state


class MessageManager:
    """Genera mensajes apropiados para el estado del juego."""

    @staticmethod
    def get_start_message() -> str:
        """Mensaje para el inicio del juego."""
        return "Presiona 'R' para decidir quién empieza."

    @staticmethod
    def get_roll_winner_message(winner: str, winner_roll: int, loser_roll: int) -> str:
        """Mensaje cuando alguien gana la tirada inicial."""
        winner_display = winner.capitalize()
        loser_display = "Blanco" if winner == "negro" else "Negro"
        return (f"{winner_display} ({winner_roll}) gana a {loser_display} "
                f"({loser_roll}). Presiona 'R' para tirar tus dados.")

    @staticmethod
    def get_awaiting_roll_message(current_player: str) -> str:
        """Mensaje cuando el jugador debe tirar dados."""
        return f"Turno de {current_player}. Presiona 'R' para tirar los dados."

    @staticmethod
    def get_doubles_roll_message(current_player: str, dice_value: int,
                                available_moves: List[int]) -> str:
        """Mensaje cuando se sacan dobles."""
        moves_count = len(available_moves)
        return f"{current_player.capitalize()} sacó dobles de {dice_value}! Tienes {moves_count} movimientos de {dice_value}. Elige ficha."

    @staticmethod
    def get_normal_roll_message(current_player: str, available_moves: List[int]) -> str:
        """Mensaje para tirada normal."""
        dice_str = ', '.join(map(str, available_moves))
        return f"Turno de {current_player}. Dados: [{dice_str}]. Elige una ficha para mover."

    @staticmethod
    def get_piece_selected_message(point: int, available_moves: List[int]) -> str:
        """Mensaje cuando se selecciona una ficha."""
        dice_str = ', '.join(map(str, available_moves))
        return f"Ficha en punto {point} seleccionada. Dados disponibles: [{dice_str}]. Elige destino."

    @staticmethod
    def get_move_completed_message(remaining_moves: int, available_moves: List[int]) -> str:
        """Mensaje cuando se completa un movimiento."""
        if remaining_moves == 0:
            return "Turno completado."
        dice_str = ', '.join(map(str, available_moves))
        return f"Movimiento realizado. Te quedan {remaining_moves} dados: [{dice_str}]. Elige ficha."

    @staticmethod
    def get_invalid_piece_message(point: int) -> str:
        """Mensaje cuando se selecciona una ficha inválida."""
        return f"No tienes fichas en el punto {point}. Elige una válida."

    @staticmethod
    def get_invalid_move_message() -> str:
        """Mensaje para movimiento inválido."""
        return "Movimiento inválido. Vuelve a elegir una ficha."

    @staticmethod
    def get_invalid_direction_message() -> str:
        """Mensaje para dirección incorrecta."""
        return "Movimiento inválido (dirección incorrecta)."

    @staticmethod
    def get_dice_not_available_message(dice_needed: int, available_moves: List[int]) -> str:
        """Mensaje cuando no se tiene el dado necesario."""
        return f"No tienes el dado {dice_needed} disponible. Dados: {available_moves}."

    @staticmethod
    def get_blocked_move_message(origin: int, destination: int) -> str:
        """Mensaje para movimiento bloqueado."""
        return f"Movimiento de {origin} a {destination} bloqueado o inválido."
    
    @staticmethod
    def get_no_moves_available_message(player: str, reason: str) -> str:
        """Mensaje cuando no hay movimientos disponibles."""
        return f"¡{player.capitalize()} no puede mover! {reason} Presiona 'R' para continuar."
    
    @staticmethod
    def get_bearing_off_available_message(player: str, home_count: int) -> str:
        """Mensaje cuando puede hacer bearing off."""
        return f"{player.capitalize()}: Puedes sacar fichas ({home_count}/15). Click fuera del tablero."

    @staticmethod
    def get_cannot_bear_off_message() -> str:
        """Mensaje cuando intenta bearing off pero no puede."""
        return "No puedes sacar. Tienes fichas fuera del cuadrante casa."

    @staticmethod
    def get_bearing_off_success_message(player: str, home_count: int, remaining_moves: int) -> str:
        """Mensaje cuando saca una ficha exitosamente."""
        if remaining_moves > 0:
            return f"¡Ficha sacada! ({home_count}/15) Te quedan {remaining_moves} dados."
        return f"Ficha sacada ({home_count}/15). Turno completado."

    @staticmethod
    def get_victory_message(player: str) -> str:
        """Mensaje de victoria."""
        return f"🎉 ¡{player.upper()} GANA EL JUEGO! 🎉"

class MovementValidator:
    """Valida si un jugador tiene movimientos disponibles."""

    def __init__(self, board, bar_manager):
        self.board = board
        self.bar_manager = bar_manager

    def has_any_valid_move(self, player: str, available_moves: list) -> bool:
        """Verifica si el jugador tiene algún movimiento válido disponible."""
        # Primero verificar si debe mover desde la barra
        if self.bar_manager.has_pieces_on_bar(player):
            return self._can_enter_from_bar(player, available_moves)
        
        # Si no hay fichas en la barra, verificar movimientos desde el tablero
        return self._can_move_from_board(player, available_moves)
    

    def _can_enter_from_bar(self, player: str, available_moves: list) -> bool:
        """Verifica si el jugador puede entrar desde la barra con alguno de los dados."""
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
        """Verifica si el jugador puede mover alguna ficha del tablero."""
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
        """Verifica si un destino específico es accesible para el jugador."""
        destination_state = self.board.obtener_estado_punto(destination)
        
        if destination_state is None:
            return True
        
        dest_color, dest_count = destination_state
        
        # Accesible si: tiene fichas propias, o tiene solo 1 ficha enemiga (captura)
        return dest_color == player or dest_count == 1

    def _calculate_destination(self, player: str, origin: int, dice_value: int) -> int:
        """Calcula el punto de destino basado en el origen y el valor del dado."""
        if player == "negro":
            return origin + dice_value
        else:
            return origin - dice_value

    def _get_entry_point(self, player: str, dice_value: int) -> int:
        """Calcula el punto de entrada desde la barra."""
        if player == "negro":
            return dice_value
        else:
            return 25 - dice_value

    def get_blocked_reason(self, player: str, available_moves: list) -> str:
        """Obtiene una descripción del por qué el jugador no puede mover."""
        if self.bar_manager.has_pieces_on_bar(player):
            return ("No puedes entrar desde la barra. Todos los puntos de entrada "
                   "están bloqueados por el oponente.")
        else:
            return ("No tienes movimientos válidos. Todas tus fichas están bloqueadas "
                   "por el oponente.")


class BarManager:
    """Gestiona la lógica de la barra central."""

    def __init__(self):
        self.__bar_pieces__ = {"negro": 0, "blanco": 0}

    def add_piece_to_bar(self, color: str) -> None:
        """Agrega una ficha a la barra."""
        if color in self.__bar_pieces__:
            self.__bar_pieces__[color] += 1
        else:
            raise ValueError(f"Color inválido: {color}")

    def remove_piece_from_bar(self, color: str) -> bool:
        """Remueve una ficha de la barra."""
        if color in self.__bar_pieces__ and self.__bar_pieces__[color] > 0:
            self.__bar_pieces__[color] -= 1
            return True
        return False

    def get_pieces_count(self, color: str) -> int:
        """Obtiene el número de fichas en la barra."""
        return self.__bar_pieces__.get(color, 0)

    def has_pieces_on_bar(self, color: str) -> bool:
        """Verifica si un jugador tiene fichas en la barra."""
        return self.get_pieces_count(color) > 0

    def get_bar_state(self) -> dict:
        """Obtiene el estado completo de la barra."""
        return self.__bar_pieces__.copy()


class CaptureValidator:
    """Valida y determina capturas."""

    @staticmethod
    def can_capture_piece(destination_state: tuple, attacking_color: str) -> bool:
        """Determina si se puede capturar una ficha."""
        if destination_state is None:
            return False
        destination_color, destination_count = destination_state
        return destination_color != attacking_color and destination_count == 1

    @staticmethod
    def is_move_blocked(destination_state: tuple, attacking_color: str) -> bool:
        """Determina si un movimiento está bloqueado."""
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
    """Valida y gestiona las reglas de bearing off (sacar fichas a casa)."""

    def __init__(self, board):
        self.board = board

    def can_bear_off(self, player: str) -> bool:
        """
        Verifica si un jugador puede empezar a sacar fichas.
        Solo puede hacerlo si todas sus fichas están en su cuadrante casa.
        
        Args:
            player: Color del jugador ("negro" o "blanco")
            
        Returns:
            bool: True si puede sacar fichas
        """
        if player == "negro":
            home_quadrant = range(1, 7)  # Puntos 1-6
            other_points = range(7, 25)  # Puntos 7-24
        else:  # blanco
            home_quadrant = range(19, 25)  # Puntos 19-24
            other_points = list(range(1, 19))  # Puntos 1-18

        # Verificar que no haya fichas fuera del cuadrante casa
        for point in other_points:
            state = self.board.obtener_estado_punto(point)
            if state and state[0] == player:
                return False

        return True

    def is_bearing_off_move(self, player: str, origin: int, destination: int) -> bool:
        """
        Determina si un movimiento es un intento de bearing off.
        
        Args:
            player: Color del jugador
            origin: Punto de origen
            destination: Punto de destino
            
        Returns:
            bool: True si es intento de bearing off
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
        
        Args:
            player: Color del jugador
            origin: Punto desde donde se saca la ficha
            dice_value: Valor del dado usado
            
        Returns:
            tuple: (es_valido, mensaje_error)
        """
        # 1. Verificar que puede hacer bearing off
        if not self.can_bear_off(player):
            return False, "No puedes sacar fichas. Tienes fichas fuera del cuadrante casa."

        # 2. Verificar que la ficha está en el cuadrante casa
        if player == "negro":
            home_quadrant = range(1, 7)
            position = origin  # Para negro, la posición relativa es igual al punto
        else:
            home_quadrant = range(19, 25)
            position = 25 - origin  # Para blanco, invertir

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
        
        Args:
            player: Color del jugador
            origin: Punto de referencia
            
        Returns:
            bool: True si hay fichas en posiciones superiores
        """
        if player == "negro":
            # Para negro, posiciones superiores son números mayores (2,3,4,5,6)
            higher_points = range(origin + 1, 7)
        else:
            # Para blanco, posiciones superiores son números menores (19,20,21,22,23)
            higher_points = range(19, origin)

        for point in higher_points:
            state = self.board.obtener_estado_punto(point)
            if state and state[0] == player:
                return True

        return False

    def get_bearing_off_destination(self, player: str) -> int:
        """
        Obtiene el punto de destino ficticio para bearing off.
        Usado para calcular movimientos fuera del tablero.
        
        Args:
            player: Color del jugador
            
        Returns:
            int: Punto de destino (25 para negro, 0 para blanco)
        """
        return 25 if player == "negro" else 0


class HomeManager:
    """Gestiona las fichas que han salido del tablero (en casa)."""

    def __init__(self):
        self.__home_pieces__ = {"negro": 0, "blanco": 0}

    def add_piece_to_home(self, color: str) -> None:
        """Agrega una ficha a casa."""
        if color in self.__home_pieces__:
            self.__home_pieces__[color] += 1
        else:
            raise ValueError(f"Color inválido: {color}")

    def get_pieces_count(self, color: str) -> int:
        """Obtiene el número de fichas en casa."""
        return self.__home_pieces__.get(color, 0)

    def get_home_state(self) -> dict:
        """Obtiene el estado completo de casa."""
        return self.__home_pieces__.copy()

    def has_won(self, color: str) -> bool:
        """Verifica si un jugador ha ganado (15 fichas en casa)."""
        return self.__home_pieces__.get(color, 0) == 15

    
class PygameUI:
    """Interfaz gráfica principal del juego de Backgammon."""

    def __init__(self, board_width: int = 1600, board_height: int = 900):
        """Inicializa la interfaz gráfica."""
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
        """Inicia el bucle principal del juego."""
        while self.__running__:
            self.__handle_events()
            self.__update()
            self.__draw()
            self.__clock__.tick(60)
        pygame.quit()  # pylint: disable=no-member
        sys.exit()

    def __handle_events(self) -> None:
        """Gestiona las entradas del usuario."""
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
        """Maneja las solicitudes de tirada."""
        current_state = self.__game_state_manager__.get_current_state()
        if current_state == 'START_ROLL':
            self.__roll_to_start()
        elif current_state == 'AWAITING_ROLL':
            self.__roll_player_dice()
        elif current_state == 'AWAITING_SKIP_CONFIRMATION':
            self.__end_turn()

    def __handle_piece_selection(self, mouse_pos: Tuple[int, int]) -> None:
        """Maneja la selección de fichas."""
        clicked_point = self.__get_point_from_mouse_pos(mouse_pos)
        if clicked_point is None:
            return
        if self.__selected_point__ is None:
            self.__attempt_piece_selection(clicked_point)
        else:
            self.__execute_move(self.__selected_point__, clicked_point)
            self.__selected_point__ = None

    def __attempt_piece_selection(self, point: int) -> None:
        """Intenta seleccionar una ficha."""
        if point == 0:
            if self.__bar_manager__.has_pieces_on_bar(self.__current_player__):
                self.__selected_point__ = 0
                self.__message__ = (f"Ficha en la barra seleccionada. Dados: "
                                   f"{self.__available_moves__}. Elige punto de entrada.")
            else:
                self.__message__ = "No tienes fichas en la barra."
            return
        if BarMovementRules.must_enter_from_bar_first(self.__bar_manager__,
                                                       self.__current_player__):
            self.__message__ = ("Debes mover primero desde la barra. "
                               "Haz clic en el centro del tablero.")
            return
        estado_punto = self.__board__.obtener_estado_punto(point)
        if estado_punto and estado_punto[0] == self.__current_player__:
            self.__selected_point__ = point
            self.__message__ = self.__message_manager__.get_piece_selected_message(
                point, self.__available_moves__)
        else:
            self.__message__ = self.__message_manager__.get_invalid_piece_message(point)

    def __attempt_move(self, origen: int, destino: int) -> None:
        """Intenta realizar un movimiento - REEMPLAZAR MÉTODO COMPLETO."""
        try:
            # Verificar si es bearing off
            if hasattr(self, '__bearing_off_validator__') and \
            self.__bearing_off_validator__.is_bearing_off_move(
                    self.__current_player__, origen, destino):
                self.__attempt_bearing_off(origen, destino)
                return
            
            # Movimiento normal - validar primero
            if not self.__validate_and_report_move(origen, destino):
                # Ya hay mensaje de error en __validate_and_report_move
                return
            
            # Si la validación pasó, ejecutar movimiento
            self.__execute_move(origen, destino)
            
        except Exception as e:
            # Capturar CUALQUIER error y mostrar mensaje amigable
            error_str = str(e).lower()
            if "not in list" in error_str:
                self.__message__ = "Dado no disponible para este movimiento."
            elif "bloqueado" in error_str:
                self.__message__ = "Punto bloqueado por el rival."
            else:
                self.__message__ = "Movimiento inválido. Intenta de nuevo."


    def __attempt_bearing_off(self, origen: int, destino: int) -> None:
        """Intenta realizar un bearing off."""
        try:
            # Calcular dado necesario
            dice_needed = self.__calculate_bearing_off_dice(origen)
            
            # Verificar que el dado esté disponible
            if dice_needed not in self.__available_moves__:
                available_str = ', '.join(map(str, self.__available_moves__))
                self.__message__ = f"Necesitas dado {dice_needed}. Tienes: {available_str}"
                return
            
            # Validar el bearing off
            is_valid, error_msg = self.__bearing_off_validator__.validate_bearing_off_move(
                self.__current_player__, origen, dice_needed)
            
            if not is_valid:
                self.__message__ = error_msg
                return
            
            # Ejecutar el bearing off
            self.__execute_bearing_off(origen, dice_needed)
            
        except Exception as e:
            self.__message__ = "No puedes sacar esta ficha."


    def __calculate_bearing_off_dice(self, origen: int) -> int:
        """Calcula qué dado se necesita para bearing off."""
        if self.__current_player__ == "negro":
            return origen
        else:
            return 25 - origen


    def __execute_bearing_off(self, origen: int, dice_used: int) -> None:
        """Ejecuta un bearing off válido."""
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
        """Verifica si el jugador tiene movimientos válidos de bearing off."""
        if not self.__bearing_off_validator__.can_bear_off(self.__current_player__):
            return False
        
        if self.__current_player__ == "negro":
            home_quadrant = range(1, 7)
        else:
            home_quadrant = range(19, 25)
        
        for point in home_quadrant:
            state = self.__board__.obtener_estado_punto(point)
            if state and state[0] == self.__current_player__:
                for dice_value in set(self.__available_moves__):
                    is_valid, _ = self.__bearing_off_validator__.validate_bearing_off_move(
                        self.__current_player__, point, dice_value)
                    if is_valid:
                        return True
        
        return False


    # 5. __execute_move - Mensajes más cortos
    def __execute_move(self, origen: int, destino: int) -> None:
        """Ejecuta un movimiento - REEMPLAZAR MÉTODO COMPLETO."""
        try:
            # Calcular dado necesario ANTES de hacer nada
            dado_usado = self.__calculate_dice_needed(origen, destino)
            
            # VALIDAR que el dado esté disponible ANTES de mover
            if dado_usado not in self.__available_moves__:
                self.__message__ = f"No tienes dado {dado_usado}. Disponibles: {self.__available_moves__}"
                return
            
            destination_state = self.__board__.obtener_estado_punto(destino)
            capture_occurred = False
            captured_color = None

            # Verificar si hay captura
            if (destination_state is not None and 
                self.__capture_validator__.can_capture_piece(destination_state,
                                                            self.__current_player__)):
                captured_color = destination_state[0]
                capture_occurred = True
                
                # Limpiar el punto destino
                try:
                    self.__board__.remover_ficha(destino, 1)
                except TypeError:
                    self.__board__.remover_ficha(destino)
                
                # Agregar la ficha capturada a la barra
                self.__bar_manager__.add_piece_to_bar(captured_color)

            # Realizar el movimiento según el origen
            movimiento_exitoso = False
            
            if origen == 0:  # Desde la barra
                # Verificar que tiene fichas en barra
                if not self.__bar_manager__.has_pieces_on_bar(self.__current_player__):
                    if capture_occurred:
                        # Restaurar captura
                        self.__bar_manager__.remove_piece_from_bar(captured_color)
                        self.__board__.colocar_ficha(destino, captured_color, 1)
                    self.__message__ = "No tienes fichas en la barra."
                    return
                
                try:
                    # Primero colocar la ficha
                    self.__board__.colocar_ficha(destino, self.__current_player__, 1)
                    # Solo si tuvo éxito, remover de barra
                    self.__bar_manager__.remove_piece_from_bar(self.__current_player__)
                    movimiento_exitoso = True
                except Exception as e:
                    # Si falla, restaurar captura
                    if capture_occurred:
                        self.__bar_manager__.remove_piece_from_bar(captured_color)
                        self.__board__.colocar_ficha(destino, captured_color, 1)
                    self.__message__ = f"No puedes mover a punto {destino}."
                    return
                    
            else:  # Movimiento normal desde un punto
                try:
                    self.__board__.mover_ficha(origen, destino, self.__current_player__)
                    movimiento_exitoso = True
                except Exception as e:
                    # Si falla, restaurar captura
                    if capture_occurred:
                        self.__bar_manager__.remove_piece_from_bar(captured_color)
                        self.__board__.colocar_ficha(destino, captured_color, 1)
                    self.__message__ = f"No puedes mover de {origen} a {destino}."
                    return

            # Si llegamos aquí, el movimiento fue exitoso
            if movimiento_exitoso:
                # Remover el dado usado
                self.__available_moves__.remove(dado_usado)
                
                remaining_moves = len(self.__available_moves__)

                if remaining_moves == 0:
                    self.__end_turn()
                else:
                    # Verificar si quedan movimientos válidos
                    has_valid_moves = self.__movement_validator__.has_any_valid_move(
                        self.__current_player__, self.__available_moves__)
                    
                    # También verificar bearing off si aplica
                    if hasattr(self, '__bearing_off_validator__'):
                        has_valid_moves = has_valid_moves or self.__has_valid_bearing_off_moves()
                    
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
            # Último recurso - capturar cualquier error no manejado
            error_str = str(e).lower()
            if "not in list" in error_str:
                self.__message__ = "Error con los dados. Intenta de nuevo."
            else:
                self.__message__ = "Error al ejecutar movimiento. Intenta de nuevo."

    # 6. __end_turn - Limpiar selección
    def __end_turn(self) -> None:
        """Termina el turno actual."""
        self.__switch_player()
        self.__game_state_manager__.change_state('AWAITING_ROLL')
        self.__dice_rolls__ = []
        self.__available_moves__ = []
        self.__is_doubles_roll__ = False
        self.__selected_point__ = None  # Limpiar selección al cambiar turno
        self.__message__ = self.__message_manager__.get_awaiting_roll_message(
            self.__current_player__)

    def __switch_player(self) -> None:
        """Cambia al siguiente jugador."""
        self.__current_player__ = "blanco" if self.__current_player__ == "negro" else "negro"

    def __roll_to_start(self) -> None:
        """Realiza la tirada inicial."""
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
        """El jugador tira los dados."""
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
        """Valida un movimiento completo."""
        if (origen != 0 and BarMovementRules.must_enter_from_bar_first(
                self.__bar_manager__, self.__current_player__)):
            self.__message__ = "Debes mover primero desde la barra."
            return False
        if origen == 0:
            if not self.__bar_manager__.has_pieces_on_bar(self.__current_player__):
                self.__message__ = "No tienes fichas en la barra."
                return False
            dado_necesario = (destino if self.__current_player__ == "negro" else 25 - destino)
            if dado_necesario not in self.__available_moves__:
                self.__message__ = self.__message_manager__.get_dice_not_available_message(
                    dado_necesario, self.__available_moves__)
                return False
            destination_state = self.__board__.obtener_estado_punto(destino)
            if self.__capture_validator__.is_move_blocked(destination_state,
                                                          self.__current_player__):
                self.__message__ = f"Punto {destino} bloqueado: tiene 2+ fichas del oponente."
                return False
            return True
        if not self.__is_valid_direction(origen, destino):
            self.__message__ = self.__message_manager__.get_invalid_direction_message()
            return False
        dado_necesario = self.__calculate_dice_needed(origen, destino)
        if dado_necesario not in self.__available_moves__:
            self.__message__ = self.__message_manager__.get_dice_not_available_message(
                dado_necesario, self.__available_moves__)
            return False
        destination_state = self.__board__.obtener_estado_punto(destino)
        if self.__capture_validator__.is_move_blocked(destination_state, self.__current_player__):
            self.__message__ = f"Bloqueado: el punto {destino} tiene 2+ fichas del oponente."
            return False
        return True

    def __calculate_dice_needed(self, origen: int, destino: int) -> int:
        """Calcula qué dado se necesita."""
        if origen == 0:
            return destino if self.__current_player__ == "negro" else 25 - destino
        return abs(origen - destino)

    def __is_valid_direction(self, origen: int, destino: int) -> bool:
        """Verifica dirección correcta."""
        if self.__current_player__ == "negro":
            return destino > origen
        return destino < origen

    def __get_point_from_mouse_pos(self, mouse_pos: Tuple[int, int]) -> Optional[int]:
        """Calcula en qué punto se hizo click."""
        mx, my = mouse_pos
        side_width = (self.__board_width__ - self.__bar_width__) // 2
        point_width = side_width // 6
        bar_x_start = self.__board_margin__ + side_width
        bar_x_end = bar_x_start + self.__bar_width__
        if (bar_x_start <= mx <= bar_x_end and self.__board_margin__ <= my <=
                self.__board_margin__ + self.__board_height__):
            return 0
        if self.__board_margin__ < my < self.__board_margin__ + self.__board_height__ // 2:
            start_x_top_right = self.__board_margin__ + side_width + self.__bar_width__
            if start_x_top_right < mx < self.__board_margin__ + self.__board_width__:
                point_idx = (self.__board_margin__ + self.__board_width__ - mx) // point_width
                if 0 <= point_idx < 6:
                    return point_idx + 1
            start_x_top_left = self.__board_margin__
            if start_x_top_left < mx < self.__board_margin__ + side_width:
                point_idx = (mx - start_x_top_left) // point_width
                if 0 <= point_idx < 6:
                    return 12 - point_idx
        elif (self.__board_margin__ + self.__board_height__ // 2 < my <
              self.__board_margin__ + self.__board_height__):
            start_x_bottom_left = self.__board_margin__
            if start_x_bottom_left < mx < self.__board_margin__ + side_width:
                point_idx = (mx - start_x_bottom_left) // point_width
                if 0 <= point_idx < 6:
                    return 13 + point_idx
            start_x_bottom_right = self.__board_margin__ + side_width + self.__bar_width__
            if start_x_bottom_right < mx < self.__board_margin__ + self.__board_width__:
                point_idx = (self.__board_margin__ + self.__board_width__ - mx) // point_width
                if 0 <= point_idx < 6:
                    return 24 - point_idx
                
        if self.__bearing_off_validator__.can_bear_off(self.__current_player__):
        # Zona bearing off para negro (parte superior derecha, fuera del tablero)
         if (self.__current_player__ == "negro" and 
            mx > self.__board_margin__ + self.__board_width__ and
            my < self.__board_margin__ + self.__board_height__ // 2):
            # Retornar 25 para indicar bearing off negro
            return 25
        
        # Zona bearing off para blanco (parte inferior derecha, fuera del tablero)
        if (self.__current_player__ == "blanco" and 
            mx > self.__board_margin__ + self.__board_width__ and
            my > self.__board_margin__ + self.__board_height__ // 2):
            # Retornar 0 para indicar bearing off blanco
            return 0
    
        return None

    def __update(self) -> None:
        """Actualiza la lógica del juego."""

    def __draw_bar_pieces(self) -> None:
        """Dibuja las fichas en la barra."""
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
        Dibuja las fichas que han salido del tablero (en casa).
        Añadir esta llamada en el método __draw().
        """
        font_small = pygame.font.Font(None, 30)
        
        # Fichas negras en casa (lado derecho superior)
        negro_count = self.__home_manager__.get_pieces_count("negro")
        if negro_count > 0:
            text = f"Casa Negro: {negro_count}/15"
            color = self.__white__ if negro_count < 15 else (0, 255, 0)
            text_surface = font_small.render(text, True, color)
            x = self.__screen__.get_width() - 200
            y = self.__board_margin__ + 50
            self.__screen__.blit(text_surface, (x, y))
        
        # Fichas blancas en casa (lado derecho inferior)
        blanco_count = self.__home_manager__.get_pieces_count("blanco")
        if blanco_count > 0:
            text = f"Casa Blanco: {blanco_count}/15"
            color = self.__white__ if blanco_count < 15 else (0, 255, 0)
            text_surface = font_small.render(text, True, color)
            x = self.__screen__.get_width() - 200
            y = self.__board_margin__ + self.__board_height__ - 70
            self.__screen__.blit(text_surface, (x, y))

    def __draw(self) -> None:
        """Dibuja todos los elementos."""
        self.__screen__.fill((139, 69, 19))
        self.__draw_backgammon_board()
        self.__draw_checkers()
        self.__draw_bar_pieces()
        self.__draw_message()
        if self.__dice_rolls__:
            self.__draw_dice()
        self.__draw_available_moves()
        pygame.display.flip()

    def __draw_available_moves(self) -> None:
        """Dibuja los movimientos disponibles."""
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
        """Renderiza el mensaje de estado."""
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
        """Dibuja los dos dados."""
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
        """Dibuja los puntos en la cara de un dado."""
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
        """Dibuja el tablero de Backgammon."""
        board_rect = pygame.Rect(self.__board_margin__, self.__board_margin__, self.__board_width__, self.__board_height__)
        pygame.draw.rect(self.__screen__, self.__brown_light__, board_rect)
        pygame.draw.rect(self.__screen__, self.__board_border__, board_rect, 5)
        
        bar_x = self.__board_margin__ + (self.__board_width__ // 2) - (self.__bar_width__ // 2)
        bar_rect = pygame.Rect(bar_x, self.__board_margin__, self.__bar_width__, self.__board_height__)
        pygame.draw.rect(self.__screen__, self.__bar_color__, bar_rect)
        pygame.draw.rect(self.__screen__, self.__black__, bar_rect, 3)
        
        self.__draw_points()
        
    def __draw_points(self) -> None:
        """Dibuja los 24 puntos triangulares del tablero con colores correctamente intercalados."""
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

    def __draw_triangle_point(self, x: int, y: int, width: int, height: int, color: Tuple[int, int, int], pointing_down: bool = True) -> None:
        """Dibuja un único punto triangular en el tablero."""
        if pointing_down:
            points = [(x + width // 2, y + height), (x, y), (x + width, y)]
        else:
            points = [(x + width // 2, y), (x, y + height), (x + width, y + height)]
        pygame.draw.polygon(self.__screen__, color, points)
        pygame.draw.polygon(self.__screen__, self.__black__, points, 2)
    
    def __draw_checkers(self) -> None:
        """Itera sobre todos los puntos del tablero y dibuja las fichas correspondientes."""
        checker_radius = 25
        for point_num in range(1, 25):
            point_data = self.__board__.obtener_estado_punto(point_num)
            if point_data:
                color, cantidad = point_data
                point_x, point_y = self.__get_point_screen_position(point_num)
                self.__draw_checker_stack(point_x, point_y, color, cantidad, point_num, checker_radius)
    
    def __get_point_screen_position(self, point_num: int) -> Tuple[int, int]:
        """Calcula la posición central en la pantalla para apilar fichas en un punto específico."""
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

    def __draw_checker_stack(self, x: int, y: int, color: str, cantidad: int, point_num: int, radius: int) -> None:
        """Dibuja una pila de fichas en una posición específica."""
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
