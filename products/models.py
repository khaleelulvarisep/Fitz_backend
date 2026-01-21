from django.db import models

class Product(models.Model):
    CATEGORY_CHOICES = (
        ('men', 'Men'),
        ('women', 'Women'),
    )

    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.URLField(max_length=500)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering=['created_at']
    def __str__(self):
        return self.name


# Create your models here.
