# from django.db import models
# from django.contrib.auth.models import AbstractBaseUser
# from django.core.validators import RegexValidator

# class User(AbstractBaseUser):
#   regex_validator = RegexValidator(r"^[\w.@+-]+$", "Username does not comply")
#   username = models.CharField(max_length=150, validators=[regex_validator], unique=True, help_text='Required. 150 characters or fewer.')
  
#   USERNAME_FIELD = "username"