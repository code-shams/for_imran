from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.files.storage import default_storage
from django.templatetags.static import static

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='profile_pics',
        blank=True,
        null=True,  # Remove default from field definition
    )
    bio = models.TextField(max_length=500, blank=True)

    @property
    def image_url(self):
        """
        Returns the profile image URL if exists, otherwise returns default avatar
        from static files. This is the proper way to handle default images.
        """
        if self.image and default_storage.exists(self.image.name):
            return self.image.url
        return static('images/default-avatar.jpg')

    def __str__(self):
        return f'{self.user.username} Profile'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Automatically create profile when new user signs up"""
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Ensure profile is saved when user is saved"""
    if hasattr(instance, 'profile'):
        instance.profile.save()