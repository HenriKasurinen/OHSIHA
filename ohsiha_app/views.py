from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Moimoi tän kirjotti Henri juu")

# Create your views here.
