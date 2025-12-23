try:
    from django.core.management.base import BaseCommand
except Exception:  # pragma: no cover - allow editing when Django isn't installed
    class _DummyStyle:
        def SUCCESS(self, msg):
            return msg
        def WARNING(self, msg):
            return msg

    class _DummyStdout:
        def write(self, msg):
            print(msg)

    class BaseCommand:
        help = ''
        def __init__(self):
            self.stdout = _DummyStdout()
            self.style = _DummyStyle()

from core.models import Team, User, Activity, Workout, Leaderboard

from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Deleting old data...'))
        Activity.objects.all().delete()
        Workout.objects.all().delete()
        Leaderboard.objects.all().delete()
        User.objects.all().delete()
        Team.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('Creating teams...'))
        marvel = Team.objects.create(name='Marvel')
        dc = Team.objects.create(name='DC')

        self.stdout.write(self.style.SUCCESS('Creating users...'))
        users = [
            User.objects.create(name='Spider-Man', email='spiderman@marvel.com', team=marvel),
            User.objects.create(name='Iron Man', email='ironman@marvel.com', team=marvel),
            User.objects.create(name='Wonder Woman', email='wonderwoman@dc.com', team=dc),
            User.objects.create(name='Batman', email='batman@dc.com', team=dc),
        ]

        self.stdout.write(self.style.SUCCESS('Creating activities...'))
        Activity.objects.create(user=users[0], type='Running', duration=30, date='2025-12-01')
        Activity.objects.create(user=users[1], type='Cycling', duration=45, date='2025-12-02')
        Activity.objects.create(user=users[2], type='Swimming', duration=60, date='2025-12-03')
        Activity.objects.create(user=users[3], type='Yoga', duration=50, date='2025-12-04')

        self.stdout.write(self.style.SUCCESS('Creating workouts...'))
        w1 = Workout.objects.create(name='Hero HIIT', description='High intensity interval training for heroes.')
        w2 = Workout.objects.create(name='Power Yoga', description='Yoga for strength and flexibility.')
        w1.suggested_for.set([users[0], users[1]])
        w2.suggested_for.set([users[2], users[3]])

        self.stdout.write(self.style.SUCCESS('Creating leaderboards...'))
        Leaderboard.objects.create(team=marvel, points=100)
        Leaderboard.objects.create(team=dc, points=120)


        self.stdout.write(self.style.SUCCESS('Ensuring unique index on email field...'))
        try:
            client = MongoClient('localhost', 27017, serverSelectionTimeoutMS=2000)
            db = client['octofit_db']
            db.core_user.create_index([('email', 1)], unique=True)
            client.close()
        except Exception:
            self.stdout.write(self.style.WARNING('Could not connect to MongoDB — skipping index creation.'))

        self.stdout.write(self.style.SUCCESS('Database populated with test data!'))
