from django.db import models
from app.metadata import MetaData
from datetime import datetime, timezone


class Sprocket(MetaData):
    teeth = models.IntegerField(help_text="Number of teeth on the sprocket.")
    pitch_diameter = models.FloatField(
        help_text="Diameter of the pitch circle of the sprocket."
    )
    outside_diameter = models.FloatField(help_text="Overall diameter of the sprocket.")
    pitch = models.IntegerField(
        help_text="The distance between corresponding points on adjacent teeth."
    )


class Factory(MetaData):
    name = models.CharField(max_length=128, help_text="Factory name")


class SprocketProduction(MetaData):
    sprocket = models.ForeignKey(Sprocket, on_delete=models.CASCADE)
    factory = models.ForeignKey(Factory, on_delete=models.CASCADE)
    sprocket_goal = models.IntegerField(help_text="How many sprockets to make")
    sprocket_actual = models.IntegerField(help_text="How many sprockets were made")
    date_produced = models.DateTimeField(
        help_text="Since there are imported data with different timestamps we use this to make a difference between db date creation and productiton date"
    )

    def save(self, *args, **kwargs):
        self.date_produced = (
            self.date_produced if self.date_produced else datetime.now(timezone.utc)
        )
        return super().save(*args, **kwargs)
