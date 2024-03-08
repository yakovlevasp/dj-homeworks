import random
import pytest
from rest_framework.test import APIClient
from model_bakery import baker

from students.models import Student, Course


COURSES_ROUTE = '/api/v1/courses/'


@pytest.fixture
def client():
    """
    Фикстура для api-client'a
    """
    return APIClient()


@pytest.fixture
def course_factory():
    """
    Фабрика для создания курсов
    """
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory


@pytest.fixture
def student_factory():
    """
    Фабрика для создания студентов
    """
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory


@pytest.mark.django_db
def test_retrieve_course(client, course_factory, student_factory):
    """
    Проверка получения первого курса
    """
    course = course_factory(make_m2m=True, _fill_optional=True)
    response = client.get(f'{COURSES_ROUTE}{course.pk}/')
    data = response.json()

    assert response.status_code == 200
    assert data['id'] == course.pk
    assert data['name'] == course.name
    assert data['students'] == list(course.students.values_list('id', flat=True))


@pytest.mark.django_db
def test_courses_list(client, course_factory):
    """
    Проверка получения списка курсов
    """
    courses = course_factory(_quantity=15, make_m2m=True, _fill_optional=True)
    response = client.get(COURSES_ROUTE)
    data = response.json()

    assert response.status_code == 200
    assert len(data) == len(courses)
    for i, course in enumerate(data):
        assert course['name'] == courses[i].name
        assert len(course['students']) == baker.MAX_MANY_QUANTITY


@pytest.mark.django_db
def test_filter_by_id(client, course_factory):
    """
    Проверка фильтрации списка курсов по id
    """
    courses = course_factory(_quantity=15)
    random_course = random.choice(courses)
    response = client.get(COURSES_ROUTE, {'id': random_course.pk})
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]['id'] == random_course.pk
    assert data[0]['name'] == random_course.name


@pytest.mark.django_db
def test_filter_by_name(client, course_factory):
    """
    Проверка фильтрации списка курсов по name
    """
    test_name = 'test course'
    named_courses = course_factory(_quantity=5, name=test_name)
    course_factory(_quantity=10)
    response = client.get(COURSES_ROUTE, {'name': test_name})
    data = response.json()

    assert response.status_code == 200
    assert len(data) == len(named_courses)
    for course in data:
        assert course['name'] == test_name


@pytest.mark.django_db
def test_create(client):
    """
    Тест успешного создания курса
    """
    test_name = 'test course'
    response = client.post(COURSES_ROUTE, {'name': test_name})
    data = response.json()

    assert response.status_code == 201
    assert 'id' in data
    course = Course.objects.get(pk=data['id'])
    assert data['name'] == course.name == test_name


@pytest.mark.django_db
def test_update(client, course_factory, student_factory):
    """
    Тест успешного обновления курса
    """
    course = course_factory()
    students_ids = [student.id for student in student_factory(_quantity=3)]
    test_name = 'test course'
    response = client.patch(
        f'{COURSES_ROUTE}{course.pk}/',
        {'name': test_name, 'students': students_ids}
    )
    data = response.json()

    assert response.status_code == 200
    assert data['name'] == test_name
    assert data['students'] == students_ids


@pytest.mark.django_db
def test_delete(client, course_factory):
    """
    Тест успешного удаления курса
    """
    course = course_factory()
    response = client.delete(f'{COURSES_ROUTE}{course.pk}/')
    assert response.status_code == 204
    assert not Course.objects.filter(pk=course.pk).exists()


@pytest.mark.django_db
@pytest.mark.parametrize("students_quantity, except_status, field", [(2, 201, "id"), (3, 400, "students")])
def test_create_with_students(students_quantity, except_status, field,
                              client, student_factory, course_factory, settings):
    """
    Проверка валидации максимального числа студентов на курсе
    """
    settings.MAX_STUDENTS_PER_COURSE = 2
    students = student_factory(_quantity=students_quantity)
    response = client.post(
        COURSES_ROUTE,
        {
            'name': 'test course',
            'students': [student.id for student in students]
        }
    )
    data = response.json()
    assert response.status_code == except_status
    assert field in data
