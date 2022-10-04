from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.validators import RegexValidator


# Create your models here.

class UserModel(AbstractUser):
    class Meta:
        db_table = 'user'
        
    # GENDERS = (
    #     ('M', '남성(Man)'),
    #     ('W', '여성(Woman)'),
    #     )
    
    bio = models.CharField(max_length=256, default='')
    follow = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followee')
    image = models.ImageField(blank= True, upload_to = "profile/")
    # gender = models.CharField(verbose_name='성별', max_length=1, choices=GENDERS, default='밝히고 싶지 않음')
    # phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    # phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
