"""
URL configuration for myPrject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('login/', LoginView.as_view(template_name="login.html"), name='login'),
    path('logout/', LogoutView.as_view(template_name="logout.html"), name='logout'),
    path('redirect/', views.redirect_page, name="redirect_page"),

    path('admin_page/', views.admin_page, name='admin_page'),

    path('addUser/', views.add_user, name='addUser'),
    path('addCourse/', views.add_course, name='addCourse'),

    path('editUser/<int:id>', views.edit_user, name='editUser'),
    path('editCourse/<int:id>', views.edit_course, name='editCourse'),

    path('confirm_delete/<int:id>', views.confirm_delete, name='confirm_delete'),
    path('confirm_del_course/<int:id>',
         views.confirm_del_course, name='confirm_del_course'),

    path('dlelete_user/<int:id>', views.dlelete_user, name='delete'),
    path('dlelete_course/<int:id>', views.dlelete_course, name='delete_course'),

    path('courseDetails/<int:id>',
         views.course_details, name='courseDetails'),

    path('profesor_details/<int:id>',
         views.profesor_details, name='profesor_details'),
    path('assign_course/<int:user_id>/<int:course_id>',
         views.assign_course, name='prof_assign_course'),
    path('unassign_course/<int:user_id>/<int:course_id>',
         views.unassign_course, name='prof_unassign_course'),

    path('student_details/<int:id>', views.student_details, name='student_details'),
    path('enroll_course/<int:student_id>/<int:course_id>',
         views.enroll_course, name='enroll_course'),
    path('update_course_status/<int:student_id>/<int:course_id>/<str:new_status>',
         views.update_course_status, name='update_course_status'),
    path('delete_course_status/<int:student_id>/<int:course_id>',
         views.delete_course_status, name='delete_course_status'),


    path('profesor_page/<int:id>', views.profesor_page, name='profesor_page'),
    path('student_page/<int:id>', views.student_page, name='student_page'),


]
