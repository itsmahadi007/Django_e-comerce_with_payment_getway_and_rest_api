from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.urls import re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from backend import settings
from backend.settings import DEBUG

schema_view = get_schema_view(
    openapi.Info(
        title="Mahadis API",
        default_version="v1",
        description="Created to Show Developer eXperience Hub",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("admin/", admin.site.urls),
]

if DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
        re_path(
            r"api_doc_v2/",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
        re_path(
            r"api_doc_v1/",
            schema_view.with_ui("redoc", cache_timeout=0),
            name="schema-redoc",
        ),
    ]

urlpatterns += [
    path("api/", include("apps.users_management.urls")),
    path("api/", include("apps.ecommerce.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
