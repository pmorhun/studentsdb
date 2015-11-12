import random

from django.core.management.base import BaseCommand

from django.utils import timezone

from ...models import Student


class Command(BaseCommand):
    help = "Add to database student."

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('number', nargs='+', type=int)

    def handle(self, *args, **options):
        for number in options['number']:
            for k in range(number):
                stud = Student(first_name=''.join(random.sample('stjshdkjadhring',7)),
                               last_name=''.join(random.sample('strhdjhskhsding',7)),
                               birthday=timezone.now(),
                               ticket=''.join(random.sample('0123456789',5))
                               )
                stud.save()
                self.stdout.write('Add student %s ' %  (stud))
                self.stdout.write('Number: %s ' %  (number))
