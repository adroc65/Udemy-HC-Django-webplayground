# Comandos para ejecutar o llenar DB de mensajes, desde la SHELL
#
# Iniciar con : ->> python manage.py shell
#
from django.contrib.auth.models import User
from messenger.models import Thread, Message


DonMax = User.objects.get(username="max")
Aaron = User.objects.get(username="aaron")
thread = Thread.objects.find_or_create(DonMax, Aaron)
thread.messages.add(Message.objects.create(user=DonMax, content='Aaron, ya es hora, me va a sacar?'))
thread.messages.add(Message.objects.create(user=Aaron, content='No Max, esperese un toque esta lloviendo'))
thread.messages.add(Message.objects.create(user=DonMax, content='Ya paso una hora ya escampo, salgamos ya'))
thread.messages.add(Message.objects.create(user=Aaron, content='Bueno, pero se porta bien nada de pelear'))

# salir de la SHELL
exit()
