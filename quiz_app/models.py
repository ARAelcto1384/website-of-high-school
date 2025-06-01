from django.db import models
from extensions.utils import jalali_converter
from django.utils import timezone
from django.utils.html import mark_safe, format_html
from django.contrib.auth.models import AbstractUser
from tinymce.models import HTMLField
#**********************************************************************************
class User(AbstractUser):
	def __str__(self):
		return self.get_full_name()
#**********************************************************************************
class News(models.Model): 
	NEWS_CHOICES = (
		('b', 'پرورشی'),
		('e', 'آموزشی'),
	)
	name = models.CharField(max_length=100, verbose_name='موضوع خبر')
	description = HTMLField(verbose_name='توضیحات خبر')
	image = models.ImageField(upload_to='images/', verbose_name='تصویر')
	status = models.CharField(max_length=1, choices=NEWS_CHOICES, verbose_name='نوع خبر')
	likes = models.ManyToManyField(User, verbose_name='تعداد لایک ها', blank=True)
	date_added = models.DateTimeField(default=timezone.now, verbose_name='تاریخ ثبت خبر')

	class Meta():
		verbose_name = 'خبر'
		verbose_name_plural = 'اخبار'

	def __str__(self):
		return self.name

	def image_tag(self):
		return format_html("<img width='100px' height='75px' style='border-radius: 15px;' src='{}'>".format(self.image.url))
	image_tag.short_description = "تصویر خبر"
#**********************************************************************************
class Class(models.Model):
	name = models.CharField(max_length=100, verbose_name='نام کلاس')
	owners = models.ManyToManyField(User, verbose_name='اعضای کلاس')

	class Meta():
		verbose_name = 'کلاس'
		verbose_name_plural = 'کلاس ها'

	def __str__(self):
		return self.name
#**********************************************************************************
class Question(models.Model):
	STATUS_CHOICES = (
		('d', 'پیش نویس'),
		('p', 'انتشار'),
	)
	LESSON_CHOICES = (
		('قرآن', 'قرآن'),
		('پیام های آسمانی', 'پیام های آسمانی'),
		('فارسی', 'فارسی'),
		('نگارش', 'نگارش'),
		('ریاضی', 'ریاضی'),
		('علوم تجربی', 'علوم تجربی'),
		('مطالعات اجتماعی', 'مطالعات اجتماعی'),
		('فرهنگ و هنر', 'فرهنگ و هنر'),
		('عربی', 'عربی'),
		('انگلیسی', 'انگلیسی'),
		('آمادگی دفاعی', 'آمادگی دفاعی'),
		('کار و فناوری', 'کار و فناوری'),
		('تفکر و سبک زندگی', 'تفکر و سبک زندگی'),
		('تربیت بدنی', 'تربیت بدنی'),
		('سایر', 'سایر'),
	)
	CLASS_CHOICES = (
			('نهم نظامی', 'نهم نظامی'),
			('نهم فردوسی', 'نهم فردوسی'),
			('هشتم حافظ', 'هشتم حافظ'),
			('هشتم سعدی', 'هشتم سعدی'),
			('هفتم دانش', 'هفتم دانش'),
			('هفتم اندیشه', 'هفتم اندیشه'),
			('سایر', 'سایر'),
		)
	soal = HTMLField(verbose_name='سوال')
	lesson = models.CharField(max_length=200, choices=LESSON_CHOICES, verbose_name='درس')
	image = models.ImageField(upload_to='images/', verbose_name='تصویر سوال', blank=True, null=True)
	status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='d', verbose_name='وضعیت')
	nomreh = models.FloatField(verbose_name='بارم سوال')
	owner = models.ForeignKey(Class, verbose_name='کلاس پاسخ دهنده', on_delete=models.CASCADE)
	teacher = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='معلم')
	time = models.FloatField(verbose_name='زمان پاسخ دهی (به دقیقه)')
	date_added = models.DateTimeField(default=timezone.now, verbose_name='تاریخ طراحی')

	class Meta():
		verbose_name = 'سوال'
		verbose_name_plural = 'بانک سوال'

	def soal_tag(self):
		return format_html(self.soal)

	def __str__(self):
		return format_html(self.soal)

	def image_tag(self):
		if self.image:
			return format_html("<img width='100px' height='75px' style='border-radius: 15px;' src='{}'>".format(self.image.url))
		else:
			return format_html("<p>----</p>")
	image_tag.short_description = "تصویر سوال"
	soal_tag.short_description = "سوال"
#**********************************************************************************
class Response(models.Model):
	LESSON_CHOICES = (
		('قرآن', 'قرآن'),
		('پیام های آسمانی', 'پیام های آسمانی'),
		('فارسی', 'فارسی'),
		('نگارش', 'نگارش'),
		('ریاضی', 'ریاضی'),
		('علوم تجربی', 'علوم تجربی'),
		('مطالعات اجتماعی', 'مطالعات اجتماعی'),
		('فرهنگ و هنر', 'فرهنگ و هنر'),
		('عربی', 'عربی'),
		('انگلیسی', 'انگلیسی'),
		('آمادگی دفاعی', 'آمادگی دفاعی'),
		('کار و فناوری', 'کار و فناوری'),
		('تفکر و سبک زندگی', 'تفکر و سبک زندگی'),
		('تربیت بدنی', 'تربیت بدنی'),
		('سایر', 'سایر'),
	)
	soal = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='سوال')
	owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر پاسخ دهنده')
	pasokh = models.TextField(verbose_name='پاسخ', blank=True, null=True)
	image = models.ImageField(upload_to='images/', verbose_name='تصویر پاسخ', blank=True, null=True)
	nomreh = models.FloatField(blank=True, null=True, verbose_name='نمره این پاسخ')
	date_added = models.DateTimeField(default=timezone.now, verbose_name='تاریخ پاسخ دادن')
	lesson = models.CharField(max_length=200, choices=LESSON_CHOICES, verbose_name='درس')
	ip_address = models.GenericIPAddressField(verbose_name='آدرس آیپی')

	class Meta():
		verbose_name = 'پاسخ'
		verbose_name_plural = 'پاسخ ها'

	def pasokh_tag(self):
		if self.pasokh:
			return format_html(self.pasokh)
		else:
			return format_html("<p>----</p>")

	def __str__(self):
		if self.pasokh:
			return format_html(self.pasokh)
		else:
			return format_html("<p>----</p>")

	def image_tag(self):
		if self.image:
			return format_html("<img width='100px' height='75px' style='border-radius: 15px;' src='{}'>".format(self.image.url))
		else:
			return format_html("<p>----</p>")
	image_tag.short_description = "تصویر  پاسخ"
	pasokh_tag.short_description = "پاسخ"
#**********************************************************************************
class Absence_presence(models.Model):
	name = models.CharField(max_length=100, verbose_name='نام و نام خانوادگی')
	date_added = models.DateTimeField(default=timezone.now, verbose_name='تاریخ ثبت حضور')

	def __str__(self):
		return self.name

	class Meta():
		verbose_name = 'حضور غیاب'
		verbose_name_plural = 'حضور غیاب'
#**********************************************************************************
class Paye_abpresence(models.Model):
	STATUS_CHOICES = (
		('d', 'پیش نویس'),
		('p', 'انتشار'),
	)
	name = models.CharField(max_length=100, verbose_name='نام کلاس')
	status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name='وضعیت')
	date_start = models.DateTimeField(default=timezone.now, verbose_name='زمان شروع حضورغیاب')
	date_stop = models.DateTimeField(default=timezone.now, verbose_name='زمان پایان حضورغیاب')
	date_added = models.DateTimeField(default=timezone.now, verbose_name='تاریخ ثبت شدن')


	def __str__(self):
		return self.name

	class Meta():
		verbose_name = 'ساخت حضورغیاب'
		verbose_name_plural = 'ساخت حضورغیاب ها'
#**********************************************************************************
class Criticize(models.Model):
	name = models.CharField(max_length=200, verbose_name='موضوع')
	description =  HTMLField(verbose_name='توضیحات')

	def __str__(self):
		return self.name

	def description_tag(self):
			return format_html(self.description)
	description_tag.short_description = "توضیحات"

	class Meta():
		verbose_name = 'انتقاد و پیشنهاد'
		verbose_name_plural = 'انتقادات و پیشنهادات'
#**********************************************************************************
class Exam_Scheduling(models.Model):
	date_start = models.DateTimeField(default=timezone.now, verbose_name='زمان شروع آزمون')
	date_stop = models.DateTimeField(default=timezone.now, verbose_name='زمان پایان آزمون')
	soalat = models.ManyToManyField(Question, verbose_name='سوالات')

	def __str__(self):
		return 'شروع: {}, پایان: {}'.format(self.date_start , self.date_stop)

	class Meta():
		verbose_name = 'زمان بندی آزمون'
		verbose_name_plural = 'زمان بندی آزمون ها'
#**********************************************************************************
class registration(models.Model):
	username = models.CharField(max_length=200, verbose_name='نام کاربر')
	soalid = models.IntegerField(verbose_name='آیدی سوال پاسخ داده شده')

	def __str__(self):
		return 'نام کاربر: {}, سوالی که پاسخ داده است: {}'.format(self.username , self.soalid)

	class Meta():
		verbose_name = 'ثبت سوال'
		verbose_name_plural = 'ثبت سوالات پاسخ داده شده'
