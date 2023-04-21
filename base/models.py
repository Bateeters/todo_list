from django.db import models
from django.contrib. auth.models import User

# Create your models here.

# database table. "models.Model" makes this a model


class Task(models.Model):
    # attributes

    user = models.ForeignKey(
        # if a user gets deleted, the items with the user get deleted as well.
        User, on_delete=models.CASCADE,
        # means this could be empty field in database
        null=True,
        # when submitting a form
        blank=True
    )

    # setting title to string value
    title = models.CharField(
        # how long this title can be
        max_length=200
    )

    # setting description to string and gives larger text box for input
    description = models.TextField(
        null=True,
        blank=True
    )

    # sets complete to boolean value
    complete = models.BooleanField(
        # sets task to incomplete at default
        default=False
    )

    # gives date and time task is created
    created = models.DateTimeField(
        # whenever task created, system will snapshot the date and time and make it timestamp
        auto_now_add=True
    )

    # set string value
    def __str__(self):
        # setting default value to the title input
        return self.title

    class Meta:
        # ordering query set to place completed tasks at bottom of list
        ordering = ['complete']
