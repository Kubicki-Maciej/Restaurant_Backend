from django.test import TestCase
from storage.models import Storage, Product, ProductInStorage
# Create your tests here.


class ProductTestCaste(TestCase):
    def setUp(self):
        Product.objects.create(name="Tomato", product_type="KG")
        Product.objects.create(name="Potato", product_type="KG")
        Product.objects.create(name="Avocado", product_type="P")
        Product.objects.create(name="Cheese", product_type="KG")
        Product.objects.create(name="BeefSteak", product_type="KG")
        Product.objects.create(name="Apple", product_type="KG")


class StorageTest(TestCase):
    def setUp(self):
        Storage.objects.create(name="Fridge1")
        Storage.objects.create(name="MagazineShelf1")


class ProductInStorageTest(TestCase):
    def setUp(self):
        Product.objects.create(name="Tomato", product_type="KG")
        Storage.objects.create(name="MagazineShelf1")
        tomato = Product.objects.get(name='Tomato')
        shelf = Storage.objects.get(name='MagazineShelf1')
        ProductInStorage.objects.create(product_id=tomato, number_of_product=20, storage_id=shelf, product_date_expired='2023-05-01',product_price=19.99)

    def test_product_in_storage(self):
        t = Product.objects.get(name='Tomato')
        pis = ProductInStorage.objects.get(product_id = t)
        self.assertEqual(pis.number_of_product ,20)            

