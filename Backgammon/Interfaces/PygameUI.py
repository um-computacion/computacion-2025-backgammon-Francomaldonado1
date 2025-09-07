import pygame
import sys
from typing import Tuple, Optional
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Core'))
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
            self.__clock__.tick(60)  # 60 FPS
        
        pygame.quit()
        sys.exit()
            
    def __handle_events(self) -> None:
        """Maneja los eventos del usuario."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running__ = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.__running__ = False
                    
    def __update(self) -> None:
        """Actualiza el estado del juego."""
        pass
        
    def __draw(self) -> None:
        """Dibuja todos los elementos en pantalla."""
        # Limpiar pantalla con fondo marrón como tablero de madera
        self.__screen__.fill((139, 69, 19))
        
        # Dibujar tablero de Backgammon
        self.__draw_backgammon_board()
        
        # Dibujar las fichas del juego
        self.__draw_checkers()
        
        # Actualizar pantalla
        pygame.display.flip()
    
    def __draw_backgammon_board(self) -> None:
        """Dibuja el tablero completo de Backgammon."""
        
        board_rect = pygame.Rect(self.__board_margin__, self.__board_margin__, 
                                self.__board_width__, self.__board_height__)
        
        # Dibujar fondo del tablero
        pygame.draw.rect(self.__screen__, self.__brown_light__, board_rect)
        pygame.draw.rect(self.__screen__, self.__board_border__, board_rect, 5)
        
        # Dibujar barra central
        bar_x = self.__board_margin__ + (self.__board_width__ // 2) - (self.__bar_width__ // 2)
        bar_rect = pygame.Rect(bar_x, self.__board_margin__, self.__bar_width__, self.__board_height__)
        pygame.draw.rect(self.__screen__, self.__bar_color__, bar_rect)
        pygame.draw.rect(self.__screen__, self.__black__, bar_rect, 3)
        
        # Dibujar los 24 puntos
        self.__draw_points()
        
    def __draw_points(self) -> None:
        """Dibuja los 24 puntos con numeración correcta de Backgammon."""
        
        side_width = (self.__board_width__ - self.__bar_width__) // 2  # 710 píxeles por lado
        point_width = side_width // 6  # 118 píxeles por triángulo
        point_height = 320
        
        # PUNTOS 1-6: Arriba derecha (1 más a la derecha, 6 más a la izquierda)
        start_x_top_right = self.__board_margin__ + side_width + self.__bar_width__
        for i in range(6):
            point_num = i + 1  # Puntos 1, 2, 3, 4, 5, 6
            x = start_x_top_right + ((5-i) * point_width)  # 1 está más a la derecha
            y = self.__board_margin__ + 10
            color = self.__brown_dark__ if i % 2 == 0 else self.__brown_light__
            self.__draw_triangle_point(x, y, point_width, point_height, color, pointing_down=True)
            
        # PUNTOS 7-12: Arriba izquierda (7 más a la izquierda, 12 más a la derecha)
        start_x_top_left = self.__board_margin__
        for i in range(6):
            point_num = i + 7  # Puntos 7, 8, 9, 10, 11, 12
            x = start_x_top_left + (i * point_width)  # 7 está más a la izquierda
            y = self.__board_margin__ + 10
            color = self.__brown_light__ if i % 2 == 0 else self.__brown_dark__
            self.__draw_triangle_point(x, y, point_width, point_height, color, pointing_down=True)
            
        # PUNTOS 13-18: Abajo izquierda (13 más a la izquierda, 18 más a la derecha)
        for i in range(6):
            point_num = i + 13  # Puntos 13, 14, 15, 16, 17, 18
            x = start_x_top_left + (i * point_width)  # 13 está más a la izquierda
            y = self.__board_margin__ + self.__board_height__ - point_height - 10
            color = self.__brown_dark__ if i % 2 == 0 else self.__brown_light__
            self.__draw_triangle_point(x, y, point_width, point_height, color, pointing_down=False)
            
        # PUNTOS 19-24: Abajo derecha (19 más a la izquierda, 24 más a la derecha)
        for i in range(6):
            point_num = i + 19  # Puntos 19, 20, 21, 22, 23, 24
            x = start_x_top_right + ((5-i) * point_width)  # 24 está más a la derecha
            y = self.__board_margin__ + self.__board_height__ - point_height - 10
            color = self.__brown_light__ if i % 2 == 0 else self.__brown_dark__
            self.__draw_triangle_point(x, y, point_width, point_height, color, pointing_down=False)
    
    def __draw_triangle_point(self, x: int, y: int, width: int, height: int, 
                             color: Tuple[int, int, int], pointing_down: bool = True) -> None:
        """Dibuja un punto triangular del tablero."""
        
        if pointing_down:
            points = [
                (x + width // 2, y + height),  # Punto inferior (punta)
                (x, y),                        # Esquina superior izquierda
                (x + width, y)                 # Esquina superior derecha
            ]
        else:
            points = [
                (x + width // 2, y),          # Punto superior (punta)
                (x, y + height),              # Esquina inferior izquierda  
                (x + width, y + height)       # Esquina inferior derecha
            ]
            
        pygame.draw.polygon(self.__screen__, color, points)
        pygame.draw.polygon(self.__screen__, self.__black__, points, 2)
    
    def __draw_checkers(self) -> None:
        """Dibuja todas las fichas en sus posiciones correctas."""
        
        checker_radius = 25
        
        for point_num in range(1, 25):  # Puntos 1-24
            try:
                point_data = self.__board__.obtener_estado_punto(point_num)
                
                if point_data is not None:
                    color = point_data[0]      # color: "negro" o "blanco"
                    cantidad = point_data[1]   # cantidad de fichas
                    
                    if cantidad > 0:
                        # Obtener posición del punto
                        point_x, point_y = self.__get_point_screen_position(point_num)
                        
                        # Dibujar fichas apiladas
                        self.__draw_checker_stack(point_x, point_y, color, cantidad, 
                                                point_num, checker_radius)
                        
            except Exception as e:
                print(f"Error en punto {point_num}: {e}")
                continue
    
    def __get_point_screen_position(self, point_num: int) -> Tuple[int, int]:
        """Calcula la posición exacta en pantalla de cada punto según numeración Backgammon."""
        
        side_width = (self.__board_width__ - self.__bar_width__) // 2  # 710 píxeles por lado
        point_width = side_width // 6  # 118 píxeles por triángulo
        
        if 1 <= point_num <= 6:  # PUNTOS 1-6: Arriba derecha
            start_x = self.__board_margin__ + side_width + self.__bar_width__
            # Punto 1 es el más a la derecha (posición 5), punto 6 el más a la izquierda (posición 0)
            x = start_x + ((6 - point_num) * point_width) + (point_width // 2)
            y = self.__board_margin__ + 50
            
        elif 7 <= point_num <= 12:  # PUNTOS 7-12: Arriba izquierda  
            start_x = self.__board_margin__
            # Punto 7 es el más cerca de la barra (posición 5), punto 12 el más a la izquierda (posición 0)
            x = start_x + ((12 - point_num) * point_width) + (point_width // 2)
            y = self.__board_margin__ + 50
            
        elif 13 <= point_num <= 18:  # PUNTOS 13-18: Abajo izquierda
            start_x = self.__board_margin__
            # Punto 13 es el más a la izquierda (posición 0), punto 18 el más cerca de la barra (posición 5)
            x = start_x + ((point_num - 13) * point_width) + (point_width // 2)
            y = self.__board_margin__ + self.__board_height__ - 50
            
        else:  # PUNTOS 19-24: Abajo derecha
            start_x = self.__board_margin__ + side_width + self.__bar_width__
            # Punto 19 es el más cerca de la barra (posición 0), punto 24 el más a la derecha (posición 5)
            x = start_x + ((point_num - 19) * point_width) + (point_width // 2)
            y = self.__board_margin__ + self.__board_height__ - 50
            
        return (x, y)
    
    def __draw_checker_stack(self, x: int, y: int, color: str, cantidad: int, 
                           point_num: int, radius: int) -> None:
        """Dibuja una pila de fichas."""
        
        # Color de la ficha
        checker_color = self.__checker_white__ if color == "blanco" else self.__checker_black__
        
        # Dirección del apilamiento
        going_up = point_num >= 13  # Puntos 13-24 van hacia arriba
        
        # Dibujar cada ficha
        for i in range(min(cantidad, 10)):  # Máximo 10 fichas visibles
            if going_up:
                ficha_y = y - (i * (radius // 2))
            else:
                ficha_y = y + (i * (radius // 2))
                
            # Dibujar ficha
            pygame.draw.circle(self.__screen__, checker_color, (x, ficha_y), radius)
            pygame.draw.circle(self.__screen__, self.__checker_border__, (x, ficha_y), radius, 2)

if __name__ == "__main__":
    game = PygameUI()
    game.run()