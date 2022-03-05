from django.urls import path, include

from rest_framework.routers import DefaultRouter
from approve.views import approve,check_approve
router = DefaultRouter()
router.register(r'approve', approve.ApproveViewSet)
router.register(r'confirm', check_approve.checkApproveViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('approve/',approve.ApproveViewSet.as_view()),

    ]
