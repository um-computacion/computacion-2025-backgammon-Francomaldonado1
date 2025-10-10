"""Interfaz de línea de comandos para Backgammon."""
from Backgammon.Core.Board import Board
from Backgammon.Core.Dice import Dice


class CLI:
    """
    Interfaz de línea de comandos para el juego de Backgammon.

    Rol:
        - Capa de presentación (I/O) que comunica al usuario con el dominio.
    Principios SOLID:
        - SRP: La clase se ocupa exclusivamente de la interacción textual (entrada/salida).
        - OCP: Puede extenderse (por ejemplo, agregar opciones o soporte para GUI) sin modificar su núcleo.
        - LSP: Puede sustituirse por otra interfaz manteniendo el contrato público.
        - ISP: Expone una interfaz pequeña y coherente centrada en la interacción con el usuario.
        - DIP: Usa las clases del núcleo (Board, Dice) sin depender de sus implementaciones internas.
    """

    def __init__(self):
        """
        Inicializa la interfaz CLI.

        SRP: Configura el estado inicial de la interfaz (tablero, dados, jugadores, turno).
        DIP: Depende de las abstracciones del dominio sin modificar su implementación.
        """
        self.board = Board()
        self.dados = Dice()
        self.jugador_negro = ""
        self.jugador_blanco = ""
        self.turno_actual = "negro"

    def iniciar_juego(self):
        """
        Inicia el juego de Backgammon.

        SRP: Se encarga exclusivamente del flujo de inicio del juego.
        DIP: Interactúa con Board y Dice a través de sus métodos públicos.
        """
        print("=" * 50)
        print("   🎲 BIENVENIDO AL BACKGAMMON 🎲")
        print("=" * 50)

        self.jugador_negro = input("Ingrese el nombre del Jugador 1 (fichas ○): ").strip()
        self.jugador_blanco = input("Ingrese el nombre del Jugador 2 (fichas ●): ").strip()

        if not self.jugador_negro:
            self.jugador_negro = "Jugador 1"
        if not self.jugador_blanco:
            self.jugador_blanco = "Jugador 2"

        print(f"\n{self.jugador_negro} jugará con fichas ○ (NEGRAS)")
        print(f"{self.jugador_blanco} jugará con fichas ● (BLANCAS)")

        self.board.inicializar_posiciones_estandar()

        print("\n" + "=" * 50)
        print("TABLERO INICIAL:")
        print("=" * 50)
        self.mostrar_tablero()

        self.determinar_primer_jugador()
        self.loop_principal()

    def determinar_primer_jugador(self):
        """
        Determina quién comienza la partida tirando un dado cada jugador.

        SRP: Separa la lógica de determinación del flujo principal del juego.
        DIP: Depende del objeto Dice para las tiradas iniciales.
        """
        print("\n" + "=" * 50)
        print("DETERMINANDO QUIÉN EMPIEZA:")
        print("=" * 50)

        while True:
            input(f"\n{self.jugador_negro}, presiona ENTER para tirar tu dado...")
            self.dados.tirar()
            dado_negro = self.dados.obtener_dado1()
            print(f"🎲 {self.jugador_negro} sacó: {dado_negro}")

            input(f"\n{self.jugador_blanco}, presiona ENTER para tirar tu dado...")
            self.dados.tirar()
            dado_blanco = self.dados.obtener_dado1()
            print(f"🎲 {self.jugador_blanco} sacó: {dado_blanco}")

            if dado_negro > dado_blanco:
                print(f"\n🎯 ¡{self.jugador_negro} empieza el juego!")
                self.turno_actual = "negro"
                break
            elif dado_blanco > dado_negro:
                print(f"\n🎯 ¡{self.jugador_blanco} empieza el juego!")
                self.turno_actual = "blanco"
                break
            else:
                print("\n🔄 ¡Empate! Vuelvan a tirar...")

        print("=" * 50)

    def mostrar_tablero(self):
        """
        Muestra el estado actual del tablero en consola.

        SRP: Encargado únicamente de la presentación del estado del tablero.
        LSP: Puede reemplazarse por una interfaz visual sin afectar el flujo del juego.
        """
        print("\nESTADO DEL TABLERO:")
        print("-" * 80)

        print("🏠 CUADRANTE CASA NEGRO (Puntos 1-6):")
        for i in range(1, 7):
            estado = self.board.obtener_estado_punto(i)
            if estado is None:
                print(f"  {i:2d}: vacío")
            else:
                color, cantidad = estado
                simbolo = "○" if color == "negro" else "●"
                print(f"  {i:2d}: {simbolo} x{cantidad} ({color})")

        print("\n⬆️ CUADRANTE EXTERIOR NEGRO (Puntos 7-12):")
        for i in range(7, 13):
            estado = self.board.obtener_estado_punto(i)
            if estado is None:
                print(f"  {i:2d}: vacío")
            else:
                color, cantidad = estado
                simbolo = "○" if color == "negro" else "●"
                print(f"  {i:2d}: {simbolo} x{cantidad} ({color})")

        barra = self.board.get_barra()
        if barra and any(cantidad > 0 for cantidad in barra.values()):
            print("\n🚫 BARRA:")
            for color, cantidad in barra.items():
                if cantidad > 0:
                    simbolo = "○" if color == "negro" else "●"
                    print(f"  {simbolo} x{cantidad} ({color})")
        else:
            print("\n🚫 BARRA: vacía")

        print("\n⬇️ CUADRANTE EXTERIOR BLANCO (Puntos 13-18):")
        for i in range(13, 19):
            estado = self.board.obtener_estado_punto(i)
            if estado is None:
                print(f"  {i:2d}: vacío")
            else:
                color, cantidad = estado
                simbolo = "○" if color == "negro" else "●"
                print(f"  {i:2d}: {simbolo} x{cantidad} ({color})")

        print("\n🏠 CUADRANTE CASA BLANCO (Puntos 19-24):")
        for i in range(19, 25):
            estado = self.board.obtener_estado_punto(i)
            if estado is None:
                print(f"  {i:2d}: vacío")
            else:
                color, cantidad = estado
                simbolo = "○" if color == "negro" else "●"
                print(f"  {i:2d}: {simbolo} x{cantidad} ({color})")

        casa = self.board.get_casa()
        if casa and any(cantidad > 0 for cantidad in casa.values()):
            print("\n🎯 CASA:")
            for color, cantidad in casa.items():
                if cantidad > 0:
                    simbolo = "○" if color == "negro" else "●"
                    print(f"  {simbolo} x{cantidad} ({color})")
        else:
            print("\n🎯 CASA: vacía")

        print("-" * 80)

    def loop_principal(self):
        """
        Bucle principal del juego.

        SRP: Controla el flujo general de la partida (verifica victoria y alterna turnos).
        DIP: Interactúa con Board a través de sus métodos públicos.
        """
        while True:
            if self.board.ha_ganado("negro"):
                print(f"\n🎉 ¡{self.jugador_negro} HA GANADO! 🎉")
                break
            elif self.board.ha_ganado("blanco"):
                print(f"\n🎉 ¡{self.jugador_blanco} HA GANADO! 🎉")
                break

            self.turno_jugador()
            self.turno_actual = "blanco" if self.turno_actual == "negro" else "negro"

    def turno_jugador(self):
        """
        Gestiona el turno de un jugador.

        SRP: Coordina tirada de dados y llamadas al tablero, sin implementar reglas.
        DIP: Usa Board y Dice sin conocer sus detalles internos.
        """
        nombre_jugador = self.jugador_negro if self.turno_actual == "negro" else self.jugador_blanco
        simbolo = "○" if self.turno_actual == "negro" else "●"

        print(f"\n{'='*20} TURNO DE {nombre_jugador.upper()} {simbolo} {'='*20}")

        input(f"{nombre_jugador}, presiona ENTER para tirar los dados...")
        self.dados.tirar()
        print(f"\n🎲 {self.dados}")

        movimientos_posibles = self.board.obtener_movimientos_posibles(self.turno_actual, self.dados)

        if not movimientos_posibles:
            print(f"❌ No hay movimientos posibles para {nombre_jugador}.")
            self.dados.reiniciar()
            return

        if self.dados.es_doble():
            self.manejar_dobles()
        else:
            self.manejar_movimientos_normales()

        self.dados.reiniciar()

    def mostrar_movimientos_disponibles(self):
        """
        Muestra los movimientos posibles del jugador actual.

        SRP: Solo presentación de información.
        ISP: Método pequeño enfocado en una tarea concreta.
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

        SRP: Organiza el flujo de movimientos con los dados normales.
        DIP: Utiliza el tablero y los dados sin lógica de validación interna.
        """

        movimientos_realizados = 0
        dado1_usado = False
        dado2_usado = False

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

            # Mostrar dados disponibles
            dados_disponibles = []
            if not dado1_usado:
                dados_disponibles.append(f"Dado 1: {self.dados.obtener_dado1()}")
            if not dado2_usado:
                dados_disponibles.append(f"Dado 2: {self.dados.obtener_dado2()}")

            if not dados_disponibles:
                break

            print(f"Dados disponibles: {', '.join(dados_disponibles)}")

            # Preguntar tipo de movimiento
            opciones_disponibles = ["1. Mover una ficha con un dado"]

            # Solo permitir movimiento doble si ambos dados están disponibles
            if not dado1_usado and not dado2_usado:
                opciones_disponibles.append("2. Mover una ficha con ambos dados (movimiento doble)")

            opciones_disponibles.append("3. Pasar turno")

            print("\nOpciones:")
            for opcion in opciones_disponibles:
                print(opcion)

            try:
                opcion = input("Seleccione una opción: ").strip()

                if opcion == "1":
                    # Determinar qué dado usar según disponibilidad
                    if not dado1_usado and not dado2_usado:
                        # Ambos disponibles, preguntar cuál usar
                        print(f"Dado 1: {self.dados.obtener_dado1()}")
                        print(f"Dado 2: {self.dados.obtener_dado2()}")
                        try:
                            dado_elegido = input("¿Qué dado quiere usar? (1 o 2): ").strip()
                        except (StopIteration, EOFError):
                            print("\nEntrada agotada. Finalizando manejo de movimientos.")
                            return

                        if dado_elegido == "1":
                            usar_dado1, usar_dado2 = True, False
                            dado1_usado = True
                        elif dado_elegido == "2":
                            usar_dado1, usar_dado2 = False, True
                            dado2_usado = True
                        else:
                            print("❌ Debe seleccionar 1 o 2.")
                            continue
                    elif not dado1_usado:
                        # Solo el dado 1 está disponible
                        usar_dado1, usar_dado2 = True, False
                        dado1_usado = True
                        print(f"Usando el único dado disponible: {self.dados.obtener_dado1()}")
                    else:
                        # Solo el dado 2 está disponible
                        usar_dado1, usar_dado2 = False, True
                        dado2_usado = True
                        print(f"Usando el único dado disponible: {self.dados.obtener_dado2()}")

                    if self.realizar_movimiento_simple_con_dados(usar_dado1, usar_dado2):
                        movimientos_realizados += 1
                    else:
                        # Si el movimiento falló, liberar el dado para permitir otro intento
                        if usar_dado1:
                            dado1_usado = False
                        else:
                            dado2_usado = False

                elif opcion == "2" and not dado1_usado and not dado2_usado:
                    if self.realizar_movimiento_doble():
                        movimientos_realizados = 2  # Movimiento doble cuenta como ambos datos
                        break

                elif opcion == "3":
                    print("Pasando turno...")
                    break
                else:
                    print("❌ Opción inválida.")

            except KeyboardInterrupt:
                print("\n\nJuego interrumpido.")
                exit()
            except (StopIteration, EOFError):
                # En tests con mock_input agotado llega StopIteration; terminamos el manejo sin fallar
                print("\n\nEntrada agotada. Finalizando manejo de movimientos.")
                return

    def manejar_dobles(self):
        """
        Maneja los movimientos cuando la tirada es doble.

        SRP: Método especializado en el caso de dobles.
        DIP: Invoca los métodos del tablero según los valores de los dados.
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
                    if self.realizar_movimiento_simple_con_dados(True, False):
                        movimientos_realizados += 1
                elif opcion == "2":
                    print("Pasando turno...")
                    break
                else:
                    print("❌ Opción inválida. Seleccione 1 o 2.")

            except KeyboardInterrupt:
                print("\n\nJuego interrumpido.")
                exit()
            except (StopIteration, EOFError):
                print("\n\nEntrada agotada. Finalizando manejo de dobles.")
                return

    def realizar_movimiento_simple_con_dados(self, usar_dado1, usar_dado2) -> bool:
        """
        Realiza un movimiento con el dado especificado.

        SRP: Encapsula la ejecución y visualización de un movimiento.
        DIP: Llama a Board.realizar_movimiento_completo para validar y aplicar la jugada.
        """
        try:
            # Pedir punto de origen
            try:
                origen_str = input("Desde qué punto quiere mover (0 para barra): ").strip()
            except (StopIteration, EOFError):
                print("\nEntrada agotada. Cancelando movimiento simple.")
                return False
            origen = int(origen_str)

            # Realizar el movimiento
            exito = self.board.realizar_movimiento_completo(
                self.turno_actual, self.dados, origen, usar_dado1, usar_dado2
            )

            if exito:
                print("✅ Movimiento realizado exitosamente.")
            else:
                print("❌ Movimiento inválido. Intente de nuevo.")

            # SIEMPRE mostrar el tablero después de cualquier intento de movimiento
            self.mostrar_tablero()
            return exito

        except ValueError:
            print("❌ Por favor ingrese números válidos.")
            self.mostrar_tablero()
            return False
        except Exception as e:
            print(f"❌ Error: {e}")
            self.mostrar_tablero()
            return False

    def realizar_movimiento_simple(self) -> bool:
        """
        Versión simplificada para mantener compatibilidad.

        ISP: Método de interfaz mínima para retrocompatibilidad.
        """
        return self.realizar_movimiento_simple_con_dados(True, False)

    def realizar_movimiento_doble(self) -> bool:
        """
        Realiza un movimiento usando ambos dados.

        SRP: Gestiona la interacción para un movimiento doble.
        DIP: Depende del método Board.realizar_movimiento_doble para aplicar la jugada.
        """
        try:
            try:
                origen_str = input("Desde qué punto quiere mover la ficha con ambos dados: ").strip()
            except (StopIteration, EOFError):
                print("\nEntrada agotada. Cancelando movimiento doble.")
                return False
            origen = int(origen_str)

            # Mostrar qué pasaría
            dado1, dado2 = self.dados.obtener_valores()
            intermedio = self.board.calcular_destino(origen, dado1, self.turno_actual)
            final = self.board.calcular_destino(intermedio, dado2, self.turno_actual)

            print(f"La ficha se moverá: {origen} → {intermedio} → {final}")

            try:
                confirmar = input("¿Confirma este movimiento? (s/n): ").strip().lower()
            except (StopIteration, EOFError):
                print("\nEntrada agotada. Cancelando movimiento doble.")
                self.mostrar_tablero()
                return False

            if confirmar not in ['s', 'si', 'sí', 'y', 'yes']:
                self.mostrar_tablero()
                return False

            # Realizar el movimiento
            exito = self.board.realizar_movimiento_doble(self.turno_actual, self.dados, origen)

            if exito:
                print("✅ Movimiento doble realizado exitosamente.")
            else:
                print("❌ Movimiento doble inválido. Intente de nuevo.")

            # SIEMPRE mostrar el tablero después de cualquier intento de movimiento
            self.mostrar_tablero()
            return exito

        except ValueError:
            print("❌ Por favor ingrese un número válido.")
            self.mostrar_tablero()
            return False
        except Exception as e:
            print(f"❌ Error: {e}")
            self.mostrar_tablero()
            return False


def main():
    """
    Punto de entrada de la aplicación CLI.

    SRP: Encargado solo de iniciar la interfaz y manejar excepciones generales.
    DIP: No depende de detalles del dominio, solo del contrato de la clase CLI.
    """
    juego = CLI()
    try:
        juego.iniciar_juego()
    except KeyboardInterrupt:
        print("\n\n¡Hasta luego! 👋")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")


if __name__ == "__main__":
    main()
