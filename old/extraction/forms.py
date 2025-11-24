from django import forms
from .models import Tag
from design.models import ResearchQuestion


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name', 'color', 'justification', 'question']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'color': forms.TextInput(attrs={'type': 'color', 'class': 'input input-bordered w-full'}),
            'justification': forms.Textarea(attrs={'class': 'textarea textarea-bordered w-full', 'rows': 3}),
            'question': forms.Select(attrs={'class': 'select select-bordered w-full'}),
        }

    def __init__(self, *args, **kwargs):
        # 1. Sacamos el 'project' que la Vista nos va a inyectar
        project = kwargs.pop('project', None)

        super().__init__(*args, **kwargs)

        if project:
            # 2. Filtramos el queryset del campo 'question'
            # para mostrar SÓLO las PIs de este proyecto.
            self.fields['question'].queryset = ResearchQuestion.objects.filter(project=project)
            self.fields['question'].empty_label = "Sin Pregunta de Investigación (Tag Inductivo)"