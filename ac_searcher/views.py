# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from src.ac_searcher.ac_searcher import AcSearcher
from src.ac_searcher.config import config
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

a = AcSearcher(config)  # Import your class containing create_task and check_for_task methods

class CreateTaskAPIView(APIView):
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'query': openapi.Schema(type=openapi.TYPE_STRING),
            'positive': openapi.Schema(type=openapi.TYPE_STRING),
            'negative': openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=['query', 'positive', 'negative'],
    ))
    def post(self, request):
        # Assuming you're sending query, positive, and negative data in the request's POST data
        query = request.data.get('query')
        positive = request.data.get('positive')
        negative = request.data.get('negative')

        # Call the create_task method
        task_id = a.create_task(query, positive, negative)

        return Response({'message': 'Task created successfully', 'id': task_id}, status=status.HTTP_201_CREATED)

class CheckForTaskAPIView(APIView):
    def get(self, request, task_id):
        print(task_id)
        task = a.check_for_task(task_id)

        task_result_data = [result.__json__() for result in task.result]

        if task is not None:
            return Response({'status': task.status, 'result': task_result_data}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)