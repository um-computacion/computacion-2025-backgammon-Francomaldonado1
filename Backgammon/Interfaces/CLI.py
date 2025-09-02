from Backgammon.Core.Board import Board
from Backgammon.Core.Dice import Dice


class BackgammonCLI:
    """
    Interfaz de línea de comandos para el juego de Backgammon.
    """
    
    def __init__(self):
        self.board = Board()
        self.dados = Dice()
        self.jugador_negro = ""
        self.jugador_blanco = ""
        self.turno_actual = "negro"  # Negro siempre empieza
        
    def iniciar_juego(self):
        """
        Inicia el juego de Backgammon.
        """
        print("=" * 50)
        print("   🎲 BIENVENIDO AL BACKGAMMON 🎲")
        print("=" * 50)
        
        # Pedir nombres de jugadores
        self.jugador_negro = input("Ingrese el nombre del Jugador 1 (fichas negras): ").strip()
        self.jugador_blanco = input("Ingrese el nombre del Jugador 2 (fichas blancas): ").strip()
        
        if not self.jugador_negro:
            self.jugador_negro = "Jugador Negro"
        if not self.jugador_blanco:
            self.jugador_blanco = "Jugador Blanco"
            
        print(f"\n{self.jugador_negro} jugará con fichas NEGRAS")
        print(f"{self.jugador_blanco} jugará con fichas BLANCAS")
        
        # Inicializar tablero
        self.board.inicializar_posiciones_estandar()
        
        print("\n" + "=" * 50)
        print("TABLERO INICIAL:")
        print("=" * 50)
        self.mostrar_tablero()
        
        # Comenzar el juego
        self.loop_principal()
    
    def mostrar_tablero(self):
        """
        Muestra el estado actual del tablero en formato CLI.
        """
        print("\nESTADO DEL TABLERO:")
        print("-" * 60)
        
        # Mostrar puntos 1-12 (parte inferior primero)
        print("Puntos 1-12:")
        for i in range(1, 13):
            estado = self.board.obtener_estado_punto(i)
            if estado is None:
                print(f"  {i:2d}: vacío")
            else:
                color, cantidad = estado
                simbolo = "●" if color == "negro" else "○"
                print(f"  {i:2d}: {simbolo} x{cantidad} ({color})")
        
        print()
        
        # Mostrar barra
        barra = self.board.get_barra()
        if barra:
            print("BARRA:")
            for color, cantidad in barra.items():
                if cantidad > 0:
                    simbolo = "●" if color == "negro" else "○"
                    print(f"  {simbolo} x{cantidad} ({color})")
        else:
            print("BARRA: vacía")
            
        print()
        
        # Mostrar puntos 13-24 (parte superior después)
        print("Puntos 13-24:")
        for i in range(13, 25):
            estado = self.board.obtener_estado_punto(i)
            if estado is None:
                print(f"  {i:2d}: vacío")
            else:
                color, cantidad = estado
                simbolo = "●" if color == "negro" else "○"
                print(f"  {i:2d}: {simbolo} x{cantidad} ({color})")
        
        # Mostrar casa
        casa = self.board.get_casa()
        if casa:
            print("\nCASA:")
            for color, cantidad in casa.items():
                if cantidad > 0:
                    simbolo = "●" if color == "negro" else "○"
                    print(f"  {simbolo} x{cantidad} ({color})")
        else:
            print("\nCASA: vacía")
            
        print("-" * 60)
    
    def loop_principal(self):
        """
        Bucle principal del juego.
        """
        while True:
            # Verificar si alguien ganó
            if self.board.ha_ganado("negro"):
                print(f"\n🎉 ¡{self.jugador_negro} HA GANADO! 🎉")
                break
            elif self.board.ha_ganado("blanco"):
                print(f"\n🎉 ¡{self.jugador_blanco} HA GANADO! 🎉")
                break
            
            # Turno del jugador actual
            self.turno_jugador()
            
            # Cambiar turno
            self.turno_actual = "blanco" if self.turno_actual == "negro" else "negro"
    
    def turno_jugador(self):
        """
        Maneja el turno de un jugador.
        """
        nombre_jugador = self.jugador_negro if self.turno_actual == "negro" else self.jugador_blanco
        simbolo = "●" if self.turno_actual == "negro" else "○"
    
        print(f"\n{'='*20} TURNO DE {nombre_jugador.upper()} {simbolo} {'='*20}")
    
        # Tirar dados
        input(f"{nombre_jugador}, presiona ENTER para tirar los dados...")
        self.dados.tirar()
    
        print(f"\n🎲 {self.dados}")
    
        # Verificar movimientos posibles
        movimientos_posibles = self.board.obtener_movimientos_posibles(self.turno_actual, self.dados)
    
        if not movimientos_posibles:
            print(f"❌ No hay movimientos posibles para {nombre_jugador}. Se pierde el turno.")
            self.dados.reiniciar()
            return
    
        # Manejar movimientos según si hay dobles o no
        if self.dados.es_doble():
            self.manejar_dobles()
        else:
            self.manejar_movimientos_normales()
    
        # Reiniciar los dados después del turno
        self.dados.reiniciar()
    
    def mostrar_movimientos_disponibles(self):
        """
        Muestra los movimientos posibles para el jugador actual.
        """
        movimientos_posibles = self.board.obtener_movimientos_posibles(self.turno_actual, self.dados)
        
        if not movimientos_posibles:
            print("❌ No hay movimientos posibles.")
            return False
            
        print(f"\n📍 Movimientos posibles desde los puntos: {movimientos_posibles}")
        if 0 in movimientos_posibles:
            print("  (0 = barra)")
        return True
    
    def manejar_movimientos_normales(self):
        """
        Maneja los movimientos cuando no hay dobles.
        """
        movimientos_realizados = 0
        
        while movimientos_realizados < 2:
            # Verificar si aún hay movimientos posibles
            movimientos_posibles = self.board.obtener_movimientos_posibles(self.turno_actual, self.dados)
            if not movimientos_posibles:
                print("No hay más movimientos posibles.")
                break
                
            # Mostrar movimientos disponibles antes de cada movimiento
            print(f"\n📍 Movimientos posibles desde los puntos: {movimientos_posibles}")
            if 0 in movimientos_posibles:
                print("  (0 = barra)")
                
            print(f"\nMovimiento {movimientos_realizados + 1} de 2")
            print(f"Dados disponibles: {self.dados.obtener_dado1()}, {self.dados.obtener_dado2()}")
            
            # Preguntar tipo de movimiento
            print("\nOpciones:")
            print("1. Mover una ficha con un solo dado")
            print("2. Mover una ficha con ambos dados (movimiento doble)")
            print("3. Pasar turno (si no hay movimientos válidos)")
            
            try:
                opcion = input("Seleccione una opción (1, 2 o 3): ").strip()
                
                if opcion == "1":
                    if self.realizar_movimiento_simple():
                        movimientos_realizados += 1
                elif opcion == "2":
                    if self.realizar_movimiento_doble():
                        movimientos_realizados = 2  # Movimiento doble cuenta como ambos dados
                        break
                elif opcion == "3":
                    print("Pasando turno...")
                    break
                else:
                    print("❌ Opción inválida. Seleccione 1, 2 o 3.")
                    
            except KeyboardInterrupt:
                print("\n\nJuego interrumpido.")
                exit()
    
    def manejar_dobles(self):
        """
        Maneja los movimientos cuando hay dobles (4 movimientos).
        """
        print(f"\n🎲 ¡DOBLES! Puedes hacer 4 movimientos con el valor {self.dados.obtener_dado1()}")
        
        movimientos_realizados = 0
        while movimientos_realizados < 4:
            movimientos_posibles = self.board.obtener_movimientos_posibles(self.turno_actual, self.dados)
            if not movimientos_posibles:
                print("No hay más movimientos posibles.")
                break
                
            # Mostrar movimientos disponibles antes de cada movimiento
            print(f"\n📍 Movimientos posibles desde los puntos: {movimientos_posibles}")
            if 0 in movimientos_posibles:
                print("  (0 = barra)")
                
            print(f"\nMovimiento {movimientos_realizados + 1} de 4")
            print("Opciones:")
            print("1. Realizar movimiento")
            print("2. Pasar turno")
            
            try:
                opcion = input("Seleccione una opción (1 o 2): ").strip()
                
                if opcion == "1":
                    if self.realizar_movimiento_simple():
                        movimientos_realizados += 1
                elif opcion == "2":
                    print("Pasando turno...")
                    break
                else:
                    print("❌ Opción inválida. Seleccione 1 o 2.")
                    
            except KeyboardInterrupt:
                print("\n\nJuego interrumpido.")
                exit()
    
    def realizar_movimiento_simple(self) -> bool:
        """
        Realiza un movimiento simple con un solo dado.
        
        Returns:
            bool: True si el movimiento fue exitoso, False en caso contrario.
        """
        try:
            # Pedir punto de origen
            origen_str = input("Desde qué punto quiere mover (0 para barra): ").strip()
            origen = int(origen_str)
            
            # Pedir qué dado usar (solo si no son dobles)
            if not self.dados.es_doble():
                print(f"Dados disponibles: {self.dados.obtener_dado1()}, {self.dados.obtener_dado2()}")
                dado_str = input("¿Qué dado quiere usar? (1 o 2): ").strip()
                
                if dado_str == "1":
                    usar_dado1 = True
                    usar_dado2 = False
                elif dado_str == "2":
                    usar_dado1 = False
                    usar_dado2 = True
                else:
                    print("❌ Debe seleccionar 1 o 2.")
                    return False
            else:
                # En dobles, ambos dados tienen el mismo valor
                usar_dado1 = True
                usar_dado2 = False
            
            # Realizar el movimiento
            exito = self.board.realizar_movimiento_completo(
                self.turno_actual, self.dados, origen, usar_dado1, usar_dado2
            )
            
            if exito:
                print("✅ Movimiento realizado exitosamente.")
                self.mostrar_tablero()
                return True
            else:
                print("❌ Movimiento inválido. Intente de nuevo.")
                return False
                
        except ValueError:
            print("❌ Por favor ingrese números válidos.")
            return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def realizar_movimiento_doble(self) -> bool:
        """
        Realiza un movimiento doble (una ficha usando ambos dados).
        
        Returns:
            bool: True si el movimiento fue exitoso, False en caso contrario.
        """
        try:
            origen_str = input("Desde qué punto quiere mover la ficha con ambos dados: ").strip()
            origen = int(origen_str)
            
            # Mostrar qué pasaría
            dado1, dado2 = self.dados.obtener_valores()
            intermedio = self.board.calcular_destino(origen, dado1, self.turno_actual)
            final = self.board.calcular_destino(intermedio, dado2, self.turno_actual)
            
            print(f"La ficha se moverá: {origen} → {intermedio} → {final}")
            
            confirmar = input("¿Confirma este movimiento? (s/n): ").strip().lower()
            if confirmar not in ['s', 'si', 'sí', 'y', 'yes']:
                return False
            
            # Realizar el movimiento
            exito = self.board.realizar_movimiento_doble(self.turno_actual, self.dados, origen)
            
            if exito:
                print("✅ Movimiento doble realizado exitosamente.")
                self.mostrar_tablero()
                return True
            else:
                print("❌ Movimiento doble inválido. Intente de nuevo.")
                return False
                
        except ValueError:
            print("❌ Por favor ingrese un número válido.")
            return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False


def main():
    """
    Función principal para ejecutar el juego.
    """
    juego = BackgammonCLI()
    try:
        juego.iniciar_juego()
    except KeyboardInterrupt:
        print("\n\n¡Hasta luego! 👋")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")


if __name__ == "__main__":
    main()