from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from user_app.api.serializers import RegistrationSerializer
from rest_framework.authtoken.models import Token
from user_app import models
# from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['POST'])
def logout_view(request):
    
    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)



@api_view(['POST'])
def registration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        
        if serializer.is_valid():
            account = serializer.save()
            data = {
                'response': "Registration Successfully Registered",
                'username': account.username,
                'email': account.email,
                'token': Token.objects.get(user=account).key
            }
            return Response(data, status=status.HTTP_201_CREATED)  # HTTP 201 Created
        else:
            data = serializer.errors 
            return Response(data, status=status.HTTP_400_BAD_REQUEST)  # HTTP 400 Bad Request

    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED) 