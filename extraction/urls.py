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
    path(
        'pending/',
        views.PendingExtractionListView.as_view(),
        name='pending-list'
    ),
    path(
        'project/<int:project_id>/tags/',
        views.TagManagementView.as_view(),
        name='tag-management'
    ),

    # 2. Página para Actualizar un Tag
    path(
        'tags/<int:pk>/update/',
        views.TagUpdateView.as_view(),
        name='tag-update'
    ),

    # 3. Página para Eliminar un Tag
    path(
        'tags/<int:pk>/delete/',
        views.TagDeleteView.as_view(),
        name='tag-delete'
    ),
    # --- URL PARA VISTA DEL RESEARCHER ---
    path(
        'project/<int:project_id>/tags/view/',
        views.ResearcherTagListView.as_view(),
        name='tag-list-researcher'
    ),
]