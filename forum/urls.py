from django.urls import path
from . import views

app_name = 'forum'
urlpatterns = [
    path('themes/', views.ThemesView.as_view(), name='themes'),
    path('questions/<int:theme_id>', views.QuestionsView.as_view(), name='questions'),
    path('question_detail/<int:question_id>/', views.QuestionDetail.as_view(), name='question_detail'),
    path('create_message/', views.CreateMessageView.as_view(), name='create_message'),
    path('create_question', views.CreateQuestionView.as_view(), name='create_question')
]
