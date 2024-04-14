from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from WordWeaver.renderers import CustomJSONRenderer
from services.customize_response import customize_response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny


class CustomAuthToken(ObtainAuthToken):
    renderer_classes = [CustomJSONRenderer]
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        response = Response(token.key)
        return customize_response(
            response,
            'Auth api token'
        )


class InvalidateToken(APIView):

    def get(self, request, format=None):
        request.user.auth_token.delete()
        response = Response("User token is successfully invalidated")
        return customize_response(
            response,
            'Successful logout'
        )
