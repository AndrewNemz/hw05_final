from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from ..models import Post, Group, User


User = get_user_model()
TEST_OF_POST: int = 13
FIRST_PAGE_POSTS: int = 10
SECOND_PAGE_POSTS: int = 3


class PostPaginatorTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username="NoName")
        cls.group = Group.objects.create(
            title="Тестовая группа",
            slug="test-slug",
            description="Тестовое описание",
        )
        for post in range(TEST_OF_POST):
            cls.post = Post.objects.create(
                author=cls.user,
                text="Тестовая пост",
                group=cls.group,
            )
            post += 1

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_index_show_correct_context(self):
        """Постов на странице index  равно ожидаемому кол-ву(10)."""
        response = self.guest_client.get(reverse("posts:home_page"))
        expected = list(Post.objects.all()[:FIRST_PAGE_POSTS])
        self.assertEqual(list(response.context["page_obj"]), expected)

    def test_group_list_show_correct_context(self):
        """Постов на странице group_posts  равно ожидаемому кол-ву(10)."""
        response = self.guest_client.get(
            reverse("posts:group_posts", kwargs={"slug": self.group.slug})
        )
        expected = list(
            Post.objects.filter(group_id=self.group.id)[:FIRST_PAGE_POSTS]
        )
        self.assertEqual(list(response.context["page_obj"]), expected)

    def test_profile_show_correct_context(self):
        """Постов на странице profile  равно ожидаемому кол-ву(10)."""
        response = self.guest_client.get(
            reverse("posts:profile", args=(self.post.author,))
        )
        expected = list(
            Post.objects.filter(author_id=self.user.id)[:FIRST_PAGE_POSTS]
        )
        self.assertEqual(list(response.context["page_obj"]), expected)

    def test_second_page_contains_three_records(self):
        """Постов на странице index равно ожидаемому кол-ву(3)."""
        response = self.client.get(reverse('posts:home_page') + '?page=2')
        self.assertEqual(len(response.context['page_obj']), SECOND_PAGE_POSTS)

    def test_second_page_profile_contains_three_records(self):
        """Постов на странице profile равно ожидаемому кол-ву(3)."""
        response = self.client.get(
            reverse(
                'posts:profile', args=(self.post.author,)
            )
            + '?page=2'
        )
        self.assertEqual(len(response.context['page_obj']), SECOND_PAGE_POSTS)

    def test_second_page_profile_contains_three_records(self):
        """Постов на странице group_posts равно ожидаемому кол-ву(3)."""
        response = self.client.get(
            reverse(
                'posts:group_posts', kwargs={"slug": self.group.slug}
            )
            + '?page=2'
        )
        self.assertEqual(len(response.context['page_obj']), SECOND_PAGE_POSTS)
