from rest_framework import serializers
from .models import Ans

class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ans
        fields = ("respondent_name", "question", "choise", "date")