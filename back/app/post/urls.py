from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import *

router = DefaultRouter()
router.register(r'Tags', TagViewSet)
router.register(r'Category', CategoryViewSet)
router.register(r'Post', PostViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('posts/check-exists/', CheckPostExists.as_view(), name='check-post-exists'),
    path('tags/check-exists/', CheckTagExists.as_view(), name='check-tags-exists'),
    path('categories/check-exists/', CheckCategoryExists.as_view(), name='check-categories-exists'),
]