from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib import messages


from .forms import RegisterForm

from .models import Ticket
from .forms import TicketForm


def home(request):
    return render(request, 'home.html')


def register(request):

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect('dashboard')

    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {
        'form': form
    })


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def ticket_list(request):

    tickets = Ticket.objects.all()

    return render(request, 'tasks/ticket_list.html', {
        'tickets': tickets
    })


@login_required
def create_ticket(request):

    if request.method == 'POST':

        form = TicketForm(request.POST)

        if form.is_valid():

            ticket = form.save(commit=False)

            ticket.created_by = request.user

            ticket.save()

            messages.success(request, 'Ticket created successfully.')

            return redirect('ticket_list')

    else:

        form = TicketForm()

    return render(request, 'tasks/create_ticket.html', {
        'form': form
    })


@login_required
def update_ticket(request, id):

    ticket = get_object_or_404(Ticket, id=id)

    if request.user != ticket.created_by and not request.user.is_superuser:
        
        messages.error(
            request,
            "Access denied. You cannot edit another user's ticket."
        )

        return redirect('ticket_list')

    if request.method == 'POST':

        form = TicketForm(request.POST, instance=ticket)

        if form.is_valid():

            form.save()

            messages.success(request, 'Ticket updated successfully.')
            
            return redirect('ticket_list')

    else:

        form = TicketForm(instance=ticket)

    return render(request, 'tasks/update_ticket.html', {
        'form': form
    })



@login_required
def delete_ticket(request, id):

    ticket = get_object_or_404(Ticket, id=id)

    if request.user != ticket.created_by and not request.user.is_superuser:

        messages.error(
            request,
            "Access denied. You cannot delete another user's ticket."
        )

        return redirect('ticket_list')

    if request.method == 'POST':

        ticket.delete()
        
        messages.success(request, 'Ticket deleted successfully.')
        
        return redirect('ticket_list')

    return render(request, 'tasks/delete_ticket.html', {
        'ticket': ticket
    })


