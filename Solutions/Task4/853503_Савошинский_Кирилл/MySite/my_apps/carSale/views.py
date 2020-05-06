from django.contrib.auth import authenticate, login
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import generic
from django.views.generic import FormView
from .forms import LoginForm, CarForm, UserRegistrationForm, ProfileEditForm
from .models import Car, Profile


class AutoListView(generic.ListView):
    model = Car
    template_name = 'carSale/Home.html'


class AutoDetailView(generic.DetailView):
    model = Car
    template_name = 'carSale/DetailCarInfo.html'


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            profile = Profile.objects.create(user=new_user)
            return render(request, 'carSale/Home.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'carSale/register.html', {'user_form': user_form})


class LoginFormView(FormView):
    form_class = AuthenticationForm
    template_name = "carSale/login.html"
    success_url = "/"

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)


def user_logout(request):
    auth.logout(request)
    return redirect('Home')


def new_car(request):
    car_form = CarForm()
    if request.method == 'POST':
        car_form = CarForm(request.POST, request.FILES)
        if car_form.is_valid():
            car_form.save()
        return redirect('Home')
    return render(request, 'carSale/newCar.html', {'car_form': car_form})
