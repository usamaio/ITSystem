from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):

    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

from .models import Ticket


class TicketForm(forms.ModelForm):

    class Meta:
        model = Ticket

        fields = [
            'title',
            'description',
            'due_date',
            'priority',
            'status',
            'category',
        ]