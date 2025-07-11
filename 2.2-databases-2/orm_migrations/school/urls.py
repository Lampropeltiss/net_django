import debug_toolbar
from django.urls import path, include

from school.views import students_list, teachers_list

urlpatterns = [
    path('', students_list, name='students'),
    path('teachers', teachers_list, name='teachers'),
    path('__debug__/', include(debug_toolbar.urls)),
]
