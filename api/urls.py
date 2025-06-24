from django.urls import path
from .views import (
    SignupView,
    LoginView,
    UserProfileView,
    UpdateInterestCategoryView,
    LogoutView,
    NewsListView,
    SearchView,
    ScrapListView,
    ScrapToggleView,
    AnalysisView,
)

urlpatterns = [
    # Account
    path('account/signup', SignupView.as_view(), name='signup'),
    path('account/login', LoginView.as_view(), name='login'),
    path('account/profile', UserProfileView.as_view(), name='profile'),
    path('account/update-category', UpdateInterestCategoryView.as_view(), name='update-category'),
    path('account/logout', LogoutView.as_view(), name='logout'),

    # News
    path('news', NewsListView.as_view(), name='news-list'),

    # Search
    path('search', SearchView.as_view(), name='search'),

    # Scrap
    path('scraps', ScrapListView.as_view(), name='scrap-list'),
    path('scrap', ScrapToggleView.as_view(), name='scrap-toggle'),

    # Analysis
    path('analysis', AnalysisView.as_view(), name='analysis'),
] 