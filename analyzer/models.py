from django.db import models
from django.contrib.auth.models import User
import random
import string

def generate_tracking_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

class Institution(models.Model):
    name = models.CharField(max_length=200, verbose_name="Kurum/Üniversite Adı")
    is_active = models.BooleanField(default=True, verbose_name="Aktif Müşteri")

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, verbose_name="Bağlı Olduğu Kurum")

    def __str__(self):
        return f"{self.user.username} - {self.institution.name}"

class Feedback(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, verbose_name="İlgili Kurum")
    category = models.CharField(max_length=100)
    text = models.TextField()
    sentiment = models.CharField(max_length=20)
    score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    tracking_code = models.CharField(max_length=10, unique=True, default=generate_tracking_code)
    status = models.CharField(max_length=50, default='Beklemede')
    admin_note = models.TextField(blank=True, null=True)
    student_email = models.EmailField(max_length=254, blank=True, null=True, verbose_name="Öğrenci E-Posta")

    def __str__(self):
        return f"{self.tracking_code} - {self.institution.name}"