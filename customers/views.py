from django.shortcuts import render

# Create your views here.

def show_account(request):
    return render(request,"account.html")

