from django.db import models


class Business(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField(blank=True)
    gst_number = models.CharField(max_length=50, blank=True)
    logo = models.ImageField(upload_to="business_logos/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Customer(models.Model):
    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name="customers"
    )

    name = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Service(models.Model):
    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name="services"
    )

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - ₹{self.price}"

class QuoteRequest(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name="quote_requests"
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="quote_requests"
    )

    requirements = models.TextField()

    quantity = models.PositiveIntegerField(default=1)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Quote Request #{self.id} - {self.customer.name}"