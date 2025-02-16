from django.urls import path
from . import views

# url configuration

urlpatterns = [
    path('',views.home),
    path('about',views.about),
    path('delhi',views.delhi),
    path('mumbai',views.mumbai),
    path('bangalore',views.bangalore),
    path('chargers',views.showchargers)
]