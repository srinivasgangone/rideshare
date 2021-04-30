from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .forms import SignUpForm, RideForm, SearchRideForm
from .models import User, Ride

def home(request):
    rides = Ride.objects.all()
    if request.method == 'POST':
        try:
            user = User.objects.get(username=request.user.username)
            signup_form = SignUpForm(request.POST)
            
            if signup_form.is_valid():
                signup_form.save()
                username = signup_form.cleaned_data.get('username')
                raw_password = signup_form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return redirect('home')
        except:
            print("User does not exist")

    else:
        signup_form = SignUpForm()

    context = {
        'signup_form' : signup_form,
        'rides': rides
    }

    return render(request, 'index.html', context)

def signup_driver(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            driver_form = form.save(commit=False)
            driver_form.is_driver = True
            driver_form.save()
            
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup-driver.html', {'form': form})

def signup_customer(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            customer_form = form.save(commit=False)
            customer_form.is_customer = True
            customer_form.save()

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup-customer.html', {'form': form})


@login_required
def create_ride(request):
    if request.method == 'POST':
        try:
            form = RideForm(request.POST)
            user = User.objects.get(username=request.user.username)
            if form.is_valid():
                ride = form.save(commit=False)
                ride.driver = user
                form.save()
                return redirect("home")
        except:
            print("User does not existt")

    else:
        form = RideForm()

    return render(request, 'add-ride.html', {'form': form})

@login_required
def book_ride(request, id):
    form = SearchRideForm()
    ride = get_object_or_404(Ride, id=id)
    # user = User.objects.get(username=request.user.username)
    try:
        ride.customer = request.user
        ride.save()

        message = "Ride successfully booked"

    except:
        message = "Encountered an error while processing your request"
        
    return render(request, 'book-ride.html', {'message': message, "form": form})

@login_required
def search_ride(request):
    message = "Search for rides on a given route"
    if request.method == 'POST':
        form = SearchRideForm(request.POST)

        if form.is_valid():
            departure = form.cleaned_data.get('departure')
            destination = form.cleaned_data.get('destination')
            rides = Ride.objects.filter(departure=departure, destination=destination)
            
            if rides:
                message = f"Below are the available rides from {departure} to {destination}"
            else:
                message = f"There are no available rides from {departure} to {destination}"

        else:
            message = ""

    else:
        form = SearchRideForm()
        rides = None

    context = {
        "rides": rides,
        "form": form,
        "message" : message
    }
    return render(request, 'search-rides.html', context)


def contact(request):
    return render(request, 'contact-page.html', {})
