from concurrent.futures import thread
from django.db import models
from django.contrib.auth.models import User

# El siguiente es para uso de señales
from django.db.models.signals import m2m_changed


# Create your models here.
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']


# Se crea esta para poder configurar nuestros métodos
class ThreadManager(models.Manager):
    def find(self, user1, user2):
        # Dentro de un método de un OBJECT manager, la palabra "self" equivale
        # a las instancias del modelo en este caso Threads.object.all()
        queryset = self.filter(users=user1).filter(users=user2)
        if len(queryset) > 0:   # Si es mayor que 0 => hay un Hilo
            return queryset[0]
        return None

    def find_or_create(self, user1, user2):
        # Detecta si el Thread existe, si no es asi lo crea:
        thread = self.find(user1, user2)
        if thread is None:
            # Se procede a crear.
            thread = Thread.objects.create()
            thread.users.add(user1, user2)
        return thread


class Thread(models.Model):
    users = models.ManyToManyField(User, related_name='threads')
    messages = models.ManyToManyField(Message)
    updated = models.DateTimeField(auto_now=True)

    objects = ThreadManager()   # Se llaman nuestros métodos creados.

    class Meta:
        ordering = ['-updated']


# Se crea la señal para determinar un cambio en los hilos
def messages_changed(sender, **kwargs):
    instance = kwargs.pop("instance", None)
    action = kwargs.pop("action", None)
    pk_set = kwargs.pop("pk_set", None)
    print(instance, action, pk_set)

    # Se debe de ver si un mensaje se esta colando y no es de la instancia
    # Se crea un conjunto para guardar mensajes falsos:
    false_pk_set = set()
    # Se determina si en la precarga del mensaje se nos cuela un mensaje de
    # un usuario incorrecto.
    if action == "pre_add":
        for msg_pk in pk_set:
            msg = Message.objects.get(pk=msg_pk)
            if msg.user not in instance.users.all():
                print(f"Alerta !!, el usuario {msg.user} quiere enviar un mensaje a este Hilo")
                false_pk_set.add(msg_pk)
        # Forzar la actualización haciendo save, Para actualizar el como se muestran los mensajes
        instance.save()
    # Usando la teoria de conjuntos, sacamos de los mensajes correctos el MSG fraudulento
    pk_set.difference_update(false_pk_set)


m2m_changed.connect(messages_changed, sender=Thread.messages.through)
