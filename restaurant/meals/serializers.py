from rest_framework import serializers
from meals.models import Meal, Ingredient
from storage.models import ProductInStorage
from storage.serializers import PriceProductInStorageSerializer


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model=Ingredient
        fields = ['product_id','weight_pices_used']

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
    cost_of_meal = serializers.SerializerMethodField(read_only=True)

    class Meta(MealSerializer.Meta):
        
        fields = MealSerializer.Meta.fields + ['ingredient', 'cost_of_meal']

    def get_ingredient(self, obj):

        i = Ingredient.objects.filter(meal_id = obj.id)
        serializer = IngredientSerializer(i, many=True)
        print(serializer)
        return serializer.data

    def get_cost_of_meal(self, obj):
        price = 0.00

        i = Ingredient.objects.filter(meal_id = obj.id)
        serializer = IngredientSerializer(i, many=True)
       
        for product in serializer.data:
            weight=product['weight_pices_used']
            id=product['product_id']
            pis = ProductInStorage.objects.filter(id=id).filter(product_waste=False).exclude(number_of_product=0)
            s = PriceProductInStorageSerializer(pis, many=True)
            p = s.data[0]['product_price']
            price += float(weight) * float(p)       

        return price
