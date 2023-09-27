from django.urls import path
from . import views

app_name = "cars"

urlpatterns = [
    path("", views.index_view, name="index"),
    path("detail/<int:id>/", views.car_detail, name="detail"),
    path("contact/", views.contact_us, name="contact-us"),
    path("cars/", views.cars_list_view, name="car-list"),
    path("wishlist/", views.wish_list_view, name="wish-list"),
    path("pricing-list/", views.pricing_list_view, name="pricing-list"),
    path("pricing/", views.pricing_view, name="pricing"),
    path("about/", views.about_view, name="about"),
    path("privacy/", views.privacy_view, name="privacy"),
    path("wish/", views.wish_view, name="wish"),
    path("vacancy/", views.vacancies_view, name="vacancy"),
    path("vacancy-detail/<int:id>/", views.vacancy_detail, name="vacancy-detail"),
    path("vacancy-appleal/<int:id>/", views.vacancy_appleal, name="vacancy-appleal"),
    path("faq/", views.faq_view, name="faq"),
    path("car-order/<int:id>/", views.car_order_view, name="car-order"),
    path("order-cancel/", views.order_cancel_view, name="order-cancel"),
]