from django.urls import path
from . import views

app_name = 'saletracker'

urlpatterns = [
    path("", views.index, name="index"),
    path('log', views.log, name="log"),
    path('<int:pk>', views.remove_log, name="log_delete")
]