from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseForbidden

# Modelos
from .models import ExtractionRecord, Tag
from projects.models import ResearchProject

# Lógica de Negocio
from . import services
from .forms import TagForm

class PendingExtractionListView(LoginRequiredMixin, ListView):
    """
    Muestra la lista de 'ExtractionRecords' que están
    asignados al usuario logueado y tienen estado 'Pending'.
    """
    model = ExtractionRecord
    # Usamos un nombre de template específico
    template_name = 'extraction/papers/pending_list.html'
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


class TagManagementView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """
    Vista "2-en-1": Muestra la lista de Tags (ListView) y
    maneja la creación de un nuevo Tag (manejando POST).
    """
    model = Tag
    template_name = 'extraction/tags/tag_management.html'
    context_object_name = 'tags'

    def test_func(self):
        """Verifica que el usuario sea el Owner del proyecto."""
        project = self.get_project()
        return project.owner == self.request.user

    def get_project(self):
        """Obtiene el proyecto desde la URL (lo usaremos varias veces)"""
        return get_object_or_404(
            ResearchProject,
            id=self.kwargs['project_id']
        )

    def get_queryset(self):
        """Filtra los tags para mostrar solo los de este proyecto."""
        return Tag.objects.filter(
            question__project=self.get_project()
        ).select_related('question')

    def get_context_data(self, **kwargs):
        """Añade el proyecto y el formulario al contexto."""
        context = super().get_context_data(**kwargs)
        project = self.get_project()
        context['project'] = project
        context['form'] = TagForm(project=project)  # Inyecta el proyecto al form
        return context

    def post(self, request, *args, **kwargs):
        """Maneja la creación del nuevo Tag."""
        project = self.get_project()
        form = TagForm(request.POST, project=project)

        if form.is_valid():
            # No usamos form.save()
            # Usamos nuestro SERVICIO para encapsular la lógica de negocio
            tag_name = form.cleaned_data['name']
            question = form.cleaned_data['question']

            # ¡Llamamos al servicio que probamos con BDD!
            services.create_tag_with_pi(
                creator=request.user,
                project=project,
                tag_name=tag_name,
                pi_text=question.text if question else None
            )

            # Guardamos el resto de los datos del form
            tag_instance = form.save(commit=False)
            tag_instance.creator = request.user
            # El servicio ya creó el tag, aquí solo actualizamos
            # los campos 'color' y 'justification'
            # (Esto se puede refinar, pero es un buen inicio)

            # --- Refinamiento ---
            # El servicio create_tag_with_pi ya crea el tag.
            # Deberíamos tener un servicio `create_tag` más genérico.
            # Por ahora, vamos a usar la lógica del BDD:
            tag = form.save(commit=False)
            tag.created_by = request.user
            tag.type = Tag.TagType.DEDUCTIVE  # Asumimos

            # Regla de Negocio (Regla #10)
            tag.is_mandatory = (tag.question is not None)

            tag.save()
            form.save_m2m()  # Para ManyToMany (si los tuvieras)

            return redirect('extraction:tag-management', project_id=project.id)

        # Si el form no es válido, re-renderiza la página
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)


# --- VISTA 2: ACTUALIZAR TAG (Owner) ---

class TagUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Tag
    form_class = TagForm
    template_name = 'extraction/tags/tag_form_update.html'

    def test_func(self):
        """Verifica que el usuario sea el Owner."""
        tag = self.get_object()
        return tag.question.project.owner == self.request.user

    def get_form_kwargs(self):
        """Inyecta el 'project' al __init__ del formulario."""
        kwargs = super().get_form_kwargs()
        kwargs['project'] = self.get_object().question.project
        return kwargs

    def form_valid(self, form):
        """Aplica la lógica de negocio al actualizar."""
        tag = form.save(commit=False)
        tag.is_mandatory = (tag.question is not None)
        tag.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('extraction:tag-management',
                       kwargs={'project_id': self.get_object().question.project.id})


# --- VISTA 3: ELIMINAR TAG (Owner) ---

class TagDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Tag
    template_name = 'extraction/tags/tag_confirm_delete.html'

    def test_func(self):
        """Verifica que el usuario sea el Owner."""
        tag = self.get_object()
        return tag.question.project.owner == self.request.user

    def get_success_url(self):
        """Redirige de vuelta a la lista de manejo."""
        return reverse_lazy('extraction:tag-management',
                            kwargs={'project_id': self.get_object().question.project.id})


# --- VISTA 4: LISTA DE TAGS (Researcher) ---

class ResearcherTagListView(LoginRequiredMixin, ListView):
    """
    Muestra la lista de Tags "públicos" a un Researcher.
    Respeta la regla de negocio 'is_tag_list_public'.
    """
    model = Tag
    template_name = 'extraction/tags/tag_list_researcher.html'
    context_object_name = 'tags'

    def get_project(self):
        return get_object_or_404(
            ResearchProject,
            id=self.kwargs['project_id']
        )

    def get_queryset(self):
        project = self.get_project()

        # --- AQUÍ LA LÓGICA DE NEGOCIO (BDD) ---
        # 1. Verificamos si la lista debe ser pública
        is_public = services.is_tag_list_public(project)

        if not is_public:
            # Regla #9: Si no es pública, no mostramos nada.
            return Tag.objects.none()

            # 2. Si es pública, mostramos solo los tags públicos de este proyecto
        return Tag.objects.filter(
            question__project=project,
            is_public=True  # (Futura Regla: Owner puede ocultar tags)
        ).select_related('question')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = self.get_project()
        # Verificamos si la lista está vacía por la lógica de negocio
        context['is_list_public'] = (context['tags'].exists() or
                                     not services.is_tag_list_public(self.get_project()))
        return context