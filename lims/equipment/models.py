from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import DateTimeRangeField

from psycopg2.extras import DateTimeTZRange

from lims.inventory.models import Location


class Equipment(models.Model):
    EQUIPMENT_STATUS_CHOICES = (
        ('active', 'Active',),
        ('idle', 'Idle',),
        ('error', 'Error',),
        ('broken', 'Out of order',),
    )

    name = models.CharField(max_length=50, unique=True)
    location = models.ForeignKey(Location)

    status = models.CharField(choices=EQUIPMENT_STATUS_CHOICES, max_length=30)

    can_reserve = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class EquipmentReservation(models.Model):
    start = models.DateTimeField(db_index=True)
    end = models.DateTimeField(db_index=True)

    reservation = DateTimeRangeField(null=True)

    reserved_for = models.CharField(max_length=200, null=True, blank=True)
    reserved_by = models.ForeignKey(User, related_name='reserved_by')
    equipment_reserved = models.ForeignKey(Equipment)

    is_confirmed = models.BooleanField(default=False)
    confirmed_by = models.ForeignKey(User, null=True, blank=True)

    checked_in = models.BooleanField(default=False)

    def __str__(self):
        return '{} reserved for {} from {} to {}'.format(
            self.equipment_reserved.name, self.title(),
            self.start, self.end)

    def save(self, *args, **kwargs):
        # Staff are automatically confirmed.
        if self.reserved_by.is_staff:
            self.is_confirmed = True
            self.confirmed_by = self.reserved_by
        # Take the start and end dates to generate a timerange
        # to actually query on as solves issues just using start
        # and end dates.
        self.reservation = DateTimeTZRange(self.start, self.end)
        super(EquipmentReservation, self).save(*args, **kwargs)

    def title(self):
        if self.reserved_for:
            return self.reserved_for
        else:
            return self.reserved_by.username
