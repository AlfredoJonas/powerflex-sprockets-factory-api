from django.db import models

class BaseClass(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Date the object was created"
    )
    deleted = models.BooleanField(default=False, help_text="For logical deletion")