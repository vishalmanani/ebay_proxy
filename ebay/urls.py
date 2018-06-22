from django.conf.urls import url
from .views import EbayAPI, EbayNotification

urlpatterns = [
    url(r'^api/$', EbayAPI.as_view(), name='api'),
    url(r'^notification/$', EbayNotification.as_view(), name='notification'),
]
