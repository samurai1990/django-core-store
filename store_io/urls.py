from django.urls import path,include

urlpatterns = [
    path('ht/',include('health_check.urls')),
    path('', include('accounts.urls')),
]