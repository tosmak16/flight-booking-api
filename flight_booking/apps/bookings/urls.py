from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register(r'bookings', views.BookingsDetailsViewSet, basename='bookings')


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^bookings/users', views.users),
    url(r'^bookings', views.BookingsViewSet.as_view({'get': 'list', 'post': 'create'}), name='bookings'),
]


