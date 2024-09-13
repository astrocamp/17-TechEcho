from django.shortcuts import render, get_object_or_404, redirect
from .models import Article
from .forms import ArticleForm

def article_list(request):
    articles = Article.objects.all().order_by('-created_at')
    return render(request, 'blogs/articles_index.html', {'articles': articles})  

def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'blogs/articles_show.html', {'article': article})  

def article_create(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blogs:articles_index')  
    else:
        form = ArticleForm()
    return render(request, 'blogs/articles_new.html', {'form': form})  

def article_update(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('blogs:articles_show', pk=article.pk)  
    else:
        form = ArticleForm(instance=article)
    return render(request, 'blogs/articles_new.html', {'form': form})  

def article_delete(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == "POST":
        article.delete()
        return redirect('blogs:articles_index') 
    return render(request, 'blogs/articles_delete.html', {'article': article})  