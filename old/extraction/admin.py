from django.contrib import admin
from .models import (
    ExtractionPhase,
    PaperExtraction,
    Tag,
    Quote,
    Comment,
    ErrorHandler
)

# Registramos los modelos para que aparezcan en el admin
admin.site.register(ExtractionPhase)
admin.site.register(PaperExtraction)
admin.site.register(Tag)
admin.site.register(Quote)
admin.site.register(Comment)
admin.site.register(ErrorHandler)