from django.urls import path
from . import views  # Aquí importaremos nuestras vistas (views.py)

# Esta es una buena práctica (KISS, DRY) para el 'namespacing'.
# Nos permite referirnos a las URLs como 'extraction:quote-list'
app_name = 'extraction'

urlpatterns = [
    # A medida que creemos vistas, las añadiremos aquí.
    # Ejemplo (aún no lo añadas si no tienes la vista):
    # path('quotes/', views.QuoteListView.as_view(), name='quote-list'),
    # path('quotes/<int:pk>/', views.QuoteDetailView.as_view(), name='quote-detail'),
]