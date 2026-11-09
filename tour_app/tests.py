from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.utils import IntegrityError
from .models import Category, Tour, Booking, TourComment


class HorseTourAppTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='rider1', password='password123')

        # Создаем категории
        self.cat_horse = Category.objects.create(name='Конный')
        self.cat_hiking = Category.objects.create(name='Пеший')

        # Создаем тур и привязываем категории (Many-to-Many)
        self.tour = Tour.objects.create(
            title='Конный тур в Чон-Кемин',
            description='Прогулка по горам на лошадях',
            price=2000.00
        )
        self.tour.categories.add(self.cat_horse, self.cat_hiking)

    # 1. Проверка связи Many-to-Many (Категории туров)
    def test_tour_categories_many_to_many(self):
        self.assertEqual(self.tour.categories.count(), 2)

    # 2. Проверка ограничения: 1 человек не может взять 2 тура на одно время
    def test_user_cannot_book_duplicate_time(self):
        Booking.objects.create(
            user=self.user,
            tour=self.tour,
            booking_date='2026-06-01',
            booking_time='10:00:00'
        )
        with self.assertRaises(IntegrityError):
            Booking.objects.create(
                user=self.user,
                tour=self.tour,
                booking_date='2026-06-01',
                booking_time='10:00:00'
            )

    # 3. Проверка: 1 человек может оставить несколько комментариев
    def test_user_can_leave_multiple_comments(self):
        TourComment.objects.create(tour=self.tour, user=self.user, text='Супер тур!')
        TourComment.objects.create(tour=self.tour, user=self.user, text='Отличный гид')
        self.assertEqual(TourComment.objects.filter(user=self.user).count(), 2)

    # 4. Проверка отправки POST-запроса на бронирование
    def test_post_create_booking_view(self):
        self.client.login(username='rider1', password='password123')
        response = self.client.post(reverse('create_booking', args=[self.tour.id]), {
            'date': '2026-07-15',
            'time': '14:00:00'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Booking.objects.count(), 1)

    # 5. Проверка отправки POST-запроса на добавление комментария
    def test_post_add_comment_view(self):
        self.client.login(username='rider1', password='password123')
        response = self.client.post(reverse('add_comment', args=[self.tour.id]), {
            'text': 'Прекрасный маршрут!'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(TourComment.objects.count(), 1)