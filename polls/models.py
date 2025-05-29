from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Election(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title
    
    def is_ongoing(self):
        now = timezone.now()
        return self.start_date <= now <= self.end_date and self.is_active
    
    def has_ended(self):
        return timezone.now() > self.end_date or not self.is_active

class Candidate(models.Model):
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name='candidates')
    name = models.CharField(max_length=100)
    bio = models.TextField()
    image = models.CharField(max_length=255, blank=True, null=True)  # URL to candidate image
    
    def __str__(self):
        return f"{self.name} - {self.election.title}"
    
    def vote_count(self):
        return self.votes.count()

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='votes')
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name='votes')
    timestamp = models.DateTimeField(auto_now_add=True)
    verification_code = models.CharField(max_length=50, unique=True)
    
    class Meta:
        # Ensure a user can vote only once per election
        unique_together = ('user', 'election')
    
    def __str__(self):
        return f"{self.user.username} voted in {self.election.title}"