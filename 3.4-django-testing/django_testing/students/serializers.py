from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.conf import settings
from students.models import Course


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ("id", "name", "students")

    def validate_students(self, value):
        """
        Проверка количества студентов на курсе
        """
        if len(set(value)) > settings.MAX_STUDENTS_PER_COURSE:
            raise ValidationError(f"Number of students per course exceeded {settings.MAX_STUDENTS_PER_COURSE}")
        return value
