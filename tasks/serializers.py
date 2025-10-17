from rest_framework import serializers
from django.utils import timezone
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'due_date', 'priority', 'status', 'created_at', 'user', 'completed_at']
        read_only_fields = ['id', 'created_at', 'user', 'completed_at']

    def validate_due_date(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError('Due date must be in the future.')
        return value

    def validate_status(self, value):
        if value not in ['Pending', 'Completed']:
            raise serializers.ValidationError('Invalid status.')
        return value

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user and request.user.is_authenticated:
            validated_data['user'] = request.user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        new_status = validated_data.get('status')
        if instance.status == 'Completed' and new_status != 'Pending' and len(validated_data.keys()) > (1 if new_status else 0):
            raise serializers.ValidationError({'detail': 'Task is completed. Revert to Pending before editing.'})
        return super().update(instance, validated_data)
