from django.test import TestCase
from django.contrib.auth.models import User
from .models import Thread, Message


# Create your tests here.
class ThreadTestCase(TestCase):
    # Se define entorno de pruebas
    def setUp(self) -> None:
        self.user1 = User.objects.create_user('user1', None, 'test1234')
        self.user2 = User.objects.create_user('user2', None, 'test1234')
        self.user3 = User.objects.create_user('user3', None, 'test1234')

        self.thread = Thread.objects.create()

    # Se configura la prueba a hacer
    def test_add_user_to_thread(self):
        self.thread.users.add(self.user1, self.user2)
        # Se comprueba que hayan 2 usuarios en el hilo.
        self.assertEqual(len(self.thread.users.all()), 2)

    # Prueba para saber si hay usuarios en un hilo
    def test_filter_thread_by_users(self):
        self.thread.users.add(self.user1, self.user2)
        threads = Thread.objects.filter(users=self.user1).filter(users=self.user2)
        self.assertEqual(self.thread, threads[0])

    # Prueba para comprobar que si no se definen usuarios no hay Hilos
    def test_filter_non_existent_thread(self):
        threads = Thread.objects.filter(users=self.user1).filter(users=self.user2)
        self.assertEqual(len(threads), 0)

    # Pruebas de envio de mensaje:
    def test_add_messages_to_thread(self):
        self.thread.users.add(self.user1, self.user2)
        message1 = Message.objects.create(user=self.user1, content='hablo con User2')
        message2 = Message.objects.create(user=self.user2, content='correcto, ¿es user1?')
        self.thread.messages.add(message1, message2)
        self.assertEqual(len(self.thread.messages.all()), 2)

        for message in self.thread.messages.all():
            print(f"({message.user} - {message.content})")

    # En este se muestra una falla, que un mensaje definido aunque no sea parte de
    # los usuarios de conversación es contado como los mensajes de un hilo.
    # Para corregir se hacen ajustes en el Modelo.
    def test_add_messages_fron_user_not_in_thread(self):
        self.thread.users.add(self.user1, self.user2)
        message1 = Message.objects.create(user=self.user1, content='Hablo con user2')
        message2 = Message.objects.create(user=self.user2, content='Correcto, ¿es user1?')
        message3 = Message.objects.create(user=self.user3, content='¡Soy un espia!')
        self.thread.messages.add(message1, message2, message3)
        self.assertEqual(len(self.thread.messages.all()), 2)

    def test_find_thread_with_custom_manager(self):
        self.thread.users.add(self.user1, self.user2)
        # Este método find, no existe, se debe de crear.
        thread = Thread.objects.find(self.user1, self.user2)
        self.assertEqual(self.thread, thread)

    # Prueba que si no existe el hilo lo crea
    def test_find_or_create_thread_with_custom_manager(self):
        self.thread.users.add(self.user1, self.user2)
        # Este método find, no existe, se debe de crear.
        thread = Thread.objects.find_or_create(self.user1, self.user2)
        self.assertEqual(self.thread, thread)
        # Entre user1 y user3 no se ha creado previamente un thread
        thread = Thread.objects.find_or_create(self.user1, self.user3)
        self.assertIsNotNone(thread)
