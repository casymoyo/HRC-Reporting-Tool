from rest_framework import serializers
from . models import ExcludedClient, Reports, RawCsvFile


class ExcludedClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExcludedClient
        fields = ['id', 'name']


class ReportsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reports
        fields = ['name', 'file', 'date_created']


class RawCsvFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawCsvFile
        fields = ['file']

