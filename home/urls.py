from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "home"

urlpatterns = [
    path('', views.HomeView.as_view(), name = "home"),
    path('category/<slug>/', views.CategoryView.as_view(), name = "category"),
    path('add-to-cart/', views.add_to_cart, name = "add-to-cart"),
    path('order-summary/', views.OrderSummaryView.as_view(), name = "summary"),
    path('update-cart/', views.update_cart, name = "update_cart")
]

urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL,
                      document_root=settings.STATIC_ROOT)
