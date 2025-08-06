from django.urls import path, include
from Payments.views import *


urlpatterns = [
    # path('start_course/',start_course,name="start_course"),
    # path('payment-server', Payment_server, name="payment-server"),
    path('payment-success', payment_success, name="payment-success"),
    # path('payment-cancel', payment_cancel, name="payment-cancel"),
    # path('payment_webhook', payment_webhook, name="payment-webhook"),
]
