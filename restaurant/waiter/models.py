from django.db import models
from core.models import CustomUser
from order.models import Order

#

class Waiter(models.Model):

    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    waiter_name = models.CharField(max_length=100, null=False)


class WaiterOrder(models.Model):

    waiter_id = models.ForeignKey(Waiter, on_delete=models.CASCADE)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)