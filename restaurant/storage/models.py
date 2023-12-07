from django.db import models

# Create your models here.

class ProductManager(models.Manager):
    def get_by_natural_key(self, name, product_type):
        return self.get(name=name, product_type=product_type)
    
    class Meta:
        
         permissions = [
            ('codename', 'productmanager'),
        ]


class Product(models.Model):
    objects = ProductManager()

    PRODUCT_TYPE_NAMES =(
        ("KG", "Kilograms"),
        ("P", "Piece"),        
    )
    name = models.CharField(max_length=255)
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPE_NAMES)
    product_EAN = models.IntegerField(blank=True, null=True)
    
    def __str__(self) -> str:
        return self.name

    def natural_key(self):
        return (self.name, self.product_type)

    class Meta:
        unique_together=(('name', 'product_type'))

class Storage(models.Model):
    name = models.CharField(max_length=255)
    storage_EAN = models.IntegerField(blank=True, null=True)

        
    def __str__(self) -> str:
        return self.name


class ProductInStorage(models.Model):
    # add if product is removed flag and add second table to keep products ? and waste table ?

    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    storage_id = models.ForeignKey(Storage, on_delete=models.CASCADE)
    product_date_added = models.DateTimeField(auto_now_add=True)
    product_date_expired = models.DateField(blank=False)
    number_of_product = models.DecimalField(max_digits=10, decimal_places=3, default=0.0)
    product_waste = models.BooleanField(default=False)
    product_price = models.DecimalField(max_digits=10,decimal_places=2, default=0)


    def __str__(self):
        return f'{self.number_of_product}_{self.product_id.name}'
    
    class Meta:
        
         permissions = [
            ('codename', 'productinstorage'),
        ]


class ProductMinimal(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    expected_quantity = models.DecimalField(max_digits=10, decimal_places=3, default=0.0)