from django import forms
from .models import Response, Absence_presence, Criticize, Paye_abpresence, Question, News, Class, Exam_Scheduling
from bootstrap_datepicker_plus import DateTimePickerInput
#**********************************************************************************
class QuestionForm(forms.ModelForm):
	class Meta:
		model = Question
		fields = ['soal', 'image', 'nomreh', 'lesson', 'time', 'owner']
		labels = {'soal' : ' متن سوال:',
				 'image' : 'تصویر سوال:',
				 'nomreh' : ' بارم سوال:',
				 'lesson' : 'درس:', 'time' : 'زمان (به دقیقه):',
				 'owner' : 'کلاس:',}
#**********************************************************************************
class ResponseForm(forms.ModelForm):
	class Meta:
		model = Response
		fields = ['pasokh', 'image']
		labels = {'pasokh' : 'پاسخ:', 'image' : 'تصویر پاسخ:'}
		widgets = {'pasokh': forms.Textarea(attrs={'cols':80})}
#**********************************************************************************
class ResponseMForm(forms.ModelForm):
	class Meta:
		model = Response
		fields = ['nomreh']
		labels = {'nomreh' : 'نمره:'}
#**********************************************************************************
class Absence_presenceForm(forms.ModelForm):
	class Meta:
		model = Absence_presence
		fields = ['name']
		labels = {'name' : 'نام و نام خانوادگی:'}
#**********************************************************************************
class Paye_abpresenceForm(forms.ModelForm):
	class Meta:
		model = Paye_abpresence
		fields = ['name' , 'date_start' , 'date_stop']
		labels = {'name' : 'نام کلاس:' , 'date_start' : 'زمان شروع حضورغیاب:' , 'date_stop' : 'زمان پایان حضورغیاب:'}
		widgets = {
			'date_start': DateTimePickerInput(), 
			'date_stop': DateTimePickerInput(),
		}
#**********************************************************************************
class NewsForm(forms.ModelForm):
	class Meta:
		model = News
		fields = ['name', 'description', 'image', 'status']
		labels = {'name' : 'موضوع خبر:', 'description' : 'توضیحات خبر:', 'image' : 'تصویر خبر:', 'status' : 'وضعیت:',}
#**********************************************************************************
class ClassForm(forms.ModelForm):
	class Meta:
		model = Class
		fields = ['name' , 'owners']
		labels = {'name' : 'نام کلاس::' , 'owners' : 'اعضای کلاس:'}
#**********************************************************************************
class CriticizeForm(forms.ModelForm):
	class Meta:
		model = Criticize
		fields = ['name' , 'description']
		labels = {'name' : 'موضوع:' , 'description' : 'توضیحات:'}
#**********************************************************************************
class Exam_SchedulingForm(forms.ModelForm):
	class Meta:
		model = Exam_Scheduling
		fields = ['date_start' , 'date_stop', 'soalat']
		labels = {'date_start' : 'زمان شروع آزمون:' , 'date_stop' : 'زمان پایان آزمون:', 'soalat' : 'سوالات:'}
		widgets = {
			'date_start': DateTimePickerInput(), 
			'date_stop': DateTimePickerInput(),
		}