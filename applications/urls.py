from django.urls import path, include

urlpatterns = [
    path('api/ads/', include('applications.ad.urls')),
    path('api/application/', include('applications.application.urls')),
    path('api/category/', include('applications.category.urls')),
    path('api/comment/', include('applications.comment.urls')),
    path('api/notification/', include('applications.notification.urls')),
    path('api/user/', include('applications.user.urls')),
]
