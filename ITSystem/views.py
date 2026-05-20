from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Ticket
from .forms import TicketForm


# HOME PAGE
def home(request):

    return render(request, 'home.html')


# REGISTER PAGE
def register(request):

    if request.method == 'POST':

        form = UserCreationForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(request, 'Account created successfully.')

            return redirect('login')

    else:

        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})


# DASHBOARD
@login_required
def dashboard(request):

    if request.user.is_superuser:

        tickets = Ticket.objects.all().order_by('-id')[:5]

        ticket_count = Ticket.objects.count()

    else:

        tickets = Ticket.objects.filter(
            assigned_to=request.user
        ).order_by('-id')[:5]

        ticket_count = Ticket.objects.filter(
            assigned_to=request.user
        ).count()

    context = {

        'tickets': tickets,
        'ticket_count': ticket_count

    }

    return render(request, 'dashboard.html', context)


# VIEW TICKETS
@login_required
def ticket_list(request):

    if request.user.is_superuser:

        tickets = Ticket.objects.all()

    else:

        tickets = Ticket.objects.filter(
            assigned_to=request.user
        )

    context = {

        'tickets': tickets

    }

    return render(request, 'tasks/ticket_list.html', context)


# CREATE TICKET
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


# UPDATE TICKET
@login_required
def update_ticket(request, pk):

    ticket = get_object_or_404(Ticket, id=pk)

    if not request.user.is_superuser and ticket.created_by != request.user:

        messages.error(request, 'You are not allowed to edit this ticket.')

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


# DELETE TICKET
@login_required
def delete_ticket(request, pk):

    ticket = get_object_or_404(Ticket, id=pk)

    if not request.user.is_superuser:

        messages.error(request, 'Only admin can delete tickets.')

        return redirect('ticket_list')

    if request.method == 'POST':

        ticket.delete()

        messages.success(request, 'Ticket deleted successfully.')

        return redirect('ticket_list')

    return render(request, 'tasks/delete_ticket.html', {

        'ticket': ticket

    })
