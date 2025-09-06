import pygame
import sys
from typing import Tuple, Optional

class PygameUI:
    def __init__(self, board_width: int = 1280, board_height: int = 720):
        """Interfaz gráfica para el juego de Backgammon usando pygame."""
        pygame.init()
        self.__screen = pygame.display.set_mode((board_width, board_height))
        pygame.display.set_caption("Backgammon - Prueba de Interfaz")
        self.__clock = pygame.time.Clock()
        self.__running = True
        
        # Colores para las figuras de prueba
        self.__white = (255, 255, 255)
        self.__black = (0, 0, 0)
        self.__red = (255, 0, 0)
        self.__blue = (0, 0, 255)
        self.__green = (0, 255, 0)
        self.__gray = (128, 128, 128)
        
    def run(self) -> None:
        """Loop principal del juego."""
        while self.__running:
            self.__handle_events()
            self.__update()
            self.__draw()
            self.__clock.tick(60)  # 60 FPS
        
        pygame.quit()
        sys.exit()
            
    def __handle_events(self) -> None:
        """Maneja los eventos del usuario."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.__running = False
                    
    def __update(self) -> None:
        """Actualiza el estado del juego."""
        pass
        
    def __draw(self) -> None:
        """Dibuja todos los elementos en pantalla."""
        # Limpiar pantalla con fondo gris claro
        self.__screen.fill((240, 240, 240))
        
        # Dibujar figuras de prueba
        self.__draw_test_shapes()
        
        # Actualizar pantalla
        pygame.display.flip()
    
    def __draw_test_shapes(self) -> None:
        """Dibuja figuras de prueba para verificar que pygame funciona."""
        
        # Cuadrado rojo con círculo azul adentro (izquierda)
        square_rect = pygame.Rect(200, 260, 200, 200)
        pygame.draw.rect(self.__screen, self.__red, square_rect)
        pygame.draw.rect(self.__screen, self.__black, square_rect, 4)  # Borde negro
        
        # Círculo azul dentro del cuadrado
        circle_center = (square_rect.centerx, square_rect.centery)
        pygame.draw.circle(self.__screen, self.__blue, circle_center, 80)
        pygame.draw.circle(self.__screen, self.__black, circle_center, 80, 3)  # Borde negro
        
        # Rectángulo verde (centro)
        green_rect = pygame.Rect(540, 260, 280, 150)
        pygame.draw.rect(self.__screen, self.__green, green_rect)
        pygame.draw.rect(self.__screen, self.__black, green_rect, 3)
        
        # Círculo amarillo independiente (derecha)
        pygame.draw.circle(self.__screen, (255, 255, 0), (1000, 360), 60)
        pygame.draw.circle(self.__screen, self.__black, (1000, 360), 60, 3)
        
        # Líneas de prueba (cruz que divide la pantalla)
        pygame.draw.line(self.__screen, self.__black, (100, 550), (1180, 550), 4)  # Horizontal
        pygame.draw.line(self.__screen, self.__red, (640, 100), (640, 620), 3)      # Vertical centro
        
        # Pequeños círculos en las esquinas
        corners = [(80, 80), (1200, 80), (80, 640), (1200, 640)]
        for corner in corners:
            pygame.draw.circle(self.__screen, self.__gray, corner, 20)
        
        # Título en la parte superior (usando texto básico con formas)
        # Rectángulo de fondo para el "título"
        title_rect = pygame.Rect(440, 50, 400, 80)
        pygame.draw.rect(self.__screen, self.__white, title_rect)
        pygame.draw.rect(self.__screen, self.__black, title_rect, 3)

if __name__ == "__main__":
    game = PygameUI()
    game.run()