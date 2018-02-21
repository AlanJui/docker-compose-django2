from django.db import models

# Create your models here.
class Member(models.Model):
    first_name = models.CharField(max_length=10)
    last_name = models.CharField(max_length=10)
    member_id = models.IntegerField()

    class Meta:
        db_table = 'members'

    def __str__(self):
        return self.first_name + ' ' + self.last_name