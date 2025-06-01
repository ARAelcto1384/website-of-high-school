from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView, PasswordResetView
from quiz_app.models import Class
from .forms import ProfileForm
from .forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages

@login_required
def my_account(request):
	for c in Class.objects.all():
		for o in c.owners.all():
			if o == request.user:
				clas = c
				break
	try:
		return render(request, 'users/my_account.html', {'clas' : clas})
	except:
		return render(request, 'users/my_account.html')
#**********************************************************************************
@login_required
def my_accountep(request):
	try:
		if request.method != 'POST':
			form = ProfileForm(instance=request.user.profile)
		else:
			form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
			if form.is_valid():
				form.save()
				messages.success(request, 'پروفایل شما با موفقیت تغییر کرد')
				return redirect('users:my_account')
	except:
		if request.method != 'POST':
			form = ProfileForm()
		else:
			form = ProfileForm(request.POST, request.FILES)
			if form.is_valid():
				form = form.save(commit=False)
				form.user = request.user
				form.save()
				messages.success(request, 'پروفایل شما با موفقیت تغییر کرد')
				return redirect('users:my_account')

	context = {'form': form}
	return render(request, 'users/my_accountep.html', context)
#**********************************************************************************
class PasswordChangeView(PasswordChangeView):
	success_url = reverse_lazy("users:password_change_done")
class PasswordResetView(PasswordResetView):
	success_url = reverse_lazy("users:password_reset_done")
#**********************************************************************************
def register(request):
	if not request.user.is_superuser:
		raise Http404
	if request.method != 'POST':
		form = UserCreationForm()
	else:
		form = UserCreationForm(data=request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'کاربر با موفقیت ثبت نام شد.')
			return redirect('users:register')
	context = {'form': form}
	return render(request, 'registration/register.html', context)
