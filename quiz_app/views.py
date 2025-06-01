from django.shortcuts import render, redirect, get_object_or_404
from .models import Question, Response, News, registration, Exam_Scheduling
from .models import Absence_presence, Criticize, Paye_abpresence, Class, User
from .forms import ResponseForm, Absence_presenceForm, CriticizeForm, Exam_SchedulingForm
from .forms import ResponseMForm, Paye_abpresenceForm, QuestionForm, NewsForm, ClassForm
from django.http import Http404
from django.contrib.auth.decorators import login_required
import socket, time
import datetime
from django.utils import timezone
from django.contrib import messages
#**********************************************************************************
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
#**********************************************************************************
def home(request):
	n = 0
	not_allowed = False
	soalat = Question.objects.filter(status='p')
	for soal in soalat:
		n+=1
	if n != 0:
		not_allowed = True
	try:
		for new in News.objects.filter(status='b').order_by('-date_added'):
			new_b = new
			break
		for new in News.objects.filter(status='e').order_by('-date_added'):
			news_a = new
			break
		context = {'news' : news_a, 'new1' : new_b, 'not_allowed' : not_allowed}
		return render(request, 'quiz_app/home.html', context)
	except:
		context = {'not_allowed' : not_allowed}
		return render(request, 'quiz_app/home.html', context)
#**********************************************************************************
@login_required
def moallem(request):
	if not request.user.is_superuser:
		raise Http404
	soalat = Question.objects.filter(teacher=request.user)
	for soal in soalat:
		soal = soal
		break
	pasokhat = Response.objects.filter(nomreh=None, lesson=soal.lesson).order_by('id')
	context = {'pasokhat' : pasokhat, 'path' : request.get_full_path()}
	return render(request, 'quiz_app/moallem.html', context)
#**********************************************************************************
@login_required
def moallema(request):
	if not request.user.is_superuser:
		raise Http404
	soalat = Question.objects.filter(teacher=request.user)
	for soal in soalat:
		soal = soal
		break
	pasokhat = Response.objects.filter(lesson=soal.lesson).order_by('id')
	context = {'pasokhat' : pasokhat, 'path' : request.get_full_path()}
	return render(request, 'quiz_app/moallem.html', context)
#**********************************************************************************
@login_required
def mpasokh(request, pasokh_id):
	if not request.user.is_superuser:
		raise Http404

	pasokh = Response.objects.get(id=pasokh_id)
	pasokhat = Response.objects.filter(lesson=pasokh.lesson).order_by('id')

	fraud = False

	for response in pasokhat:
		if pasokh.ip_address == response.ip_address and pasokh.id != response.id and pasokh.owner != response.owner:
			fraud = True
			break
		else:
			fraud = False

	if request.method != 'POST':
		form = ResponseMForm(instance=pasokh)
	else:
		form = ResponseMForm(request.POST, request.FILES, instance=pasokh)
		if form.is_valid():
			form.save()
			messages.success(request, 'نمره پاسخ ثبت گردید!')
			return redirect('quiz_app:moallem')
	context = {'pasokh': pasokh, 'form': form, 'fraud': fraud}
	return render(request, 'quiz_app/mpasokh.html', context)
#**********************************************************************************
@login_required
def mabpresence(request):
	if not request.user.is_staff:
		raise Http404
	abpresence = Paye_abpresence.objects.all().order_by('id')
	context = {'abpresence' : abpresence}
	return render(request, 'quiz_app/mabpresence.html', context)
#**********************************************************************************
@login_required
def mabpresencen(request):
	if not request.user.is_staff:
		raise Http404
	if request.method != 'POST':
		form = Paye_abpresenceForm()
	else:
		form = Paye_abpresenceForm(data=request.POST)
		if form.is_valid():
			a = form.save(commit=False)
			a.status = 'd'
			a.save()
			messages.success(request, 'حضورغیاب ساخته شد!')
			return redirect('quiz_app:mabpresence')
	context = {'form' : form}
	return render(request, 'quiz_app/mabpresencen.html', context)
#**********************************************************************************
@login_required
def mabpresencee(request, paye_abpresence_id):
	if not request.user.is_staff:
		raise Http404
	abpresence = Paye_abpresence.objects.get(id=paye_abpresence_id)
	if request.method != 'POST':
		form = Paye_abpresenceForm(instance=abpresence)
	else:
		form = Paye_abpresenceForm(instance=abpresence, data=request.POST)
		if form.is_valid():
			a = form.save(commit=False)
			a.status = 'd'
			a.save()
			messages.success(request, 'حضورغیاب ویرایش شد!')
			return redirect('quiz_app:mabpresence')
	context = {'abpresence': abpresence, 'form': form}
	return render(request, 'quiz_app/mabpresencee.html', context)
#**********************************************************************************
@login_required
def absences(request):
	if not request.user.is_staff:
		raise Http404
	absences = Absence_presence.objects.all().order_by('date_added')
	name_students = []
	for i in Class.objects.all():
		a = i
		break
	for i in a.owners.all():
		n = 0
		names = Absence_presence.objects.filter(name__contains=i.get_full_name())
		for name in names:
			n+=1
		if n==0:
			name_students.append(i.get_full_name())

	context = {'absences' : absences, 'name_students' : name_students}
	return render(request, 'quiz_app/absences.html', context)
#**********************************************************************************
@login_required
def question(request):
	if not request.user.is_superuser:
		raise Http404
	soalat = Question.objects.filter(teacher=request.user).order_by('date_added')
	context = {'soalat' : soalat}
	return render(request, 'quiz_app/question.html', context)
#**********************************************************************************
@login_required
def questionn(request):
	if not request.user.is_superuser:
		raise Http404
	if request.method != 'POST':
		form = QuestionForm()
	else:
		form = QuestionForm(request.POST, request.FILES)
		if form.is_valid():
			soal = form.save(commit=False)
			soal.teacher = request.user
			soal.status = 'd'
			soal.save()
			messages.success(request, 'سوال ساخته شد!')
			return redirect('quiz_app:question')
	context = {'form' : form}
	return render(request, 'quiz_app/questionn.html', context)
#**********************************************************************************
@login_required
def questione(request, question_id):
	if not request.user.is_superuser:
		raise Http404
	soal = Question.objects.get(id=question_id)
	if request.method != 'POST':
		form = QuestionForm(instance=soal)
	else:
		form = QuestionForm(request.POST, request.FILES, instance=soal)
		if form.is_valid():
			soal = form.save(commit=False)
			soal.teacher = request.user
			soal.status = 'd'
			soal.save()
			messages.success(request, 'سوال ویرایش شد!')
			return redirect('quiz_app:question')
	context = {'soal': soal, 'form': form}
	return render(request, 'quiz_app/questione.html', context)
#**********************************************************************************
@login_required
def exam_scheduling(request):
	if not request.user.is_staff:
		raise Http404
	exam_schedulings = Exam_Scheduling.objects.all().order_by('-id')
	context = {'exam_schedulings' : exam_schedulings}
	return render(request, 'quiz_app/exam_scheduling.html', context)
#**********************************************************************************
@login_required
def exam_schedulingn(request):
	if not request.user.is_superuser:
		raise Http404
	if request.method != 'POST':
		form = Exam_SchedulingForm()
	else:
		form = Exam_SchedulingForm(data=request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'برنامه زمانی  ساخته شد!')
			return redirect('quiz_app:exam_scheduling')
	context = {'form' : form}
	return render(request, 'quiz_app/exam_schedulingn.html', context)
#**********************************************************************************
@login_required
def exam_schedulinge(request, exam_schedulingn_id):
	if not request.user.is_superuser:
		raise Http404
	exam_scheduling = Exam_Scheduling.objects.get(id=exam_schedulingn_id)
	if request.method != 'POST':
		form = Exam_SchedulingForm(instance=exam_scheduling)
	else:
		form = Exam_SchedulingForm(data=request.POST, instance=exam_scheduling)
		if form.is_valid():
			form.save()
			messages.success(request, 'برنامه زمانی ویرایش شد!')
			return redirect('quiz_app:exam_scheduling')
	context = {'exam_scheduling': exam_scheduling, 'form': form}
	return render(request, 'quiz_app/exam_schedulinge.html', context)
#**********************************************************************************
@login_required
def news(request):
	if not request.user.is_staff:
		raise Http404
	news = News.objects.all().order_by('-date_added')
	context = {'news' : news}
	return render(request, 'quiz_app/news.html', context)
#**********************************************************************************
@login_required
def newsn(request):
	if not request.user.is_staff:
		raise Http404
	if request.method != 'POST':
		form = NewsForm()
	else:
		form = NewsForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			messages.success(request, 'خبر ساخته شد!')
			return redirect('quiz_app:news')
	context = {'form' : form}
	return render(request, 'quiz_app/newsn.html', context)
#**********************************************************************************
@login_required
def newse(request, news_id):
	if not request.user.is_superuser:
		raise Http404
	new = News.objects.get(id=news_id)
	if request.method != 'POST':
		form = NewsForm(instance=new)
	else:
		form = NewsForm(request.POST, request.FILES, instance=new)
		if form.is_valid():
			form.save()
			messages.success(request, 'خبر ویرایش شد!')
			return redirect('quiz_app:news')
	context = {'new': new, 'form': form}
	return render(request, 'quiz_app/newse.html', context)
#**********************************************************************************
@login_required
def list_of_users(request):
	if not request.user.is_superuser:
		raise Http404
	users = User.objects.all().order_by('-username')
	context = {'users' : users}
	return render(request, 'quiz_app/list_of_users.html', context)
#**********************************************************************************
@login_required
def Classes(request):
	if not request.user.is_superuser:
		raise Http404
	Classs = Class.objects.all().order_by('-id')
	context = {'Classs' : Classs}
	return render(request, 'quiz_app/Class.html', context)
#**********************************************************************************
@login_required
def classn(request):
	if not request.user.is_superuser:
		raise Http404
	if request.method != 'POST':
		form = ClassForm()
	else:
		form = ClassForm(data=request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'کلاس ساخته شد!')
			return redirect('quiz_app:class')
	context = {'form' : form}
	return render(request, 'quiz_app/classn.html', context)
#**********************************************************************************
@login_required
def classe(request, news_id):
	if not request.user.is_superuser:
		raise Http404
	Classs = Class.objects.get(id=news_id)
	if request.method != 'POST':
		form = ClassForm(instance=Classs)
	else:
		form = ClassForm(data=request.POST, instance=Classs)
		if form.is_valid():
			form.save()
			messages.success(request, 'کلاس ویرایش شد!')
			return redirect('quiz_app:class')
	context = {'Classs': Classs, 'form': form}
	return render(request, 'quiz_app/classe.html', context)
#**********************************************************************************
@login_required
def mcriticize(request):
	if not request.user.is_superuser:
		raise Http404
	criticizes = Criticize.objects.all().order_by('-id')
	context = {'criticizes' : criticizes}
	return render(request, 'quiz_app/mcriticize.html', context)
#**********************************************************************************
@login_required
def delete(request, object_id, model_name):
	if not request.user.is_staff:
		raise Http404
	try:
		if model_name == 'Absence_presence':
			objects = Absence_presence.objects.all()
			for o in objects:
				o.delete()
			messages.success(request, 'انجام شد!')
			return redirect('quiz_app:absences')

		elif model_name == 'News':
			o = News.objects.get(id=object_id)
			o.delete()
			messages.success(request, 'انجام شد!')
			return redirect('quiz_app:news')

		elif model_name == 'Question':
			o = Question.objects.get(id=object_id)
			o.delete()
			messages.success(request, 'انجام شد!')
			return redirect('quiz_app:question')

		elif model_name == 'Response':
			o = Response.objects.get(id=object_id)
			o.delete()
			messages.success(request, 'انجام شد!')
			return redirect('quiz_app:moallem')

		elif model_name == 'Paye_abpresence':
			o = Paye_abpresence.objects.get(id=object_id)
			o.delete()
			messages.success(request, 'انجام شد!')
			return redirect('quiz_app:mabpresence')

		elif model_name == 'Criticize':
			o = Criticize.objects.get(id=object_id)
			o.delete()
			messages.success(request, 'انجام شد!')
			return redirect('quiz_app:mcriticize')
			
		elif model_name == 'Exam_Scheduling':
			o = Exam_Scheduling.objects.get(id=object_id)
			o.delete()
			messages.success(request, 'انجام شد!')
			return redirect('quiz_app:exam_scheduling')

		elif model_name == 'Class':
			o = Class.objects.get(id=object_id)
			o.delete()
			messages.success(request, 'انجام شد!')
			return redirect('quiz_app:class')

	except:
		raise Http404
#**********************************************************************************	
def timetable():
	for timetable in Exam_Scheduling.objects.all():

		date_start = timetable.date_start

		date_now = timezone.now()

		date_stop = timetable.date_stop
		
		if date_start<=date_now and date_now<=date_stop:
			for v in timetable.soalat.all():
				v.status='p'
				v.save()
		else:
			for v in timetable.soalat.all():
				v.status='d'
				v.save()
#**********************************************************************************		
def timetableap():
	for timetable in Paye_abpresence.objects.all():

		date_start = timetable.date_start

		date_now = timezone.now()

		date_stop = timetable.date_stop
		
		if date_start<=date_now and date_now<=date_stop:
			timetable.status = 'p'
			timetable.save()		
		else:
			timetable.status = 'd'
			timetable.save()
#**********************************************************************************
@login_required
def azmon(request):
	timetable()
	x = 0
	y = 0
	z = 0
	try:
		for c in Class.objects.all():
			for o in c.owners.all():
				if o == request.user:
					clas = c
					break
		soalat = Question.objects.filter(owner=clas, status='p').order_by('id')
		for soal in soalat:
			s = soal
			break
		for soal in soalat:
			lesson = soal.lesson
			teacher = soal.teacher
			x+=1
		pasokhat = Response.objects.filter(owner=request.user).order_by('id')
		for pasokh in pasokhat:
			y+=1
		for register in registration.objects.filter(username=request.user):
			z+=1
		if x==y and x>0 and y>0:
			return render(request, 'quiz_app/payan.html')
		elif x==z and x>0 and z>0:
			return render(request, 'quiz_app/payan.html')
		context = {'soal' : s, 'len' : len(soalat), 'lesson' : lesson, 'teacher':teacher}
		return render(request, 'quiz_app/azmon.html', context)
	except:
		pasokhat = Response.objects.filter(owner=request.user)
		a = []
		for pasokh in pasokhat:
			a.append(pasokh)
		if len(a)==0:
			return render(request, 'quiz_app/not.html')
		else:
			return render(request, 'quiz_app/payan.html')
#**********************************************************************************
@login_required
def new_pasokh(request, question_id):
	x = 0
	y = 0
	for c in Class.objects.all():
		for o in c.owners.all():
			if o == request.user:
				clas = c
				break
	soalat = Question.objects.filter(owner=clas, status='p').order_by('id')
	for soal in soalat:
		x+=1
	pasokhat = Response.objects.filter(owner=request.user).order_by('id')
	for pasokh in pasokhat:
		y+=1
	if x==y:
		return redirect('quiz_app:azmon')

	soal = get_object_or_404(Question, id=question_id)

	if request.method != 'POST':
		for register in registration.objects.filter(username=request.user):
			if register.soalid == soal.id:
				try:
					for s in soalat:
						if s.id>soal.id:
							question = s
							break
					context = {'soal': question.id}
					return render(request, 'quiz_app/registration.html', context)
				except:
					return redirect('quiz_app:azmon')
		registration.objects.create(username=request.user, soalid=soal.id)

	owners = soal.owner.owners.all()
	for owner in owners:
		if owner != request.user:
			n=1
		else:
			n=0
			break
	if n==1:
		raise Http404

	ip_address = get_client_ip(request)

	if request.method != 'POST':
		form = ResponseForm()
	else:
		form = ResponseForm(request.POST, request.FILES)
		if form.is_valid():
			response = form.save(commit=False)
			response.soal = soal
			response.owner = request.user
			response.lesson = soal.lesson
			response.ip_address = ip_address
			response.save()
			try:
				for c in Class.objects.all():
					for o in c.owners.all():
						if o == request.user:
							clas = c
							break
				for quiz in Question.objects.filter(owner=clas, status='p').order_by('id'):
					s = quiz
					if s.id>soal.id:
						break
					else:
						continue
				return redirect('quiz_app:new_pasokh', question_id=s.id)
			except:
				return redirect('quiz_app:azmon')
	context = {'form' : form , 'soal' : soal}
	return render(request, 'quiz_app/new_pasokh.html', context)
#**********************************************************************************
@login_required
def pasokhat(request):
	pasokhat = Response.objects.filter(owner=request.user).order_by('id')
	correct = 0
	unanswered = 0
	try:
		for pasokh in pasokhat:
			if pasokh.nomreh>0:
				correct += 1
		for pasokh in pasokhat:
			if pasokh.pasokh == '' and not pasokh.image:
				unanswered +=1
		number = len(pasokhat)
		wrong = number - (correct + unanswered)
	except: 
		wrong = 0
		number = 0
	context = {'pasokhat' : pasokhat , 'a' : correct, 'c' : wrong, 'd' : unanswered, 'e' : number}
	return render(request, 'quiz_app/pasokhat.html', context)
#**********************************************************************************
@login_required
def class_selection(request):
	if not request.user.is_superuser:
		raise Http404
	classs = Class.objects.all()
	return render(request, 'quiz_app/class_selection.html', {'classs' : classs})
#**********************************************************************************
@login_required
def repord_card(request):
	class_name = str(request.GET)
	class_name = class_name.split('[')
	class_name = class_name[1]
	class_name = class_name.split(']')
	class_name = class_name[0]
	class_name = class_name[1:-1]
	result = Class.objects.filter(name__contains=class_name)
	classs = Class.objects.all()
	a = []
	for c in result:
		for o in c.owners.all():
			b = 0
			pasokhat = Response.objects.filter(owner=o).order_by('id')
			try:
				for pasokh in pasokhat:
					b+=pasokh.nomreh
			except:
				b=0
			a.append([o.get_full_name(), b])
	context = {'class_name' : class_name, 'a' : a, 'classs' : classs}
	return render(request, 'quiz_app/repord_card.html', context)
#**********************************************************************************
def abpresence(request):
	timetableap()
	paye = Paye_abpresence.objects.filter(status='p').order_by('id')

	if request.method != 'POST':
		form = Absence_presenceForm()
	else:
		form = Absence_presenceForm(data=request.POST)
		if form.is_valid():
			reza = form.save(commit=False)
			for a in Absence_presence.objects.all():
				if a.name==reza.name:
					return render(request, 'quiz_app/abpresence_error.html')
			reza.save()
			messages.success(request, 'نام شما ثبت گردید! باتشکر')
			return redirect('quiz_app:home')

	context = {'form' : form, 'paye' : paye}
	return render(request, 'quiz_app/abpresence.html', context)
#**********************************************************************************
def breeding(request):
	news_b = News.objects.filter(status='b').order_by('-date_added')
	context = {'news_b' : news_b}
	return render(request, 'quiz_app/breeding.html', context)
#**********************************************************************************
@login_required
def like_unlike(request, news_id):
	try:
		new = News.objects.get(id=news_id)
	except:
		raise Http404
	else:
		if request.user in new.likes.all():
			new.likes.remove(request.user)
		else:
			new.likes.add(request.user)
		messages.success(request, 'انجام شد!')
		HTTP_REFERER = request.META.get('HTTP_REFERER')
		if HTTP_REFERER == "http://127.0.0.1:8000/breeding/" or HTTP_REFERER == "https://sh-shojaei.fandogh.cloud/breeding/":
			return redirect('quiz_app:Breeding')
		else:
			return redirect('quiz_app:educational')
#**********************************************************************************
def educational(request):
	news_a = News.objects.filter(status='e').order_by('-date_added')
	context = {'news_a' : news_a}
	return render(request, 'quiz_app/educational.html', context)
#**********************************************************************************
def contact_us(request):
	return render(request, 'quiz_app/contact_us.html')
#**********************************************************************************
def criticize(request):
	if request.method != 'POST':
		form = CriticizeForm()
	else:
		form = CriticizeForm(data=request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'انتقاد یا پیشنهاد شما با موفقیت برای ما ارسال  شد! باسپاس')
			return redirect('quiz_app:home')
	context = {'form' : form}
	return render(request, 'quiz_app/criticize.html', context)
#**********************************************************************************
def search(request):
	search_title = str(request.GET)
	search_title = search_title.split('[')
	search_title = search_title[1]
	search_title = search_title.split(']')
	search_title = search_title[0]
	search_title = search_title[1:-1]
	result = News.objects.filter(name__contains=search_title)
	n = 0
	for i in result:
		n+=1
	if n==0:
		result = News.objects.filter(description__contains=search_title)
	context = {'search_title' : search_title, 'result' : result}
	return render(request, 'quiz_app/search.html', context)
#**********************************************************************************