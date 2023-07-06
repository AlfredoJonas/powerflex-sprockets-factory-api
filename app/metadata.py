from django.db import models
from datetime import datetime, timezone

class MetaData(models.Model):
    deleted = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def date_created_(self):
        return (
            self.date_created_
            if self.date_created_
            else datetime.now(timezone.utc)
        )

    def last_updated_(self):
        return (
            self.last_updated_
            if self.last_updated_
            else datetime.now(timezone.utc)
        )

    date_created_.admin_order_field = "date_created"
    last_updated_.admin_order_field = "last_updated"

    class Meta:
        abstract = True
