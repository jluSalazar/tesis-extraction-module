from django.contrib import admin
from .models import (
    Extraction,
    ExtractionRecord,
    Tag,
    Quote,
    Comment,
    ErrorHandler
)

# Registramos los modelos para que aparezcan en el admin
admin.site.register(Extraction)
admin.site.register(ExtractionRecord)
admin.site.register(Tag)
admin.site.register(Quote)
admin.site.register(Comment)
admin.site.register(ErrorHandler)