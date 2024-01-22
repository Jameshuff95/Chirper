from django.db import models
from django.contrib.auth.models import User

# Create a user profile model

class Profile(models.Model):
    # This associates one user with one profile, in other words, one user can only create one profile 
    # ondelete means if the user is deleted so is the profile
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Profiles can follow many other profiles
    # related_name is used for sql queries
    # symmetrical means a user can follow a person without requiring the other person follow them back
    # blank means users don't have to follow anyone
    follows = models.ManyToManyField("self", related_name="followed_by", symmetrical=False, blank=True)

    # Assign username to user profile in admin
    def __str__(self):
        return self.user.username

    