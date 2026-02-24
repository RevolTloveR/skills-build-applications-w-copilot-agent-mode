from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from djongo import models

from octofit_tracker import models as app_models

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        User = get_user_model()
        # Clear all data
        User.objects.all().delete()
        app_models.Team.objects.all().delete()
        app_models.Activity.objects.all().delete()
        app_models.Leaderboard.objects.all().delete()
        app_models.Workout.objects.all().delete()

        # Create Teams
        marvel = app_models.Team.objects.create(name='Marvel')
        dc = app_models.Team.objects.create(name='DC')

        # Create Users (super heroes)
        users = [
            User.objects.create_user(username='ironman', email='ironman@marvel.com', password='pass', team=marvel),
            User.objects.create_user(username='spiderman', email='spiderman@marvel.com', password='pass', team=marvel),
            User.objects.create_user(username='batman', email='batman@dc.com', password='pass', team=dc),
            User.objects.create_user(username='superman', email='superman@dc.com', password='pass', team=dc),
        ]

        # Create Activities
        for user in users:
            app_models.Activity.objects.create(user=user, type='run', duration=30, calories=200)
            app_models.Activity.objects.create(user=user, type='cycle', duration=60, calories=500)

        # Create Leaderboard
        app_models.Leaderboard.objects.create(team=marvel, points=1000)
        app_models.Leaderboard.objects.create(team=dc, points=900)

        # Create Workouts
        app_models.Workout.objects.create(name='Morning Cardio', description='Run and cycle combo', duration=45)
        app_models.Workout.objects.create(name='Strength Training', description='Weights and resistance', duration=60)

        self.stdout.write(self.style.SUCCESS('octofit_db populated with test data'))
