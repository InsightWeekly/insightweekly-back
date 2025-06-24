from django.db import models
from django.contrib.auth.models import AbstractUser

class Account(AbstractUser):
    interest_category = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.username

class News(models.Model):
    CATEGORY_CHOICES = [
        ("IT_과학", "IT_과학"), ("건강", "건강"), ("경제", "경제"), ("교육", "교육"),
        ("국제", "국제"), ("라이프스타일", "라이프스타일"), ("문화", "문화"),
        ("사건사고", "사건사고"), ("사회일반", "사회일반"), ("산업", "산업"),
        ("스포츠", "스포츠"), ("여성복지", "여성복지"), ("여행레저", "여행레저"),
        ("연예", "연예"), ("정치", "정치"), ("지역", "지역"), ("취미", "취미"),
        ("기타", "기타"),
    ]
    title = models.TextField()
    summary = models.TextField()
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    publication_date = models.DateField()
    collact_date = models.DateField(auto_now_add=True)
    author = models.CharField(max_length=100, blank=True)
    news_company = models.CharField(max_length=100)
    link = models.URLField(max_length=500)

    def __str__(self):
        return self.title

class Scrap(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    scrap_date = models.DateField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['account', 'news'], name='unique_scrap')
        ]

class View(models.Model):
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    view_time = models.DateTimeField(auto_now_add=True)
