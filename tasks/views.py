from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from .models import Task
from .serializers import TaskSerializer
from datetime import datetime, date
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            base_qs = Task.objects.all()
        else:
            base_qs = Task.objects.filter(user=self.request.user)

        params = self.request.query_params
        status_param = params.get('status')
        priority_param = params.get('priority')
        due_param = params.get('due_date')

        if status_param:
            base_qs = base_qs.filter(status=status_param)
        if priority_param:
            base_qs = base_qs.filter(priority=priority_param)
        if due_param:
            parsed = None
            try:
                if len(due_param) <= 10:
                    parsed_date = date.fromisoformat(due_param)
                    base_qs = base_qs.filter(due_date__date=parsed_date)
                else:
                    iso_value = due_param.replace('Z', '+00:00')
                    parsed = datetime.fromisoformat(iso_value)
                    base_qs = base_qs.filter(due_date=parsed)
            except Exception:
                pass

        return base_qs

    def perform_update(self, serializer):
        instance = self.get_object()
       
        new_status = self.request.data.get('status')
        is_reverting = new_status == 'Pending'
        if instance.status == 'Completed' and not is_reverting:
            return Response({'detail': 'Task is completed. Revert to Pending before editing.'}, status=status.HTTP_400_BAD_REQUEST)
        updated_instance = serializer.save()
       
        if new_status == 'Completed' and updated_instance.completed_at is None:
            updated_instance.completed_at = timezone.now()
            updated_instance.save(update_fields=['completed_at'])
        if new_status == 'Pending' and updated_instance.completed_at is not None:
            updated_instance.completed_at = None
            updated_instance.save(update_fields=['completed_at'])

    @action(detail=True, methods=['patch'], url_path='complete')
    def complete(self, request, pk=None):
        task = self.get_object()
        # Block editing when task is completed

        completed = request.data.get('completed')
        if completed is None:
            return Response({'detail': 'Field "completed" is required (true/false).'}, status=status.HTTP_400_BAD_REQUEST)
        if isinstance(completed, str):
            completed = completed.lower() in ['true', '1', 'yes']
        if completed:
            task.status = 'Completed'
            task.completed_at = timezone.now()
        else:
            task.status = 'Pending'
            task.completed_at = None
        task.save(update_fields=['status', 'completed_at'])
        return Response(TaskSerializer(task, context={'request': request}).data, status=status.HTTP_200_OK)
