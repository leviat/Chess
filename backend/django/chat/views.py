from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.

class Cookie(APIView):
    def get(self, request, format=None):
        if request.session.session_key is None:
            request.session.create()
        return Response()

class Test(APIView):
    def get(self, request, format=None):
        data = {'foo': 'bar'}
        return Response(data)