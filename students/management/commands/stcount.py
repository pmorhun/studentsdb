from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from ...models import Student, Group


class Command(BaseCommand):
    args = '<model_name model_name ...>'
    help = "Prints to console number of student related objects in a database."

    models = (('student', Student), ('group', Group), ('user', User))

    def handle(self, *args, **options):
        for name, model in self.models:
            if name in args:
                self.stdout.write('Number of %s in database: %d' %
                    (name, model.objects.count()))
