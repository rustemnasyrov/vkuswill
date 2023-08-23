import datetime
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
        
    def time_remind(self):
        if self.lock_time:
            delta = timezone.now() - self.lock_time
            t_30 = datetime.timedelta(minutes=30)
            return max(t_30-delta, datetime.timedelta(minutes=0))
        return datetime.timedelta(minutes=0)
    
    def time_reminder_str(self):
        minutes, seconds = divmod(self.time_remind().total_seconds(), 60)
        return f"{int(minutes):02}:{int(seconds):02}"

    def response_params(self):
        return {"id": self.id,
            "text": self.__str__(),
            "name": self.description,
            "locked": self.locked,
            "locked_by": self.owner,
            "time_remind": self.time_reminder_str()};
    
    @classmethod    
    def has_zones_locked_by(cls, owner_id):
        return cls.objects.filter(owner=owner_id).exists()

    def __str__(self):
        if self.locked:
            reminder_str = self.time_reminder_str()
        else:
            reminder_str = ""
        return f"{self.number} - {self.description} {reminder_str}"

