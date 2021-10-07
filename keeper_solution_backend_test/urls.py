"""keeper_solution_backend_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers, permissions
from apps.bookmarks import views as bookmark_views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Api router
router = routers.DefaultRouter()
router.register('bookmarks', bookmark_views.BookMarkViewSet, basename='Bookmark')

schema_view = get_schema_view(
    openapi.Info(
        title="Keeper API",
        default_version='v1.0',
        description="Public Bookmark managment API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="diegomazorra@keepersolutions.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # Api routes
    path('api/', include('apps.authentication.urls')),
    path('api/', include(router.urls)),
    # Swagger
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
