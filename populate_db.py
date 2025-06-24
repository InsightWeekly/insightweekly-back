import os
import sys
import django
import random
from datetime import date, timedelta
from faker import Faker

# Django 환경 설정
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from api.models import News

def populate_news(n=100):
    """지정된 숫자(n)만큼 가짜 뉴스 데이터를 생성합니다."""
    fake = Faker('ko_KR')  # 한국어 데이터 생성
    News.objects.all().delete() # 기존 뉴스 데이터 초기화
    
    print(f'{n}개의 뉴스 데이터 생성을 시작합니다...')

    for _ in range(n):
        publication_date = fake.date_between(start_date='-1y', end_date='today')
        
        News.objects.create(
            title=fake.sentence(nb_words=10),
            summary=fake.text(max_nb_chars=200),
            category=random.choice(News.CATEGORY_CHOICES)[0],
            publication_date=publication_date,
            collact_date=publication_date + timedelta(days=random.randint(1, 3)), # 수집일은 발행일 1~3일 후로 설정
            author=fake.name(),
            news_company=fake.company(),
            link=fake.url()
        )
    
    print(f'{n}개의 뉴스 데이터 생성이 완료되었습니다.')

if __name__ == '__main__':
    populate_news(100) 