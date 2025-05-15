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
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)  # Поле для аватарки
    family = models.ForeignKey('Family', on_delete=models.SET_NULL, null=True, blank=True, related_name='members_profiles')

    def __str__(self):
        return self.user.username

class Family(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=12, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

class FamilyMember(models.Model):
    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name='members')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='families')
    joined_at = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.profile.user.username} in {self.family.name}"
