from django.urls import path
from .views import register_user,PostQueries,WriteAnswers,QueryDetails
from .views import  MyObtainTokenPairView
from rest_framework_simplejwt.views import TokenRefreshView



urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('sendqueries/', PostQueries.as_view(), name='postqueries'),
    path('respondqueries/<int:pk>/', WriteAnswers.as_view(), name='writeanswers'),
    path('querydetails/',QueryDetails.as_view(), name='querydetails'),
]
