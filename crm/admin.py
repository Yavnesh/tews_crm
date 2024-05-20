from django.contrib import admin
from .models import Scrape, Post, TwitterPost, Trending
# Register your models here.
class ScrapeAdmin(admin.ModelAdmin):
    list_display = ('id', 'trending_id', 'title', 'status')
    search_fields = ('title', 'status')
    list_per_page = 50

class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'post_id', 'category', 'subcategory','author', 'status', 'title')
    search_fields = ('title', 'category')
    list_per_page = 50

class TwitterPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'post_id', 'content', 'status')
    search_fields = ('content', 'status')
    list_per_page = 50

class TrendingAdmin(admin.ModelAdmin):
    list_display = ('id', 'topic', 'status', 'source')
    search_fields = ('topic', 'status')
    list_per_page = 50

admin.site.register(Scrape, ScrapeAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(TwitterPost, TwitterPostAdmin)
admin.site.register(Trending, TrendingAdmin)