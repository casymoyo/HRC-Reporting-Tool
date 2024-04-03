from . import views
from rest_framework import routers
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'reports', views.ReportViewSet, basename='reports')
router.register(r'raw_csv_files', views.RawCsvFileViewSet, basename='raw_csv_files')
router.register(r'excluded_clients', views.ExcludedClientViewSet, basename='excluded_clients')

app_name = 'reporting_tool'
urlpatterns = [
    path('', include(router.urls)),
    path('process/', views.process_csv, name='process'),
    path('delete/', views.delete_directory, name='delete')
]