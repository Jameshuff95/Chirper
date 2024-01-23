from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create Chirp model
class Chirp(models.Model):
    # keep track of each user;s chirps
    user = models.ForeignKey(
        # Related name helps acccess chirps in the db
        User, related_name="chirps",
        on_delete = models.DO_NOTHING
    )
    body = models.CharField(max_length=200)
    # keep track of when each chirp is created by adding the time of chirp automatically 
    created_at = models.DateTimeField(auto_now_add=True)

    # Helps view chirps on admin backend
    def __str__(self):
        return(
            f"{self.user} "
            f"({self.created_at:%Y-%m-%d %H:%M}): "
            f"{self.body}..."
        )

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
    # Determine the date of last modification
    date_modified = models.DateTimeField(User, auto_now=True)

    # Assign username to user profile in admin
    def __str__(self):
        return self.user.username

# Create profile for each new signup
def create_profile(sender, instance, created, **kwargs):
    if created:
        # add new user to profile
        user_profile = Profile(user=instance)
        user_profile.save()
        # Have the user follow themselves
        user_profile.follows.set([instance.profile.id])
        # save again once a profile is created then edited
        user_profile.save()

post_save.connect(create_profile, sender=User)
