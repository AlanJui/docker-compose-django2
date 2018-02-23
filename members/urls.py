from django.urls import path, re_path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import MemberViewSet

member_list = MemberViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

member_detail = MemberViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy',
})

urlpatterns = format_suffix_patterns([
    path('members/', member_list, name='member-list'),
    re_path('members/(?P<pk>[0-9]+)/', member_detail, name='member-detail')
])