import pygame
import sys
from typing import Tuple, Optional
import os

# Agregamos la ruta para encontrar los módulos del Core
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Backgammon.Core.Board import Board
from Backgammon.Core.Dice import Dice # Se importa la clase para los dados

class PygameUI:
    def __init__(self, board_width: int = 1600, board_height: int = 900):
        """
        Inicializa la interfaz gráfica para el juego de Backgammon usando pygame.

        Args:
            board_width (int): Ancho de la ventana del juego.
            board_height (int): Alto de la ventana del juego.
        """
        pygame.init()
        self.__screen__ = pygame.display.set_mode((board_width, board_height))
        pygame.display.set_caption("Backgammon")
        self.__clock__ = pygame.time.Clock()
        self.__running__ = True
        
        # --- Lógica de la partida ---
        self.__game_state__ = 'START_ROLL' # Estados posibles: 'START_ROLL', 'GAMEPLAY'
        self.__dice__ = Dice()
        self.__dice_rolls__ = [0, 0] # Almacena el resultado de los dados: [Dado 1, Dado 2]
        self.__current_player__ = None # Puede ser 'negro' o 'blanco'
        self.__font__ = pygame.font.Font(None, 45)
        self.__message__ = "Presiona 'R' para decidir quién empieza."

        # Instancia del tablero de juego
        self.__board__ = Board()
        self.__board__.inicializar_posiciones_estandar()
        
        # Estado de la UI
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
        
        # --- Dimensiones del Tablero ---
        self.__board_margin__ = 50
        self.__board_width__ = 1500
        self.__board_height__ = 800
        self.__bar_width__ = 80
        
    def run(self) -> None:
        """
        Inicia el bucle principal del juego, que maneja eventos, actualizaciones y renderizado.
        """
        while self.__running__:
            self.__handle_events()
            self.__update()
            self.__draw()
            self.__clock__.tick(60)
        
        pygame.quit()
        sys.exit()
            
    def __handle_events(self) -> None:
        """
        Gestiona todas las entradas del usuario, como cerrar la ventana,
        presionar teclas y hacer clics con el ratón.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running__ = False
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.__running__ = False
                
                # Si el juego está en la fase de tirada inicial, la tecla 'R' tira los dados.
                if event.key == pygame.K_r and self.__game_state__ == 'START_ROLL':
                    self.__roll_to_start()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Click izquierdo
                    # La detección de clics en el tablero solo se activa después de la tirada inicial.
                    if self.__game_state__ == 'GAMEPLAY':
                        mouse_pos = pygame.mouse.get_pos()
                        clicked_point = self.__get_point_from_mouse_pos(mouse_pos)
                        
                        if clicked_point is not None:
                            self.__selected_point__ = clicked_point
                            print(f"Click detectado en el punto: {self.__selected_point__}")
                        else:
                            self.__selected_point__ = None
                            print("Click fuera de un punto válido.")


    def __roll_to_start(self):
        """
        Realiza la tirada de un dado por jugador para determinar quién empieza.
        Utiliza el método tirar() de la clase Dice y maneja los empates.
        """
        self.__message__ = "Tirando los dados..."
        self.__draw()
        pygame.time.wait(400)

        # Tira los dados y obtiene los valores
        self.__dice__.tirar()
        roll1 = self.__dice__.obtener_dado1()
        roll2 = self.__dice__.obtener_dado2()
        
        # Vuelve a tirar si hay empate
        while roll1 == roll2:
            self.__dice__.tirar()
            roll1 = self.__dice__.obtener_dado1()
            roll2 = self.__dice__.obtener_dado2()
            
        self.__dice_rolls__ = [roll1, roll2]
        
        if roll1 > roll2:
            self.__current_player__ = "negro"
            self.__message__ = f"Negro saca un {roll1} y Blanco un {roll2}. ¡Empieza Negro!"
        else:
            self.__current_player__ = "blanco"
            self.__message__ = f"Blanco saca un {roll2} y Negro un {roll1}. ¡Empieza Blanco!"
            
        self.__game_state__ = 'GAMEPLAY'

    def __get_point_from_mouse_pos(self, mouse_pos: Tuple[int, int]) -> Optional[int]:
        """
        Calcula en qué punto del tablero (1-24) se hizo click.

        Args:
            mouse_pos (Tuple[int, int]): Las coordenadas (x, y) del click del ratón.

        Returns:
            Optional[int]: El número del punto (1-24) si el click fue en un punto válido,
                           o None si fue fuera de cualquier punto.
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
        """
        Actualiza la lógica del juego en cada frame. (Actualmente sin uso).
        """
        pass
        
    def __draw(self) -> None:
        """
        Dibuja todos los elementos del juego en la pantalla, incluyendo el tablero,
        las fichas, los dados y los mensajes de estado.
        """
        self.__screen__.fill((139, 69, 19))
        self.__draw_backgammon_board()
        self.__draw_checkers()
        self.__draw_message()
        
        if self.__dice_rolls__[0] != 0:
            self.__draw_dice()
            
        pygame.display.flip()
    
    def __draw_message(self):
        """
        Renderiza y muestra el mensaje de estado actual en la parte superior central de la pantalla.
        """
        text_surface = self.__font__.render(self.__message__, True, self.__white__)
        text_rect = text_surface.get_rect(center=(self.__screen__.get_width() / 2, 25))
        self.__screen__.blit(text_surface, text_rect)

    def __draw_dice(self):
        """
        Dibuja los dos dados en el centro del tablero, a cada lado de la barra central,
        mostrando los resultados de la última tirada.
        """
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

    def __draw_pips(self, rect: pygame.Rect, number: int):
        """
        Dibuja los puntos (pips) en la cara de un dado según el número resultado.

        Args:
            rect (pygame.Rect): El rectángulo que define la superficie del dado.
            number (int): El número (de 1 a 6) a representar con pips.
        """
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
        """Dibuja el tablero de Backgammon, incluyendo el fondo, borde y la barra central."""
        board_rect = pygame.Rect(self.__board_margin__, self.__board_margin__, self.__board_width__, self.__board_height__)
        pygame.draw.rect(self.__screen__, self.__brown_light__, board_rect)
        pygame.draw.rect(self.__screen__, self.__board_border__, board_rect, 5)
        
        bar_x = self.__board_margin__ + (self.__board_width__ // 2) - (self.__bar_width__ // 2)
        bar_rect = pygame.Rect(bar_x, self.__board_margin__, self.__bar_width__, self.__board_height__)
        pygame.draw.rect(self.__screen__, self.__bar_color__, bar_rect)
        pygame.draw.rect(self.__screen__, self.__black__, bar_rect, 3)
        
        self.__draw_points()
        
    def __draw_points(self) -> None:
        """Dibuja los 24 puntos triangulares del tablero con colores alternados."""
        side_width = (self.__board_width__ - self.__bar_width__) // 2
        point_width = side_width // 6
        point_height = 320
        
        start_x_top_right = self.__board_margin__ + side_width + self.__bar_width__
        for i in range(6):
            x = start_x_top_right + ((5 - i) * point_width) 
            y = self.__board_margin__
            color = self.__brown_dark__ if i % 2 != 0 else self.__brown_light__ 
            self.__draw_triangle_point(x, y, point_width, point_height, color, pointing_down=True)
            
        start_x_top_left = self.__board_margin__
        for i in range(6):
            x = start_x_top_left + i * point_width
            y = self.__board_margin__
            color = self.__brown_light__ if i % 2 != 0 else self.__brown_dark__
            self.__draw_triangle_point(x, y, point_width, point_height, color, pointing_down=True)
            
        for i in range(6):
            x = start_x_top_left + i * point_width
            y = self.__board_margin__ + self.__board_height__ - point_height
            color = self.__brown_dark__ if i % 2 == 0 else self.__brown_light__
            self.__draw_triangle_point(x, y, point_width, point_height, color, pointing_down=False)
            
        for i in range(6):
            x = start_x_top_right + ((5 - i) * point_width)
            y = self.__board_margin__ + self.__board_height__ - point_height
            color = self.__brown_light__ if i % 2 == 0 else self.__brown_dark__
            self.__draw_triangle_point(x, y, point_width, point_height, color, pointing_down=False)

    def __draw_triangle_point(self, x: int, y: int, width: int, height: int, color: Tuple[int, int, int], pointing_down: bool = True) -> None:
        """
        Dibuja un único punto triangular en el tablero.

        Args:
            x (int): Coordenada x de la esquina superior izquierda del rectángulo del punto.
            y (int): Coordenada y de la esquina superior izquierda del rectángulo del punto.
            width (int): Ancho del punto.
            height (int): Alto del punto.
            color (Tuple[int, int, int]): Color RGB del punto.
            pointing_down (bool): True si el triángulo apunta hacia abajo, False si apunta hacia arriba.
        """
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
        """
        Calcula la posición central en la pantalla para apilar fichas en un punto específico.

        Args:
            point_num (int): El número del punto (1-24).

        Returns:
            Tuple[int, int]: Las coordenadas (x, y) del centro de la base del punto.
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

    def __draw_checker_stack(self, x: int, y: int, color: str, cantidad: int, point_num: int, radius: int) -> None:
        """
        Dibuja una pila de fichas en una posición específica.

        Args:
            x (int): Coordenada x del centro de la pila.
            y (int): Coordenada y de la base de la pila.
            color (str): "blanco" o "negro".
            cantidad (int): Número de fichas a dibujar.
            point_num (int): Número del punto para determinar la dirección del apilamiento.
            radius (int): Radio de cada ficha.
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