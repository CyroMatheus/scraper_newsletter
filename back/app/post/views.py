from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, status
from .serializer import *

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class CheckPostExists(APIView):
    def post(self, request):
        url = request.data.get("link")
        post_data = Post.objects.filter(link=url).first()
        if post_data:
            serializer = PostSerializer(post_data)
            return Response({'resp': serializer.data}, status=status.HTTP_200_OK)
        return Response({'resp': None}, status=status.HTTP_400_BAD_REQUEST)

class CheckTagExists(APIView):
    def post(self, request):
        tag = request.data.get("tag")
        model = request.data.get("model")
        tag_data = Tag.objects.filter(tag=tag, model=model).first()
        if tag_data:
            serializer = TagSerializer(tag_data)
            return Response({'resp': serializer.data}, status=status.HTTP_200_OK)
        else: return Response({'resp': None}, status=status.HTTP_400_BAD_REQUEST)

class CheckCategoryExists(APIView):
    def post(self, request):
        data = request.data
        category = request.data.get("category")
        model = request.data.get("model")
        category_data = Category.objects.filter(category=category, model=model).first()
        if category_data:
            serializer = CategorySerializer(category_data)
            return Response({'resp': serializer.data}, status=status.HTTP_200_OK)
        return Response({'resp': None}, status=status.HTTP_400_BAD_REQUEST)
