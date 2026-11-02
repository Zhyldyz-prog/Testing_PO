from django.test import TestCase
from django.urls import reverse
from .models import Item


class ItemCRUDTests(TestCase):

    def setUp(self):
        """Создаем тестовый элемент перед каждым тестом"""
        self.item = Item.objects.create(
            title='Тестовый товар',
            description='Описание тестового товара',
            price=150.00
        )

    # 1. Тест создания (CREATE)
    def test_item_create_view(self):
        response = self.client.post(reverse('item_create'), {
            'title': 'Новый товар',
            'description': 'Описание нового товара',
            'price': 250.00
        })
        # Проверяем редирект обратно на список
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Item.objects.count(), 2)

    # 2. Тест просмотра списка (READ LIST)
    def test_item_list_view(self):
        response = self.client.get(reverse('item_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'crud_app/item_list.html')
        self.assertContains(response, 'Тестовый товар')

    # 3. Тест просмотра одного элемента (READ DETAIL)
    def test_item_detail_view(self):
        response = self.client.get(reverse('item_detail', args=[self.item.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'crud_app/item_detail.html')
        self.assertContains(response, 'Описание тестового товара')

    # 4. Тест редактирования (UPDATE)
    def test_item_update_view(self):
        response = self.client.post(reverse('item_update', args=[self.item.pk]), {
            'title': 'Обновленный товар',
            'description': 'Обновленное описание',
            'price': 300.00
        })
        self.assertEqual(response.status_code, 302)
        self.item.refresh_from_db()
        self.assertEqual(self.item.title, 'Обновленный товар')

    # 5. Тест удаления (DELETE)
    def test_item_delete_view(self):
        response = self.client.post(reverse('item_delete', args=[self.item.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Item.objects.count(), 0)