from django.db import models


def upload_location(instance, filename):
    fighter = instance.first_name + '_' + instance.last_name
    return 'fighter_images/%s/%s' % (fighter, filename)


class Event(models.Model):
    name = models.CharField(max_length=32)
    poll_status = models.CharField(max_length=6, default='Closed')
    date = models.DateTimeField()

    def __str__(self):
        return self.name


class Fighter(models.Model):
    event = models.ForeignKey(Event, null=True, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_location,
                              blank=True,
                              null=True,
                              )
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    weight = models.FloatField(null=True, blank=True)
    gym = models.CharField(max_length=32, null=True, blank=True)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Match(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    red_corner = models.ForeignKey(Fighter, on_delete=models.CASCADE, related_name='fighter1')
    blue_corner = models.ForeignKey(Fighter, on_delete=models.CASCADE, related_name='fighter2')
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.red_corner.first_name + ' ' + self.red_corner.last_name + ' vs ' + \
                self.blue_corner.first_name + ' ' + self.blue_corner.last_name

    class Meta:
        verbose_name_plural = 'Matches'


