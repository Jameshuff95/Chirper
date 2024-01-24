""" All comments above each definition appear in order from top to bottom as written """

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create Chirp model
# Keep track of each user's chirps
# Related name helps acccess chirps in the db
# Keep track of when each chirp is created by adding the time of chirp automatically 
# def __str__(self): helps view chirps on admin backend
class Chirp(models.Model):
    user = models.ForeignKey(
        User, related_name="chirps",
        on_delete = models.DO_NOTHING
    )
    body = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return(
            f"{self.user} "
            f"({self.created_at:%Y-%m-%d %H:%M}): "
            f"{self.body}..."
        )

# Create a user profile model
# This associates one user with one profile, in other words, one user can only create one profile 
# ondelete means if the user is deleted so is the profile
# Profiles can follow many other profiles
# related_name is used for sql queries
# symmetrical means a user can follow a person without requiring the other person follow them back
# blank means users don't have to follow anyone
# Determine the date of last modification
# Assign username to user profile in admin in def __str__(self):
# null=True and blank=True meana having a profile picture if optional
# upload_to uploads pictures to media directory
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField("self", related_name="followed_by", symmetrical=False, blank=True)
    date_modified = models.DateTimeField(User, auto_now=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to="images/")


    def __str__(self):
        return self.user.username


# Create profile for each new signup
# Add new user to profile
# Have the user follow themselves
# Save again once a profile is created then edited
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        user_profile.follows.set([instance.profile.id])
        user_profile.save()

post_save.connect(create_profile, sender=User)
