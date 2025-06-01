from django.contrib import admin
from .models import Question, Response, News, registration, Exam_Scheduling
from .models import Absence_presence, Criticize, Paye_abpresence, Class
from users.models import Profile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'پروفایل'

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, )

class NewsAdmin(admin.ModelAdmin):
	list_display = ('name', 'image_tag', 'status')

class QuestionAdmin(admin.ModelAdmin):
	list_display = ('soal_tag', 'lesson', 'image_tag', 'time', 'nomreh', 'status')

class ResponseAdmin(admin.ModelAdmin):
	list_display = ('pasokh_tag', 'image_tag', 'owner', 'nomreh')

class Paye_abpresenceAdmin(admin.ModelAdmin):
	list_display = ('name', 'status')

class CriticizeAdmin(admin.ModelAdmin):
	list_display = ('name', 'description_tag')

class Exam_SchedulingAdmin(admin.ModelAdmin):
	list_display = ('date_start', 'date_stop')

admin.site.register(Question, QuestionAdmin)
admin.site.register(Response, ResponseAdmin)
admin.site.register(Profile)
admin.site.register(Exam_Scheduling, Exam_SchedulingAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Paye_abpresence, Paye_abpresenceAdmin)
admin.site.register(Absence_presence)
admin.site.register(Criticize, CriticizeAdmin)
admin.site.register(Class)
admin.site.register(registration)
admin.site.register(User, UserAdmin)