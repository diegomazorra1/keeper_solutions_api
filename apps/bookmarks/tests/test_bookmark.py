from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from apps.authentication.models import CustomUser
from apps.bookmarks.models import BookMark


class BookMarkAPITest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user_1 = CustomUser.objects.create_user(username='lab1', email='admin@admin.com', password='nep-lab1')
        self.user_2 = CustomUser.objects.create_user(username='lab2', email='admin2@admin.com', password='nep-lab1')
        self.user_3 = CustomUser.objects.create_user(username='lab3', email='admin3@admin.com', password='nep-lab1')
        self.url = '/api/bookmarks/'
        self.bookmark_1 = BookMark.objects.create(title="Pueba 0", url="https://stackoverflow.com/", is_public=True,
                                                  user=self.user_1)
        self.bookmark_2 = BookMark.objects.create(title="Pueba 1", url="https://google.com/", is_public=True,
                                                  user=self.user_2)
        self.bookmark_3 = BookMark.objects.create(title="Pueba 2", url="https://stackingoverflow.com/", is_public=False,
                                                  user=self.user_1)
        self.bookmark_4 = BookMark.objects.create(title="Pueba 3", url="https://yahoo.com/", is_public=False,
                                                  user=self.user_3)

    def test_create_bookmark(self):
        self.client.force_authenticate(self.user_1)
        response = self.client.post(
            self.url,
            {
                "title": "PRUEBA ",
                "url": "https://www.django-rest-framework.org/",
                "is_public": "true"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_bookmark_without_auth(self):
        response = self.client.post(
            self.url,
            {
                "title": "PRUEBA ",
                "url": "https://www.django-rest-framework.org/",
                "is_public": "true"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_bookmark(self):
        self.client.force_authenticate(self.user_3)
        response = self.client.get(self.url)
        output = response.data

        self.assertEqual(output[0]['title'], self.bookmark_1.title)
        self.assertEqual(output[1]['title'], self.bookmark_2.title)
        self.assertEqual(output[2]['title'], self.bookmark_4.title)

    def test_get_bookmark_without_auth(self):
        response = self.client.get(self.url)
        output = response.data
        self.assertEqual(output[0]['title'], self.bookmark_1.title)
        self.assertEqual(output[1]['title'], self.bookmark_2.title)
        self.assertEqual(len(output), 2)

    def test_update_bookmark(self):
        self.client.force_authenticate(self.user_3)
        new_url = self.url + '4/'
        response = self.client.put(
            new_url,
            {
                "title": "Pueba 3 updated",
                "url": "https://www.django-rest-framework-updated.org/",
                "is_public": "false"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual("Pueba 3 updated", response.data['title'])
        self.assertEqual("https://www.django-rest-framework-updated.org/", response.data['url'])

    def test_update_private_bookmark_another_user(self):
        self.client.force_authenticate(self.user_1)
        new_url = self.url + '4/'
        response = self.client.put(
            new_url,
            {
                "title": "Pueba 3 updated",
                "url": "https://www.django-rest-framework-updated.org/",
                "is_public": "false"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_public_bookmark_another_user(self):
        self.client.force_authenticate(self.user_3)
        new_url = self.url + '2/'
        response = self.client.put(
            new_url,
            {
                "title": "Pueba 3 updated",
                "url": "https://www.django-rest-framework-updated.org/",
                "is_public": "false"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
