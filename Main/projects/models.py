from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


def calculate_priority(price, complexity, urgency):
    return (price * 0.5) + (complexity * 0.3) + (urgency * 0.2)


class Project(models.Model):

    STATUS_CHOICES = [
        ('new', 'New'),
        ('assigned', 'Assigned'),
        ('in_progress', 'In Progress'),
        ('review', 'Review'),
        ('completed', 'Completed'),
        ('closed', 'Closed'),
    ]

    # Relationships
    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='client_projects'
    )

    manager = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_projects'
    )

    associates = models.ManyToManyField(
        User,
        blank=True,
        related_name='assigned_projects'
    )

    # Project details
    title = models.CharField(max_length=255)
    description = models.TextField()

    price_bid = models.FloatField()
    complexity = models.IntegerField(default=1)
    urgency = models.IntegerField(default=1)

    priority_score = models.FloatField(default=0)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Only calculate priority here
        self.priority_score = calculate_priority(
            self.price_bid,
            self.complexity,
            self.urgency
        )
        super().save(*args, **kwargs)