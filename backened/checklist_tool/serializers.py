from rest_framework import serializers
from checklist_tool.models import *


class HouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = ['name','user']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name','user']


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class CheckListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckList
        fields =  '__all__'

