from django.db import models
from order.models import Order, OrderedMeals
import datetime
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
    # waiting_time_start = models.DateTimeField(auto_now=True)
    # in_progress_time_start = models.DateTimeField(null=True)
    # end_time = models.DateTimeField(null=True)
    
    # def delta_start_order_time(self):
    #     return self.in_progress_time_start - self.waiting_time_start
    
    class Meta:
         permissions = [
            ('codename', 'kitchenorder'),
        ]