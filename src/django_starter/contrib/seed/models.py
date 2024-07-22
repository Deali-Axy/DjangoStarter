import uuid
from django.db import models


class SeedTestModel(models.Model):
    char_field = models.CharField(max_length=255)
    text_field = models.TextField()
    integer_field = models.IntegerField()
    float_field = models.FloatField()
    boolean_field = models.BooleanField()
    date_field = models.DateField()
    datetime_field = models.DateTimeField()
    email_field = models.EmailField()
    url_field = models.URLField()
    decimal_field = models.DecimalField(max_digits=10, decimal_places=2)
    slug_field = models.SlugField(max_length=50)
    uuid_field = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    binary_field = models.BinaryField(max_length=100)
    duration_field = models.DurationField()
    ip_address_field = models.GenericIPAddressField(protocol='both', unpack_ipv4=False)
    ip_address_v4_field = models.GenericIPAddressField(protocol='IPv4')
    ip_address_v6_field = models.GenericIPAddressField(protocol='IPv6')
    json_field = models.JSONField()

    def __str__(self):
        return self.char_field

    class Meta:
        db_table = 'djs_seed_test_model'
        managed = False
