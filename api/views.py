from django.shortcuts import render
from datetime import date, timedelta
from django.db.models import Count
from django.contrib.auth import authenticate

from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token

from .models import Account, News, Scrap, View
from .serializers import AccountSerializer, NewsSerializer
from .pagination import ScrapPageNumberPagination

# Create your views here.

# Account
class SignupView(generics.CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [AllowAny]

class LoginView(views.APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response(AccountSerializer(request.user).data)

class UpdateInterestCategoryView(views.APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        categories = request.data.get('categories', [])
        if len(categories) > 3:
            return Response({"error": "You can select up to 3 categories."}, status=status.HTTP_400_BAD_REQUEST)
        
        user = request.user
        user.interest_category = ','.join(categories)
        user.save()
        
        return Response(AccountSerializer(user).data)

class LogoutView(views.APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# News
class NewsListView(generics.ListAPIView):
    serializer_class = NewsSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        """
        뉴스 목록을 반환합니다. sort, category 파라미터로 정렬 및 필터링을 제어할 수 있습니다.
        - sort=1: 최신순 (기본값)
        - sort=0: 오래된 순
        - category: 카테고리 이름
        """
        queryset = News.objects.all()
        sort = self.request.query_params.get('sort', '1')
        category = self.request.query_params.get('category', None)

        if category and category != '전체':
            queryset = queryset.filter(category=category)

        if sort == '0':
            return queryset.order_by('publication_date')
        else:
            return queryset.order_by('-publication_date')

# Search
class SearchView(generics.ListAPIView):
    serializer_class = NewsSerializer
    permission_classes = [AllowAny]
    def get_queryset(self):
        keyword = self.request.query_params.get('keyword', '')
        sort = self.request.query_params.get('sort', '1')

        if not keyword:
            return News.objects.none()

        queryset = News.objects.filter(title__icontains=keyword) | News.objects.filter(summary__icontains=keyword)

        if sort == '0':
            return queryset.order_by('publication_date')
        else:
            return queryset.order_by('-publication_date')

# Scrap
class ScrapListView(generics.ListAPIView):
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = ScrapPageNumberPagination

    def get_queryset(self):
        return News.objects.filter(scrap__account=self.request.user, scrap__active=True).order_by('-scrap__id')

class ScrapToggleView(views.APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, *args, **kwargs):
        news_id = request.query_params.get('news')
        if not news_id:
            return Response({"error": "News ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            news = News.objects.get(pk=news_id)
        except News.DoesNotExist:
            return Response({"error": "News not found."}, status=status.HTTP_404_NOT_FOUND)

        scrap, created = Scrap.objects.get_or_create(account=request.user, news=news)

        if not created:
            scrap.active = not scrap.active
            scrap.save()
        
        return Response({"active": scrap.active}, status=status.HTTP_200_OK)

# Analysis
class AnalysisView(views.APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        today = date.today()
        one_week_ago = today - timedelta(days=7)

        # Summary
        summary = {
            'today_collected_news_count': News.objects.filter(collact_date=today).count(),
            'today_views_count': View.objects.filter(view_time__date=today).count(),
            'today_scraps_count': Scrap.objects.filter(scrap_date=today).count()
        }

        # Weekly Trends
        weekly_view_trend = list(View.objects.filter(view_time__date__gte=one_week_ago)
                                 .values('view_time__date')
                                 .annotate(views=Count('id'))
                                 .values('view_time__date', 'views')
                                 .order_by('-view_time__date'))
        
        weekly_scrap_trend = list(Scrap.objects.filter(scrap_date__gte=one_week_ago)
                                  .values('scrap_date')
                                  .annotate(scraps=Count('id'))
                                  .values('scrap_date', 'scraps')
                                  .order_by('-scrap_date'))

        # Weekly Top 10 News
        weekly_top10_news = list(News.objects.filter(view__view_time__date__gte=one_week_ago)
                                 .annotate(view_count=Count('view'))
                                 .order_by('-view_count')[:10]
                                 .values('id', 'title', 'category', 'view_count'))

        # Weekly Top 10 News by Category
        categories = News.objects.values_list('category', flat=True).distinct()
        weekly_top10_by_category = {}
        for category in categories:
            top_news = list(News.objects.filter(category=category, view__view_time__date__gte=one_week_ago)
                            .annotate(view_count=Count('view'))
                            .order_by('-view_count')[:10]
                            .values('id', 'title', 'view_count'))
            if top_news:
                weekly_top10_by_category[category] = top_news

        response_data = {
            "summary": summary,
            "weekly_view_trend": weekly_view_trend,
            "weekly_scrap_trend": weekly_scrap_trend,
            "weekly_top10_news": weekly_top10_news,
            "weekly_top10_news_by_category": weekly_top10_by_category
        }
        
        return Response(response_data)
