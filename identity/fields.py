from django.db import models
from django.utils.translation import gettext_lazy as _


class HandField(models.Field):

    description = _("String (up to %(max_length)s)")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def db_type(self, connection):
        return 'char(%s)' % self.max_length

    def from_db_value(self, value, expression, connection):
        """
        Will be called in all circumstances when the data is loaded from the
        database, including in aggregates and values() calls
        """
        if value is None:
            return value
        return

    def to_python(self, value):
        """
        Called by deserialization and during the clean() method used from
        forms.

        This allows you to use backend-specific conversion logic if it is
        required
        """
        if value is None:
            return value

        return

    def get_db_prep_value(self, value, connection, prepared=False):
        """
        Converts data types to be in a specific format before they can be used
        by a database backend
        """
        value = super().get_db_prep_value(value, connection, prepared)
        if value is not None:
            return connection.Database.Binary(value)
        return value
