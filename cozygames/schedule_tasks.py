import random

from celery import shared_task
from django.db.models import Count
from django.utils import timezone


@shared_task()
def update_voting():
    from cozygames.models import Voting, CardGame

    voting: Voting = Voting.objects.filter(date=timezone.now().date()).first()
    if not voting:
        print(f"\033[33mINFO:\033[0m Voting doesn't exist")
    else:
        votes = voting.votes.all()

        if not votes:
            voting.result = None
            voting.save()
        else:
            votes_per_game: dict = votes.values('card_game').annotate(num_votes=Count('card_game'))
            max_votes = max(votes_per_game, key=lambda x: x['num_votes'])['num_votes']
            games_with_max_votes = [vote['card_game'] for vote in votes_per_game if vote['num_votes'] == max_votes]
            winner_game = random.choice(games_with_max_votes)
            winner_game_instance = CardGame.objects.get(pk=winner_game)
            voting.result = winner_game_instance
            voting.save()

    current_voting = Voting.objects.filter(date=timezone.now().date()).first()
    if current_voting:
        print(f"\033[33mINFO:\033[0m Today voting is exists")
    else:
        Voting.objects.create()
