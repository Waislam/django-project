from django.db import models
from django.contrib.auth.models import User
from django.utils.text import Truncator

# Create your models here.

class Board(models.Model):
	name=models.CharField(max_length=30, unique=True)
	description=models.CharField(max_length=100)
	def __str__ (self):
		return self.name

	def get_post_count(self):
		return Post.objects.filter(topic__board=self).count()

	def get_last_post(self):
		return Post.objects.filter(topic__board=self).order_by('-created_at').first()


class Topic(models.Model):
	subject=models.CharField(max_length=100)
	board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='topics')
	starter=models.ForeignKey(User, on_delete=models.CASCADE, related_name='topics')
	last_updated =models.DateTimeField(auto_now_add=True)
	views = models.PositiveIntegerField(default=0)

	def __str__ (self):
		return self.subject

class Post(models.Model):
	message=models.TextField(max_length=4000)
	topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='posts')
	created_by=models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
	created_at=models.DateTimeField(auto_now_add=True)
	updated_by=models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='+')
	updated_at=models.DateTimeField(null=True)


	def __str__ (self):
		truncated_messag = Truncator(self.message)
		return truncated_messag.chars(30)