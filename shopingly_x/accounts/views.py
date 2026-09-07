from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, AddressForm
from .models import Profile, Address
from orders.models import Order
from django import forms 
from django.views.decorators.cache import never_cache



@never_cache
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            Profile.objects.create(user=user)
            login(request, user)
            messages.success(request, f'Welcome to Shopingly X, {user.first_name or user.username}!')
            return redirect('products:product_list')
        else:
            return render(request, 'registration/register.html', {'form': form})
    else:
        form = RegisterForm()
        return render(request, 'registration/register.html', {'form': form})




@login_required
def dashboard(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')[:10]
    addresses = request.user.addresses.all()
    return render(request, 'accounts/dashboard.html', {'orders': orders, 'addresses': addresses})


@login_required
def address_list(request):
    addresses = request.user.addresses.all()
    return render(request, 'accounts/address_list.html', {'addresses': addresses})


@login_required
def address_add(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            if address.is_default:
                request.user.addresses.update(is_default=False)
            address.save()
            messages.success(request, 'Address saved.')
            next_url = request.GET.get('next', 'accounts:address_list')
            return redirect(next_url)
    else:
        form = AddressForm()
    return render(request, 'accounts/address_form.html', {'form': form})


@login_required
def address_delete(request, pk):
    address = get_object_or_404(Address, pk=pk, user=request.user)
    address.delete()
    messages.info(request, 'Address removed.')
    return redirect('accounts:address_list')
