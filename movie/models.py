import uuid
from django.db import models

class Customer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    telephone_number = models.CharField(max_length=20)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'customers'

class Movie(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    year = models.IntegerField()
    awards = models.TextField(blank=True, null=True)
    description = models.TextField()
    actors = models.TextField()
    ratings = models.DecimalField(max_digits=3, decimal_places=1)
    # price = models.DecimalField(max_digits=8, decimal_places=2)
    link_to_pictures = models.URLField()
    duration = models.CharField(max_length=20)
    producer = models.CharField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'movies'

class Transaction(models.Model):
    PURCHASE_METHOD_CHOICES = [
        ('VISA', 'VISA'),
        ('Cash', 'Cash'),
        ('Gcash', 'Gcash'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Failed', 'Failed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, default="3d32f864-f172-4de2-b9d0-6819d3845210")
    quantity = models.PositiveIntegerField()
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_method = models.CharField(max_length=10, choices=PURCHASE_METHOD_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'transactions'

class TicketPurchase(models.Model):
    TICKET_STATUS_CHOICES = [
        ('Valid', 'Valid'),
        ('Redeemed', 'Redeemed'),
        ('Expired', 'Expired'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    ticket_status = models.CharField(max_length=10, choices=TICKET_STATUS_CHOICES, default='VALID')
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ticket_purchases'

class Schedule(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    showroom_number = models.IntegerField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    showtimes = models.CharField(max_length=255)
    intermission = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    capacity = models.PositiveIntegerField()
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'schedules'
