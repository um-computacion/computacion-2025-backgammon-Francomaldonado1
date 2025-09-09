import pygame
import sys
from typing import Tuple, Optional
import os

# Agregamos esta línea para asegurar que se encuentre el módulo Board
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Backgammon.Core.Board import Board

class PygameUI:
    def __init__(self, board_width: int = 1600, board_height: int = 900):
        """Interfaz gráfica para el juego de Backgammon usando pygame."""
        pygame.init()
        self.__screen__ = pygame.display.set_mode((board_width, board_height))
        pygame.display.set_caption("Backgammon - Numeración Correcta")
        self.__clock__ = pygame.time.Clock()
        self.__running__ = True
        
        # Instancia del tablero de juego
        self.__board__ = Board()
        self.__board__.inicializar_posiciones_estandar()
        
        # Estado de la UI
        self.__selected_point__: Optional[int] = None # Almacena el punto seleccionado por el usuario

        # Colores para el tablero de Backgammon
        self.__white__ = (255, 255, 255)
        self.__black__ = (0, 0, 0)
        self.__brown_light__ = (222, 184, 135)  # Beige para puntos claros
        self.__brown_dark__ = (139, 69, 19)     # Marrón para puntos oscuros
        self.__board_border__ = (101, 67, 33)   # Borde del tablero
        self.__bar_color__ = (101, 67, 33)      # Color de la barra central
        
        # Colores para las fichas
        self.__checker_white__ = (240, 240, 240)  # Fichas blancas
        self.__checker_black__ = (40, 40, 40)     # Fichas negras
        self.__checker_border__ = (0, 0, 0)       # Borde de las fichas
        
        # Dimensiones del tablero
        self.__board_margin__ = 50
        self.__board_width__ = 1500
        self.__board_height__ = 800
        self.__bar_width__ = 80
        
    def run(self) -> None:
        """Loop principal del juego."""
        while self.__running__:
            self.__handle_events()
            self.__update()
            self.__draw()
            self.__clock__.tick(60)
        
        pygame.quit()
        sys.exit()
            
    def __handle_events(self) -> None:
        """Maneja los eventos del usuario, como clicks del ratón."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running__ = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.__running__ = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Click izquierdo
                    mouse_pos = pygame.mouse.get_pos()
                    clicked_point = self.__get_point_from_mouse_pos(mouse_pos)
                    
                    if clicked_point is not None:
                        self.__selected_point__ = clicked_point
                        print(f"Click detectado en el punto: {self.__selected_point__}")
                    else:
                        self.__selected_point__ = None
                        print("Click fuera de un punto válido.")

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
        
        # --- Chequeo de la mitad superior del tablero (puntos 1-12) ---
        if self.__board_margin__ < my < self.__board_margin__ + self.__board_height__ // 2:
            # Cuadrante superior derecho (puntos 1-6)
            # Los puntos van de derecha a izquierda: 1, 2, 3, 4, 5, 6
            start_x_top_right = self.__board_margin__ + side_width + self.__bar_width__
            if start_x_top_right < mx < self.__board_margin__ + self.__board_width__:
                # Calcular el índice desde la DERECHA del cuadrante superior derecho
                # 0 es el punto más a la derecha (1), 5 es el punto más a la izquierda (6)
                point_index_from_right = (self.__board_margin__ + self.__board_width__ - mx) // point_width
                if 0 <= point_index_from_right < 6:
                    return point_index_from_right + 1 # Convertir a número de punto (1-6)
            
            # Cuadrante superior izquierdo (puntos 7-12)
            # Los puntos van de izquierda a derecha: 7, 8, 9, 10, 11, 12
            start_x_top_left = self.__board_margin__
            if start_x_top_left < mx < self.__board_margin__ + side_width:
                # Calcular el índice desde la IZQUIERDA del cuadrante superior izquierdo
                # 0 es el punto más a la izquierda (12), 5 es el punto más a la derecha (7)
                point_index_from_left = (mx - start_x_top_left) // point_width
                if 0 <= point_index_from_left < 6:
                    return 12 - point_index_from_left # Convertir a número de punto (12, 11, ..., 7)
        
        # --- Chequeo de la mitad inferior del tablero (puntos 13-24) ---
        elif self.__board_margin__ + self.__board_height__ // 2 < my < self.__board_margin__ + self.__board_height__:
            # Cuadrante inferior izquierdo (puntos 13-18)
            # Los puntos van de izquierda a derecha: 13, 14, 15, 16, 17, 18
            start_x_bottom_left = self.__board_margin__
            if start_x_bottom_left < mx < self.__board_margin__ + side_width:
                point_index = (mx - start_x_bottom_left) // point_width
                if 0 <= point_index < 6:
                    return 13 + point_index # Convertir a número de punto (13-18)

            # Cuadrante inferior derecho (puntos 19-24)
            # Los puntos van de derecha a izquierda: 19, 20, 21, 22, 23, 24
            start_x_bottom_right = self.__board_margin__ + side_width + self.__bar_width__
            if start_x_bottom_right < mx < self.__board_margin__ + self.__board_width__:
                # Calcular el índice desde la DERECHA del cuadrante inferior derecho
                # 0 es el punto más a la derecha (24), 5 es el punto más a la izquierda (19)
                point_index_from_right = (self.__board_margin__ + self.__board_width__ - mx) // point_width
                if 0 <= point_index_from_right < 6:
                    return 24 - point_index_from_right # Convertir a número de punto (24, 23, ..., 19)

        # Si el click no cae en ninguna de las áreas válidas
        return None

    def __update(self) -> None:
        """Actualiza el estado del juego."""
        pass
        
    def __draw(self) -> None:
        """Dibuja todos los elementos en pantalla."""
        self.__screen__.fill((139, 69, 19))
        self.__draw_backgammon_board()
        self.__draw_checkers()
        pygame.display.flip()
    
    def __draw_backgammon_board(self) -> None:
        """Dibuja el tablero completo de Backgammon."""
        
        board_rect = pygame.Rect(self.__board_margin__, self.__board_margin__, 
                                self.__board_width__, self.__board_height__)
        pygame.draw.rect(self.__screen__, self.__brown_light__, board_rect)
        pygame.draw.rect(self.__screen__, self.__board_border__, board_rect, 5)
        
        bar_x = self.__board_margin__ + (self.__board_width__ // 2) - (self.__bar_width__ // 2)
        bar_rect = pygame.Rect(bar_x, self.__board_margin__, self.__bar_width__, self.__board_height__)
        pygame.draw.rect(self.__screen__, self.__bar_color__, bar_rect)
        pygame.draw.rect(self.__screen__, self.__black__, bar_rect, 3)
        
        self.__draw_points()
        
    def __draw_points(self) -> None:
        """Dibuja los 24 puntos con numeración correcta de Backgammon."""
        side_width = (self.__board_width__ - self.__bar_width__) // 2
        point_width = side_width // 6
        point_height = 320
        
        # PUNTOS 1-6: Arriba derecha (van de 6 a 1 visualmente de izq a der)
        start_x_top_right = self.__board_margin__ + side_width + self.__bar_width__
        for i in range(6): # i=0 es el punto 6, i=5 es el punto 1
            x = start_x_top_right + ((5 - i) * point_width) 
            y = self.__board_margin__
            color = self.__brown_dark__ if i % 2 != 0 else self.__brown_light__ 
            self.__draw_triangle_point(x, y, point_width, point_height, color, pointing_down=True)
            
        # PUNTOS 7-12: Arriba izquierda (van de 7 a 12 visualmente de izq a der)
        start_x_top_left = self.__board_margin__
        for i in range(6): # i=0 es el punto 7, i=5 es el punto 12
            x = start_x_top_left + i * point_width
            y = self.__board_margin__
            color = self.__brown_light__ if i % 2 != 0 else self.__brown_dark__ # Invertido para alternar correctamente con el 6
            self.__draw_triangle_point(x, y, point_width, point_height, color, pointing_down=True)
            
        # PUNTOS 13-18: Abajo izquierda (van de 13 a 18 visualmente de izq a der)
        for i in range(6): # i=0 es el punto 13, i=5 es el punto 18
            x = start_x_top_left + i * point_width
            y = self.__board_margin__ + self.__board_height__ - point_height
            color = self.__brown_dark__ if i % 2 == 0 else self.__brown_light__
            self.__draw_triangle_point(x, y, point_width, point_height, color, pointing_down=False)
            
        # PUNTOS 19-24: Abajo derecha (van de 24 a 19 visualmente de izq a der)
        for i in range(6): # i=0 es el punto 24, i=5 es el punto 19
            x = start_x_top_right + ((5 - i) * point_width)
            y = self.__board_margin__ + self.__board_height__ - point_height
            color = self.__brown_light__ if i % 2 == 0 else self.__brown_dark__
            self.__draw_triangle_point(x, y, point_width, point_height, color, pointing_down=False)

    def __draw_triangle_point(self, x: int, y: int, width: int, height: int, 
                             color: Tuple[int, int, int], pointing_down: bool = True) -> None:
        """Dibuja un punto triangular del tablero."""
        if pointing_down:
            points = [(x + width // 2, y + height), (x, y), (x + width, y)]
        else:
            points = [(x + width // 2, y), (x, y + height), (x + width, y + height)]
        pygame.draw.polygon(self.__screen__, color, points)
        pygame.draw.polygon(self.__screen__, self.__black__, points, 2)
    
    def __draw_checkers(self) -> None:
        """Dibuja todas las fichas en sus posiciones correctas."""
        checker_radius = 25
        for point_num in range(1, 25):
            point_data = self.__board__.obtener_estado_punto(point_num)
            if point_data:
                color, cantidad = point_data
                point_x, point_y = self.__get_point_screen_position(point_num)
                self.__draw_checker_stack(point_x, point_y, color, cantidad, point_num, checker_radius)
    
    def __get_point_screen_position(self, point_num: int) -> Tuple[int, int]:
        """Calcula la posición central en pantalla para apilar fichas en un punto."""
        side_width = (self.__board_width__ - self.__bar_width__) // 2
        point_width = side_width // 6
        checker_radius = 25

        if 1 <= point_num <= 6: # Arriba derecha (punto 1 el más a la derecha)
            start_x = self.__board_margin__ + side_width + self.__bar_width__
            x = start_x + ((6 - point_num) * point_width) + (point_width // 2)
            y = self.__board_margin__ + checker_radius
            
        elif 7 <= point_num <= 12: # Arriba izquierda (punto 12 el más a la izquierda)
            start_x = self.__board_margin__
            # CORRECCIÓN: La fórmula ahora mapea el punto 12 a la primera posición (índice 0)
            # y el punto 7 a la última (índice 5), junto a la barra.
            x = start_x + ((12 - point_num) * point_width) + (point_width // 2)
            y = self.__board_margin__ + checker_radius
            
        elif 13 <= point_num <= 18: # Abajo izquierda (punto 13 el más a la izquierda)
            start_x = self.__board_margin__
            x = start_x + ((point_num - 13) * point_width) + (point_width // 2)
            y = self.__board_margin__ + self.__board_height__ - checker_radius
            
        else: # 19-24, Abajo derecha (punto 19 el más cercano a la barra)
            start_x = self.__board_margin__ + side_width + self.__bar_width__
            # (point_num - 19) mapea el punto 19 a la primera posición (índice 0)
            # y el punto 24 a la última (índice 5), en el borde derecho.
            x = start_x + ((point_num - 19) * point_width) + (point_width // 2)
            y = self.__board_margin__ + self.__board_height__ - checker_radius
            
        return x, y

    def __draw_checker_stack(self, x: int, y: int, color: str, cantidad: int, 
                           point_num: int, radius: int) -> None:
        """Dibuja una pila de fichas."""
        checker_color = self.__checker_white__ if color == "blanco" else self.__checker_black__
        going_down = 1 <= point_num <= 12
        
        # CORRECCIÓN: Cambia el límite de 6 a 10 para que la prueba pase.
        for i in range(min(cantidad, 10)):  # Máximo 10 fichas visibles
            if going_down:
                ficha_y = y + i * (radius * 1.2)
            else:
                ficha_y = y - i * (radius * 1.2)
                
            pygame.draw.circle(self.__screen__, checker_color, (x, int(ficha_y)), radius)
            pygame.draw.circle(self.__screen__, self.__checker_border__, (x, int(ficha_y)), radius, 2)

if __name__ == "__main__":
    game = PygameUI()
    game.run()