from random import randrange

import pytest
from model_bakery import baker
from rest_framework.test import APIClient

from django_testing import settings
from students.models import Student, Course

PATH = '/api/v1/courses/'
COURSES_AMOUNT = 0


@pytest.fixture()
def client():
    return APIClient()


@pytest.fixture()
def course_factory(increase_courses_amount):
    def factory(*args, **kwargs):
        increase_courses_amount(kwargs['_quantity'])
        return baker.make(Course, *args, **kwargs)

    return factory


@pytest.fixture()
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory


@pytest.fixture()
def increase_courses_amount():
    def function(quantity):
        global COURSES_AMOUNT
        COURSES_AMOUNT += quantity
        return COURSES_AMOUNT

    return function


@pytest.fixture()
def set_settings():
    def function(amount):
        settings.MAX_STUDENTS_PER_COURSE = amount
        return settings.MAX_STUDENTS_PER_COURSE

    return function


@pytest.mark.django_db
def test_retrieve_course(client, course_factory):
    course = course_factory(_quantity=1)

    response = client.get(PATH)
    data = response.json()

    assert response.status_code == 200
    assert course[0].name == data[0]['name']


@pytest.mark.django_db
def test_list_courses(client, course_factory):
    quantity = 10
    courses = course_factory(_quantity=quantity)

    response = client.get(PATH)
    data = response.json()

    assert response.status_code == 200
    assert len(data) == len(courses)
    for i, course in enumerate(data):
        assert courses[i].name == course['name']


@pytest.mark.django_db
def test_filter_id(client, course_factory):
    quantity = 10
    start_amount = COURSES_AMOUNT + 1
    courses = course_factory(_quantity=quantity)
    fin_amount = COURSES_AMOUNT + 1

    id = randrange(start_amount, fin_amount)
    filter_path = f'{PATH}{id}/'
    response = client.get(filter_path)
    data = response.json()

    assert response.status_code == 200
    assert courses[id - fin_amount].id == data['id']


@pytest.mark.django_db
def test_filter_name(client, course_factory):
    quantity = 10
    courses = course_factory(_quantity=quantity)
    course_number = randrange(10)
    course_name = courses[course_number].name

    response = client.get(PATH, {'name': course_name})
    data = response.json()

    assert response.status_code == 200
    assert len(data) != 0
    for i, course in enumerate(data):
        assert course_name == course['name']


@pytest.mark.django_db
def test_create_course(client):
    course_data = {
        'name': 'Logics'
    }

    response = client.post(PATH, course_data)

    assert response.status_code == 201


@pytest.mark.django_db
def test_patch_course(client, increase_courses_amount):
    response_1 = client.post(PATH, {'name': 'Languages'})
    response_2 = client.patch(f'{PATH}{COURSES_AMOUNT + 2}/', {'name': 'Language'})
    increase_courses_amount(1)

    assert response_1.status_code == 201
    assert response_2.status_code == 200


@pytest.mark.django_db
def test_delete_course(client):
    response_1 = client.post(PATH, {'name': 'Course to delete'})
    response_2 = client.delete(f'{PATH}{COURSES_AMOUNT + 2}/', {'name': 'Language'})

    assert response_1.status_code == 201
    assert response_2.status_code == 204


@pytest.mark.parametrize('max_amount', [0, 1, 10, 20])
def test_limit(max_amount, set_settings, client):
    limit = set_settings(max_amount)
    assert limit == max_amount
