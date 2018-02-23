from django.db import models

# Create your models here.
class Member(models.Model):
    first_name = models.CharField(max_length=10)
    last_name = models.CharField(max_length=10)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    # class Meta:
    #     db_table = 'members'

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)