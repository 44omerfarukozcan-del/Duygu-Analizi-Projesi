from django.db import models

class Feedback(models.Model):
    CATEGORY_CHOICES = [
        ('Yemekhane', 'Yemekhane'),
        ('Kütüphane', 'Kütüphane'),
        ('İnternet', 'İnternet'),
        ('Ders Programı', 'Ders Programı'),
        ('Ulaşım', 'Ulaşım'),
        ('Temizlik', 'Temizlik'),
    ]

    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, verbose_name="Kategori")
    text = models.TextField(verbose_name="Öğrenci Geri Bildirimi")
    sentiment = models.CharField(max_length=20, blank=True, null=True, verbose_name="Duygu Durumu")
    score = models.FloatField(blank=True, null=True, verbose_name="Eminlik Oranı")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Eklenme Tarihi")

    def __str__(self):
        return f"{self.category} - {self.sentiment}"
