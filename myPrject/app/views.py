from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseNotAllowed
from app.forms import KorisnikForm, PredmetiForm
from .models import Korisnik, Predmeti, AssignedCourse, UpisniList


def redirect_page(request):
    role = request.user.role
    if role == 'admin':
        return redirect('admin_page')
    elif role == 'prof':
        return redirect('profesor_page', request.user.id)
    elif role == 'stu':
        return redirect('student_page', request.user.id)
    else:
        return HttpResponseNotAllowed()


def profesor_page(request, id):
    return HttpResponse("Welcome, professor!")


def student_page(request, id):
    return HttpResponse("Welcome, student!")


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


def add_user(request):
    if request.method == 'GET':
        form = KorisnikForm()
    elif request.method == 'POST':
        form = KorisnikForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_page')

    return render(request, 'add_user.html', {'form': form})


def add_course(request):
    if request.method == 'GET':
        form = PredmetiForm()

    elif request.method == 'POST':
        form = PredmetiForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_page')

    return render(request, 'add_course.html', {'form': form})


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


def confirm_delete(request, id):
    if request.method == 'GET':
        return render(request, 'delete_student.html', {"data": id})
    else:
        return HttpResponseNotAllowed()


def confirm_del_course(request, id):
    if request.method == 'GET':
        return render(request, 'delete_course.html', {"data": id})
    else:
        return HttpResponseNotAllowed()


def dlelete_user(request, id):
    user = Korisnik.objects.get(pk=id)
    if 'da' in request.POST:
        user.delete()
        return redirect('admin_page')
    else:
        return redirect('admin_page')


def dlelete_course(request, id):
    course = Predmeti.objects.get(pk=id)
    if 'da' in request.POST:
        course.delete()
        return redirect('admin_page')
    else:
        return redirect('admin_page')


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


def enroll_course(request, student_id, course_id):
    student = Korisnik.objects.get(pk=student_id)
    course = Predmeti.objects.get(pk=course_id)

    try:
        UpisniList.objects.create(student=student, predmet=course, status='up')
    except:
        return HttpResponseNotAllowed()

    return redirect('student_details', student_id)


def update_course_status(request, student_id, course_id, new_status):
    student = Korisnik.objects.get(pk=student_id)
    course = Predmeti.objects.get(pk=course_id)

    try:
        upisni_list = UpisniList.objects.get(student=student, predmet=course)
        upisni_list.status = new_status
        upisni_list.save()
    except:
        return HttpResponseNotAllowed()

    return redirect('student_details', student_id)


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


def assign_course(request, user_id, course_id):
    user = Korisnik.objects.get(pk=user_id)
    course = Predmeti.objects.get(pk=course_id)

    if user.role == 'prof':
        try:
            AssignedCourse.objects.create(profesor=user, predmet=course)
        except:
            return HttpResponseNotAllowed()

        return redirect('profesor_details', user_id)

    return redirect('loggout')


def unassign_course(request, user_id, course_id):

    user = Korisnik.objects.get(pk=user_id)
    course = Predmeti.objects.get(pk=course_id)

    if user.role == 'prof':
        try:
            assigned_course = AssignedCourse.objects.get(
                profesor=user, predmet=course)
            assigned_course.delete()
        except:
            return redirect('profesor_details', user_id)

        return redirect('profesor_details', user_id)

    return redirect('loggout')
