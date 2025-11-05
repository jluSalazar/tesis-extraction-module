from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

# Importamos nuestro servicio
from . import services
from .models import ExtractionRecord

class PendingExtractionListView(LoginRequiredMixin, ListView):
    """
    Muestra la lista de 'ExtractionRecords' que están
    asignados al usuario logueado y tienen estado 'Pending'.
    """
    model = ExtractionRecord
    # Usamos un nombre de template específico
    template_name = 'extraction/pending_list.html'
    # Damos un nombre claro a la variable en el template
    context_object_name = 'pending_records'

    def get_queryset(self):
        """
        Sobrescribimos este método para que la vista llame
        a nuestro servicio, en lugar de usar el ORM directamente.
        """
        # ¡La vista no sabe CÓMO se obtienen los datos!
        # Solo pide al servicio los datos que necesita.
        user = self.request.user
        return services.get_pending_extractions(user=user)