from django.shortcuts import render
import joblib
from rest_framework.decorators import api_view
from rest_framework.response import Response 

model = joblib.load('ml_model/model/model.pkl')
# Create your views here.

@api_view(['GET'])
def get_prediction(request, format=None):
    if request.method == 'GET':    
        predicted_value = model.predict([[45]])[0][0]
        return Response(
            {
                'predicted_area' : predicted_value
            }
        )
