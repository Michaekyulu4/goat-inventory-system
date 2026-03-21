from django.db import models
from datetime import date

class Goat(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female')
    ]

    STATUS_CHOICES = [
        ('alive', 'Alive'),
        ('sold', 'Sold'),
        ('dead', 'Dead'),
    ]

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='alive')
    tag_number = models.CharField(max_length=50, unique=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(null=True, blank=True)
    mother = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='kids'
    )
    image = models.ImageField(upload_to='goat_images/', null=True, blank=True)
    date_bought = models.DateField(null=True, blank=True)
    purchase_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    health_status = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Goat {self.tag_number}"
    
    def age_display(self):
        if not self.date_of_birth:
            return "Unknown"
        today = date.today()
        years = today.year - self.date_of_birth.year
        months = today.month - self.date_of_birth.month
        
        if today.day < self.date_of_birth.day:
            months -= 1
            
        if months < 0:
            years -= 1
            months += 12

        if years > 0:
            return f"{years} year(s)"
        else:
            return f"{months} month(s)"
    
class DeathRecord(models.Model):

    goat = models.OneToOneField(Goat, on_delete=models.CASCADE)

    date_of_death = models.DateField()

    cause = models.TextField(blank=True)

    def __str__(self):
        return f"{self.goat.tag_number} died on {self.date_of_death}"
    
class SaleRecord(models.Model):

    goat = models.OneToOneField(Goat, on_delete=models.CASCADE)

    date_sold = models.DateField()

    sale_price = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        return f"{self.goat.tag_number} sold on {self.date_sold}"
