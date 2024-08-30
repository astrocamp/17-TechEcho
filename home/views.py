from django.shortcuts import render


def index(req):
    return render(req, "home/index.html")


def pages(req):
    return render(req, "home/pages.html")
