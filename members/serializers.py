from rest_framework import serializers

from .models import Member

class MemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = Member
        # fields = '__all__'
        fields = (
            'id',
            'first_name',
            'last_name',
            'date_created',
            'date_modified',
        )
        read_only_fields = (
            'date_created',
            'date_modified',
        )
