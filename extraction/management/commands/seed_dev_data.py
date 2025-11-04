from django.core.management.base import BaseCommand
from django.db import transaction
import random

from extraction.models import Quote, Tag
from extraction.models.external import ExtractionPaper
from papers.models import Paper
# Importa todas las factories que usarás
from user_management.factories import UserFactory
from papers.factories import PaperFactory
from extraction.factories import ExtractionRecordFactory, QuoteFactory, TagFactory
from user_management.models import CustomUser


# Asumo que design y project también tienen factories
#from design.factories import ResearchQuestionFactory
#from projects.factories import ProjectFactory

class Command(BaseCommand):
    help = 'Seeds the database with development data.'

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write('Deleting old data...')
        # Limpia la BD en orden inverso de dependencias
        # (Esto es opcional pero recomendado para dev)
        Quote.objects.all().delete()
        Tag.objects.all().delete()
        ExtractionPaper.objects.all().delete()
        Paper.objects.all().delete()
        CustomUser.objects.filter(is_superuser=False).delete()

        self.stdout.write('Creating new data...')

        # 1. Crea Usuarios
        users = UserFactory.create_batch(10)

        # 2. Crea Tags
        tags = TagFactory.create_batch(20)

        # 3. Crea Papers
        papers = PaperFactory.create_batch(100)

        # 4. Crea los Registros de Extracción (el "modelo de enlace")
        for paper in papers:
            ExtractionRecordFactory(
                paper=paper,
                assigned_to=random.choice(users) # Asigna aleatoriamente
            )

        # 5. Crea Quotes (usando los papers ya creados)
        for paper in papers:
            # Crea 5 quotes por paper
            quotes = QuoteFactory.create_batch(
                5,
                paper=paper,
                researcher=random.choice(users)
            )
            # Asigna tags aleatorios a cada quote
            for quote in quotes:
                quote.tags.add(random.choice(tags))

        self.stdout.write(self.style.SUCCESS('Successfully seeded database.'))