import tempfile
from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from captcha.models import CaptchaStore
from users.models import CustomUser


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class UserAuthTests(TestCase):
    GIF = (
        b"GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff!\xf9\x04"
        b"\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;"
    )

    def _photo(self, name='test.gif'):
        return SimpleUploadedFile(name, self.GIF, content_type='image/gif')

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='StrongPassword123',
            phone_number='+996333222111',
            date_bir='2000-01-01',
            gender='MALE',
            city='Bishkek',
            photo=self._photo('user.gif'),
        )

    # 1. Тест регистрации
    def test_register(self):
        response = self.client.post('/register/', {
            'username': "newuser",
            'password1': 'StrongPassword123',
            'password2': 'StrongPassword123',
            'first_name': 'Ivan',
            'email': 'ivan@gmail.com',
            'phone_number': '+996444222111',
            'date_bir': "1999-05-05",
            'gender': 'MALE',
            'city': 'Tokmok',
            'photo': self._photo('new.gif'),
        })
        self.assertRedirects(response, '/login/')
        self.assertEqual(CustomUser.objects.count(), 2)

    # 2. Тест авторизации с правильной капчей и перехода в личный кабинет
    def test_login_with_valid_captcha_and_profile(self):
        captcha_key = CaptchaStore.generate_key()
        captcha_obj = CaptchaStore.objects.get(hashkey=captcha_key)

        response = self.client.post('/login/', {
            'username': 'testuser',
            'password': 'StrongPassword123',
            'captcha_0': captcha_key,
            'captcha_1': captcha_obj.response,
        })
        self.assertRedirects(response, '/profile/')
        self.assertEqual(self.client.get('/profile/').status_code, 200)

    # 3. Тест отклонения авторизации при неверной капче
    def test_login_with_invalid_captcha(self):
        captcha_key = CaptchaStore.generate_key()

        response = self.client.post('/login/', {
            'username': 'testuser',
            'password': 'StrongPassword123',
            'captcha_0': captcha_key,
            'captcha_1': 'WRONG_CODE',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    # 4. Тест закрытого доступа в профиль для гостей и выхода (logout)
    def test_profile_and_logout(self):
        # Неавторизованный пользователь должен попасть на /login/
        self.assertRedirects(self.client.get('/profile/'), '/login/')

        # Авторизуемся и выходим
        self.client.force_login(self.user)
        response = self.client.get('/logout/')
        self.assertRedirects(response, '/login/')