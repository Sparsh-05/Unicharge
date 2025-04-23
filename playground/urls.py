from django.urls import path
from . import views

# url configuration

urlpatterns = [
    path('', views.filterchargers,name='home'),
    path('home', views.filterchargers ),
    path('about',views.about),
    path('delhi',views.delhi),
    path('mumbai',views.mumbai),
    path('bangalore',views.bangalore),
    path('filter-clustered/', views.filterchargers_clustered, name='filter_chargers_clustered'),

    
]