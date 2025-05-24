from django.urls import path

from . import views

app_name = 'payplan'
urlpatterns = [
    path('', views.index, name="index"),
    path('select', views.select_payplan, name="select"),
    path('add', views.add_payplan, name="add"),
    path('add/scaling', views.add_level, name="add-level"),
    path('edit', views.add_level, name="edit"),
    path('edit/<int:pk>', views.update_payplan, name="update"),
    path('flat', views.add_flat, name="flat"),
    path('volume-bonus', views.add_volume_bonus, name="volume-bonus")
]