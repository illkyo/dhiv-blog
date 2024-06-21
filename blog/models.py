from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
# from django.contrib.auth.models import User

class Post(models.Model):
  # author = models.ForeignKey(User, on_delete=models.CASCADE)
  author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  title = models.CharField(max_length = 100, verbose_name="ޕޯސްޓް ޓައިޓަލް")
  content = models.TextField(verbose_name="ޕޯސްޓް ކޮންޓެންޓް")
  date_posted = models.DateTimeField(default=timezone.now())
  
  class Meta:
    ordering = ['-date_posted']
  
  def __str__(self):
    return self.title
  
  def get_absolute_url(self):
      return reverse("blog-postdetail", kwargs={"pk": self.pk})
  