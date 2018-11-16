from django.test import TestCase
from django.urls import reverse, resolve
from .views import home, board_topic, new_topic
from .models import Board, Topic, Post
from django.contrib.auth.models import User
# Create your tests here.

class HomeTest(TestCase):
	def setUp(self):
		self.board=Board.objects.create(name='Python', description='python descriptin')
		url =reverse('boards:home')
		self.response=self.client.get(url)

	def test_home_view_status_code(self):
		self.assertEquals(self.response.status_code, 200)

	def test_home_url_resolves_home_view(self):
		view = resolve('/')
		self.assertEquals(view.func, home)

	def test_home_view_contains_link_to_topic_page(self):
		board_topic_url =reverse('boards:topic', kwargs={'topic_id':self.board.pk})
		self.assertContains(self.response, 'href="{0}"'.format(board_topic_url))


class BoardTopicTest(TestCase):
	def setUp(self):
		Board.objects.create(name='Python', description='this is python')


	def test_topic_view_success_status_code(self):
		url = reverse('boards:topic', kwargs={'topic_id':1})
		response=self.client.get(url)
		self.assertEquals(response.status_code, 200)

	def test_topic_view_not_found_status_code(self):
		url = reverse('boards:topic', kwargs={'topic_id':10})
		response=self.client.get(url)
		self.assertEquals(response.status_code, 404)

	def test_topic_url_resolves_topic_view(self):
		view=resolve('/topic/1/')
		self.assertEquals(view.func, board_topic)

	def test_topic_view_contains_link_to_home_page(self):
		url =reverse('boards:topic', kwargs={'topic_id':1})
		response=self.client.get(url)
		home_url=reverse('boards:home')
		self.assertContains(response, 'href="{0}"'.format(home_url))


class NewTopicTest(TestCase):
	def setUp(self):
		Board.objects.create(name='Python', description='this is python')
		User.objects.create(username='waliul', password='w123')


	def test_new_topic_view_success_status_code(self):
		url=reverse('boards:new_topic', kwargs={'topic_id':1})
		response=self.client.get(url)
		self.assertEquals(response.status_code, 200)

	def test_new_topic_view_not_found_status_code(self):
		url=reverse('boards:new_topic', kwargs={'topic_id':10})
		response=self.client.get(url)
		self.assertEquals(response.status_code, 404)

	def test_new_topic_url_resolves_new_topic_view(self):
		view=resolve('/boards/1/new/')
		self.assertEquals(view.func, new_topic)

	def test_new_topic_view_contains_link_back_to_boards_and_topic_views(self):
		url=reverse('boards:new_topic', kwargs={'topic_id':1})
		response=self.client.get(url)
		topic_url=reverse('boards:topic', kwargs={'topic_id':1})
		boards_url=reverse('boards:home')
		self.assertContains(response, 'href="{0}"'.format(topic_url))
		self.assertContains(response, 'href="{0}"'.format(boards_url))

	def test_csrf(self):
		url = reverse('boards:new_topic', kwargs={'topic_id':1})
		response=self.client.get(url)
		self.assertContains(response, 'csrfmiddlewaretoken')

	def test_new_topic_valid_post_data(self):
		url=reverse('boards:new_topic', kwargs={'topic_id':1})
		data={'subject':'this is dude', 'message':'this is dude message'}
		response=self.client.post(url, data)
		self.assertTrue(Topic.objects.exists())
		self.assertTrue(Post.objects.exists())

	def test_new_topic_invalid_post_data(self):
		url=reverse('boards:new_topic', kwargs={'topic_id':1})
		response=self.client.post(url, {})
		self.assertEquals(response.status_code, 200)


	def test_new_topic_invalid_post_data_empty_fields(self):
		'''
		Invalid post data should not redirect
		The expected behavior is to show the form again with validation errors
		'''
		url = reverse('boards:new_topic', kwargs={'topic_id': 1})
		data = {
		    'subject': '',
		    'message': ''
		}
		response = self.client.post(url, data)
		self.assertEquals(response.status_code, 200)
		self.assertFalse(Topic.objects.exists())
		self.assertFalse(Post.objects.exists())



