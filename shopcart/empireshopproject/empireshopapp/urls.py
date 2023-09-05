from django.urls import path
from . import views


app_name='empireshopapp'
urlpatterns = [
    path('',views.allProdCat,name='allProdCat'),
    path('<slug:c_slug>/',views.allProdCat,name='product_by_category'),
    path('<slug:c_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
    path('', views.home_page, name='home'),

]

