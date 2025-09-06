import pygame
import sys
from typing import Tuple, Optional

class PygameUI:
    def __init__(self, board_width: int = 1600, board_height: int = 900):
        """Interfaz gráfica para el juego de Backgammon usando pygame."""
        pygame.init()
        self.__screen__ = pygame.display.set_mode((board_width, board_height))
        pygame.display.set_caption("Backgammon - Tablero Perfecto")
        self.__clock__ = pygame.time.Clock()
        self.__running__ = True
        
        # Colores para el tablero de Backgammon
        self.__white__ = (255, 255, 255)
        self.__black__ = (0, 0, 0)
        self.__brown_light__ = (222, 184, 135)  # Beige para puntos claros
        self.__brown_dark__ = (139, 69, 19)     # Marrón para puntos oscuros
        self.__board_border__ = (101, 67, 33)   # Borde del tablero
        self.__bar_color__ = (101, 67, 33)      # Color de la barra central
        
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
        
        # Actualizar pantalla
        pygame.display.flip()
    
    def __draw_backgammon_board(self) -> None:
        """Dibuja el tablero completo de Backgammon con dimensiones perfectas."""
        
        # Dimensiones calculadas para ocupar toda la pantalla
        board_margin = 50
        board_width = 1500   # Ocupa casi toda la pantalla
        board_height = 800   # Ocupa casi toda la altura
        board_rect = pygame.Rect(board_margin, board_margin, board_width, board_height)
        
        # Dibujar fondo del tablero
        pygame.draw.rect(self.__screen__, self.__brown_light__, board_rect)
        pygame.draw.rect(self.__screen__, self.__board_border__, board_rect, 5)
        
        # Dibujar barra central perfectamente centrada
        bar_width = 80
        bar_x = board_margin + (board_width // 2) - (bar_width // 2)
        bar_rect = pygame.Rect(bar_x, board_margin, bar_width, board_height)
        pygame.draw.rect(self.__screen__, self.__bar_color__, bar_rect)
        pygame.draw.rect(self.__screen__, self.__black__, bar_rect, 3)
        
        # Dibujar los 24 puntos perfectamente alineados
        self.__draw_points()
        
    def __draw_points(self) -> None:
        """Dibuja los 24 puntos perfectamente alineados y ocupando todo el espacio."""
        
        # Cálculos precisos para ocupar todo el espacio disponible
        board_margin = 50
        board_width = 1500
        board_height = 800  # Definir board_height aquí también
        bar_width = 80
        
        # Espacio disponible para cada lado (sin contar la barra)
        side_width = (board_width - bar_width) // 2  # 710 píxeles por lado
        point_width = side_width // 6  # 118 píxeles por triángulo
        point_height = 320  # Altura grande para los triángulos
        
        # LADO DERECHO - Cuadrante superior derecho (puntos 1-6)
        start_x_right = board_margin + side_width + bar_width
        for i in range(6):
            x = start_x_right + (i * point_width)
            y = board_margin + 10
            color = self.__brown_dark__ if i % 2 == 0 else self.__brown_light__
            self.__draw_triangle_point(x, y, point_width, point_height, color, pointing_down=True)
            
        # LADO IZQUIERDO - Cuadrante superior izquierdo (puntos 7-12)
        start_x_left = board_margin
        for i in range(6):
            x = start_x_left + ((5-i) * point_width)  # Orden inverso
            y = board_margin + 10
            color = self.__brown_light__ if i % 2 == 0 else self.__brown_dark__
            self.__draw_triangle_point(x, y, point_width, point_height, color, pointing_down=True)
            
        # LADO IZQUIERDO - Cuadrante inferior izquierdo (puntos 13-18)
        for i in range(6):
            x = start_x_left + (i * point_width)
            y = board_margin + board_height - point_height - 10
            color = self.__brown_dark__ if i % 2 == 0 else self.__brown_light__
            self.__draw_triangle_point(x, y, point_width, point_height, color, pointing_down=False)
            
        # LADO DERECHO - Cuadrante inferior derecho (puntos 19-24)
        for i in range(6):
            x = start_x_right + ((5-i) * point_width)  # Orden inverso
            y = board_margin + board_height - point_height - 10
            color = self.__brown_light__ if i % 2 == 0 else self.__brown_dark__
            self.__draw_triangle_point(x, y, point_width, point_height, color, pointing_down=False)
    
    def __draw_triangle_point(self, x: int, y: int, width: int, height: int, 
                             color: Tuple[int, int, int], pointing_down: bool = True) -> None:
        """Dibuja un punto triangular del tablero perfectamente."""
        
        if pointing_down:
            # Triángulo apuntando hacia abajo
            points = [
                (x + width // 2, y + height),  # Punto inferior (punta)
                (x, y),                        # Esquina superior izquierda
                (x + width, y)                 # Esquina superior derecha
            ]
        else:
            # Triángulo apuntando hacia arriba
            points = [
                (x + width // 2, y),          # Punto superior (punta)
                (x, y + height),              # Esquina inferior izquierda  
                (x + width, y + height)       # Esquina inferior derecha
            ]
            
        pygame.draw.polygon(self.__screen__, color, points)
        pygame.draw.polygon(self.__screen__, self.__black__, points, 2)

if __name__ == "__main__":
    game = PygameUI()
    game.run()