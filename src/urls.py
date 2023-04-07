from django.urls import path,include
from django.conf import settings
from .views import home,success,failure
from django.conf.urls.static import static

urlpatterns = [
    path('',home,name ='home'),
    path('success',success,name ='success'),
    path('failed',failure,name ='failure'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)