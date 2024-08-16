from django.shortcuts import render

def handshake_view(request):
    return render(request, 'index.html')
