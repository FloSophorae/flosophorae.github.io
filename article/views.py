import markdown
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator

from .models import ArticleCategory, Article
from .forms import NewArticleForm, NewArticleCategoryForm

# Create your views here.
def category_list(request):
    search = request.GET.get('search')
    if search:
        category_list = ArticleCategory.objects.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search)
            )
    else:
        search = ''
        category_list = ArticleCategory.objects.all()
    categories = category_list
    context = {
        'categories': categories,
        'search': search,
        'father': None
    }
    return render(request, 'category/list.html', context)

def category_detail(request, id):
    category = ArticleCategory.objects.get(id=id)
    category.description = markdown.markdown(category.description,
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])
    articles = Article.objects.filter(category=category)
    categories = ArticleCategory.objects.all()
    fathers = []
    cur = category
    while(cur.father != None):
        fathers.insert(0, cur.father)
        cur = cur.father
    context = {
        'category': category,
        'categories': categories,
        'articles': articles,
        'fathers': fathers,
    }
    return render(request, 'category/detail.html', context)


def new_category(request, father=-1):
    if request.method == "POST":
        category_post_form = NewArticleCategoryForm(data=request.POST)
        if category_post_form.is_valid():
            category_post_form.save()
            if father == -1:
                return redirect("article:category_list")
            else:
                return redirect("article:category_detail", father)
        else:
            return HttpResponse("Invalid Form! Please rewrite!")
    else:
        category_post_form = NewArticleCategoryForm()
        categories = ArticleCategory.objects.all()
        context = {
            'category_post_form': category_post_form,
            'categories': categories,
            'father': father,
        }
        return render(request, 'category/create.html', context)

def update_category(request, id):
    category = ArticleCategory.objects.get(id=id)
    if request.method == "POST":
        category_post_form = NewArticleCategoryForm(data=request.POST)
        if category_post_form.is_valid():
            category.title = request.POST['title']
            category.description = request.POST['description']
            if request.POST['father'] != 'none':
                category.father = ArticleCategory.objects.get(id=request.POST['father'])
            else:
                category.father = None
            category.save()
            return redirect("article:category_detail", id=id)
        else:
            return HttpResponse("Invalid Table Content, Please rewrite!")
    else:
        category_post_form = NewArticleCategoryForm()
        category = ArticleCategory.objects.get(id=id)
        categories = ArticleCategory.objects.all()
        context = {
            'category': category,
            'categories': categories,
        }
        return render(request, 'category/update.html', context)

def delete_category(request, id):
    if request.method == 'POST':
        category = ArticleCategory.objects.get(id=id)
        category.delete()
        return redirect("article:category_list")
    else:
        return HttpResponse("Only POST is allowed")


def new_article(request, father=-1):
    if request.method == "POST":
        article_post_form = NewArticleForm(data=request.POST)
        if article_post_form.is_valid():
            new_article = article_post_form.save(commit=False)
            new_article.save()
            article_post_form.save_m2m() # tag
            # if(father == -1):
            #     return redirect("article:category_list")
            # else:
            #     return redirect("article:category_detail", id=father)
            return JsonResponse({'message': 'Saved successfully'}, status=200)
        else:
            response = HttpResponseBadRequest(NewArticleForm(request.POST).errors.as_json())
            return response
    else:
        article_post_form = NewArticleForm()
        categories = ArticleCategory.objects.all()
        context = {
            'article_post_form': article_post_form,
            'categories': categories,
            'father': father,
        }
        return render(request, 'article/create.html', context)

def article_detail(request, id):
    article = Article.objects.get(id=id)
    md = markdown.Markdown(
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ])
    article.body = md.convert(article.body)
    cur = ArticleCategory.objects.get(id=article.category.id)
    fathers = [cur]
    while(cur.father != None):
        fathers.insert(0, cur.father)
        cur = cur.father
    context = {
        'fathers': fathers,
        'article': article,
        'toc': md.toc,
    }
    return render(request, 'article/detail.html', context)

def delete_article(request, id):
    if request.method == 'POST':
        article = Article.objects.get(id=id)
        article.delete()
        return redirect("article:category_list")
    else:
        return HttpResponse("Only POST is allowed")

def update_article(request, id):
    article = Article.objects.get(id=id)
    if request.method == "POST":
        article_post_form = NewArticleForm(data=request.POST)
        if article_post_form.is_valid():
            article.title = request.POST['title']
            article.body = request.POST['body']
            if request.POST['category'] != 'none':
                article.category = ArticleCategory.objects.get(id=request.POST['category'])
            else:
                article.category = None
            article.tags.set(request.POST['tags'].split(','), clear=True)
            article.save()
            return redirect("article:article_detail", id=id)
        else:
            return HttpResponse("Invalid Table Content, Please rewrite!")
    else:
        article_post_form = NewArticleForm()
        categories = ArticleCategory.objects.all()
        context = {
            'article': article,
            'article_post_form': article_post_form,
            'categories': categories,
        }
        return render(request, 'article/update.html', context)

