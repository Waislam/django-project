from django.test import TestCase
from django.urls import reverse, resolve
from .views import signup
# Create your tests here.
class SignUpTest(TestCase):
	def test_sign_up_status_code(self):
		url = reverse('accounts:signup')
		response = self.client.get(url)
		self.assertEquals(response.status_code, 200)


	def test_sign_up_url_resolves_sign_up_view(self):
		view=resolve('/signup/')
		self.assertEquals(view.func, signup)

