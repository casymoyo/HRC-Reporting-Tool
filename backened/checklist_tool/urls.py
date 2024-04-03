from . import views
from rest_framework import routers
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'house',views.HouseViewset, basename='house')
router.register(r'question', views.QuestionViewset, basename='question')
router.register(r'category', views.CategoryViewset, basename='category')
router.register(r'check_list', views.CheckListViewset, basename='check_list')

app_name = 'checklist_tool'
urlpatterns = [
    path('', include(router.urls)),
]