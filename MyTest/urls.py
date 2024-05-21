from django.urls import path
from .views import main

app_name = 'test_app'

urlpatterns = [
                  path('', main, name='test_app'),
              ]
