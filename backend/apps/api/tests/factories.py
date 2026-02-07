import factory
from faker import Faker
from django.contrib.auth import get_user_model
from apps.car.models import Car
from apps.order.models import Order
from apps.work.models import Work
from apps.workstatus.models import Workstatus

fake = Faker()



class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    email = factory.Sequence(lambda n: f'user{n}@example.com')
    password = factory.PostGenerationMethodCall('set_password', 'testpass123')
    first_name = factory.LazyAttribute(lambda _: fake.first_name())
    last_name = factory.LazyAttribute(lambda _: fake.last_name())
    phone_number = factory.LazyAttribute(lambda _: fake.phone_number())
    is_active = True


class CarFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Car

    mark = factory.LazyAttribute(lambda _: fake.company())
    model = factory.LazyAttribute(lambda _: fake.word())
    year = factory.LazyAttribute(lambda _: fake.year())
    vin = factory.LazyAttribute(lambda _: fake.uuid4())


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    owner = factory.SubFactory(UserFactory)
    worker = factory.SubFactory(UserFactory)
    car = factory.SubFactory(CarFactory)
    start_date = factory.LazyAttribute(lambda _: fake.past_date())


class WorkStatusFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Workstatus

    work = factory.LazyAttribute(lambda _: WorkFactory())
    order = factory.SubFactory(OrderFactory)
    fix_price = factory.LazyAttribute(lambda _: fake.random_int(min=100, max=10000))



class WorkFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Work
    name = factory.LazyAttribute(lambda _: fake.word())
    description = factory.LazyAttribute(lambda _: fake.word())
    price = factory.LazyAttribute(lambda _: fake.random_int(min=100, max=10000))
