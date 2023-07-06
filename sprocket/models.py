from django.db import models
from sprocket import BaseClass

class Sprocket(BaseClass):
    teeth = models.IntegerField(help_text="Number of teeth on the sprocket.")
    pitch_diameter = models.FloatField(help_text="Diameter of the pitch circle of the sprocket.")
    outside_diameter = models.FloatField(help_text="Overall diameter of the sprocket.")
    pitch = models.IntegerField(help_text="The distance between corresponding points on adjacent teeth.")

class Factory(BaseClass):
    name = models.CharField(max_length=128, help_text="Factory name")

class SprocketProduction(BaseClass):
    sprocket = models.ForeignKey(Sprocket, on_delete=models.CASCADE)
    factory = models.ForeignKey(Factory, on_delete=models.CASCADE)
    sprocket_goal = models.IntegerField(help_text="How many sprockets to make")
    sprocket_actual = models.IntegerField(help_text="How many sprockets were made")
