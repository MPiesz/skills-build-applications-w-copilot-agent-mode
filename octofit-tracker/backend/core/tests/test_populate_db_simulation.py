import runpy
import sys
import types


def test_populate_db_simulation(capsys):
    """Run `populate_db.Command.handle()` with fake `core.models` to ensure it executes without Django.

    This test doesn't require Django or pymongo; it verifies the script's control flow.
    """
    backend = '.'
    sys.path.insert(0, backend)

    # Create fake core.models module with minimal API used by populate_db
    mod = types.ModuleType('core.models')

    class DummyManager:
        def __init__(self, cls):
            self.cls = cls
            self._items = []

        def all(self):
            return self

        def delete(self):
            self._items.clear()

        def create(self, **kwargs):
            inst = self.cls(**kwargs)
            self._items.append(inst)
            return inst

    class SuggestedFor:
        def set(self, lst):
            self._list = list(lst)

    class Team:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

    class User:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

    class Activity:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

    class Workout:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)
            self.suggested_for = SuggestedFor()

    class Leaderboard:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

    mod.Team = Team
    mod.User = User
    mod.Activity = Activity
    mod.Workout = Workout
    mod.Leaderboard = Leaderboard
    mod.Team.objects = DummyManager(Team)
    mod.User.objects = DummyManager(User)
    mod.Activity.objects = DummyManager(Activity)
    mod.Workout.objects = DummyManager(Workout)
    mod.Leaderboard.objects = DummyManager(Leaderboard)

    sys.modules['core.models'] = mod

    # Run the populate_db script
    g = runpy.run_path('core/management/commands/populate_db.py')
    Command = g['Command']
    cmd = Command()
    cmd.handle()

    captured = capsys.readouterr()
    assert 'Database populated with test data!' in captured.out
