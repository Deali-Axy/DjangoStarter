from typing import Type
from faker import Faker
from django.db import models


class Seeder(object):
    def __init__(self, locale: str = 'zh-CN'):
        self.fake = Faker(locale)
        self.fake_en = Faker('en_US')

    def seed(self, model: Type[models.Model]) -> dict:
        fake_data = {}
        for field in model._meta.get_fields():
            if field.many_to_many or field.one_to_many:
                continue
            field_class = field.__class__
            if field_class == models.CharField:
                fake_data[field.name] = self.fake.text(max_nb_chars=field.max_length)
            elif field_class == models.TextField:
                fake_data[field.name] = self.fake.text()
            elif field_class == models.IntegerField:
                fake_data[field.name] = self.fake.random_int()
            elif field_class == models.FloatField:
                fake_data[field.name] = self.fake.pyfloat(left_digits=4, right_digits=4, positive=True)
            elif field_class == models.BooleanField:
                fake_data[field.name] = self.fake.boolean()
            elif field_class == models.DateField:
                fake_data[field.name] = self.fake.date()
            elif field_class == models.DateTimeField:
                fake_data[field.name] = self.fake.date_time()
            elif field_class == models.EmailField:
                fake_data[field.name] = self.fake.email()
            elif field_class == models.URLField:
                fake_data[field.name] = self.fake.url()
            elif field_class == models.DecimalField:
                max_digits = field.max_digits
                decimal_places = field.decimal_places
                fake_data[field.name] = self.fake.pydecimal(left_digits=max_digits - decimal_places,
                                                            right_digits=decimal_places)
            elif field_class == models.SlugField:
                fake_data[field.name] = self.fake.slug(self.fake_en.text(max_nb_chars=field.max_length))
            elif field_class == models.UUIDField:
                fake_data[field.name] = self.fake.uuid4()
            elif field_class == models.BinaryField:
                fake_data[field.name] = self.fake.binary(length=field.max_length)
            elif field_class == models.DurationField:
                fake_data[field.name] = self.fake.time_delta(self.fake.future_datetime())
            elif field_class == models.IPAddressField:
                fake_data[field.name] = self.fake.ipv4()
            elif field_class == models.GenericIPAddressField:
                if field.protocol == 'both':
                    fake_data[field.name] = self.fake.ipv4() if self.fake.boolean() else self.fake.ipv6()
                elif field.protocol == 'IPv4':
                    fake_data[field.name] = self.fake.ipv4()
                elif field.protocol == 'IPv6':
                    fake_data[field.name] = self.fake.ipv6()
            elif field_class == models.JSONField:
                fake_data[field.name] = self.fake.pydict()
            elif field_class == models.ForeignKey:
                related_model = field.related_model
                # Ensure there is at least one instance of the related model
                related_instance = related_model.objects.order_by('?').first()
                if not related_instance:
                    related_instance = related_model.objects.create(**self.seed(related_model))
                # Set the foreign key ID field
                fake_data[field.attname] = related_instance.pk
            # Add more field types as needed
        return fake_data
