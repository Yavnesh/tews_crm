from rest_framework import serializers
from crm.models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id','post_id','title','meta','subtitle','content','conclusion','category','subcategory','tags','author','survey','image_data']