from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .forms import SignUpForm, OrderItemFormSet
from .models import MenuItem, Order, OrderItem
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.urls import reverse


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.email = form.cleaned_data.get('email')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('home')  # Redirect to a 'home' or appropriate page
    else:
        form = SignUpForm()
    return render(request, 'orders/signup.html', {'form': form})

def home_view(request):
    menu_items = MenuItem.objects.all()  
    return render(request, 'orders/home.html', {'menu_items': menu_items})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Invalid credentials')
    else:
        form = AuthenticationForm()
    return render(request, 'orders/login.html', {'form': form})

def manage_orders_view(request):
    if not request.user.is_staff:
        return redirect('home')  # Or some error page
    orders = Order.objects.filter(completed=False)
    return render(request, 'orders/manage_orders.html', {'orders': orders})

def complete_order_view(request, order_id):
    if request.user.is_staff and request.method == 'POST':
        order = Order.objects.get(id=order_id)
        order.completed = True
        order.save()
        return HttpResponseRedirect(reverse('manage_orders'))
    return HttpResponseRedirect(reverse('home'))


def create_order_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        formset = OrderItemFormSet(request.POST)
        if formset.is_valid():
            order = Order(customer=request.user)
            order.save()  # Save the order to get an order_id
            instances = formset.save(commit=False)
            for instance in instances:
                instance.order = order
                instance.save()
            # Redirect to order confirmation with the order ID
            return redirect('order_confirmation', order_id=order.id)
    else:
        formset = OrderItemFormSet(queryset=OrderItem.objects.none())

    return render(request, 'orders/create_order.html', {'formset': formset})

def order_confirmation_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    # Optional: check if the logged in user is the one who placed the order or if the user is staff
    if request.user != order.customer and not request.user.is_staff:
        return redirect('home')

    return render(request, 'orders/order_confirmation.html', {'order': order})

def custom_logout(request):
    logout(request)
    return redirect('home') 