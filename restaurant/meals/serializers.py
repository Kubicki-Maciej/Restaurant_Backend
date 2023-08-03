from rest_framework import serializers
from meals.models import Meal, Ingredient, CategoryMenu
from storage.models import ProductInStorage
from storage.serializers import PriceProductInStorageSerializer


class IngredientSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model=Ingredient
        fields = ['product_id','weight_pices_used','product_name']

    def get_product_name(self,obj):
        return obj.product_id.name

"""



ZROBIC DZIEDZICZENIE SERIALIZER MEAL DLA CREATE MEAL W VIEW



"""

class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = ['meal_name','meal_cost','description']



class CreateMealSerializer(MealSerializer):
    ingredient = IngredientSerializer(many=True)

    class Meta(MealSerializer.Meta):
        
        fields = MealSerializer.Meta.fields + ['ingredient']
    
    

    def create(self, validated_data):
        
        print(self.initial_data)
        print('data v')
        print(validated_data)
        meal_ingradient_data = validated_data.pop("ingredient")
        meal = Meal.objects.create(**validated_data)
        for i in meal_ingradient_data:
            Ingredient.objects.create(meal_id=meal, **i)
        print(f'meal data {meal}')
        return meal

    
class FullInformationMealSerializer(MealSerializer):
    ingredient = serializers.SerializerMethodField(read_only=True)
    cost_of_meal_production = serializers.SerializerMethodField(read_only=True)

    class Meta(MealSerializer.Meta):
        
        fields = MealSerializer.Meta.fields + ['ingredient', 'cost_of_meal_production']

    def get_ingredient(self, obj):

        i = Ingredient.objects.filter(meal_id = obj.id)
        serializer = IngredientSerializer(i, many=True)
        
        return serializer.data

    def get_cost_of_meal_production(self, obj):
        price = 0.00
        list_of_product_except =[]

        i = Ingredient.objects.filter(meal_id = obj.id)
        serializer = IngredientSerializer(i, many=True)
        for product in serializer.data:
            weight=product['weight_pices_used']
            id=product['product_id']

            pis = ProductInStorage.objects.filter(product_id=id).filter(product_waste=False).exclude(number_of_product=0)
    
            serialized_product = PriceProductInStorageSerializer(pis, many=True)

            dataproduct = serialized_product.data[:]
        
            try:
                product_cost = dataproduct[0]['product_price']
                price += float(weight) * float(product_cost)   
            except:
                print(f'No product in storage || product_id:{id}')
                list_of_product_except.append(f'No product in storage || product_id:{id}')
                 
        if list_of_product_except:
            return f'No product in storage to produce meal|| product_id:{id}' 
        
        return price


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model=CategoryMenu