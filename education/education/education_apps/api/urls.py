from django.urls import include, path

urlpatterns =[
    path('users/', include(('education.education_apps.users.urls', 'users'))),
    path('education/', include(('education.education_apps.educa.urls', 'education'))),
]