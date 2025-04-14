from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLE_CHOICES = [
        ('parent', 'Родитель'),
        ('child', 'Ребенок'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='parent')
    bio = models.TextField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.user.username
