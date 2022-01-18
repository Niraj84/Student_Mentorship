from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from query.models import Query
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import CreateAPIView, ListAPIView,UpdateAPIView
from .serializers import RegisterSerializer,QuerySerializer,AnswerSerializer
from rest_framework.authtoken.serializers import AuthTokenSerializer
from .serializers import MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView




@api_view(['POST',])
@permission_classes([AllowAny])
def register_user(request):

    if request.method == "POST":
        serializer = RegisterSerializer(data=request.data)
        data={}
        if serializer.is_valid():
            user=serializer.save()
            data['response']='successfully registered a new user.'
            data['email']=user.email
        else:
            data=serializer.errors
        
        return Response(data)


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

class PostQueries(CreateAPIView):
    queryset= Query.objects.all()
    serializer_class=QuerySerializer
    pemission_class=[IsAuthenticated,]
    authentication_class=[JWTAuthentication,]

    def post(self, request, **kwargs):
        serializer = QuerySerializer(data=request.data)
        data={}
        if serializer.is_valid():
            query=serializer.save()
            data['response']='Question submitted successfully.'
            data['question_title']=query.question_title
        else:
            data=serializer.errors
        
        return Response(data)

class WriteAnswers(UpdateAPIView):
    queryset= Query.objects.all()
    serializer_class=AnswerSerializer
    pemission_class=[IsAuthenticated,]
    authentication_class=[JWTAuthentication,]

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class QueryDetails(ListAPIView):

    queryset= Query.objects.all()
    serializer_class=QuerySerializer
    pemission_class=[IsAuthenticated,]
    authentication_class=[JWTAuthentication,]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)



        


