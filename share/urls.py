from django.urls import path
from share import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/driver', views.signup_driver, name='signup_driver'),
    path('accounts/signup/customer', views.signup_customer, name='signup_customer'),
    path('create-ride', views.create_ride, name="create_ride"),
    path('search-ride', views.search_ride, name="search_ride"),
    path('contact', views.contact, name="contact"),
    path('book-ride/<str:id>', views.book_ride, name="book_ride")
]
