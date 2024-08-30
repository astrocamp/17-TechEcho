# home/views.py
from django.shortcuts import render


def index(req):
    return render(req, "home/index.html")


def nav(req):
    return render(req, "home/nav.html")


def pages(req):
    return render(req, "home/pages.html")
