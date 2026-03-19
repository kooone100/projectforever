from django.urls import path, include
from Eshop import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('categories/', views.CategoryView.as_view(), name='categories'),
    path('productList/', views.ProductListView.as_view(), name='productList'),
    path('faucets/', views.FaucetView.as_view(), name='faucets'),
    path('sanware/', views.SanwareView.as_view(), name='sanware'),
    path('products/by-category/<int:category_id>/', views.ProductByCategoryView.as_view(), name='products_by_category'),
    path('products/<int:product_id>/', views.ProductView.as_view(), name='product'),
    path('products/<int:product_id>/images/', views.ProductImageView.as_view(), name='product_images'),
    path('new-arrivals/', views.NewArrivalView.as_view(), name='new-arrivals'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
