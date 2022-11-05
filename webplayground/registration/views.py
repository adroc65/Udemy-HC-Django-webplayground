# El FORMULARIO de registro se importa del archivo FORMS.PY, ya que se
# modifica para que muestre el campo de EMAIL.
# from django.contrib.auth.forms import UserCreationForm
from .forms import UserCreationFormWithEmail, ProfileForm, EmailForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# from django.views.generic.base import TemplateView # Se uso temporalmente para ver la página
from django.views.generic.edit import UpdateView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import Profile
from django import forms


# Create your views here.
class SignUpView(CreateView):
    form_class = UserCreationFormWithEmail
    # success_url = reverse_lazy('login')  # Se quita ya que el metodo "get_success_url" hace lo mismo
    template_name = 'registration/signup.html'

    def get_success_url(self):
        return reverse_lazy('login') + '?register'

    def get_form(self, form_class=None):
        # Se recupera el formulario dado por Django
        form = super(SignUpView, self).get_form()
        # Modificar en tiempo de ejecución, haciendo referencia a los campos, se hace de esta forma
        # para no perder la validación que ya de por si DJANGO hace.
        form.fields['username'].widget = forms.TextInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Nombre de Usuario'})
        form.fields['email'].widget = forms.EmailInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Correo de Usuario'})
        form.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Digite el Password'})
        form.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Repita el Password'})
        return form


@method_decorator(login_required, name='dispatch')
class ProfileUpdate(UpdateView):
    form_class = ProfileForm
    success_url = reverse_lazy('profile')
    template_name = 'registration/profile_form.html'

    def get_object(self):
        # Recuperar objeto (USER) que se va a editar
        profile, create = Profile.objects.get_or_create(user=self.request.user)
        return profile


# Vista para editar el EMAIL
@method_decorator(login_required, name='dispatch')
class EmailUpdate(UpdateView):
    form_class = EmailForm
    success_url = reverse_lazy('profile')
    template_name = 'registration/profile_email_form.html'

    def get_object(self):
        # Recuperar objeto (USER) que se va a editar
        return self.request.user

    def get_form(self, form_class=None):
        # Se recupera el formulario dado por Django
        form = super(EmailUpdate, self).get_form()
        # Modificar en tiempo de ejecución, haciendo referencia a los campos, se hace de esta forma
        # para no perder la validación que ya de por si DJANGO hace.
        form.fields['email'].widget = forms.EmailInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Correo de Usuario'})
        return form
