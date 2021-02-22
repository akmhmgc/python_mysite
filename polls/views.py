from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def index(request):
    return HttpResponse("Hello, world. Fuck you man!!")


def show(request, user):
    return HttpResponse("あなたは{}番目の訪問者です".format(user))
