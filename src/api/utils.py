from faker import Faker

from .models import RandomData

faker = Faker()

# TODO replace to migrations
def generate_random_data():
    # total = faker.random_int(80000, 100000)
    total = faker.random_int(8000, 10000)
    batch_size = 1000
    batch = []

    for i in range(total):
        data = RandomData(
            date=faker.date_time_between(),
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