from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExtractionViewSet

router = DefaultRouter()
router.register(r'extractions', ExtractionViewSet, basename='extraction')

urlpatterns = [
    path('', include(router.urls)),
]