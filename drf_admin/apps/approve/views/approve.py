from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet
from approve.models import Approve,CheckApprove
from approve.serializers.approve import Approveserializer
from approve.serializers.check_approve import CheckApproveserializer
from rest_framework.response import Response
import  json
from rest_framework import  status
from rest_framework.decorators import action
from  rest_framework.views import APIView

class ApproveViewSet(ModelViewSet):
    queryset = Approve.objects.all()
    serializer_class = Approveserializer

    # def get_queryset(self):
    #     if self.action == 'partial_update':
    #         return CheckApprove.objects.all()
    #     else:
    #         return Approve.objects.all()
    #
    #
    # def get_serializer_class(self):
    #     if self.action == 'partial_update':
    #         return CheckApproveserializer
    #     else:
    #         return Approveserializer


    # def update(self, request, *args, **kwargs):
    #     print("patch")
    #     print(request.data)
    #     instance = request.data
    #     if 'id' in instance:
    #         instance_id  =instance['id']
    #         check_step_key = instance['step_key']
    #         check_step_value = instance['step_value']
    #         check_approve_instance = CheckApprove.objects.get(approve_id=instance_id)
    #         if check_step_key == 'first':
    #             check_approve_instance.first  = check_step_value
    #             check_approve_instance.save()
    #         elif check_step_key == 'second':
    #             check_approve_instance.second = check_step_value
    #             check_approve_instance.save()
    #         elif check_step_key == 'third':
    #             check_approve_instance.third = check_step_value
    #             check_approve_instance.save()
    #     partial = kwargs.pop('partial', False)
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data, partial=partial)
    #     print(serializer.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #
    #     if getattr(instance, '_prefetched_objects_cache', None):
    #         # If 'prefetch_related' has been applied to a queryset, we need to
    #         # forcibly invalidate the prefetch cache on the instance.
    #         instance._prefetched_objects_cache = {}
    #
    #     return Response(serializer.data)


class ApproveView(APIView):

    def post(self,request):
        print(request.data)
        return Response(data=request.data,status=status.HTTP_200_OK)

