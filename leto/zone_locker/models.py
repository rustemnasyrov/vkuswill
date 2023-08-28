import datetime
from django.db import models
from django.db.models import Q


# Create your models here.
from django.utils import timezone

class Zone(models.Model):
   # id = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    number = models.IntegerField()
    description = models.CharField(max_length=200)
    locked = models.BooleanField(default=False)
    owner = models.CharField(max_length=100, blank=True, null=True)
    lock_time = models.DateTimeField(default=timezone.now, blank=True, null=True)
    
    _lock_limit_sec = 5

    
    def lock(self):
        self.locked = True
        self.lock_time = timezone.now()
        self.save()

    def unlock(self, owner=None):
        if self.owner == owner or owner == None:
            self.locked = False
            self.lock_time = None
            self.owner = None
            self.save()
        
    def time_remind(self):
        if self.lock_time:
            delta = timezone.now() - self.lock_time
            t_30 = datetime.timedelta(seconds=self.lock_limit)
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
    @property
    def lock_limit(cls):
        return cls._lock_limit_sec
    
    @classmethod
    @property
    def time_threshold(sel):
        return timezone.now() - timezone.timedelta(seconds=Zone.lock_limit)   

    @classmethod    
    def update_locks(self):
        time_threshold = timezone.now() - timezone.timedelta(seconds=Zone.lock_limit)    
        Zone.objects.filter(locked=True, lock_time__lte=time_threshold).update(locked=False, owner=None, lock_time=None)

    @classmethod    
    def has_zones_locked_by(cls, owner_id):
        return cls.objects.filter(owner=owner_id).exists()

    def __str__(self):
        if self.locked:
            reminder_str = self.time_reminder_str()
        else:
            reminder_str = ""
        return f"{self.number} - {self.description} {reminder_str}"

