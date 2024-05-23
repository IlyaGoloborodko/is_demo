from django.urls import path
from .views import main_view

app_name = 'my_tg_bot'

urlpatterns = [
    path('', main_view, name='main_tg'),
]
