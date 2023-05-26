from django.urls import path

from . import views


app_name = "payments"

urlpatterns = [
    path("", views.PaymentListView.as_view(), name="payment_list"),
    path("verify/<ref>/", views.verify_payment, name="verify_payment"),
    path("delete/<ref>/", views.PaymentDeleteView.as_view(), name="delete_payment"),
]
