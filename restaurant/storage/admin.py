from django.contrib import admin

from storage.models import Product, ProductInStorage , Storage
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','name','product_type']


class ProductInStorageAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_product_name' ,  'get_storage_name', 'get_product_type']

    def get_product_name(self, obj):
        return obj.product_id.name
    
    get_product_name.admin_order_field = 'product_id'
    get_product_name.short_description = 'Product'
    
    def get_storage_name(self, obj):
        return obj.storage_id.name
    
    get_storage_name.admin_order_field = 'storage_id'
    get_storage_name.short_description = 'Storage'

    def get_product_type(self, obj):
        return obj.product_id.product_type

    get_product_type.admin_order_field = 'product_id'
    get_product_type.short_description = 'Product Type'



class StorageAdmin(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductInStorage, ProductInStorageAdmin)
admin.site.register(Storage, StorageAdmin)

