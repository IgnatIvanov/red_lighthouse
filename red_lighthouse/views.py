from django.shortcuts import render, redirect
from django.http import HttpResponse



def menu(request):
    return render(request, 'red_lighthouse/main.html')