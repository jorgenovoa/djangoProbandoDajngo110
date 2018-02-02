from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from boletin.models import Registrado
from .forms import RegForm,RegModelForm



# Create your views here.
def inicio(request):
    titulo = "HOLA"
    if request.user.is_authenticated:
        titulo = "Bienvenido %s" %(request.user)
    form = RegModelForm(request.POST or None)

    #print(dir(form)):

    context = {
        "titulo": titulo,
        "el_form": form,
    }

    if form.is_valid():
        instance = form.save(commit=False)
        email = form.cleaned_data.get("email")
        nombre = form.cleaned_data.get("nombre")
        if not instance.nombre:
            instance.nombre="PERSONA"
        instance.save()

        context = {
            "titulo" : "Gracias %s!" %(nombre)
        }

        if not nombre:
            context = {
                "titulo" : "Gracias %s!" %(email)
            }

        print(instance)
        print(instance.timestamp)
        # form_data = form.cleaned_data
        # print(form_data)
        # abc= form_data.get("email")
        # nom = form_data.get("nombre")
        # obj = Registrado.objects.create(email=abc,nombre=nom)


    return render(request, 'inicio.html', context)
    # return HttpResponse('hello,world!')


class HomePageView(TemplateView):
    template_name = 'home.html'
