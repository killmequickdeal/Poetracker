from django.db import models


# create database models
class Item(models.Model):
    icon = models.CharField(max_length=500)
    league = models.CharField(max_length=30)
    name = models.CharField(max_length=50)
    typeline = models.CharField(max_length=50)
    ilvl = models.IntegerField(default=0)
    note = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Property(models.Model):
    PROPERTY_CHOICES = (
        ("I", "Implicit"),
        ("E", "Explicit"),
        ("C", "Crafted"),
    )

    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    mod = models.CharField(max_length=500)
    type = models.CharField(max_length=1,
                            choices=PROPERTY_CHOICES,
                            default="E")

    def __str__(self):
        return self.mod


class Categories(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
