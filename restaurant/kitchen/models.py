from django.db import models
from order.models import Order, OrderedMeals
# Create your models here.

class KitchenOrder(models.Model):
    STATUS = (
        ('DONE', 'DONE'),
        ('IN_PROGRESS', 'IN_PROGRESS'),
        ('WAITING', 'WAITING'),
    )
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    order_status = models.CharField(choices=STATUS, default='WAITING', max_length=20)
    is_done = models.BooleanField(default=False)
    