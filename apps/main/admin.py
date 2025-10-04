from django.contrib import admin

from .models import Category, FAQ, Article, Comment, ArticleImage

class ArticleImageInline(admin.TabularInline):
    model = ArticleImage
    extra = 1

class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'views', 'is_visible', 'category', 'author', 'created_at']
    list_display_links = ['id', 'title']
    list_editable = ['category', 'is_visible', 'author']
    list_filter = ['category', 'is_visible', 'created_at']
    search_fields = ['title']
    readonly_fields = ['views']
    inlines = [ArticleImageInline]

admin.site.register(Category)
admin.site.register(FAQ)
admin.site.register(Comment)
admin.site.register(Article, ArticleAdmin)