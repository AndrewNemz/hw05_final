from http import HTTPStatus
from django.core.cache import cache
from django.test import Client, TestCase
from ..models import Post, Group, User
from django.urls import reverse


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username="NoName")
        cls.group = Group.objects.create(
            title="Тестовая группа",
            slug="test-slug",
            description="Тестовое описание",
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text="Тестовая пост",
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        cache.clear()

    def test_task_added_url_exists_at_desired_location(self):
        """Страницы доступна любому пользователю."""
        self.public_urls = (
            reverse("posts:home_page"),
            reverse(
                "posts:group_posts", kwargs={"slug": self.group.slug}
            ),
            reverse(
                "posts:post_detail", kwargs={"post_id": self.post.id}
            ),
            reverse(
                "posts:profile", kwargs={"username": self.post.author}
            ),
        )
        for adress in self.public_urls:
            with self.subTest(adress):
                response = self.guest_client.get(adress)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_posts_post_id_edit_url_exists_at_author(self):
        """Страница /posts/post_id/edit/ доступна только автору."""
        response = self.authorized_client.get(f"/posts/{self.post.id}/edit/")
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_create_url_uses_correct_template(self):
        """Страница /create/ перенаправляет пользователя."""
        response = self.guest_client.get('/create/')
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        # Шаблоны по адресам
        templates_url_names = {
            reverse("posts:home_page"): "posts/index.html",
            reverse(
                "posts:group_posts", kwargs={"slug": self.group.slug}
            ): "posts/group_list.html",
            reverse(
                "posts:profile", kwargs={"username": self.post.author}
            ): "posts/profile.html",
            reverse(
                "posts:post_detail", kwargs={"post_id": self.post.id}
            ): "posts/post_detail.html",
            reverse(
                "posts:post_edit", kwargs={"post_id": self.post.id}
            ): "posts/create_post.html",
            reverse("posts:post_create"): "posts/create_post.html",
        }
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)
