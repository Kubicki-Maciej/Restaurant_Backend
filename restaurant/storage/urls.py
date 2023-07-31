from django.urls import path
from storage.views import get_all_products, get_product, get_product_by_name, get_all_pis, create_product, get_product_by_name_from_pis,  get_products_by_storage_name_by_expire, get_products_by_storage_name, CreateProductInStorageView, use_product

urlpatterns = [
    # Product Get
    path('products/', view=get_all_products, name='all_products'),
    path('products/<int:pk>', view=get_product),
    path('product_by_name/<str:product_name>', view=get_product_by_name),
    # Product Post
    path('products/post/', view=create_product),

    path('products_in_storage/', view=get_all_pis, name='all_products_in_storage'),
    path('products_in_storage/<str:product_name>', view=get_product_by_name_from_pis),
    path('product_by_storage_name/<str:storage_name>', view=get_products_by_storage_name),


    path('pos/<str:product_name>', view=get_products_by_storage_name_by_expire),
#   Used X pices or KG Product
    path('pos/<str:product_name>/<str:number_of_product>', view=use_product),
#   Add new product to storage, number_of_product, product_price, product date expired. 
    path('create-product/', CreateProductInStorageView.as_view())
]