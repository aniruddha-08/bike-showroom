from django.db import models

# Company Model
class Company(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


# Bike Model
class Bike(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="bikes")
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.company.name} - {self.name}"


# Cart Item Model
class CartItem(models.Model):
    bike = models.ForeignKey(Bike, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_total(self):
        return self.bike.price * self.quantity

    def __str__(self):
        return f"{self.bike.name} x {self.quantity}"
