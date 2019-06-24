from django.db import models

# Create your models here.


class product(models.Model):
    name = models.CharField(max_length=30, unique=True, default="")
    price = models.IntegerField(default=1)
    img = models.ImageField(upload_to="images", null=True, blank=True)
    preview = models.FileField(upload_to="previews", null=True)
    actual = models.FileField(upload_to="actuals", null=True)

    def __str__(self):
        return self.name


class subuser(models.Model):
    username = models.CharField(max_length=30)
    email = models.EmailField(max_length=196, default="", blank=True)
    password = models.TextField(max_length=30, default="")

    def __str__(self):
        return self.username


class order(models.Model):
    name = models.CharField(max_length=30, unique=True, default="")
    order_id = models.CharField(max_length=90)
    order_uid = models.CharField(max_length=30)
    price = models.IntegerField(default=1)
    pay_price = models.IntegerField()
    sign = models.CharField(max_length=90)

    def __str__(self):
        return self.order_id
