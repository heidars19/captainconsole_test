from django.db import models
from account.models import User
from store.models import Product


# Maybe these models can change locations but I'll leave it here for now

class OrderProduct(models.Model):
    '''Shoppingcart'''
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()


class Order(models.Model):
    total_price = models.FloatField()
    tracking_nr = models.CharField(max_length=128)
    date = models.DateField(auto_now_add=True)
    orderproduct_id = models.ManyToManyField('OrderProduct')


#
# class OrderCart(models.Model):
#     order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
#     orderproduct_id = models.ForeignKey(OrderProduct, on_delete=models.CASCADE)
#




#######################