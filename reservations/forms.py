from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


User = get_user_model()


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(label="Nombre", max_length=150)
    last_name = forms.CharField(label="Apellido", max_length=150)
    email = forms.EmailField(label="Correo electrónico")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name", "last_name", "email")
        labels = {"username": "Nombre de usuario"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].help_text = "Usa letras, números y los símbolos @, ., +, - o _."
        self.fields["password1"].help_text = (
            "Usa al menos 8 caracteres y evita datos personales o contraseñas comunes."
        )
        self.fields["password2"].help_text = "Repite la contraseña para confirmar."

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Ya existe una cuenta con este correo electrónico.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

