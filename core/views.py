from django.http import JsonResponse
from .models import MyModel
from .serializers import MyModelSerializer
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response 
from rest_framework import status 

@api_view(['GET', 'POST'])
def my_model_list(request, format=None):
    if request.method == 'GET':    
        myModels = MyModel.objects.all()
        serializer = MyModelSerializer(myModels, many=True)
        return Response(serializer.data)

    
    if request.method == 'POST':    
        serializer = MyModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'status' : 'SUCCESS',
                    'message':'Created successfully!',
                    'data':serializer.data,
                }, 
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def my_model_details(request, id, format=None):
    try:
        myModel = MyModel.objects.get(pk=id)
    except MyModel.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':    
        serializer = MyModelSerializer(myModel)
        return Response(serializer.data)

    if request.method == 'PUT':    
        serializer = MyModelSerializer(myModel, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'status' : 'SUCCESS',
                    'message':'Updated successfully!',
                    'data':serializer.data,
                }, 
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':   
        myModel.delete(); 
        return Response(
            {
                'status' : 'SUCCESS',
                'message':'Deleted successfully!'
            }, 
            status=status.HTTP_200_OK
        )