from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import ContactForm
from .models import ContactMessage
from vehicles.models import Car
# Create your views here.


def is_admin_or_staff(user):
    return user.is_authenticated and user.is_staff



def home(request):

    try:
        cars = Car.objects.all().order_by('-created_at')[:4]
        expensive_cars = Car.objects.all().order_by('-daily_price')[:8]
    except Exception:
        cars = []

    context = {
        'cars': cars,
        'expensive_cars':expensive_cars,
    }

    return render(request, "main/home.html", context)



def about_us(request):
    return render(request, "main/about_us.html")




def careers(request):
    return render(request, "main/careers.html")




def contact(request):
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you! Your message has been sent successfully. We will get back to you soon.')
            return redirect('main:contact') 
        else:
            messages.error(request, 'There was an error in your submission. Please check the fields below.')
    else:
        form = ContactForm()
    
    context = {'form': form}
    return render(request, "main/contact.html", context)



@login_required(login_url='accounts:login')
@user_passes_test(is_admin_or_staff, login_url='/') 
def contact_messages_dashboard(request):

    contact_messages = ContactMessage.objects.all()
    context = {
        'contact_messages': contact_messages
    }
    return render(request, "main/admin_contact_messages.html", context)