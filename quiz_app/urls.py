from django.urls import path 
from . import views

app_name = 'quiz_app'

urlpatterns = [
	path('', views.home, name='home'),
	path('azmon/', views.azmon, name='azmon'),
	path('azmon/new_pasokh/<str:question_id>/', views.new_pasokh, name='new_pasokh'),
	path('pasokhat/', views.pasokhat, name='pasokhat'),
	path('mclass_selection/', views.class_selection, name='class_selection'),
	path('mrepord_card/', views.repord_card, name='repord_card'),
	path('abpresence/', views.abpresence, name='abpresence'),
	path('moallem/', views.moallem, name='moallem'),
	path('moallem/all', views.moallema, name='moallema'),
	path('moallem/<int:pasokh_id>', views.mpasokh, name='mpasokh'),
	path('mabpresence/', views.mabpresence, name='mabpresence'),
	path('mabpresence/new/', views.mabpresencen, name='mabpresencen'),
	path('mabpresence/edit/<int:paye_abpresence_id>/', views.mabpresencee, name='mabpresencee'),
	path('mabsences/', views.absences, name='absences'),
	path('mquestion/', views.question, name='question'),
	path('mquestion/new/', views.questionn, name='questionn'),
	path('mquestion/edit/<int:question_id>/', views.questione, name='questione'),
	path('mexam_scheduling/', views.exam_scheduling, name='exam_scheduling'),
	path('mexam_schedulingn/', views.exam_schedulingn, name='exam_schedulingn'),
	path('mexam_schedulinge/<int:exam_schedulingn_id>/', views.exam_schedulinge, name='exam_schedulinge'),
	path('mnews/', views.news, name='news'),
	path('mnews/new/', views.newsn, name='newsn'),
	path('mnews/edit/<int:news_id>/', views.newse, name='newse'),
	path('mlist_of_users/', views.list_of_users, name='list_of_users'),
	path('mclass/', views.Classes, name='class'),
	path('mclass/new/', views.classn, name='classn'),
	path('mclass/edit/<int:news_id>/', views.classe, name='classe'),
	path('mcriticize/', views.mcriticize, name='mcriticize'),
	path('delete/<int:object_id>/<str:model_name>', views.delete, name='delete'),
	path('breeding/', views.breeding, name='Breeding'),
	path('like_unlike/<int:news_id>/', views.like_unlike, name='like_unlike'),
	path('educational/', views.educational, name='educational'),
	path('contact-us/', views.contact_us, name='contact_us'),
	path('criticize/', views.criticize, name='criticize'),
	path('search/', views.search, name='search'),

]