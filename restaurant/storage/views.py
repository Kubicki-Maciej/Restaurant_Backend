from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from storage.models import Product, ProductInStorage, Storage
from storage.serializers import ProductSerializer, ProductInStorageSerializer, CreateProductSerializer, CreateProductInStorageSerializer
from storage.operations_class import ProductInMagazine, ProductManager
# Create your views here.


@api_view(['GET',])
def get_all_products(request):
    if request.method == "GET":
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    else:
        return Response({'nic'})

@api_view(['GET',])
def get_product(request, pk):
    if request.method == "GET":
        print('1')
        product = Product.objects.get(pk=pk)
        print(product)
        serializer = ProductSerializer(product, many=False)
        return Response(serializer.data)
    else:
        return Response({'nic'})

@api_view(['GET',])
def get_product_by_name(request, product_name):
    if request.method == "GET":
        products = Product.objects.get(name=product_name)
        serializer = ProductSerializer(products)
        return Response(serializer.data)
    else:
        return Response({'nic'})
    
@api_view(['POST'])
def create_product(request):
    if request.method == "POST":
        serializer = ProductSerializer(data=request.data)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateProductView(APIView):
    serializer_class = CreateProductSerializer

    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            product_id = serializer.data.id
            product_name = serializer.data.name
            product_type = serializer.data.product_type
            # host = self.request.session.session_key
            query_set = Product.objects.filter(id= product_id)



### Product in storage views ###
 
@api_view(['GET',])
def get_all_pis(request): # pis - Product in Storage
    if request.method == "GET":
        product_in_storage = ProductInStorage.objects.all()
        print(product_in_storage)
        serializer = ProductInStorageSerializer(product_in_storage, many=True)
        return Response(serializer.data)
    else:
        return Response({'nic'})

@api_view(['GET',])
def get_product_by_name_from_pis(request, product_name):
    print(product_name)
    if request.method == "GET":
        print(product_name)
        product = Product.objects.get(name=product_name)
        
        if product:
            product_in_storage = ProductInStorage.objects.filter(product_id=product.id)
            serializer = ProductInStorageSerializer(product_in_storage, many=True)
            return Response(serializer.data)
        else:
            print("niema")
            return Response({'nic'})
    else:
        return Response({'nic'})

@api_view(['GET',])
def get_products_by_storage_name(request, storage_name):
    print(storage_name)

    if request.method == "GET":
        storage = Storage.objects.get(name=storage_name)
        
        if storage:
            product_in_storage = ProductInStorage.objects.filter(storage_id=storage.id)
            serializer = ProductInStorageSerializer(product_in_storage, many=True)
            return Response(serializer.data)
        else:
            print("niema")
            return Response({'nic'})
    else:
        return Response({'nic'})
    

@api_view(['GET',])
def get_products_by_storage_name_by_expire(request, product_name):
    if request.method == "GET":

        product = Product.objects.get(name=product_name)

        if product:
            product_in_storage = ProductInStorage.objects.filter(product_id=product.id)
            serializer = ProductInStorageSerializer(product_in_storage, many=True)
            print(serializer.data)
            PM = ProductManager(serializer.data)
            PM.sort_object_list_by_date_exp()
            PM.get_from_objects_weights_count()
            data = PM.return_dict_list()      
            
            return Response(data)
        else:
            print("niema")
            return Response({'nic'})

@api_view(['GET',])
def use_product(request, product_name, number_of_product):
    
    if request.method == "GET":
        product = Product.objects.get(name=product_name)
        if product:
            if number_of_product:
                product_used = float(number_of_product)
                product_in_storage = ProductInStorage.objects.filter(product_id=product.id).exclude(number_of_product=0)
                serializer = ProductInStorageSerializer(product_in_storage, many=True)
                print(serializer.data)
                PM = ProductManager(serializer.data)
                
                PM.sort_object_list_by_date_exp()
                PM.get_from_objects_weights_count()
                print(PM.weight_count_number)
                if PM.weight_count_number>=product_used:
                    products_change = PM.remove_weight(product_used)
                    for product in products_change:
                        id_pos = product["id_product_in_storage"]
                        pos = ProductInStorage.objects.get(id=id_pos)
                        pos.number_of_product = product["weights"]
                        if product["weights"] == 0:
                            pos.product_waste = True
                        pos.save()
                    return Response(products_change)
                else:
                    print('waga jest za mała')
                    return Response({"zamała waga"})
            else: 
                return Response({"nic"})  
        return Response({"nic"})


class CreateProductInStorageView(APIView):
    serializer_class = CreateProductInStorageSerializer

    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            product_id = serializer.data['product_id']
            storage_id = serializer.data['storage_id']
            product_price = serializer.data['product_price']
            number_of_product = serializer.data['number_of_product']
            product_date_expired = serializer.data['product_date_expired']
            product_instance = Product.objects.get(id=product_id)
            storage_instance = Storage.objects.get(id=storage_id)
    
            pis = ProductInStorage(product_id=product_instance, storage_id=storage_instance, product_price=product_price, number_of_product=number_of_product, product_date_expired=product_date_expired)
            pis.save()
            return Response(ProductInStorageSerializer(pis).data, status=status.HTTP_201_CREATED)
        else:
            return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)
        
