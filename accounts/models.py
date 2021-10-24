from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, RegexValidator


# Create your models here.
class User(AbstractUser):
    class GenderChoices(models.TextChoices):
        MALE = "M", "남성"
        FEMALE = "F", "여성"
    gender = models.CharField(max_length=1,
                            choices=GenderChoices.choices)

    phone_number = models.CharField(max_length=13,
                                    validators=[RegexValidator(r"^010-?[1-9]\d{3}-?\d{4}$")])
    
    # 20세 미만은 가입불가.
    age = models.CharField(max_length=2,
                            validators=[RegexValidator(r"^[2-9][0-9]$")])

    address = models.CharField(max_length=50, blank=True)
    
    bank = models.CharField(max_length=10, blank=True)
    card = models.CharField(max_length=30, blank=True)
