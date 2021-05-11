from django.urls import path, include
from api.views import ArticleView

# from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register('articles', ArticleView, basename='articles')

urlpatterns = [
    #path('api/', include(router.urls)),
    path('articles/',ArticleView.as_view(), name='articles')
]