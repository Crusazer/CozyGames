from django.urls import path
from . import views

app_name = 'forum'
urlpatterns = [
    path('themes/', views.ThemesView.as_view(), name='themes'),
    path('questions/<int:theme_id>', views.QuestionsView.as_view(), name='questions'),
    path('question_detail/<int:question_id>/', views.QuestionDetail.as_view(), name='question_detail'),
    path('create_message/', views.CreateMessageView.as_view(), name='create_message'),
    path('create_question/', views.CreateQuestionView.as_view(), name='create_question'),

    path('client_reviews/', views.ClientReviewView.as_view(), name='client_reviews'),
    path('create_review/', views.CreateClientReviewView.as_view(), name='create_review'),

    path('blog/', views.BlogView.as_view(), name='blog'),

    path('tournaments/', views.TournamentsView.as_view(), name='tournaments'),
    path('tournament/<int:tournament_id>/', views.TournamentDetailView.as_view(), name='tournament_detail'),
    path('finished_tournaments/', views.FinishedTournamentsView.as_view(), name='finished_tournaments'),
    path('finished_tournament_detail/<int:tournament_id>/', views.FinishedTournamentDetailView.as_view(),
         name='finished_tournament_detail'),
    path('tournament/add/', views.AddParticipantView.as_view(), name='add_participant'),
    path('tournament/remove/', views.RemoveParticipantView.as_view(), name='remove_participant'),
    path('tournament/leave_tournament/', views.LeaveTournamentView.as_view(), name='leave_tournament'),
    path('tournament/create_tournament/', views.CreateTournamentView.as_view(), name='create_tournament'),
    path('tournament/my_tournaments/', views.MyTournamentsView.as_view(), name='my_tournaments'),
    path('tournament/participating_tournaments/', views.ParticipatingTournamentView.as_view(),
         name='participating_tournaments')
]
