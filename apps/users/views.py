from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .forms import LoginForm, RegistrationForm



def show_login_page(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()

    context = {
        'form': form
    }
    return render(request, "users/login.html", context)

def show_registration_page(request):
    if request.method == 'POST':
        print(request.POST)
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('login-page')
    else:
        form = RegistrationForm()
    context = {
        'form': form
    }
    return render(request, "users/registration.html", context)


def logout_user(request):
    logout(request)
    return redirect('home')

def show_profile_page(request, username):
    author = get_object_or_404(User, username=username)
    articles = author.article_set.all()
    total_views = sum([article.views for article in articles])
    total_likes = sum([article.likes.user.all().count() for article in articles])
    total_dislikes = sum([article.dislikes.user.all().count() for article in articles])
    total_comments = sum([article.comment_set.all().count() for article in articles])


    context = {
        'author': author,
        'total_views': total_views,
        'total_likes': total_likes,
        'total_dislikes': total_dislikes,
        'total_comments': total_comments
    }
    return render(request, 'users/profile.html', context)