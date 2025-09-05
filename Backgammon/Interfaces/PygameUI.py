import pygame
import sys
from typing import Tuple, Optional

class PygameUI:
    def __init__(self, board_width: int = 800, board_height: int = 600):
        """Interfaz gráfica para el juego de Backgammon usando pygame."""
        pygame.init()
        self.__screen = pygame.display.set_mode((board_width, board_height))
        self.__clock = pygame.time.Clock()
        self.__running = True
        
    def run(self) -> None:
        """Loop principal del juego."""
        while self.__running:
            self.__handle_events()
            self.__update()
            self.__draw()
            self.__clock.tick(60)  # 60 FPS
            
    def __handle_events(self) -> None:
        """Maneja los eventos del usuario."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False
                
    def __update(self) -> None:
        """Actualiza el estado del juego."""
        pass
        
    def __draw(self) -> None:
        """Dibuja todos los elementos en pantalla."""
        self.__screen.fill((255, 255, 255))  # Fondo blanco
        pygame.display.flip()

if __name__ == "__main__":
    game = PygameUI()
    game.run()