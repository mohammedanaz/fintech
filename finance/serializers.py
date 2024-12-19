from rest_framework import serializers
from .models import *

class IncomeListSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source="category.name")
    email = serializers.ReadOnlyField(source="user.email")

    class Meta:
        model = Income
        fields = ['id', 'user', 'email', 'amount', 'source', 'category', 'category_name', 'date_received', 'notes']

class IncomeCreateSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(write_only=True) 

    class Meta:
        model = Income
        fields = ['amount', 'source', 'category_name', 'date_received', 'notes'] 

    def create(self, validated_data):
        request_user = self.context['request'].user 

        category_name = validated_data.pop('category_name', None)
        category = None
        if category_name:
            try:
                category = IncomeCategory.objects.get(name=category_name)
            except IncomeCategory.DoesNotExist:
                raise serializers.ValidationError({"category_name": "Invalid category name provided."})

        # Create the Income instance
        return Income.objects.create(user=request_user, category=category, **validated_data)

    def to_representation(self, instance):
        """
        Customize the response generated to include category name and id.
        """
        representation = super().to_representation(instance)
        representation['id'] = instance.id
        representation['category_name'] = instance.category.name if instance.category else None
        return representation
    
class IncomeUpdateSerializer(serializers.ModelSerializer): 

    category_name = serializers.CharField(write_only=True, required=False) 

    class Meta:
        model = Income
        fields = ['id', 'amount', 'source', 'category', 'category_name', 'date_received', 'notes']

    def update(self, instance, validated_data):
        category_name = validated_data.pop('category_name', None)
        if category_name:
            try:
                category = IncomeCategory.objects.get(name=category_name)
                validated_data['category'] = category
            except IncomeCategory.DoesNotExist:
                raise serializers.ValidationError({"category_name": "Invalid category name."})
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        """
        Customize the response generated to include category name.
        """
        representation = super().to_representation(instance)
        representation['category_name'] = instance.category.name if instance.category else None
        representation['email'] = instance.user.email if instance.category else None
        representation['user'] = instance.user.id if instance.category else None
        return representation