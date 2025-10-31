import redis
import json
from Backgammon.Core.Board import Board # Importa Board para type hinting

class RedisManager:
    """
    Gestiona la conexión y la lógica para guardar/cargar el estado del juego
    en una base de datos Redis.
    
    SRP: Su única responsabilidad es la persistencia de datos.
    DIP: Las interfaces (UI/CLI) dependerán de esta abstracción, no de Redis directamente.
    """
    
    def __init__(self, client=None):
        """
        Inicializa la conexión con Redis.
        
        Si se provee un 'client' (para testing), lo utiliza.
        Si no, crea una conexión real a localhost.
        """
        if client:
            # Cliente inyectado (usado para tests con fakeredis)
            self.__redis_db__ = client # <-- ¡¡DOBLE GUIÓN BAJO!!
            print("Conectado a Redis (cliente inyectado, modo Test).")
        else:
            # Conexión real (usada en producción)
            self.__redis_db__ = None # <-- ¡¡DOBLE GUIÓN BAJO!!
            try:
                # decode_responses=True es clave para que devuelva strings
                self.__redis_db__ = redis.Redis(host='localhost', port=6379, decode_responses=True) # <-- ¡¡DOBLE GUIÓN BAJO!!
                self.__redis_db__.ping()
                print("Conectado a Redis exitosamente (desde RedisManager).")
            except redis.exceptions.ConnectionError as e:
                print(f"Error al conectar con Redis: {e}")
                print("Funcionalidad de Guardar/Cargar estará desactivada.")
                self.__redis_db__ = None # <-- ¡¡DOBLE GUIÓN BAJO!!

    def guardar_partida(self, slot_id: str, estado_completo: dict) -> tuple[bool, str]:
        """
        Guarda un diccionario de estado del juego en Redis como JSON.
        """
        if not self.__redis_db__: # <-- ¡¡DOBLE GUIÓN BAJO!!
            return False, "Error: No hay conexión a Redis."

        try:
            # Convertir objeto a JSON string
            json_data = json.dumps(estado_completo)
            self.__redis_db__.set(slot_id, json_data) # <-- ¡¡DOBLE GUIÓN BAJO!!
            return True, f"Partida guardada en '{slot_id}'."
        except TypeError as e:
            # Error común si el objeto no es serializable
            return False, f"Error al guardar partida (JSON no serializable): {e}"
        except Exception as e:
            return False, f"Error al guardar partida: {e}"

    def cargar_partida(self, slot_id: str) -> tuple[dict | None, str]:
        """
        Carga un estado del juego desde Redis y lo devuelve como diccionario.
        """
        if not self.__redis_db__: # <-- ¡¡DOBLE GUIÓN BAJO!!
            return None, "Error: No hay conexión a Redis."

        try:
            # Obtener JSON string desde Redis
            json_data = self.__redis_db__.get(slot_id) # <-- ¡¡DOBLE GUIÓN BAJO!!
            if not json_data:
                return None, f"No se encontró partida guardada en '{slot_id}'."
            
            # Convertir JSON string de nuevo a objeto
            estado_completo = json.loads(json_data)
            return estado_completo, f"Partida cargada desde '{slot_id}'."
        
        except json.JSONDecodeError as e:
            # Error común si los datos en Redis están corruptos
             return None, f"Error al cargar partida (JSON corrupto): {e}"
        except Exception as e:
            return None, f"Error al cargar partida: {e}"