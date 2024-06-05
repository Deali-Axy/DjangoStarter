from faker import Faker
from django.db import models


class Seeder(object):
    def __init__(self, locale: str = 'zh-CN'):
        self.fake = Faker(locale)

    def seed(self, model) -> dict:
        fake_data = {}
        for field in model._meta.get_fields():
            if field.many_to_many or field.one_to_many:
                continue
            if isinstance(field, models.CharField):
                fake_data[field.name] = self.fake.text(max_nb_chars=field.max_length / 2)
            elif isinstance(field, models.TextField):
                fake_data[field.name] = self.fake.text()
            elif isinstance(field, models.IntegerField):
                fake_data[field.name] = self.fake.random_int()
            elif isinstance(field, models.FloatField):
                fake_data[field.name] = self.fake.random_number(digits=5, fix_len=True)
            elif isinstance(field, models.BooleanField):
                fake_data[field.name] = self.fake.boolean()
            elif isinstance(field, models.DateField):
                fake_data[field.name] = self.fake.date()
            elif isinstance(field, models.DateTimeField):
                fake_data[field.name] = self.fake.date_time()
            elif isinstance(field, models.EmailField):
                fake_data[field.name] = self.fake.email()
            elif isinstance(field, models.URLField):
                fake_data[field.name] = self.fake.url()
            elif isinstance(field, models.DecimalField):
                max_digits = field.max_digits
                decimal_places = field.decimal_places
                fake_data[field.name] = self.fake.pydecimal(
                    left_digits=max_digits - decimal_places, right_digits=decimal_places
                )
            elif isinstance(field, models.SlugField):
                fake_data[field.name] = self.fake.slug()
            elif isinstance(field, models.UUIDField):
                fake_data[field.name] = self.fake.uuid4()
            elif isinstance(field, models.BinaryField):
                fake_data[field.name] = self.fake.binary(length=field.max_length)
            elif isinstance(field, models.DurationField):
                fake_data[field.name] = self.fake.time_delta()
            elif isinstance(field, models.IPAddressField):
                fake_data[field.name] = self.fake.ipv4()
            elif isinstance(field, models.GenericIPAddressField):
                if field.protocol == 'both':
                    fake_data[field.name] = self.fake.ipv4() if self.fake.boolean() else self.fake.ipv6()
                elif field.protocol == 'IPv4':
                    fake_data[field.name] = self.fake.ipv4()
                elif field.protocol == 'IPv6':
                    fake_data[field.name] = self.fake.ipv6()
            elif isinstance(field, models.JSONField):
                fake_data[field.name] = self.fake.pydict()
            # Add more field types as needed
        return fake_data
