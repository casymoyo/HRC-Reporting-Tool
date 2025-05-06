from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from rest_framework_simplejwt import views as jwt_views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path, re_path

schema_view = get_schema_view(
   openapi.Info(
      title="HRC",
      default_version='v1',
      description="The api allows a user to upload an excel file and it will be filtered according to the company specifications",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path('users/', include('users.urls', namespace='users')),
    path('checklist/', include('checklist_tool.urls', namespace='checklist_tool')),
    path('reporting/', include('reporting_tool.urls', namespace='reporting_tool')),
    path('api-auth/', include('rest_framework.urls', namespace='hrc')),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

