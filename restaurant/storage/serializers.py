from rest_framework import serializers
from storage.models import Product, ProductInStorage, Storage


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['name', 'product_type']


class CreateProductSerializer(serializers.ModelSerializer):

    class Meta:
        model=Product
        fields= ['name', 'product_type']


class StorageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Storage
        fields = "__all__"


class ProductInStorageSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField(read_only=True)
    storages = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = ProductInStorage
        # fields = "__all__"
        fields = ['id','product_date_added', 'product_date_expired','products', 'storages', 'number_of_product']
        # fields = ['product_id', 'product_date_added']

    def get_products(self, obj):
        products = obj.product_id.id
        p = Product.objects.get(pk=products)
        serializers = ProductSerializer(p)
        return serializers.data
    
    def get_storages(self, obj):
        storage = obj.storage_id.id
        s = Storage.objects.get(pk=storage)
        serializer = StorageSerializer(s)
        return serializer.data
    
class CreateProductInStorageSerializer(serializers.ModelSerializer):

    class Meta:
        model=ProductInStorage
        fields= ['product_id', 'storage_id', 'number_of_product', 'product_date_expired', 'product_price', ]


class PriceProductInStorageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=ProductInStorage
        fields=['product_price']

    def price(self, obj):
        return obj.product_price
    

class ProductDashboardSerializer(serializers.ModelSerializer):

    class Meta:
        model=Product
        fields = ['id', 'name', 'product_type']