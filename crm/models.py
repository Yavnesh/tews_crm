from django.db import models
    
class Scrape(models.Model):
    id = models.AutoField(primary_key=True)
    trending_id = models.CharField(max_length=250,default='none')
    url = models.TextField(default=[])
    title = models.TextField(default=[])
    content = models.TextField(default=[])
    short_content = models.TextField(default='none')
    images = models.TextField(default=[])
    status = models.CharField(max_length=30,default="Not Scraped")
    rep_count = models.TextField(default='0')
    
    class Meta:
        verbose_name_plural = "Scrape"

    def __str__(self):
        return self.title
    

class TwitterPost(models.Model):
    id = models.AutoField(primary_key=True)
    post_id = models.CharField(max_length=250,default='none')
    content = models.TextField(default='none')
    status = models.CharField(max_length=50,default='No Tweet')
    created_at = models.DateTimeField(auto_now_add=True)
    rep_count = models.TextField(default='0')

    class Meta:
        verbose_name_plural = "TwitterPost"

    def __str__(self):
        return self.content

class Trending(models.Model):
    id = models.AutoField(primary_key=True)
    topic = models.TextField(default='none')
    related_topics_rising = models.TextField(default=[])
    related_topics_top = models.TextField(default=[])
    related_query_rising = models.TextField(default=[])
    related_query_top = models.TextField(default=[])
    source = models.CharField(max_length=50, default='none')
    status = models.CharField(max_length=50, default='none')
    created_at = models.DateTimeField(auto_now_add=True)
    rep_count = models.TextField(default='0')

    class Meta:
        verbose_name_plural = "Trending"

    def __str__(self):
        return self.topic
    
    
class Post(models.Model):
    id = models.AutoField(primary_key=True)
    post_id = models.CharField(max_length=250, default='none')
    title = models.TextField(default=[])
    meta = models.TextField(default='none')
    subtitle = models.TextField(default=[])
    content = models.TextField(default=[])
    conclusion= models.TextField(default=[])
    category = models.CharField(max_length=250, default=[])
    subcategory = models.CharField(max_length=250, default=[])
    tags = models.TextField(default=[])
    author = models.CharField(max_length=20, default="Max")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=30, default='Pre Draft')
    survey = models.TextField(default=[])
    image_prompt = models.TextField(default='none')
    image_data = models.TextField(default='none')
    image_path = models.CharField(max_length=250, default='none')
    image_crm = models.CharField(max_length=250, default='none')
    all_image_data = models.TextField(default=[])
    rep_count = models.TextField(default='0')
    class Meta:
        verbose_name_plural = "Post"
    
    def __str__(self):
        return self.title

