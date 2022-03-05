from rest_framework import serializers
from approve.models import CheckApprove

class CheckApproveserializer(serializers.ModelSerializer):
    """
    Server序列化器
    """

    class Meta:
        model = CheckApprove
        fields = '__all__'
