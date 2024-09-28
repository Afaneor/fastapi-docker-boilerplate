from tortoise import fields
from tortoise import models


class SampleModel(models.Model):
    name = fields.TextField()
