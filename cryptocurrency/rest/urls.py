# pylint: disable=wrong-import-order
from cryptocurrency.rest import views
from django import urls
from drf_yasg import openapi
from drf_yasg import views as drf_yasg_views
from rest_framework import permissions, routers

SchemaView = drf_yasg_views.get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


def register_views(router):
    router.register(r'transactions', views.TransactionViewSet)
    router.register(r'currencies', views.CurrencyViewSet)
    router.register(r'addresses', views.AddressViewSet)
    return router


urlpatterns = [
    urls.path(r'', urls.include(register_views(routers.SimpleRouter()).urls)),
    urls.re_path(
        r'^swagger(?P<format>\.json|\.yaml)$',
        SchemaView.without_ui(cache_timeout=0),
        name='schema-json',
    ),
    urls.re_path(
        r'^swagger/$',
        SchemaView.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui',
    ),
    urls.re_path(
        r'^redoc/$',
        SchemaView.with_ui('redoc', cache_timeout=0),
        name='schema-redoc',
    ),
]
