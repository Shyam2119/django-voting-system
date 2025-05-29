from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import PIL
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics', blank=True, null=True)
    voter_id = models.CharField(max_length=100, unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    
    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Only resize image if it exists and is not the default
        if self.image and hasattr(self.image, 'path'):
            try:
                img = Image.open(self.image.path)
                if img.height > 300 or img.width > 300:
                    output_size = (300, 300)
                    img.thumbnail(output_size)
                    img.save(self.image.path)
            except:
                pass

# Signal to create profile when user is created
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        # Only create if profile doesn't already exist
        if not hasattr(instance, 'profile'):
            Profile.objects.create(user=instance)

# Signal to save profile when user is saved
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    # Only save if profile exists
    if hasattr(instance, 'profile'):
        instance.profile.save()