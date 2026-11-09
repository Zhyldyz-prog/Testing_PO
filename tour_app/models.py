from django.db import models
from django.contrib.auth.models import User


# 1. Категории (Конный, Пеший, На мото)
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# 2. Модель Тура (Многие ко многим с Категориями)
class Tour(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    categories = models.ManyToManyField(Category, related_name="tours")

    def __str__(self):
        return f"{self.title} ({self.price} сом)"


# 3. Бронирование (Ограничение: 1 человек - 1 тур на конкретную дату и время)
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="bookings")
    booking_date = models.DateField()
    booking_time = models.TimeField()

    class Meta:
        unique_together = ('user', 'booking_date', 'booking_time')

    def __str__(self):
        return f"Бронь: {self.user.username} - {self.tour.title}"


# 4. Комментарии (1 человек может оставить несколько комментариев)
class TourComment(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Отзыв {self.user.username} на {self.tour.title}"