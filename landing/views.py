from django.shortcuts import render



def landing(request):
    # Обработчик запроса посадочной страницы

    return render(request, 'landing/landing.html')
