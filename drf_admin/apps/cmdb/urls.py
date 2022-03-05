from django.urls import path, include

from rest_framework.routers import DefaultRouter
from cmdb.views import servers,server_tencent,cdn
router = DefaultRouter()
router.register(r'servers', servers.ServerViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('tencent/cdn/urlflush/',cdn.UrlFlush.as_view()),
    path('tencent/cdn/dirflush/',cdn.DirFlush.as_view()),
    path('tencent/cdn/urlpreheat/',cdn.UrlPreHeat.as_view()),
    path('tencent/cdn/history/',cdn.History.as_view()),
    path('tencent/servers/',server_tencent.InstanceData.as_view()),
    path('servers/multiple_delete/', servers.ServerViewSet.as_view({'delete', 'multiple_delete' })),
    ]
