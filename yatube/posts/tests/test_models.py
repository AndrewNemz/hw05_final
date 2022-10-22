from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post

User = get_user_model()
LENGHT_TEXT: int = 4


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
        )

        cls.test_post = Post.objects.create(
            author=cls.user,
            text='О-о-очень длинный пост)' * LENGHT_TEXT,
        )

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        correct_values = {
            str(self.post): self.post.text[:15],
            str(self.test_post): self.test_post.text[:15],
            str(self.group): self.group.title
        }

        for str_value, expected_value in correct_values.items():
            with self.subTest(str_value=str_value):
                self.assertEqual(str_value, expected_value)
