"""Clase Checker del juego."""

class Checker:
    """
    Ficha de Backgammon con color y posición.
    
    PRINCIPIOS SOLID:
    - SRP: Responsabilidad única - Representar una ficha del juego
    - ISP: Interfaz mínima - Solo expone atributos esenciales (color, posición)
    - OCP: Extensible sin modificación - Puede heredarse para variantes
    
    Ver justificacion.md para detalles del diseño minimalista.
    """

    def __init__(self, color: str, posicion: int | None = None):
        """
        Crea una ficha.

        Args:
            color (str): Color de la ficha ('blanco' o 'negro').
            posicion (int | None): Punto del tablero (1 a 24) o None si está fuera.
        """
        self.__color__ = color
        self.__posicion__ = posicion

    def obtener_color(self) -> str:
        """Devuelve el color de la ficha."""
        return self.__color__

    def obtener_posicion(self) -> int | None:
        """Devuelve la posición actual de la ficha."""
        return self.__posicion__

    def establecer_posicion(self, nueva_posicion: int | None) -> None:
        """
        Actualiza la posición de la ficha.
        
        SRP: Modificación simple de estado sin lógica de negocio.
        """
        self.__posicion__ = nueva_posicion

    def esta_fuera(self) -> bool:
        """
        Indica si la ficha está fuera del tablero.
        
        SRP: Consulta simple de estado sin dependencias externas.
        """
        return self.__posicion__ is None

    def __str__(self) -> str:
        """Devuelve una representación legible de la ficha."""
        return f"Ficha(color={self.__color__}, posicion={self.__posicion__})"