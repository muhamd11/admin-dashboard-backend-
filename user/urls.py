from django.urls import path
from .views import RegisterUserView,LoginUserView,GetDeleteUserView,GetAllUserView,UpdateUserView

urlpatterns = [
    path('', GetAllUserView.as_view(), name='get_user' ),
    path('register/', RegisterUserView.as_view(), name='register' ),
    # path('image-upload/', ImageUploadAPIView.as_view(), name='image-upload'),
    path('login/', LoginUserView.as_view(), name='login' ),
    path('<int:pk>/', GetDeleteUserView.as_view(), name='get_user' ),
    path('<int:pk>/update/', UpdateUserView.as_view(), name='update_user'),
]



