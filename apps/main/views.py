from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Category, FAQ, Article, Like, Dislike, ArticleViewsCount
from .forms import ArticleForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView, DeleteView
from django.core.paginator import Paginator




class ArticleDeleteView(DeleteView):
    model = Article
    template_name = 'main/article_confirm_delete.html'
    success_url = '/'
    pk_url_kwarg = 'details_id'


class ArticleUpdateView(UpdateView):
    model = Article
    template_name = 'main/article_form.html'
    form_class = ArticleForm
    success_url = ''
    pk_url_kwarg = 'details_id'


    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        prefix = 'Создать' if 'create' in self.request.path else 'Изменить'
        context['prefix'] = prefix
        return context

def show_home_page(request):
    articles = Article.objects.all()

    paginator = Paginator(articles, 3)
    page = request.GET.get('page')
    articles = paginator.get_page(page)

    context = {
        'articles': articles
    }
    return render(request, "main/index.html", context)

def show_contact_page(request):
    return render(request, "main/contacts.html")

def show_faqs_page(request):
    return render(request, "main/faqs.html")


def show_category_page(request, category_id):

    query = request.GET.get('sort', 'id')



    if category_id == 0:
        category = 'Все категории'
        articles = Article.objects.all().order_by(query)
    else:
        category = Category.objects.get(pk=category_id)
        articles = Article.objects.filter(category=category).order_by(query)


    sorting_fields = {
        'По названию': ['title', '-title'],
        'По просмотрам': ['title', '-views'],
        'По дате': ['title', '-created_at'],
    }

    paginator = Paginator(articles, 8)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    context = {
        'category': category,
        'articles': articles,
        'sorting_fields': sorting_fields
    }
    return render(request, 'main/category_page.html', context)

def show_details_page(request, details_id):
    details = Article.objects.get(pk=details_id)

    try:
        details.likes
    except Exception as e:
        Like.objects.create(article=details)

    try:
        details.dislikes
    except Exception as e:
        Dislike.objects.create(article=details)

    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.article = details
            form.author = request.user
            form.save()
            return redirect('details-page', details_id)
    else:
        form = CommentForm()

    if request.user.is_authenticated:
        viewed_article, created = ArticleViewsCount.objects.get_or_create(article=details, user=request.user)


        if created:
            details.views += 1
            details.save()
    context = {
        'article': details,
        'form': form
    }
    return render(request, "main/details.html", context)

@login_required(login_url='login-page')
def show_article_form(request):
    prefix = 'Создать' if 'create' in request.path else 'Изменить'
    # if not request.user.is_authenticated:
    #     return redirect('login-page')


    if request.method == 'POST':
        form = ArticleForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = request.user
            form.save()
            return redirect('details-page', form.pk)
    else:
        form = ArticleForm

    context = {
        'prefix': prefix,
        'form': form
    }
    return render(request, "main/article_form.html", context)


def add_like_or_dislike(request, details_id, action):
    details = Article.objects.get(id=details_id)

    if action == 'add_like':
        if request.user in details.likes.user.all():
            details.likes.user.remove(request.user.id)
        else:
            details.likes.user.add(request.user.id)
            details.dislikes.user.remove(request.user.id)

    elif action == 'add_dislike':
        if request.user in details.dislikes.user.all():
            details.dislikes.user.remove(request.user.id)
        else:
            details.dislikes.user.add(request.user.id)
            details.likes.user.remove(request.user.id)
    return redirect('details-page', details.id)


def search(request):
    query = request.GET.get('q')
    articles = Article.objects.filter(title__iregex=query)
    context = {
        'articles': articles
    }
    return render(request, 'main/search.html', context)