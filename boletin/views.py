from django.http import HttpResponse
from django.shortcuts import render

from django.views.generic import TemplateView

# Create your views here.
def inicio(request):
    return render(request, 'inicio.html', {})
    #return HttpResponse('hello,world!')

class HomePageView(TemplateView):
    template_name = 'home.html'