import pygame
import sys
from typing import Tuple, Optional, List
import os

# Agregamos la ruta para encontrar los módulos del Core
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Backgammon.Core.Board import Board
from Backgammon.Core.Dice import Dice

class PygameUI:
    def __init__(self, board_width: int = 1600, board_height: int = 900):
        """Inicializa la interfaz gráfica para el juego de Backgammon."""
        pygame.init()
        self.__screen__ = pygame.display.set_mode((board_width, board_height))
        pygame.display.set_caption("Backgammon")
        self.__clock__ = pygame.time.Clock()
        self.__running__ = True
        
        # --- Lógica de la partida ---
        self.__game_state__ = 'START_ROLL'
        self.__dice__ = Dice()
        self.__dice_rolls__ = []
        self.__available_moves__ = []  # Lista de dados disponibles para usar
        self.__current_player__ = None
        self.__font__ = pygame.font.Font(None, 45)
        self.__message__ = "Presiona 'R' para decidir quién empieza."

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
                    if self.__game_state__ == 'START_ROLL':
                        self.__roll_to_start()
                    elif self.__game_state__ == 'AWAITING_ROLL':
                        self.__roll_player_dice()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.__game_state__ == 'AWAITING_PIECE_SELECTION':
                    self.__handle_piece_selection(pygame.mouse.get_pos())

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
        """
        estado_punto = self.__board__.obtener_estado_punto(point)
        
        if estado_punto and estado_punto[0] == self.__current_player__:
            self.__selected_point__ = point
            self.__message__ = f"Ficha en {point} seleccionada. Dados disponibles: {self.__available_moves__}. Elige destino."
        else:
            self.__message__ = f"No tienes fichas en el punto {point}. Elige una válida."

    def __attempt_move(self, origen: int, destino: int) -> None:
        """
        Intenta realizar un movimiento y maneja el resultado.
        """
        movimiento_valido = self.__validate_and_report_move(origen, destino)
        
        if movimiento_valido:
            self.__execute_move(origen, destino)
        else:
            self.__message__ = "Movimiento inválido. Vuelve a elegir una ficha."

    def __execute_move(self, origen: int, destino: int) -> None:
        """
        Ejecuta un movimiento válido y actualiza el estado del juego.
        """
        dado_usado = abs(origen - destino)
        
        # Realizar el movimiento en el tablero (UNA sola ficha)
        # Usamos mover_ficha() que es el método real para hacer movimientos
        self.__board__.mover_ficha(origen, destino, self.__current_player__)
        
        # Remover el dado usado de los movimientos disponibles
        self.__available_moves__.remove(dado_usado)
        
        # Actualizar mensaje y verificar si el turno debe cambiar
        remaining_moves = len(self.__available_moves__)
        
        if remaining_moves == 0:
            self.__end_turn()
        else:
            self.__message__ = f"Movimiento realizado. Te quedan {remaining_moves} dados: {self.__available_moves__}. Elige ficha."

    def __end_turn(self) -> None:
        """
        Termina el turno actual y pasa al siguiente jugador.
        Principio de Responsabilidad Única: Se enfoca solo en cambiar turnos.
        """
        self.__switch_player()
        self.__game_state__ = 'AWAITING_ROLL'
        self.__dice_rolls__ = []
        self.__available_moves__ = []
        self.__message__ = f"Turno de {self.__current_player__}. Presiona 'R' para tirar los dados."

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
            self.__message__ = f"Negro ({roll1}) gana a Blanco ({roll2}). Presiona 'R' para tirar tus dados."
        else:
            self.__current_player__ = "blanco"
            self.__message__ = f"Blanco ({roll2}) gana a Negro ({roll1}). Presiona 'R' para tirar tus dados."

        self.__game_state__ = 'AWAITING_ROLL'

    def __roll_player_dice(self) -> None:
        """El jugador actual tira los dos dados para su turno."""
        self.__dice__.tirar()
        dado1 = self.__dice__.obtener_dado1()
        dado2 = self.__dice__.obtener_dado2()
        
        self.__dice_rolls__ = [dado1, dado2]
        
        # Configurar movimientos disponibles (solo dados normales por ahora)
        self.__available_moves__ = [dado1, dado2]
        
        self.__game_state__ = 'AWAITING_PIECE_SELECTION'
        self.__message__ = f"Turno de {self.__current_player__}. Tienes dados {self.__available_moves__}. Elige una ficha."

    def __validate_and_report_move(self, origen: int, destino: int) -> bool:
        """
        Valida un movimiento completo incluyendo dirección, dados disponibles y reglas del tablero.
        IMPORTANTE: Solo valida, NO hace cambios en el tablero.
        """
        # Validar dirección del movimiento
        if not self.__is_valid_direction(origen, destino):
            self.__message__ = "Movimiento inválido (dirección incorrecta)."
            return False
        
        # Validar que el dado esté disponible
        dado_necesario = abs(origen - destino)
        if dado_necesario not in self.__available_moves__:
            self.__message__ = f"No tienes el dado {dado_necesario} disponible. Dados: {self.__available_moves__}."
            return False
        
        # Validar reglas del tablero SIN hacer cambios
        # Necesitamos una validación que no modifique el tablero
        if not self.__can_move_piece(origen, destino):
            self.__message__ = f"Movimiento de {origen} a {destino} bloqueado o inválido."
            return False
        
        return True

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
        # Por ahora retorna True, pero aquí se implementaría la lógica
        # para verificar si existen movimientos válidos con los dados disponibles
        return len(self.__available_moves__) > 0

    def __get_point_from_mouse_pos(self, mouse_pos: Tuple[int, int]) -> Optional[int]:
        """
        Calcula en qué punto del tablero (1-24) se hizo click.
        """
        mx, my = mouse_pos
        side_width = (self.__board_width__ - self.__bar_width__) // 2
        point_width = side_width // 6
        
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
        
    def __draw(self) -> None:
        """Dibuja todos los elementos del juego en la pantalla."""
        self.__screen__.fill((139, 69, 19))
        self.__draw_backgammon_board()
        self.__draw_checkers()
        self.__draw_message()
        
        if self.__dice_rolls__:
            self.__draw_dice()
        
        # Mostrar movimientos disponibles
        self.__draw_available_moves()
            
        pygame.display.flip()
    
    def __draw_available_moves(self) -> None:
        """
        Dibuja los dados/movimientos disponibles en la pantalla.
        """
        if not self.__available_moves__:
            return
            
        font_small = pygame.font.Font(None, 30)
        moves_text = f"Movimientos disponibles: {self.__available_moves__}"
        text_surface = font_small.render(moves_text, True, self.__white__)
        
        # Posicionar muy arriba para no interferir con el tablero
        text_rect = text_surface.get_rect()
        text_rect.topright = (self.__screen__.get_width() - 20, 10)
        self.__screen__.blit(text_surface, text_rect)
    
    def __draw_message(self) -> None:
        """Renderiza y muestra el mensaje de estado actual."""
        text_surface = self.__font__.render(self.__message__, True, self.__white__)
        text_rect = text_surface.get_rect(center=(self.__screen__.get_width() / 2, 25))
        self.__screen__.blit(text_surface, text_rect)

    def __draw_dice(self) -> None:
        """Dibuja los dos dados en el centro del tablero."""
        dice_size = 80
        margin = 20
        x1 = self.__board_margin__ + (self.__board_width__ / 2) - self.__bar_width__ - dice_size - margin
        x2 = self.__board_margin__ + (self.__board_width__ / 2) + self.__bar_width__ + margin
        y = (self.__screen__.get_height() / 2) - (dice_size / 2)
        
        dice_rect1 = pygame.Rect(x1, y, dice_size, dice_size)
        dice_rect2 = pygame.Rect(x2, y, dice_size, dice_size)
        
        pygame.draw.rect(self.__screen__, self.__dice_color__, dice_rect1, border_radius=10)
        pygame.draw.rect(self.__screen__, self.__dice_color__, dice_rect2, border_radius=10)
        
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
        # Punto 1=claro, 2=oscuro, 3=claro, 4=oscuro, 5=claro, 6=oscuro
        start_x_top_right = self.__board_margin__ + side_width + self.__bar_width__
        for i in range(6):
            x = start_x_top_right + ((5 - i) * point_width) 
            y = self.__board_margin__
            color = self.__brown_light__ if i % 2 == 0 else self.__brown_dark__
            self.__draw_triangle_point(x, y, point_width, point_height, color, pointing_down=True)
            
        # Cuadrante superior izquierdo (puntos 7-12)
        # Punto 7=claro, 8=oscuro, 9=claro, 10=oscuro, 11=claro, 12=oscuro
        start_x_top_left = self.__board_margin__
        for i in range(6):
            x = start_x_top_left + i * point_width
            y = self.__board_margin__
            color = self.__brown_light__ if i % 2 == 0 else self.__brown_dark__
            self.__draw_triangle_point(x, y, point_width, point_height, color, pointing_down=True)
            
        # Cuadrante inferior izquierdo (puntos 13-18)
        # Punto 13=oscuro, 14=claro, 15=oscuro, 16=claro, 17=oscuro, 18=claro
        for i in range(6):
            x = start_x_top_left + i * point_width
            y = self.__board_margin__ + self.__board_height__ - point_height
            color = self.__brown_dark__ if i % 2 == 0 else self.__brown_light__
            self.__draw_triangle_point(x, y, point_width, point_height, color, pointing_down=False)
            
        # Cuadrante inferior derecho (puntos 19-24)
        # Punto 19=oscuro, 20=claro, 21=oscuro, 22=claro, 23=oscuro, 24=claro
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