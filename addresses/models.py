from django.db import models
from delivery.models import UserProfile

# Create your models here.
class Country(models.Model):
    des = models.CharField(max_length=45, verbose_name="Description")
    def __unicode__(self):
        return self.des
    class Meta:
        db_table = u'countries'
        verbose_name = 'country'
        verbose_name_plural = 'countries'

class State(models.Model):
    des = models.CharField(max_length=85, verbose_name="Description")
    country = models.ForeignKey(Country, db_column='country', verbose_name="Country")
    def __unicode__(self):
        return self.des
    class Meta:
        db_table = u'states'
        verbose_name = 'state'
        verbose_name_plural = 'states'

class City(models.Model):
    des = models.CharField(max_length=85, verbose_name="Description")
    state = models.ForeignKey(State, db_column='state', verbose_name="State")
    def __unicode__(self):
        return self.des
    class Meta:
        db_table = u'cities'
        verbose_name = 'city'
        verbose_name_plural = 'cities'

class NeighborhoodRate(models.Model):
    val = models.FloatField(verbose_name="Value")
    def __unicode__(self):
        return u'%s' % (self.val)
    class Meta:
        db_table = u'neighborhood_rates'
        verbose_name = 'neighborhoods rate'
        verbose_name_plural = 'neighborhoods rate'

class Neighborhood(models.Model):
    des = models.CharField(max_length=100, verbose_name="Description")
    city = models.ForeignKey(City, db_column='city', verbose_name="City")
    delivery_rate = models.ForeignKey(NeighborhoodRate, db_column='delivery_rate', verbose_name="Delivery Rate")
    def __unicode__(self):
        return self.des
    class Meta:
        db_table = u'neighborhoods'
        verbose_name = 'neighborhood'
        verbose_name_plural = 'neighborhoods'

class Address(models.Model):
    cep = models.CharField(max_length=30)
    street = models.CharField(max_length=90)
    number = models.CharField(max_length=6)
    complement = models.CharField(max_length=50, null=True, blank=True)
    observations = models.CharField(max_length=250, null=True, blank=True)
    neighborhood = models.ForeignKey(Neighborhood, db_column='neighborhood')
    user = models.ForeignKey(UserProfile, db_column='user')
    class Meta:
        db_table = u'addresses'
        verbose_name_plural = "addresses"