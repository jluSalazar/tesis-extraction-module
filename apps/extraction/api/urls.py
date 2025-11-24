from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExtractionViewSet, QuoteViewSet, TagViewSet

router = DefaultRouter()
router.register(r'extractions', ExtractionViewSet, basename='extraction')
router.register(r'quotes', QuoteViewSet, basename='quote')
router.register(r'tags', TagViewSet, basename='tag')

urlpatterns = [
    path('extraction/', include(router.urls)),
]