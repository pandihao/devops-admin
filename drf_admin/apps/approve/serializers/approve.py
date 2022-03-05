from rest_framework import serializers
from approve.models import Approve

class Approveserializer(serializers.ModelSerializer):
    """
    Server序列化器
    """
    app = serializers.ListField(child=serializers.CharField(allow_blank=True))
    app_name =serializers.JSONField()
    cache = serializers.ListField(child=serializers.CharField(allow_blank=True))
    db = serializers.ListField(child=serializers.CharField(allow_blank=True))
    msg_middleware = serializers.ListField(child=serializers.CharField(allow_blank=True))
    resources =serializers.JSONField()
    domain =serializers.JSONField()


    class Meta:
        model = Approve
        fields = '__all__'