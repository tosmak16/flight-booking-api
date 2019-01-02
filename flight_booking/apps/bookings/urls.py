from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register(r'bookings', views.BookingsViewSet)
router.register(r'bookings', views.BookingsDetailsViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
]