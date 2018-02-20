from rest_framework import serializers

from .models import Member

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'
        # fields = (
        #     'first_name',
        #     'last_name',
        # )
