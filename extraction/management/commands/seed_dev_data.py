from django.core.management.base import BaseCommand
from django.db import transaction

# Importa las factories que necesitas para el "seed"
from extraction.factories import QuoteFactory, TagFactory
from papers.factories import PaperFactory
from design.factories import ResearchQuestionFactory

class Command(BaseCommand):
    help = 'Seeds the database with realistic development data.'

    @transaction.atomic # Asegura que todo se cree o nada
    def handle(self, *args, **options):
        self.stdout.write('Seeding database...')

        # Limpiar datos antiguos (opcional, cuidado en prod)
        # Quote.objects.all().delete()
        # Tag.objects.all().delete()
        # Paper.objects.all().delete()

        # Crear 10 Preguntas de Investigación
        ResearchQuestionFactory.create_batch(10)

        # Crear 50 Papers
        PaperFactory.create_batch(50)

        # Crear 200 Quotes (asociadas aleatoriamente a los papers creados)
        # Nota: QuoteFactory llama a PaperFactory, así que esto crea 200 quotes Y 200 papers más.
        # Es mejor crear los papers primero y luego asociarlos:

        # papers = PaperFactory.create_batch(50)
        # for paper in papers:
        #    QuoteFactory.create_batch(5, paper=paper) # 5 quotes por paper

        # La forma más simple para empezar:
        QuoteFactory.create_batch(200) # Creará 200 Quotes y sus dependencias

        self.stdout.write(self.style.SUCCESS('Successfully seeded database.'))