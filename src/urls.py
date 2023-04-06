from django.urls import path,include
from .views import home,success,failure

urlpatterns = [
    path('',home,name ='home'),
    path('success',success,name ='success'),
    path('failed',failure,name ='failure'),
]