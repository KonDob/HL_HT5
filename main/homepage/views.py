from django.shortcuts import render

# Create your views here.

def home(request):
    """
    Return html page
    """
    return render(request, 'home.html')