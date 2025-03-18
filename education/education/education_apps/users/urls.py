from django.urls import path

from .apis import (UserDetailApi, UserListApi, UserCreateApi,UserBecomeStudentApi,
                   UserUpdateApi)

urlpatterns = [
    path('', UserListApi.as_view(), name='list'),
    path('create/', UserCreateApi.as_view(), name='create'),
    path('<int:user_id>/', UserDetailApi.as_view(), name='detail'),
    path('<int:user_id>/update/', UserUpdateApi.as_view(), name='update'),
    path('<int:user_id>/become_student/', UserBecomeStudentApi.as_view(), name='become_student'),

]