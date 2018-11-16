from django.urls import path
from .views import home, board_topic, new_topic, topic_post, reply_topic


app_name='boards'

urlpatterns =[
	path('', home, name='home'),
	path('topic/<int:topic_id>/', board_topic, name='topic'),
	path('boards/<int:topic_id>/new/', new_topic, name='new_topic'),
	path('boards/<int:topic_id>/topic/<int:post_id>/posts/', topic_post, name='topic_post'),
	path('boards/<int:topic_id>/topic/<int:post_id>/reply/', reply_topic, name='reply_topic'),


]