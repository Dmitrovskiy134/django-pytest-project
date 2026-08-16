def test_filter_courses_by_name(self, api_client, course_factory):
    """Тест фильтрации списка курсов по name"""
    course1 = course_factory(name="Python Course")
    course2 = course_factory(name="Django Course")
    course3 = course_factory(name="Python Advanced")
    url = reverse("courses-list")

    # Используем search
    response = api_client.get(url, data={"search": "Python"})

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2
    names = [course["name"] for course in response.data]
    assert "Python Course" in names
    assert "Python Advanced" in names


from django.test import TestCase

# Create your tests here.
