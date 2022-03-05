from rest_framework import serializers
from cmdb.models import ServerData

class ServerDataSerializer(serializers.ModelSerializer):
    """
    Server序列化器
    """

    class Meta:
        model = ServerData
        fields = '__all__'





