from django.db import models
    
class Scrape(models.Model):
    id = models.AutoField(primary_key=True)
    trending_id = models.CharField(max_length=250,default='none')
    url = models.TextField(default='none')
    title = models.TextField(default='none')
    content = models.TextField(default='none')
    images = models.TextField(default='none')
    status = models.CharField(max_length=30,default="Not Scraped")
    
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

    class Meta:
        verbose_name_plural = "TwitterPost"

    def __str__(self):
        return self.content

class Trending(models.Model):
    id = models.AutoField(primary_key=True)
    topic = models.TextField(default='none')
    related_topics_rising = models.TextField(default='none')
    related_topics_top = models.TextField(default='none')
    related_query_rising = models.TextField(default='none')
    related_query_top = models.TextField(default='none')
    source = models.CharField(max_length=50, default='none')
    status = models.CharField(max_length=50, default='none')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Trending"

    def __str__(self):
        return self.topic
    
    
class Post(models.Model):
    id = models.AutoField(primary_key=True)
    post_id = models.CharField(max_length=250, default='none')
    title = models.TextField(default='none')
    meta = models.TextField(default='none')
    subtitle = models.TextField(default='none')
    content = models.TextField(default='none')
    conclusion= models.TextField(default='none')
    category = models.CharField(max_length=250, default='none')
    subcategory = models.CharField(max_length=250, default='none')
    tags = models.TextField(default='none')
    author = models.CharField(max_length=20, default="Max")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=30, default='Pre Draft')
    survey = models.TextField(default='none')
    image_prompt = models.TextField(default='none')
    image_data = models.TextField(default='none')
    image_path = models.CharField(max_length=250, default='none')
    image_crm = models.CharField(max_length=250, default='none')
    all_image_data = models.TextField(default='none')
    class Meta:
        verbose_name_plural = "Post"
    
    def __str__(self):
        return self.title

