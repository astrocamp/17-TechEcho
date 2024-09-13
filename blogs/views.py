from django.shortcuts import get_object_or_404, redirect, render

from .forms import ArticleForm
from .models import Article


def index(request):
    articles = Article.objects.all().order_by("-created_at")
    return render(request, "blogs/index.html", {"articles": articles})


def show(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, "blogs/show.html", {"article": article})


def new(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("blogs:index")
    else:
        form = ArticleForm()
    return render(request, "blogs/new.html", {"form": form})


def edit(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect("blogs:show", pk=article.pk)
    else:
        form = ArticleForm(instance=article)
    return render(request, "blogs/new.html", {"form": form})


def delete(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == "POST":
        article.delete()
        return redirect("blogs:index")
    return render(request, "blogs/edit.html", {"article": article})
