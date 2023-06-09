# Django University Management System

## INTRODUCTION
Welcome to the Django University Management System! This application, built with Django and sqlite3, functions similarly to Studomat or Moodle. It is designed to manage university courses, students, and professors, providing specific features and access levels based on user roles (admin, professor, student).

## USER ROLES AND FEATURES

### 1. Admin
An admin has full control over the application. Their features include:

  - Viewing all students, professors, and courses.
  - Adding, editing, or removing students, professors, and courses.
  - Assigning or unassigning a professor to a course.
  - Enrolling or unenrolling a student from a course.
  - Seeing which professors are assigned to each course and which students are enrolled in each course.

### 2. Professor
A professor can only access information related to their assigned courses. Their features include:

  - Viewing the courses they are assigned to.
  - Viewing the students enrolled in these courses.
  - Seeing which students have passed or failed their course.
  - Granting or revoking a student's pass status by providing or removing their signature.

### 3. Student
A student has access to their own courses and status. Their features include:

  - Viewing the courses they are enrolled in.
  - Viewing the courses they have passed or failed.
  - Enrolling or unenrolling themselves from a course.

## GETTING STARTED
The application starts with a login page where the user can enter their credentials to access their specific role and related features.

To create a superuser/admin for initial setup:

1. Run ```python manage.py createsuperuser``` from the terminal in the project root directory.
2. Follow the prompts to enter the username, email, and password
3. Access the admin interface by going to ```localhost:8000/admin``` and logging in with your superuser credentials.

The application comes with a fixture file ```'predmeti.json'``` that can be loaded to populate your application with initial data:

- Run python manage.py loaddata predmeti.json from the terminal in the project root directory.

## BUILDING AND RUNNING THE APPLICATION
To build and run this application, you need to have Python, Django, and sqlite3 installed on your machine.

Follow these steps to run the application:

1. Clone the repository from GitHub.
2. Navigate to the root directory of the project.
3. Install the required dependencies with pip: ```pip install -r requirements.txt```
4. Run the Django migration to set up your database: ```python manage.py migrate```
5. Start the Django development server: ```python manage.py runserver```
 
The application will be available at ```localhost:8000```.

## CONTRIBUTION
If you would like to contribute to the development of this Django University Management System, feel free to open a pull request or report an issue on the project's GitHub page. We welcome all contributions, big or small!

## LICENSE
This project is open-source, licensed under the GNU Affero General Public License v3.0. You are free to use, modify, and distribute it under the terms specified in the LICENSE file.





