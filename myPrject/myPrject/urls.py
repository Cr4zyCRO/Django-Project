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
    path('logout/', LogoutView.as_view(), name='logout'),
    path('redirect/', views.redirect_page, name="redirect_page"),

    path('Admin/', views.admin_page, name='admin_page'),
    path('Register-user/', views.add_user, name='addUser'),
    path('Register-course/', views.add_course, name='addCourse'),
    path('Edit-user/<int:id>', views.edit_user, name='editUser'),
    path('Edit-course/<int:id>', views.edit_course, name='editCourse'),
    path('Confirm-Delete/<int:id>', views.confirm_delete, name='confirm_delete'),
    path('Confirm-delete/<int:id>',
         views.confirm_del_course, name='confirm_del_course'),
    path('Delete-user/<int:id>', views.dlelete_user, name='delete'),
    path('Delete-course/<int:id>', views.dlelete_course, name='delete_course'),
    path('Course-details/<int:id>',
         views.course_details, name='courseDetails'),
    path('Profesor-Details/<int:id>',
         views.profesor_details, name='profesor_details'),
    path('Assign-profesor/<int:user_id>/<int:course_id>',
         views.assign_course, name='prof_assign_course'),
    path('Unassign-profesor/<int:user_id>/<int:course_id>',
         views.unassign_course, name='prof_unassign_course'),
    path('Student-Details/<int:id>', views.student_details, name='student_details'),
    path('Enroll-student/<int:student_id>/<int:course_id>',
         views.enroll_course, name='enroll_course'),
    path('Update-student-course/<int:student_id>/<int:course_id>/<str:new_status>',
         views.update_course_status, name='update_course_status'),
    path('Unenroll-student/<int:student_id>/<int:course_id>',
         views.delete_course_status, name='delete_course_status'),


    path('profesor/<int:id>', views.profesor_page, name='profesor_page'),
    path('Course-Details/<int:course_id>',
         views.assigned_course, name='assigned_course'),
    path('Student-Info/<int:student_id>',
         views.profesor_studet_course, name='profesor_studet_course'),



    path('student/<int:id>', views.student_page, name='student_page'),
    path('enroll/<int:year>', views.course_enroll, name='enroll'),
    path('passed/<int:id>', views.passed_courses, name='passed_courses'),
    path('failed/<int:id>', views.failed_courses, name='failed_courses'),
    path('enrollment/<int:student_id>/<int:course_id>',
         views.enrollment, name='enrollment'),
    path('unenrollment/<int:student_id>/<int:course_id>',
         views.unenrollment, name='unenrollment'),


]
