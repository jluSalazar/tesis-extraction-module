import factory
from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.auth import get_user_model
import random


# Importa todos los modelos que limpiarás
from projects.models import ResearchProject
from papers.models import Paper
from design.models import ResearchQuestion
from extraction.models import ExtractionRecord, Quote, Comment, Tag

# Importa todas las factories que usarás
from user_management.factories import UserFactory
from projects.factories import ProjectFactory
from papers.factories import PaperFactory
from design.factories import ResearchQuestionFactory
from extraction.factories import (
    ExtractionRecordFactory,
    QuoteFactory,
    TagFactory,
    CommentFactory
)

CustomUser = get_user_model()


class Command(BaseCommand):
    help = 'Seeds the database with development data.'

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write('Deleting old data...')

        # Limpia la BD en orden inverso de dependencias (de hijo a padre)
        Comment.objects.all().delete()
        Quote.objects.all().delete()
        Tag.objects.all().delete()
        ExtractionRecord.objects.all().delete()
        ResearchQuestion.objects.all().delete()
        Paper.objects.all().delete()
        ResearchProject.objects.all().delete()
        CustomUser.objects.filter(is_superuser=False).delete()

        self.stdout.write('Creating new data...')

        # --- 1. Crear Usuarios Base ---
        try:
            superuser = CustomUser.objects.get(username='admin')
        except CustomUser.DoesNotExist:
            superuser = UserFactory(
                username='admin',
                is_staff=True,
                is_superuser=True
            )
            superuser.set_password('admin')
            superuser.save()

        self.stdout.write(f"Superuser 'admin' (pass: 'admin') created.")

        # 1b. Crear Usuario Investigador (Researcher) con clave conocida
        try:
            researcher_user = CustomUser.objects.get(username='researcher')
            self.stdout.write("Researcher 'researcher' already exists.")
        except CustomUser.DoesNotExist:
            researcher_user = UserFactory(
                username='researcher',
                first_name='Dev',
                last_name='Researcher'
            )
            researcher_user.set_password('researcher')  # Clave simple para dev
            researcher_user.save()
            self.stdout.write(f"Researcher 'researcher' (pass: 'researcher') created.")

        project_owner = UserFactory(username='owner')
        researchers = UserFactory.create_batch(5)

        # --- 2. Crear Datos Centrados en el Proyecto (DDD) ---
        self.stdout.write('Creating 3 Projects with full data...')
        for i in range(3):
            # 2a. Crear Proyecto
            project = ProjectFactory(
                owner=project_owner,
                title=f'Systematic Review Project {i + 1}'
            )

            # 2b. Crear Preguntas de Investigación para este Proyecto
            questions = ResearchQuestionFactory.create_batch(4, project=project)

            # 2c. Crear Tags para este Proyecto
            project_tags = TagFactory.create_batch(
                10,
                created_by=project_owner,
                question=factory.Iterator(questions)  # Asigna preguntas cíclicamente
            )
            # Tags inductivos (sin pregunta)
            project_tags.extend(TagFactory.create_batch(
                5,
                created_by=project_owner,
                question=None,
                type=Tag.TagType.INDUCTIVE
            ))

            # 2d. Crear Papers para este Proyecto
            project_papers = PaperFactory.create_batch(
                25,
                project=project,
                uploaded_by=project_owner
            )

            # 2e. Crear Registros de Extracción para cada Paper
            project_records = []
            for paper in project_papers:
                record = ExtractionRecordFactory(
                    paper=paper,
                    assigned_to=random.choice(researchers)
                )
                project_records.append(record)

            # 2f. Crear Quotes y Comentarios para cada Registro
            for record in project_records:
                # Crea 3-8 quotes por papers
                quotes = QuoteFactory.create_batch(
                    random.randint(3, 8),
                    paper=record,  # FK a ExtractionRecord
                    researcher=record.assigned_to
                )

                for quote in quotes:
                    # Asigna 1-3 tags aleatorios del proyecto
                    tags_to_add = random.sample(
                        project_tags,
                        random.randint(1, 3)
                    )
                    quote.tags.add(*tags_to_add)

                    # Añade 0-2 comentarios por quote
                    CommentFactory.create_batch(
                        random.randint(0, 2),
                        quote=quote,
                        user=random.choice(researchers + [project_owner])
                    )

        self.stdout.write(self.style.SUCCESS(
            f'Successfully seeded database with {ResearchProject.objects.count()} projects.'
        ))