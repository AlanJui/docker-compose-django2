from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Member
from .serializers import MemberSerializer

# Create your views here.
def hello_world(request):
    return HttpResponse('Hello World!')

#========================================
# RESTful API
#========================================

class MemberList(APIView):

    def get(self, request):
        member_list = Member.objects.all()
        serializer = MemberSerializer(member_list, many=True)
        return Response(serializer.data)