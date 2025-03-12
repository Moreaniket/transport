from django.db import models

# Create your models here.

class customer(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=50)
    number=models.IntegerField()
    address=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    pincode=models.IntegerField()
    password=models.CharField(max_length=50)



    def __str__(self):
        return self.name

class Booking(models.Model): #model relationship
    user = models.ForeignKey(customer, on_delete=models.CASCADE,null=True)  # Foreign key to customer
    pickup = models.CharField(max_length=100)
    delivery = models.CharField(max_length=100)
    goodtype = models.CharField(max_length=100)
    vehicletype = models.CharField(max_length=100)
    pickupdate = models.DateField()
    distance = models.IntegerField()
    amount = models.CharField(max_length=5000000)

    def __str__(self):
        return self.pickup



class Contact(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField(max_length=50)
    number=models.IntegerField()
    servicetype=models.CharField(max_length=50)
    message=models.CharField(max_length=1000)

    def __str__(self):
        return self.name
