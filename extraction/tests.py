from django.test import TestCase
from django.contrib.auth import get_user_model
from projects.factories import ProjectFactory
from design.factories import ResearchQuestionFactory
from .factories import TagFactory, QuoteFactory, CommentFactory
from .models import Tag, Comment
from . import services

User = get_user_model()


class TagServiceTests(TestCase):
    """Tests para el Service Layer de Tags."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.project = ProjectFactory(owner=self.user)
        self.question = ResearchQuestionFactory(project=self.project)

    def test_create_tag_with_question_is_mandatory(self):
        """Tag con pregunta debe ser obligatorio."""
        tag = services.create_tag(
            creator=self.user,
            project=self.project,
            tag_name='Test Tag',
            question=self.question
        )

        self.assertTrue(tag.is_mandatory)
        self.assertEqual(tag.question, self.question)

    def test_create_tag_without_question_is_optional(self):
        """Tag sin pregunta debe ser opcional."""
        tag = services.create_tag(
            creator=self.user,
            project=self.project,
            tag_name='Inductive Tag'
        )

        self.assertFalse(tag.is_mandatory)
        self.assertIsNone(tag.question)


class CommentModelTests(TestCase):
    """Tests para el modelo Comment con GenericForeignKey."""

    def test_comment_on_quote(self):
        """Puede crear comentario en Quote."""
        quote = QuoteFactory()
        comment = CommentFactory(content_object=quote)

        self.assertEqual(comment.content_object, quote)
        self.assertIn(comment, quote.comments.all())

    def test_comment_on_tag(self):
        """Puede crear comentario en Tag."""
        tag = TagFactory()
        comment = CommentFactory(
            content_object=tag,
            object_id=tag.id,
            content_type=ContentType.objects.get_for_model(Tag)
        )

        self.assertEqual(comment.content_object, tag)
        self.assertIn(comment, tag.comments.all())

    def test_delete_quote_deletes_comments(self):
        """Al borrar Quote se borran sus comentarios."""
        quote = QuoteFactory()
        comment = CommentFactory(content_object=quote)
        comment_id = comment.id

        quote.delete()

        self.assertFalse(Comment.objects.filter(id=comment_id).exists())