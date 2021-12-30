from django.shortcuts import render

# Create your views here.
def landing(request):
    return render(
        request,
        'single_page/landing.html'
    )

def aboutme(request):
    return render(
        request,
        'single_page/aboutme.html'
    )