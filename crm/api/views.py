from crm.models import Post
from crm.api.serializers import PostSerializer
# from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework import status

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class PostAPI(APIView):

    # authentication_classes = [TokenAuthentication]  # Optional: Set authentication methods
    # permission_classes = [IsAuthenticated]  # Require authentication

    def get(self, request, pk = None, format = None):
        id = pk
        if id is not None:
            postapi = Post.objects.get(id=id)
            serializer = PostSerializer(postapi)
            return Response(serializer.data)
        postapi = Post.objects.all()
        serializer = PostSerializer(postapi, many = True)
        return Response(serializer.data)
    # serializer_class = ScrapeSerializer
    # authentication_classes = [SessionAuthentication]
    # permission_classes = [IsAuthenticated]