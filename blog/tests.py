
from django.test import TestCase, Client
from django.urls import reverse
from .models import Blog


class BlogTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.blog = Blog.objects.create(
            title='Тестовый заголовок',
            description='Тестовое описание',
            author='Тестовый автор'
        )

    # 1. Проверяем начальное количество просмотров
    def test_new_blog_has_zero_views(self):
        self.assertEqual(self.blog.views, 0)

    # 2. Проверяем открытие списка статей
    def test_blog_list_status_and_template(self):
        response = self.client.get(reverse('blog_list'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'blog/blog_list.html'
        )

    # 3. Проверяем отображение заголовка
    def test_blog_list_contains_title(self):
        response = self.client.get(reverse('blog_list'))

        self.assertContains(response, 'Тестовый заголовок')

    # 4. Проверяем список без статей
    def test_blog_list_empty(self):
        Blog.objects.all().delete()

        response = self.client.get(reverse('blog_list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Пока статей нет.')

    # 5. Проверяем ссылку на страницу статьи
    def test_list_has_detail_link(self):
        response = self.client.get(reverse('blog_list'))
        detail_url = reverse(
            'blog_detail', args=[self.blog.pk]
        )

        self.assertContains(response, detail_url)

    # 6. Проверяем данные на странице статьи
    def test_detail_contains_blog_data(self):
        response = self.client.get(
            reverse('blog_detail', args=[self.blog.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'blog/blog_detail.html'
        )
        self.assertContains(response, 'Тестовый заголовок')
        self.assertContains(response, 'Тестовое описание')

    # 7. Проверяем ошибку 404
    def test_detail_nonexistent_id_returns_404(self):
        response = self.client.get(
            reverse('blog_detail', args=[999])
        )

        self.assertEqual(response.status_code, 404)

    # 8. Проверяем увеличение просмотров
    def test_views_increase_after_detail_get(self):
        self.client.get(
            reverse('blog_detail', args=[self.blog.pk])
        )

        self.blog.refresh_from_db()

        self.assertEqual(self.blog.views, 1)
