import re

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core import validators
from django.utils.deconstruct import deconstructible

@deconstructible
class DhivehiUsernameValidator(validators.RegexValidator):
    regex = r"^[\w\u0780-\u07BF.@+-]+\Z"
    message = _(
        "ޔޫސަރނަމެއް ޖައްސަވާ. 150 އަކުރައް ވުރެއް ކުރު. ހަމަ އެކަނި ޖެއްސެވޭނީ ތާނަ އަކުރު، ނަންބަރ ޑިޖިޓް ނުވަތަ _/-/+/./@"
    )
    flags = 0
    
username_validator = DhivehiUsernameValidator

class User(AbstractUser):
    username = models.CharField(
        _("ޔޫސަރނަން"),
        max_length=150,
        unique=True,
        help_text=_(
            "ޔޫސަރނަމެއް ޖައްސަވާ. 150 އަކުރައް ވުރެއް ކުރު. ހަމަ އެކަނި ޖެއްސެވޭނީ ތާނަ އަކުރު، ނަންބަރ ޑިޖިޓް ނުވަތަ _/-/+/./@" 
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("ތި ނަން ވަނީ ނަންގަވާފައި"),
        },
    )
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='pfps', blank=True)
    
    def set_default_pfp(self):
        
        dhiv_akuru = ['ހ', 'ށ', 'ނ', 'ރ', 'ބ', 'ޅ', 'ކ', 'އ', 'ވ', 'މ', 'ފ', 'ދ', 'ތ', 'ލ', 'ގ', 'ޏ', 'ސ', 'ޑ', 'ޒ', 'ޓ', 'ޔ', 'ޕ', 'ޖ', 'ޗ']
        
        if self.user.username[0] in dhiv_akuru:
            self.image = f'defaults/{self.user.username[0]}.jpg'
        else:
            self.image = "default.jpg"
        
        # if self.user.username[0] == 'ހ':
        #     self.image = 'defaults/ހ.jpg'
        # if self.user.username[0] == 'ށ':
        #     self.image = 'defaults/ށ.jpg'
                
    def save(self, *args, **kwargs):
        if not self.image:
            self.set_default_pfp()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.user.username} ގެ ޕްރޮފައިލް'