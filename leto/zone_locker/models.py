from django.db import models

# Create your models here.
from django.utils import timezone

class Zone(models.Model):
   # id = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    number = models.IntegerField()
    description = models.CharField(max_length=200)
    locked = models.BooleanField(default=False)
    owner = models.CharField(max_length=100, blank=True, null=True)
    lock_time = models.DateTimeField(default=timezone.now, blank=True, null=True)
    
    def lock(self):
        self.locked = True
        self.lock_time = timezone.now()
        self.save()

    def unlock(self):
        self.locked = False
        self.lock_time = None
        self.save()
    
    @classmethod    
    def has_zones_locked_by(cls, owner_id):
        return cls.objects.filter(owner=owner_id).exists()

    def __str__(self):
        lock_str = (">> locked <<" if self.locked == True else '')
        return f"{self.number} - {self.description}"

