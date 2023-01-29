from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='default.png', upload_to='profile_image')
    city = models.CharField(max_length=50, blank=True)
    zone = models.CharField(max_length=50, blank=True)
    contact_no = models.CharField(max_length=12, blank=True)
    tole = models.CharField(max_length=50, blank=True)
    bio = models.TextField()

    def get_absolute_url(self):
        return reverse("auth_users:profile", args=[self.slug])

    def __str__(self):
        return self.user.username