from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class DeliveryTime(models.Model):
    time = models.IntegerField(max_length="3", verbose_name="Prazo esperado de entrega")
    def __unicode__(self):
        return u'%s' % (self.time)
    class Meta:
        db_table = u'daily_delivery_time'
        verbose_name = 'Tempo de Espera'

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True, null=True, blank=True)
    birth_date = models.DateField()
    #rg = models.CharField(max_length=30)
    cpf = models.CharField(max_length=30)
    tel_number = models.CharField(max_length=30)
    activation_key = models.CharField(max_length=30, null=True, blank=True)