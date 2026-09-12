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