from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from captcha.fields import CaptchaField
from users.models import CustomUser

GENDER = (
    ('MALE', "MALE"),
    ("FEMALE", "FEMALE")
)


class CustomRegisterForm(UserCreationForm):
    photo = forms.ImageField(required=True)
    email = forms.EmailField(required=True, initial="@gmail.com")
    phone_number = forms.CharField(max_length=15, required=True, initial='+996')
    date_bir = forms.DateField(required=True)
    gender = forms.ChoiceField(choices=GENDER, required=True, initial='MALE')
    city = forms.CharField(max_length=100, required=True)

    class Meta:
        model = CustomUser
        fields = (
            'username',
            'password1',
            'password2',
            'first_name',
            'photo',
            'email',
            'phone_number',
            'date_bir',
            'gender',
            'city'
        )

    def save(self, commit=True):
        user = super(CustomRegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class CustomLoginForm(AuthenticationForm):
    captcha = CaptchaField(label="Введите код с картинки")