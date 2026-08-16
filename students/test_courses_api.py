import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from model_bakery import baker
from students.models import Course, Student


@pytest.fixture
def api_client():
    """Фикстура для API клиента"""
    return APIClient()


@pytest.fixture
def course_factory():
    """Фикстура для фабрики курсов"""
    def create_course(**kwargs):
        return baker.make(Course, **kwargs)
    return create_course


@pytest.fixture
def student_factory():
    """Фикстура для фабрики студентов"""
    def create_student(**kwargs):
        return baker.make(Student, **kwargs)
    return create_student


@pytest.mark.django_db
class TestCoursesAPI:
    """Тесты для API курсов"""

    def test_retrieve_course(self, api_client, course_factory):
        """Тест получения курса (retrieve-логика)"""
        course = course_factory()
        url = reverse("courses-detail", args=[course.id])

        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == course.id
        assert response.data["name"] == course.name

    def test_list_courses(self, api_client, course_factory):
        """Тест получения списка курсов (list-логика)"""
        courses = course_factory(_quantity=5)
        url = reverse("courses-list")

        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 5
        response_ids = [course["id"] for course in response.data]
        for course in courses:
            assert course.id in response_ids

    def test_filter_courses_by_id(self, api_client, course_factory):
        """Тест фильтрации списка курсов по id"""
        courses = course_factory(_quantity=5)
        target_course = courses[0]
        url = reverse("courses-list")

        response = api_client.get(url, data={"id": target_course.id})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["id"] == target_course.id

    def test_filter_courses_by_name(self, api_client, course_factory):
        """Тест фильтрации списка курсов по name"""
        course = course_factory(name="Python Course")
        url = reverse("courses-list")

        response = api_client.get(url, data={"name": "Python Course"})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["name"] == "Python Course"

    def test_create_course_success(self, api_client):
        """Тест успешного создания курса"""
        url = reverse("courses-list")
        course_data = {
            "name": "New Course",
            "description": "Course description"
        }

        response = api_client.post(url, data=course_data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == course_data["name"]
        assert Course.objects.filter(name=course_data["name"]).exists()

    def test_update_course_success(self, api_client, course_factory):
        """Тест успешного обновления курса"""
        course = course_factory(name="Old Name")
        url = reverse("courses-detail", args=[course.id])
        update_data = {"name": "Updated Name"}

        response = api_client.patch(url, data=update_data)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "Updated Name"
        course.refresh_from_db()
        assert course.name == "Updated Name"

    def test_delete_course_success(self, api_client, course_factory):
        """Тест успешного удаления курса"""
        course = course_factory()
        url = reverse("courses-detail", args=[course.id])

        response = api_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Course.objects.filter(id=course.id).exists()