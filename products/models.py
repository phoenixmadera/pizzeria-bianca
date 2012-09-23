from django.db import models

# Create your models here.
class Product(models.Model):
    des = models.CharField(max_length=100, verbose_name = "Description")
    def __unicode__(self):
        return u'%s' % (self.des)
    class Meta:
        db_table = u'products'
        verbose_name = 'product'
        verbose_name_plural = 'products'