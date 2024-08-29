from django.shortcuts import render


def index(req):
    return render(req, "home/index.html")


def nav(req):
    return render(req, "home/navbar.html")
