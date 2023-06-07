from django import template

register = template.Library()


@register.filter
def readable_status_course(course, student):
    return course.get_readable_status(student)
