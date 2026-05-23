from django import forms
from django.contrib.auth.models import User
from django.utils import timezone

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
            'assigned_to'

        ]

        widgets = {

            'due_date': forms.DateInput(attrs={

                'type': 'date'

            })

        }

    def __init__(self, *args, **kwargs):

        user = kwargs.pop('user', None)

        super().__init__(*args, **kwargs)

        # STANDARD USER CANNOT ASSIGN TICKETS
        if user and not user.is_superuser:

            self.fields.pop('assigned_to')

        # ADMIN CAN ASSIGN TO ANYONE
        else:

            self.fields['assigned_to'].queryset = User.objects.all()

    # DUE DATE VALIDATION
    def clean_due_date(self):

        due_date = self.cleaned_data.get('due_date')

        today = timezone.now().date()

        if due_date < today:

            raise forms.ValidationError(

                'Due date cannot be in the past.'

            )

        return due_date
    
    