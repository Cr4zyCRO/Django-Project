from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseNotAllowed
from app.forms import KorisnikForm, PredmetiForm
from .models import Korisnik, Predmeti, AssignedCourse, UpisniList
from .decorators import *


def redirect_page(request):
    role = request.user.role
    if role == 'admin':
        return redirect('admin_page')
    elif role == 'prof':
        return redirect('profesor_page', request.user.id)
    elif role == 'stu':
        return redirect('student_page', request.user.id)


@admin_required
def admin_page(request):
    students = Korisnik.objects.filter(role='stu')
    profesors = Korisnik.objects.filter(role='prof')
    courses = Predmeti.objects.all()

    context = {
        'admin': request.user,
        'students': students,
        'profesors': profesors,
        'courses': courses,
    }

    return render(request, 'admin.html', context)


@admin_required
def add_user(request):
    if request.method == 'GET':
        form = KorisnikForm()
    elif request.method == 'POST':
        form = KorisnikForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_page')

    return render(request, 'add_user.html', {'form': form})


@admin_required
def add_course(request):
    if request.method == 'GET':
        form = PredmetiForm()

    elif request.method == 'POST':
        form = PredmetiForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_page')

    return render(request, 'add_course.html', {'form': form})


@admin_required
def edit_user(request, id):
    user = Korisnik.objects.get(pk=id)
    if request.method == 'GET':
        form = KorisnikForm(instance=user)
    elif request.method == 'POST':
        form = KorisnikForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('admin_page')

    return render(request, 'edit_user.html', {'form': form})


@admin_required
def edit_course(request, id):
    course = Predmeti.objects.get(pk=id)
    if request.method == 'GET':
        form = PredmetiForm(instance=course)
        return render(request, 'edit_course.html', {'form': form})
    elif request.method == 'POST':
        form = PredmetiForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('admin_page')
        else:
            return HttpResponseNotAllowed()
    else:
        return HttpResponseNotAllowed()


@admin_required
def confirm_delete(request, id):
    if request.method == 'GET':
        return render(request, 'delete_student.html', {"data": id})
    else:
        return HttpResponseNotAllowed()


@admin_required
def confirm_del_course(request, id):
    if request.method == 'GET':
        return render(request, 'delete_course.html', {"data": id})
    else:
        return HttpResponseNotAllowed()


@admin_required
def dlelete_user(request, id):
    user = Korisnik.objects.get(pk=id)
    if 'Yes' in request.POST:
        user.delete()
        return redirect('admin_page')
    else:
        return redirect('admin_page')


@admin_required
def dlelete_course(request, id):
    course = Predmeti.objects.get(pk=id)
    if 'Yes' in request.POST:
        course.delete()
        return redirect('admin_page')
    else:
        return redirect('admin_page')


@admin_required
def course_details(request, id):
    course = Predmeti.objects.get(pk=id)

    enrolled_students = course.upisnilist_set.all()
    students = [students.student for students in enrolled_students]

    assigned_profesors = course.assignedcourse_set.all()
    profesors = [profesor.profesor for profesor in assigned_profesors]

    context = {
        'course': course,
        'profesors': profesors,
        'students': students,
    }

    return render(request, 'course_details.html', context)


@admin_required
def student_details(request, id):
    student = Korisnik.objects.get(pk=id)
    assigned_courses = student.upisnilist_set.all()
    assigned_courses_ids = [course.predmet.id for course in assigned_courses]

    courses = Predmeti.objects.exclude(id__in=assigned_courses_ids)

    context = {
        'student': student,
        'courses': courses,
        'assigned_courses': assigned_courses,
    }

    return render(request, 'student_details.html', context)


@admin_required
def enroll_course(request, student_id, course_id):
    student = Korisnik.objects.get(pk=student_id)
    course = Predmeti.objects.get(pk=course_id)

    try:
        UpisniList.objects.create(student=student, predmet=course, status='up')
    except:
        return HttpResponseNotAllowed()

    return redirect('student_details', student_id)


@admin_required
def delete_course_status(request, student_id, course_id):
    student = Korisnik.objects.get(pk=student_id)
    course = Predmeti.objects.get(pk=course_id)

    try:
        assigned_course = UpisniList.objects.get(
            student=student, predmet=course)
        assigned_course.delete()
    except:
        return HttpResponseNotAllowed()

    return redirect('student_details', student_id)


@admin_required
def profesor_details(request, id):
    profesor = Korisnik.objects.get(pk=id)
    assigned_courses = profesor.assignedcourse_set.all()
    assigned_courses_ids = [course.predmet.id for course in assigned_courses]

    courses = Predmeti.objects.exclude(id__in=assigned_courses_ids)

    context = {
        'profesor': profesor,
        'courses': courses,
        'assigned_courses': assigned_courses,
    }

    return render(request, 'profesor_details.html', context)


@admin_required
def assign_course(request, user_id, course_id):
    user = Korisnik.objects.get(pk=user_id)
    course = Predmeti.objects.get(pk=course_id)

    try:
        AssignedCourse.objects.create(profesor=user, predmet=course)
    except:
        return HttpResponseNotAllowed()

    return redirect('profesor_details', user_id)


@admin_required
def unassign_course(request, user_id, course_id):

    user = Korisnik.objects.get(pk=user_id)
    course = Predmeti.objects.get(pk=course_id)

    try:
        assigned_course = AssignedCourse.objects.get(
            profesor=user, predmet=course)
        assigned_course.delete()
    except:
        return redirect('profesor_details', user_id)

    return redirect('profesor_details', user_id)


@profesor_required
def profesor_page(request, id):
    assigned_courses = AssignedCourse.objects.filter(profesor_id=id)

    context = {
        'profesor': request.user,
        'assigned_courses': assigned_courses
    }

    return render(request, 'profesor.html', context)


@profesor_required
def assigned_course(request, course_id):
    course = Predmeti.objects.get(pk=course_id)

    students = UpisniList.objects.filter(predmet=course, student__role='stu')

    context = {
        'profesor': request.user,
        'course': course,
        'students': students
    }
    return render(request, 'assigned_course.html', context)


@profesor_required
def update_course_status(request, student_id, course_id, new_status):
    student = Korisnik.objects.get(pk=student_id)
    course = Predmeti.objects.get(pk=course_id)

    try:
        upisni_list = UpisniList.objects.get(student=student, predmet=course)
        upisni_list.status = new_status
        upisni_list.save()
    except:
        return HttpResponseNotAllowed()

    return redirect('assigned_course', course_id)


@profesor_required
def profesor_studet_course(request, student_id):
    profesor = request.user
    student = Korisnik.objects.get(id=student_id)
    courses = UpisniList.objects.filter(
        predmet__assignedcourse__profesor=profesor, student=student)
    context = {
        "profesor": profesor,
        "student": student,
        "courses": courses,
    }

    return render(request, 'profesor_studnet_course.html', context)


@student_required
def student_page(request, id):
    enrolled_courses = UpisniList.objects.filter(student_id=id)

    context = {
        'student': request.user,
        'enrolled_courses': enrolled_courses
    }

    return render(request, 'student.html', context)


@student_required
def course_enroll(request, year):

    student = request.user

    all_courses = Predmeti.objects.all()
    enrolled_courses = Predmeti.objects.filter(upisnilist__student=student)
    unenrolled_courses = all_courses.exclude(id__in=enrolled_courses)

    if year == 1:
        if student.status == 'red':
            courses = unenrolled_courses.filter(sem_red__in=[1, 2])
        else:
            courses = unenrolled_courses.filter(sem_izv__in=[1, 2])

    elif year == 2:
        if student.status == 'red':
            courses = unenrolled_courses.filter(sem_red__in=[3, 4])
        else:
            courses = unenrolled_courses.filter(sem_izv__in=[3, 4])

    elif year == 3:
        if student.status == 'red':
            courses = unenrolled_courses.filter(sem_red__in=[5, 6])
        else:
            courses = unenrolled_courses.filter(sem_izv__in=[5, 6])

    elif year == 4:
        courses = unenrolled_courses.filter(sem_izv__in=[7, 8])

    context = {
        'student': student,
        'courses': courses,
    }

    return render(request, 'course_enroll.html', context)


@student_required
def passed_courses(request, id):
    student = Korisnik.objects.get(pk=id)

    passed_courses = Predmeti.objects.filter(
        upisnilist__student=student, upisnilist__status='po')

    context = {
        'student': student,
        'passed_courses': passed_courses,
    }

    return render(request, 'passed_courses.html', context)


def failed_courses(request, id):
    student = Korisnik.objects.get(pk=id)

    failed_courses = Predmeti.objects.filter(
        upisnilist__student=student, upisnilist__status='ip')

    context = {
        'student': student,
        'failed_courses': failed_courses,
    }

    return render(request, 'failed_courses.html', context)


@student_required
def enrollment(request, student_id, course_id):
    student = Korisnik.objects.get(pk=student_id)
    course = Predmeti.objects.get(pk=course_id)

    try:
        UpisniList.objects.create(student=student, predmet=course, status='up')
    except:
        return HttpResponseNotAllowed()

    if student.status == 'red':
        if course.sem_red == 1 or course.sem_red == 2:
            year = 1
        elif course.sem_red == 3 or course.sem_red == 4:
            year = 2
        elif course.sem_red == 5 or course.sem_red == 6:
            year = 3
    else:
        if course.sem_izv == 1 or course.sem_izv == 2:
            year = 1
        elif course.sem_izv == 3 or course.sem_izv == 4:
            year = 2
        elif course.sem_izv == 5 or course.sem_izv == 6:
            year = 3
        elif course.sem_izv == 5 or course.sem_izv == 6:
            year = 4

    return redirect('enroll', year)


@student_required
def unenrollment(request, student_id, course_id):
    student = Korisnik.objects.get(pk=student_id)
    course = Predmeti.objects.get(pk=course_id)

    try:
        UpisniList.objects.get(student=student, predmet=course).delete()
    except:
        return HttpResponseNotAllowed()

    return redirect('student_page', student.id)
