from django.urls import path

from .views import *

urlpatterns = [
    path('', MainPageView.as_view(), name='home'),
    path('category/<str:slug>/', CategoryDetailView.as_view(), name='category'),
    path('product-detail/<int:pk>/', ProductDetailView.as_view(), name='detail'),
    path('add-product/', ProductCreateView.as_view(), name='add-product'),
    path('update-product/<int:pk>/', ProductEditView.as_view(), name='update-product'),
    path('delete-product/<int:pk>/', ProductDeleteView.as_view(), name='delete-product'),

]