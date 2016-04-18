import factory
from . import models


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda n: 'user-%04d' % n)
    email = factory.LazyAttribute(lambda o: '%s@example.com' % o.username)
    password = factory.PostGenerationMethodCall('set_password', 'pass')

    class Meta:
        model = models.User
        django_get_or_create = ('username', )
