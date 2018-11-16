from django.shortcuts import render, get_object_or_404, redirect
from .models import Board, Topic, Post
from django.contrib.auth.models import User
from .forms import NewTopicForm, PostForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count

# Create your views here.
def home(request):
	boards = Board.objects.all()
	return render(request, 'home/index.html', {'boards':boards})

def board_topic(request, topic_id):
	board = get_object_or_404(Board, pk=topic_id)
	topics = board.topics.order_by('-last_updated').annotate(replies=Count('posts')-1)
	return render(request, 'home/board_topic.html', {'board':board, 'topics':topics})

@login_required
def new_topic(request, topic_id):
	board=get_object_or_404(Board, pk=topic_id)

	if request.method=='POST':
		form = NewTopicForm(request.POST)
		if form.is_valid():
			topic=form.save(commit=False)
			topic.board=board
			topic.starter=request.user
			topic.save()


			post=Post.objects.create(
				message=form.cleaned_data.get('message'),
				topic=topic,
				created_by=request.user
			)

			return redirect('boards:topic_post', topic_id=topic_id, post_id=topic.pk)
	else:
		form = NewTopicForm()
	return render(request, 'home/new_topic.html', {'board':board, 'form':form})


def topic_post(request, topic_id, post_id):
	topic=get_object_or_404(Topic, board__id=topic_id, pk=post_id)
	topic.views += 1
	topic.save()
	return render(request, 'home/topic_post.html',{'topic':topic})

@login_required
def reply_topic(request, topic_id, post_id):
	topic = get_object_or_404(Topic, board__id=topic_id, pk=post_id)
	if request.method == 'POST':
		form = PostForm(request.POST)
		if form.is_valid():
			post =form.save(commit=False)
			post.topic= topic
			post.created_by=request.user
			post.save()
			return redirect('boards:topic_post', topic_id=topic_id, post_id=post_id)
	else:
		form = PostForm()
	return render(request, 'home/reply_topic.html', {'topic':topic, 'form':form})
