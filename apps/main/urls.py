from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_home_page, name='home'),
    path('contacts/', views.show_contact_page, name='contacts'),
    path('faqs/', views.show_faqs_page, name='faqs'),
    path('search/', views.search, name='search'),
    path('categories/<int:category_id>/', views.show_category_page, name='category-page'),
    path('details/<int:details_id>/', views.show_details_page, name='details-page'),
    path('details/<int:details_id>/delete/', views.ArticleDeleteView.as_view(), name='details-delete'),
    path('details/<int:details_id>/update/', views.ArticleUpdateView.as_view(), name='details-update'),
    path('details/<int:details_id>/<str:action>/', views.add_like_or_dislike, name='vote'),
    path('create/', views.show_article_form, name='article_page')
]

