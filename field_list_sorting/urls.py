from django.urls import path
from .views.views import sort_companies_list

app_name = 'sort_fields'

urlpatterns = [
    path('', sort_companies_list, name='sort_fields'),
]
