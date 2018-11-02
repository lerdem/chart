from django.core.management.base import BaseCommand

from faker import Faker
from api.models import RandomData


class Command(BaseCommand):
    help = 'generates random data'

    def add_arguments(self, parser):
        parser.add_argument('--num', type=int, help='num of data sequence ex. 5000')

    def handle(self, *args, **options):
        faker = Faker()

        if options['num'] is not None:
            total = options['num']
        else:
            total = faker.random_int(80000, 100000)

        # TODO replace to migrations
        batch_size = 2000
        batch = []

        before_in_db = RandomData.objects.count()
        self.stdout.write(
            self.style.NOTICE('Before run generate - {}'.format(before_in_db))
        )

        for _ in range(total):
            data = RandomData(
                created=faker.date_time_between(),
                value1=faker.random_int(100, 450),
                value2=faker.random_int(-100, 350),
            )
            batch.append(data)
            if len(batch) == batch_size:
                RandomData.objects.bulk_create(batch)
                batch = []
        else:
            if batch:
                RandomData.objects.bulk_create(batch)

        after_in_db = RandomData.objects.count()
        self.stdout.write(
            self.style.NOTICE('After run generate - {}'.format(after_in_db))
        )
        self.stdout.write(
            self.style.NOTICE('Objs was written - {}'.format(after_in_db - before_in_db))
        )
