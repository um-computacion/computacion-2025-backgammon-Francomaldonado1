import pygame
import sys
from typing import Tuple, Optional, List
import os

# Agregamos la ruta para encontrar los módulos del Core
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Backgammon.Core.Board import Board
from Backgammon.Core.Dice import Dice

class DiceMovesCalculator:
    """
    Clase responsable de calcular los movimientos disponibles basados en los dados.
    Principio de Responsabilidad Única (SRP): Solo se encarga de la lógica de dados.
    """
    
    @staticmethod
    def calculate_available_moves(dice_roll1: int, dice_roll2: int) -> List[int]:
        """
        Calcula los movimientos disponibles basados en los dados tirados.
        
        Args:
            dice_roll1: Valor del primer dado
            dice_roll2: Valor del segundo dado
            
        Returns:
            Lista de movimientos disponibles
        """
        if dice_roll1 == dice_roll2:
            # Dobles: se pueden hacer 4 movimientos del mismo valor
            return [dice_roll1] * 4
        else:
            # Dados normales: un movimiento por cada dado
            return [dice_roll1, dice_roll2]
    
    @staticmethod
    def is_doubles_roll(dice_roll1: int, dice_roll2: int) -> bool:
        """
        Determina si la tirada es dobles.
        
        Args:
            dice_roll1: Valor del primer dado
            dice_roll2: Valor del segundo dado
            
        Returns:
            True si es dobles, False en caso contrario
        """
        return dice_roll1 == dice_roll2

class GameStateManager:
    """
    Clase responsable de gestionar los estados del juego.
    Principio de Responsabilidad Única (SRP): Solo maneja estados.
    """
    
    def __init__(self):
        self.current_state = 'START_ROLL'
        self.valid_states = {
            'START_ROLL', 
            'AWAITING_ROLL', 
            'AWAITING_PIECE_SELECTION'
        }
    
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
    """
    Clase responsable de generar mensajes apropiados para el estado del juego.
    Principio de Responsabilidad Única (SRP): Solo maneja mensajes.
    """
    
    @staticmethod
    def get_start_message() -> str:
        """Mensaje para el inicio del juego."""
        return "Presiona 'R' para decidir quién empieza."
    
    @staticmethod
    def get_roll_winner_message(winner: str, winner_roll: int, loser_roll: int) -> str:
        """Mensaje cuando alguien gana la tirada inicial."""
        winner_display = winner.capitalize()
        loser_display = "Blanco" if winner == "negro" else "Negro"
        return f"{winner_display} ({winner_roll}) gana a {loser_display} ({loser_roll}). Presiona 'R' para tirar tus dados."
    
    @staticmethod
    def get_awaiting_roll_message(current_player: str) -> str:
        """Mensaje cuando el jugador debe tirar dados."""
        return f"Turno de {current_player}. Presiona 'R' para tirar los dados."
    
    @staticmethod
    def get_doubles_roll_message(current_player: str, dice_value: int, available_moves: List[int]) -> str:
        """Mensaje cuando se sacan dobles."""
        return f"¡DOBLES! {current_player.capitalize()} sacó {dice_value}-{dice_value}. Tienes {len(available_moves)} movimientos."
    
    @staticmethod
    def get_normal_roll_message(current_player: str, available_moves: List[int]) -> str:
        """Mensaje para tirada normal."""
        return f"Turno de {current_player}. Tienes dados {available_moves}. Elige una ficha."
    
    @staticmethod
    def get_piece_selected_message(point: int, available_moves: List[int]) -> str:
        """Mensaje cuando se selecciona una ficha."""
        return f"Ficha en {point} seleccionada. Dados disponibles: {available_moves}. Elige destino."
    
    @staticmethod
    def get_invalid_piece_message(point: int) -> str:
        """Mensaje cuando se selecciona una ficha inválida."""
        return f"No tienes fichas en el punto {point}. Elige una válida."
    
    @staticmethod
    def get_move_completed_message(remaining_moves: int, available_moves: List[int]) -> str:
        """Mensaje cuando se completa un movimiento."""
        if remaining_moves == 0:
            return "Turno completado."
        else:
            return f"Movimiento realizado. Te quedan {remaining_moves} dados: {available_moves}. Elige ficha."
    
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


class BarManager:
    """
    Clase responsable de gestionar la lógica de la barra central.
    Principio SRP: Solo maneja operaciones relacionadas con la barra.
    """
    
    def __init__(self):
        """Inicializa la barra vacía para ambos jugadores."""
        self.__bar_pieces__ = {
            "negro": 0,
            "blanco": 0
        }
    
    def add_piece_to_bar(self, color: str) -> None:
        """
        Agrega una ficha a la barra.
        
        Args:
            color: Color de la ficha ("negro" o "blanco")
        """
        if color in self.__bar_pieces__:
            self.__bar_pieces__[color] += 1
        else:
            raise ValueError(f"Color inválido: {color}")
    
    def remove_piece_from_bar(self, color: str) -> bool:
        """
        Remueve una ficha de la barra.
        
        Args:
            color: Color de la ficha a remover
            
        Returns:
            True si se pudo remover, False si no había fichas
        """
        if color in self.__bar_pieces__ and self.__bar_pieces__[color] > 0:
            self.__bar_pieces__[color] -= 1
            return True
        return False
    
    def get_pieces_count(self, color: str) -> int:
        """
        Obtiene el número de fichas en la barra para un jugador.
        
        Args:
            color: Color del jugador
            
        Returns:
            Número de fichas en la barra
        """
        return self.__bar_pieces__.get(color, 0)
    
    def has_pieces_on_bar(self, color: str) -> bool:
        """
        Verifica si un jugador tiene fichas en la barra.
        
        Args:
            color: Color del jugador
            
        Returns:
            True si tiene fichas en la barra
        """
        return self.get_pieces_count(color) > 0
    
    def get_bar_state(self) -> dict:
        """
        Obtiene el estado completo de la barra.
        
        Returns:
            Diccionario con el conteo de fichas por color
        """
        return self.__bar_pieces__.copy()


class CaptureValidator:
    """
    Clase responsable de validar y determinar capturas.
    Principio SRP: Solo se encarga de la lógica de captura.
    """
    
    @staticmethod
    def can_capture_piece(destination_state: tuple, attacking_color: str) -> bool:
        """
        Determina si se puede capturar una ficha en el destino.
        
        Args:
            destination_state: Estado del punto destino (color, cantidad) o None
            attacking_color: Color de la ficha que ataca
            
        Returns:
            True si se puede capturar
        """
        if destination_state is None:
            return False  # Punto vacío, no hay nada que capturar
        
        destination_color, destination_count = destination_state
        
        # Solo se puede capturar si:
        # 1. El punto tiene fichas del oponente
        # 2. Solo hay 1 ficha (blot)
        return (destination_color != attacking_color and 
                destination_count == 1)
    
    @staticmethod
    def is_move_blocked(destination_state: tuple, attacking_color: str) -> bool:
        """
        Determina si un movimiento está bloqueado.
        
        Args:
            destination_state: Estado del punto destino
            attacking_color: Color de la ficha que ataca
            
        Returns:
            True si el movimiento está bloqueado
        """
        if destination_state is None:
            return False  # Punto vacío, no está bloqueado
        
        destination_color, destination_count = destination_state
        
        # El movimiento está bloqueado si hay 2+ fichas del oponente
        return (destination_color != attacking_color and 
                destination_count > 1)


class BarMovementRules:
    """
    Clase que define las reglas específicas para movimientos desde la barra.
    Principio SRP: Solo maneja reglas de movimiento desde la barra.
    """
    
    @staticmethod
    def get_entry_point(color: str, dice_value: int) -> int:
        """
        Calcula el punto de entrada desde la barra según el color y dado.
        
        Args:
            color: Color del jugador
            dice_value: Valor del dado
            
        Returns:
            Número del punto de entrada (1-24)
        """
        if color == "negro":
            # Negro entra por los puntos 1-6
            return dice_value
        else:  # blanco
            # Blanco entra por los puntos 19-24
            return 25 - dice_value
    
    @staticmethod
    def must_enter_from_bar_first(bar_manager: 'BarManager', color: str) -> bool:
        """
        Determina si el jugador debe mover desde la barra antes de otros movimientos.
        
        Args:
            bar_manager: Instancia del gestor de barra
            color: Color del jugador
            
        Returns:
            True si debe mover primero desde la barra
        """
        return bar_manager.has_pieces_on_bar(color)



class PygameUI:
    def __init__(self, board_width: int = 1600, board_height: int = 900):
        """Inicializa la interfaz gráfica para el juego de Backgammon."""
        pygame.init()
        self.__screen__ = pygame.display.set_mode((board_width, board_height))
        pygame.display.set_caption("Backgammon")
        self.__clock__ = pygame.time.Clock()
        self.__running__ = True
        
        # --- Gestores (aplicando principio de separación de responsabilidades) ---
        self.__game_state_manager__ = GameStateManager()
        self.__dice_calculator__ = DiceMovesCalculator()
        self.__message_manager__ = MessageManager()
        self.__bar_manager__ = BarManager()  # NUEVO: Gestor de barra
        self.__capture_validator__ = CaptureValidator()  # NUEVO: Validador de capturas
        
        # --- Lógica de la partida ---
        self.__dice__ = Dice()
        self.__dice_rolls__ = []
        self.__available_moves__ = []  # Lista de dados disponibles para usar
        self.__current_player__ = None
        self.__font__ = pygame.font.Font(None, 45)
        self.__message__ = self.__message_manager__.get_start_message()
        self.__is_doubles_roll__ = False  # Nueva propiedad para trackear dobles

        self.__board__ = Board()
        self.__board__.inicializar_posiciones_estandar()
        
        self.__selected_point__: Optional[int] = None

        # --- Paleta de Colores ---
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
        self.__doubles_highlight__ = (255, 215, 0)  # Color dorado para destacar dobles
        self.__capture_highlight__ = (255, 0, 0)  # NUEVO: Color para capturas
        
        # --- Dimensiones ---
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
        
        pygame.quit()
        sys.exit()
            
    def __handle_events(self) -> None:
        """Gestiona las entradas del usuario."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running__ = False
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.__running__ = False
                
                if event.key == pygame.K_r:
                    self.__handle_roll_request()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.__game_state_manager__.get_current_state() == 'AWAITING_PIECE_SELECTION':
                    self.__handle_piece_selection(pygame.mouse.get_pos())

    def __handle_roll_request(self) -> None:
        """
        Maneja las solicitudes de tirada según el estado actual.
        Principio Abierto/Cerrado (OCP): Fácil de extender para nuevos estados.
        """
        current_state = self.__game_state_manager__.get_current_state()
        
        if current_state == 'START_ROLL':
            self.__roll_to_start()
        elif current_state == 'AWAITING_ROLL':
            self.__roll_player_dice()

    def __handle_piece_selection(self, mouse_pos: Tuple[int, int]) -> None:
        """
        Maneja la selección de fichas y movimientos.
        Principio de Responsabilidad Única (SRP): Se enfoca solo en la selección.
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
        Intenta seleccionar una ficha en el punto dado.
        ACTUALIZADO: Incluye selección desde la barra.
        """
        if point == 0:  # Selección desde la barra
            if self.__bar_manager__.has_pieces_on_bar(self.__current_player__):
                self.__selected_point__ = 0
                self.__message__ = f"Ficha en la barra seleccionada. Dados disponibles: {self.__available_moves__}. Elige punto de entrada."
            else:
                self.__message__ = "No tienes fichas en la barra."
            return
        
        # Validar si debe mover desde la barra primero
        if BarMovementRules.must_enter_from_bar_first(self.__bar_manager__, self.__current_player__):
            self.__message__ = "Debes mover primero desde la barra. Haz clic en el centro del tablero."
            return
        
        # Lógica original para puntos normales
        estado_punto = self.__board__.obtener_estado_punto(point)
        
        if estado_punto and estado_punto[0] == self.__current_player__:
            self.__selected_point__ = point
            self.__message__ = self.__message_manager__.get_piece_selected_message(point, self.__available_moves__)
        else:
            self.__message__ = self.__message_manager__.get_invalid_piece_message(point)


    def __attempt_move(self, origen: int, destino: int) -> None:
        """
        Intenta realizar un movimiento y maneja el resultado.
        """
        movimiento_valido = self.__validate_and_report_move(origen, destino)
        
        if movimiento_valido:
            self.__execute_move(origen, destino)
        else:
            self.__message__ = self.__message_manager__.get_invalid_move_message()

    def __execute_move(self, origen: int, destino: int) -> None:
        """
        Ejecuta un movimiento válido y actualiza el estado del juego.
        ACTUALIZADO: Ahora incluye lógica de captura.
        """
        # Verificar si hay captura
        destination_state = self.__board__.obtener_estado_punto(destino)
        capture_occurred = False
        
        if self.__capture_validator__.can_capture_piece(destination_state, self.__current_player__):
            # Capturar la ficha del oponente
            captured_color = destination_state[0]
            self.__bar_manager__.add_piece_to_bar(captured_color)
            capture_occurred = True
        
        # Realizar el movimiento en el tablero
        if origen == 0:  # Movimiento desde la barra
            # Remover ficha de la barra y colocar en el tablero
            self.__bar_manager__.remove_piece_from_bar(self.__current_player__)
            self.__board__.colocar_ficha(destino, self.__current_player__, 1)
        else:
            # Movimiento normal en el tablero
            self.__board__.mover_ficha(origen, destino, self.__current_player__)
        
        # Remover el dado usado
        dado_usado = abs(origen - destino) if origen != 0 else destino
        if origen == 0:  # Desde la barra, usar valor directo del destino según las reglas
            if self.__current_player__ == "negro":
                dado_usado = destino
            else:  # blanco
                dado_usado = 25 - destino
        
        self.__available_moves__.remove(dado_usado)
        
        # Actualizar mensaje
        remaining_moves = len(self.__available_moves__)
        
        if remaining_moves == 0:
            self.__end_turn()
        else:
            if capture_occurred:
                self.__message__ = f"¡Captura realizada! Te quedan {remaining_moves} dados: {self.__available_moves__}. Elige ficha."
            else:
                self.__message__ = self.__message_manager__.get_move_completed_message(remaining_moves, self.__available_moves__)

    def __end_turn(self) -> None:
        """
        Termina el turno actual y pasa al siguiente jugador.
        Principio de Responsabilidad Única: Se enfoca solo en cambiar turnos.
        """
        self.__switch_player()
        self.__game_state_manager__.change_state('AWAITING_ROLL')
        self.__dice_rolls__ = []
        self.__available_moves__ = []
        self.__is_doubles_roll__ = False  # Resetear flag de dobles
        self.__message__ = self.__message_manager__.get_awaiting_roll_message(self.__current_player__)

    def __switch_player(self) -> None:
        """
        Cambia al siguiente jugador.
        """
        self.__current_player__ = "blanco" if self.__current_player__ == "negro" else "negro"

    def __roll_to_start(self) -> None:
        """Realiza la tirada inicial para decidir quién empieza."""
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
            self.__message__ = self.__message_manager__.get_roll_winner_message("negro", roll1, roll2)
        else:
            self.__current_player__ = "blanco"
            self.__message__ = self.__message_manager__.get_roll_winner_message("blanco", roll2, roll1)

        self.__game_state_manager__.change_state('AWAITING_ROLL')

    def __roll_player_dice(self) -> None:
        """
        El jugador actual tira los dos dados para su turno.
        Ahora incluye lógica de dobles usando DiceMovesCalculator.
        """
        self.__dice__.tirar()
        dado1 = self.__dice__.obtener_dado1()
        dado2 = self.__dice__.obtener_dado2()
        
        self.__dice_rolls__ = [dado1, dado2]
        
        # Usar el calculador de movimientos para determinar movimientos disponibles
        self.__available_moves__ = self.__dice_calculator__.calculate_available_moves(dado1, dado2)
        self.__is_doubles_roll__ = self.__dice_calculator__.is_doubles_roll(dado1, dado2)
        
        self.__game_state_manager__.change_state('AWAITING_PIECE_SELECTION')
        
        # Generar mensaje apropiado según si son dobles o no
        if self.__is_doubles_roll__:
            self.__message__ = self.__message_manager__.get_doubles_roll_message(
                self.__current_player__, dado1, self.__available_moves__
            )
        else:
            self.__message__ = self.__message_manager__.get_normal_roll_message(
                self.__current_player__, self.__available_moves__
            )

    def __validate_and_report_move(self, origen: int, destino: int) -> bool:
        """
        Valida un movimiento completo incluyendo lógica de barra y captura.
        ACTUALIZADO: Incluye validaciones de barra.
        """
        # Validar si debe mover desde la barra primero
        if (origen != 0 and 
            BarMovementRules.must_enter_from_bar_first(self.__bar_manager__, self.__current_player__)):
            self.__message__ = "Debes mover primero desde la barra."
            return False
        
        # Validar movimiento desde la barra
        if origen == 0:
            if not self.__bar_manager__.has_pieces_on_bar(self.__current_player__):
                self.__message__ = "No tienes fichas en la barra."
                return False
            
            # Calcular si el destino es correcto para entrada desde barra
            expected_destination = BarMovementRules.get_entry_point(
                self.__current_player__, 
                destino if self.__current_player__ == "negro" else (25 - destino)
            )
            
            if destino != expected_destination:
                self.__message__ = "Punto de entrada inválido desde la barra."
                return False
        
        # Validar dirección del movimiento (solo para movimientos normales)
        if origen != 0 and not self.__is_valid_direction(origen, destino):
            self.__message__ = self.__message_manager__.get_invalid_direction_message()
            return False
        
        # Validar que el dado esté disponible
        dado_necesario = self.__calculate_dice_needed(origen, destino)
        if dado_necesario not in self.__available_moves__:
            self.__message__ = self.__message_manager__.get_dice_not_available_message(
                dado_necesario, self.__available_moves__
            )
            return False
        
        # Validar que el movimiento no esté bloqueado
        destination_state = self.__board__.obtener_estado_punto(destino)
        if self.__capture_validator__.is_move_blocked(destination_state, self.__current_player__):
            self.__message__ = f"Movimiento bloqueado: el punto {destino} tiene 2+ fichas del oponente."
            return False
        
        return True

    def __calculate_dice_needed(self, origen: int, destino: int) -> int:
        """
        Calcula qué dado se necesita para un movimiento específico.
        NUEVO: Maneja cálculos desde la barra.
        """
        if origen == 0:  # Desde la barra
            if self.__current_player__ == "negro":
                return destino  # Para negro, el punto de destino ES el valor del dado
            else:  # blanco
                return 25 - destino  # Para blanco, es 25 menos el punto de destino
        else:
            return abs(origen - destino)  # Movimiento normal
        

    def __can_move_piece(self, origen: int, destino: int) -> bool:
        """
        Valida si un movimiento es posible SIN modificar el tablero.
        """
        # Validar origen
        estado_origen = self.__board__.obtener_estado_punto(origen)
        if estado_origen is None or estado_origen[0] != self.__current_player__:
            return False

        # Validar destino
        estado_destino = self.__board__.obtener_estado_punto(destino)
        if estado_destino is not None:
            color_destino, cantidad_destino = estado_destino
            if color_destino != self.__current_player__ and cantidad_destino > 1:
                return False  # Punto bloqueado

        return True

    def __is_valid_direction(self, origen: int, destino: int) -> bool:
        """
        Verifica que el movimiento sea en la dirección correcta para el jugador actual.
        Principio de Responsabilidad Única: Solo valida direcciones.
        """
        if self.__current_player__ == "negro":
            return destino > origen  # Negro mueve hacia números mayores
        else:  # blanco
            return destino < origen  # Blanco mueve hacia números menores

    def __has_valid_moves(self) -> bool:
        """
        Verifica si el jugador actual tiene movimientos válidos disponibles.
        Esto se usará en futuras implementaciones para detectar bloqueos.
        """
        return len(self.__available_moves__) > 0

    def __get_point_from_mouse_pos(self, mouse_pos: Tuple[int, int]) -> Optional[int]:
        """
        Calcula en qué punto del tablero (0-24) se hizo click.
        ACTUALIZADO: Incluye detección de clic en la barra (punto 0).
        """
        mx, my = mouse_pos
        side_width = (self.__board_width__ - self.__bar_width__) // 2
        point_width = side_width // 6
        
        # Verificar clic en la barra central
        bar_x_start = self.__board_margin__ + side_width
        bar_x_end = bar_x_start + self.__bar_width__
        
        if (bar_x_start <= mx <= bar_x_end and 
            self.__board_margin__ <= my <= self.__board_margin__ + self.__board_height__):
            return 0  # Punto especial para la barra
        
        # Lógica original para puntos 1-24
        if self.__board_margin__ < my < self.__board_margin__ + self.__board_height__ // 2:
            start_x_top_right = self.__board_margin__ + side_width + self.__bar_width__
            if start_x_top_right < mx < self.__board_margin__ + self.__board_width__:
                point_index_from_right = (self.__board_margin__ + self.__board_width__ - mx) // point_width
                if 0 <= point_index_from_right < 6:
                    return point_index_from_right + 1
            
            start_x_top_left = self.__board_margin__
            if start_x_top_left < mx < self.__board_margin__ + side_width:
                point_index_from_left = (mx - start_x_top_left) // point_width
                if 0 <= point_index_from_left < 6:
                    return 12 - point_index_from_left
        
        elif self.__board_margin__ + self.__board_height__ // 2 < my < self.__board_margin__ + self.__board_height__:
            start_x_bottom_left = self.__board_margin__
            if start_x_bottom_left < mx < self.__board_margin__ + side_width:
                point_index = (mx - start_x_bottom_left) // point_width
                if 0 <= point_index < 6:
                    return 13 + point_index

            start_x_bottom_right = self.__board_margin__ + side_width + self.__bar_width__
            if start_x_bottom_right < mx < self.__board_margin__ + self.__board_width__:
                point_index_from_right = (self.__board_margin__ + self.__board_width__ - mx) // point_width
                if 0 <= point_index_from_right < 6:
                    return 24 - point_index_from_right
        return None

    def __update(self) -> None:
        """Actualiza la lógica del juego en cada frame."""
        pass
        
    def __draw_bar_pieces(self) -> None:
        """
        NUEVO: Dibuja las fichas en la barra central.
        """
        bar_x = self.__board_margin__ + (self.__board_width__ // 2) - (self.__bar_width__ // 2)
        bar_center_x = bar_x + (self.__bar_width__ // 2)
        
        checker_radius = 20  # Ligeramente más pequeño para la barra
        
        # Dibujar fichas negras (parte superior de la barra)
        negro_count = self.__bar_manager__.get_pieces_count("negro")
        if negro_count > 0:
            start_y = self.__board_margin__ + 50
            for i in range(min(negro_count, 8)):  # Máximo 8 fichas visibles
                ficha_y = start_y + (i * checker_radius * 1.5)
                pygame.draw.circle(self.__screen__, self.__checker_black__, 
                                 (bar_center_x, int(ficha_y)), checker_radius)
                pygame.draw.circle(self.__screen__, self.__checker_border__, 
                                 (bar_center_x, int(ficha_y)), checker_radius, 2)
            
            # Si hay más de 8, mostrar número
            if negro_count > 8:
                font_small = pygame.font.Font(None, 20)
                count_text = font_small.render(str(negro_count), True, self.__white__)
                text_rect = count_text.get_rect(center=(bar_center_x, start_y + 200))
                self.__screen__.blit(count_text, text_rect)
        
        # Dibujar fichas blancas (parte inferior de la barra)
        blanco_count = self.__bar_manager__.get_pieces_count("blanco")
        if blanco_count > 0:
            start_y = self.__board_margin__ + self.__board_height__ - 50
            for i in range(min(blanco_count, 8)):
                ficha_y = start_y - (i * checker_radius * 1.5)
                pygame.draw.circle(self.__screen__, self.__checker_white__, 
                                 (bar_center_x, int(ficha_y)), checker_radius)
                pygame.draw.circle(self.__screen__, self.__checker_border__, 
                                 (bar_center_x, int(ficha_y)), checker_radius, 2)
            
            # Si hay más de 8, mostrar número
            if blanco_count > 8:
                font_small = pygame.font.Font(None, 20)
                count_text = font_small.render(str(blanco_count), True, self.__black__)
                text_rect = count_text.get_rect(center=(bar_center_x, start_y - 200))
                self.__screen__.blit(count_text, text_rect)

    def __draw(self) -> None:
        """
        Dibuja todos los elementos del juego en la pantalla.
        ACTUALIZADO: Incluye dibujo de fichas en la barra.
        """
        self.__screen__.fill((139, 69, 19))
        self.__draw_backgammon_board()
        self.__draw_checkers()
        self.__draw_bar_pieces()  # NUEVO: Dibujar fichas de la barra
        self.__draw_message()
        
        if self.__dice_rolls__:
            self.__draw_dice()
        
        self.__draw_available_moves()
            
        pygame.display.flip()

    def __draw_available_moves(self) -> None:
        """
        Dibuja los dados/movimientos disponibles en la pantalla.
        Ahora destaca visualmente cuando son dobles.
        """
        if not self.__available_moves__:
            return
            
        font_small = pygame.font.Font(None, 30)
        
        # Crear texto diferente para dobles
        if self.__is_doubles_roll__:
            moves_text = f"Movimientos: {self.__available_moves__} (Total: {len(self.__available_moves__)})"
            text_color = self.__doubles_highlight__
        else:
            moves_text = f"Movimientos disponibles: {self.__available_moves__}"
            text_color = self.__white__
        
        text_surface = font_small.render(moves_text, True, text_color)
        
        # Posicionar muy arriba para no interferir con el tablero
        text_rect = text_surface.get_rect()
        text_rect.topright = (self.__screen__.get_width() - 20, 10)
        self.__screen__.blit(text_surface, text_rect)
    
    def __draw_message(self) -> None:
        """
        Renderiza y muestra el mensaje de estado actual.
        Ahora destaca mensajes de dobles con color especial.
        """
        # Usar color especial para mensajes de dobles
        if self.__is_doubles_roll__ and "DOBLES" in self.__message__:
            text_color = self.__doubles_highlight__
        else:
            text_color = self.__white__
            
        text_surface = self.__font__.render(self.__message__, True, text_color)
        text_rect = text_surface.get_rect(center=(self.__screen__.get_width() / 2, 25))
        self.__screen__.blit(text_surface, text_rect)

    def __draw_dice(self) -> None:
        """
        Dibuja los dos dados en el centro del tablero.
        Ahora destaca visualmente los dobles con un borde dorado.
        """
        dice_size = 80
        margin = 20
        x1 = self.__board_margin__ + (self.__board_width__ / 2) - self.__bar_width__ - dice_size - margin
        x2 = self.__board_margin__ + (self.__board_width__ / 2) + self.__bar_width__ + margin
        y = (self.__screen__.get_height() / 2) - (dice_size / 2)
        
        dice_rect1 = pygame.Rect(x1, y, dice_size, dice_size)
        dice_rect2 = pygame.Rect(x2, y, dice_size, dice_size)
        
        # Dibujar dados con fondo normal
        pygame.draw.rect(self.__screen__, self.__dice_color__, dice_rect1, border_radius=10)
        pygame.draw.rect(self.__screen__, self.__dice_color__, dice_rect2, border_radius=10)
        
        # Si son dobles, agregar borde dorado destacado
        if self.__is_doubles_roll__:
            pygame.draw.rect(self.__screen__, self.__doubles_highlight__, dice_rect1, 5, border_radius=10)
            pygame.draw.rect(self.__screen__, self.__doubles_highlight__, dice_rect2, 5, border_radius=10)
        
        self.__draw_pips(dice_rect1, self.__dice_rolls__[0])
        self.__draw_pips(dice_rect2, self.__dice_rolls__[1])

    def __draw_pips(self, rect: pygame.Rect, number: int) -> None:
        """Dibuja los puntos (pips) en la cara de un dado."""
        pip_radius = 8
        margin = 20
        positions = {
            1: [rect.center],
            2: [(rect.left + margin, rect.top + margin), (rect.right - margin, rect.bottom - margin)],
            3: [(rect.left + margin, rect.top + margin), rect.center, (rect.right - margin, rect.bottom - margin)],
            4: [(rect.left + margin, rect.top + margin), (rect.right - margin, rect.top + margin),
                (rect.left + margin, rect.bottom - margin), (rect.right - margin, rect.bottom - margin)],
            5: [(rect.left + margin, rect.top + margin), (rect.right - margin, rect.top + margin),
                rect.center, (rect.left + margin, rect.bottom - margin), (rect.right - margin, rect.bottom - margin)],
            6: [(rect.left + margin, rect.top + margin), (rect.right - margin, rect.top + margin),
                (rect.left + margin, rect.centery), (rect.right - margin, rect.centery),
                (rect.left + margin, rect.bottom - margin), (rect.right - margin, rect.bottom - margin)]
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
