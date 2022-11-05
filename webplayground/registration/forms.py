# Con este archivo se va a agregar el campo de correo al formulario de Registro
# este campo ya exixte en USER pero por default no se muestra, con lo siguiente
# se muestra este campo y modificando el VIEW.PY

from django import forms
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserCreationFormWithEmail(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Requerido, máximo 254 caracteres y correo válido.")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    # Se hace una validación adicional al campo de EMAIL para ver que no se repita.
    def clean_email(self):
        # Se extrae el campo de EMAIL para analizarlo
        email = self.cleaned_data.get("email")
        # Se hace la lógica de comprobación.
        if User.objects.filter(email=email).exists():
            # Muestra un mensaje de EMAIL duplicado
            raise forms.ValidationError("El EMAIL ya esta registrado, pruebe con otro.")
        return email


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'link']
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control-file mt-3'}),
            'bio': forms.Textarea(attrs={'class': 'form-control mt-3', 'rows': 3, 'placeholder': 'Biografía'}),
            'link': forms.URLInput(attrs={'class': 'form-control mt-3', 'placeholder': 'Enlace'}),
        }


class EmailForm(forms.ModelForm):
    email = forms.EmailField(required=True, help_text="Requerido, máximo 254 caracteres y correo válido.")

    class Meta:
        model = User
        fields = ['email']

    # Se valida el email ingresado
    def clean_email(self):
        # Se extrae el campo de EMAIL para analizarlo
        email = self.cleaned_data.get("email")
        # Se hace la lógica de comprobación, pero primero se comprueba que el email cambio.
        if 'email' in self.changed_data:
            if User.objects.filter(email=email).exists():
                # Muestra un mensaje de EMAIL duplicado
                raise forms.ValidationError("El EMAIL ya esta registrado, pruebe con otro.")
        return email
