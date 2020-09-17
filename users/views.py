from django.shortcuts import render
from django.views.generic import CreateView #импортируем CreateView, чтобы создать ему наследника
from django.urls import reverse_lazy #эта функция позволит получить URL по имени функции
from .forms import CreationForm #импортируем класс формы, чтобы сослаться на него во view-классе

class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy("login") #  где login — это параметр "name" в path()
    template_name = "signup.html"
