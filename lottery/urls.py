from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LotteryViewSet, LotteryUploadView, LotteryResultDetailAPIView

router = DefaultRouter()
router.register(r'lotteries', LotteryViewSet)

urlpatterns = [
    path('', include(router.urls)),  # /api/lotteries/ etc.
    path("upload/", LotteryUploadView.as_view(), name="lottery-upload"),  # API JSON upload
    path("lottery-result/<int:pk>/", LotteryResultDetailAPIView.as_view(), name="lottery-result-detail"),
]
