import json
import os

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from cozygames.models import Table, Reservation, CardGame, Voting, Vote
from forum.models import Theme, Question, Message
from django.utils import timezone


class Command(BaseCommand):
    help = 'Load data from JSON file into the database'

    def add_arguments(self, parser):
        default_json_file = os.path.join(os.path.dirname(__file__), 'data.json')
        parser.add_argument('json_file_path', nargs='?', type=str, default=default_json_file,
                            help='Path to the JSON file')

    def handle(self, *args, **kwargs):
        json_file_path = kwargs['json_file_path']
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)

            # Create users and tables
            users_data = data.get('users', [])
            tables_data = data.get('tables', [])
            questions_data = data.get('questions', [])
            themes_data = data.get('themes', [])
            messages_data = data.get('messages', [])
            card_game_datas = data.get('card_games', [])
            voting_datas = data.get('votings', [])

            for user_data, table_data in zip(users_data, tables_data):
                user = User.objects.create_user(username=user_data['username'], email=user_data['email'],
                                                password=user_data['password'])
                table = Table.objects.create(number=table_data['number'], type=table_data['type'])
                Reservation.objects.create(user=user, table=table, date=timezone.now().date())

            # Load data for model CardGame
            for card_game_data in card_game_datas:
                CardGame.objects.create(name=card_game_data['name'],
                                        min_number_player=card_game_data['min_number_player'],
                                        max_number_player=card_game_data['max_number_player'],
                                        description=card_game_data['description'])

            # Load data for model Voting
            for voting_data, card_game_data in zip(voting_datas, card_game_datas):
                card_game = CardGame.objects.get(name=card_game_data['name'])
                Voting.objects.create(date=voting_data['date'], result=card_game)

            # Load data for model Theme
            for theme_data in themes_data:
                Theme.objects.create(title=theme_data['title'], date_created=theme_data['date_created'])

            # Load data for model Question
            for question_datas, user_data, themes_data in zip(questions_data, users_data, themes_data):
                theme = Theme.objects.get(title=themes_data['title'])
                author = User.objects.get(username=user_data['username'])
                Question.objects.create(title=question_datas['title'], theme=theme, author=author,
                                        date_created=question_datas['date_created'],
                                        date_update=question_datas['date_update'])

            # Load data for model Message
            for message_data, user_data, question_data in zip(messages_data, users_data, questions_data):
                user = User.objects.get(username=user_data['username'])
                question = Question.objects.get(title=question_data['title'])
                Message.objects.create(user=user, question=question, text=message_data['text'],
                                       date=message_data['date'])

            self.stdout.write(self.style.SUCCESS('Data loaded successfully'))
