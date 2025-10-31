# En un nuevo archivo: Tests/Test_RedisManager.py
import unittest
import fakeredis
from Backgammon.Persistence.RedisManager import RedisManager

class TestRedisManager(unittest.TestCase):

    def setUp(self):
        # 1. Creamos un servidor Redis falso en memoria
        self.fake_redis_server = fakeredis.FakeStrictRedis()
        
        # 2. Inyectamos el servidor falso en nuestro manager
        # (Esto requiere modificar RedisManager para aceptar un 'client'
        #  o usar 'patch' de una forma más avanzada)
        self.redis_manager = RedisManager()
        self.redis_manager.client = self.fake_redis_server 

    def test_connection_and_ping(self):
        # Prueba que el manager puede "hablar" con el servidor falso
        self.assertTrue(self.redis_manager.client.ping())

    def test_save_and_load_roundtrip(self):
        # ¡El test más importante!
        
        # 1. Definir un estado de juego de prueba
        estado_prueba = {
            "board_state": {"puntos": [["negro", 5]]},
            "ui_state": {"current_player": "negro"}
        }
        
        # 2. Guardar
        exito_g, msg_g = self.redis_manager.guardar_partida("slot1", estado_prueba)
        self.assertTrue(exito_g)
        
        # 3. Cargar
        estado_cargado, msg_c = self.redis_manager.cargar_partida("slot1")
        
        # 4. Verificar
        self.assertIsNotNone(estado_cargado)
        self.assertEqual(estado_cargado["ui_state"]["current_player"], "negro")
        self.assertEqual(estado_cargado["board_state"]["puntos"][0], ["negro", 5])

    def test_load_non_existent_slot(self):
        # Probar qué pasa si cargamos un slot que no existe
        estado_cargado, msg_c = self.redis_manager.cargar_partida("slot_fantasma")
        
        self.assertIsNone(estado_cargado)
        self.assertIn("No se encontró", msg_c)