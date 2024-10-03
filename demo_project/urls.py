from django.urls import path
from demo_app import views
from django.conf import settings # new
from  django.conf.urls.static import static #new

urlpatterns = [
    path('', views.home, name='home'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_URL)

    