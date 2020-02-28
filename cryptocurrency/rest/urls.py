from django.urls import include, path
from rest_framework import routers

from cryptocurrency.rest import views


def register_views(router):
    router.register(r'transactions', views.TransactionViewSet)
    return router

urlpatterns = register_views(routers.SimpleRouter()).urls
