from django.conf import settings
from django.core.mail import send_mail


from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from boletin.models import Registrado
from .forms import RegModelForm, ContactForm
from .models import Registrado

# Create your views here.
def inicio(request):
    titulo = "Bienvenido"
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

    if request.user.is_authenticated and request.user.is_staff:
        i=1
        for instance in Registrado.objects.all():
            i+=1
            print(instance.nombre)
        print(i)

        queryset = Registrado.objects.all().order_by("-timestamp")

        context = {
            "queryset":queryset,
        }
    return render(request, 'inicio.html', context)
    # return HttpResponse('hello,world!')


class HomePageView(TemplateView):
    template_name = 'home.html'

def contact(request):

    titulo = "Contacto"

    form = ContactForm(request.POST or None)
    if form.is_valid():

        # for key in form.cleaned_data:
        #     print(key)
        #     print(form.cleaned_data.get(key))

        form_email = form.cleaned_data.get("email")
        form_mensaje = form.cleaned_data.get("mensaje")
        form_nombre = form.cleaned_data.get("nombre")
        print(form_email,form_mensaje,form_nombre)

        asunto ='form de contacto'
        email_from = settings.EMAIL_HOST_USER
        email_to = [form_email]
        email_mensaje = "%s:%s enviado por %s" %(form_nombre,form_mensaje,form_email)


        send_mail(asunto,
                  email_mensaje,
                  email_from,
                  email_to,
                  fail_silently=False
                  )

    context = {
        "form":form,
        "titulo":titulo,
    }

    return render(request,"forms.html",context)