from django.urls import path, include
from rest_framework.routers import DefaultRouter
from applications.user.views import RegisterView, CustomTokenObtainPairView

# router = DefaultRouter()
# router.register(r'api/register', RegisterView, 'register')
# router.register(r'api/login', CustomTokenObtainPairView, 'login')

urlpatterns = [
    # path('', include(router.urls)),
    path('register/', RegisterView.as_view()),
    path('login/', CustomTokenObtainPairView.as_view()),
]
