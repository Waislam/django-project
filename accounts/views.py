from django.shortcuts import render, redirect
from .forms import SignUPForm
from django.contrib.auth import login

# Create your views here.

def signup(request):
	if request.method=='POST':
		form = SignUPForm(request.POST)
		if form.is_valid():
			user=form.save()
			login(request, user)
			return redirect('boards:home')
	else:
		form=SignUPForm()

	return render(request, 'accounts/signup.html', {'form':form})