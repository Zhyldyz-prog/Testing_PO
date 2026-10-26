# blog/tests.py
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

    # 1. Проверяем, что у нового блога количество просмотров равно 0
    def test_new_blog_has_zero_views(self):
        self.assertEqual(self.blog.views, 0)

    # 2. Проверяем открытие списка статей (статус-код и шаблон)
    def test_blog_list_status_and_template(self):
        response = self.client.get(reverse('blog_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blog_list.html')

    # 3. Проверяем отображение заголовка в списке
    def test_blog_list_contains_title(self):
        response = self.client.get(reverse('blog_list'))
        self.assertContains(response, 'Тестовый заголовок')

    # 4. Проверяем вывод специального сообщения, когда список пуст
    def test_blog_list_empty(self):
        Blog.objects.all().delete()
        response = self.client.get(reverse('blog_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Пока статей нет.')

    # 5. Проверяем наличие корректной ссылки на детальную страницу
    def test_list_has_detail_link(self):
        response = self.client.get(reverse('blog_list'))
        detail_url = reverse('blog_detail', args=[self.blog.pk])
        self.assertContains(response, detail_url)

    # 6. Проверяем загрузку данных на детальной странице
    def test_detail_contains_blog_data(self):
        response = self.client.get(reverse('blog_detail', args=[self.blog.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blog_detail.html')
        self.assertContains(response, 'Тестовый заголовок')
        self.assertContains(response, 'Тестовое описание')

    # 7. Проверяем запрос к несуществующей странице (должна быть ошибка 404)
    def test_detail_nonexistent_id_returns_404(self):
        response = self.client.get(reverse('blog_detail', args=[999]))
        self.assertEqual(response.status_code, 404)

    # 8. Проверяем увеличение счетчика просмотров при GET-запросе
    def test_views_increase_after_detail_get(self):
        self.client.get(reverse('blog_detail', args=[self.blog.pk]))
        self.blog.refresh_from_db()  # Обновляем данные из базы
        self.assertEqual(self.blog.views, 1)