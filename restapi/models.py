import datetime

from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models


class Subscription(models.Model):
    code = models.CharField(max_length=254, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    days = models.PositiveIntegerField()

    def __str__(self):
        return self.code


class SubscriptionStatus(models.TextChoices):
    PENDING = "pending"
    PROCESSED = "processed"
    CANCELED = "canceled"


class UserSubscription(models.Model):
    user = models.ForeignKey("User", related_name="subscriptions", on_delete=models.CASCADE)
    subscription = models.ForeignKey("Subscription", on_delete=models.SET_NULL, null=True)
    date_ended = models.DateTimeField(blank=True)
    status = models.CharField(max_length=254, choices=SubscriptionStatus.choices, default=SubscriptionStatus.PENDING)


class User(AbstractUser):

    def has_active_subscription(self) -> bool:
        """
        Check if user has right to read subscribed-only content.
        :return: True if has active not ended subscription, False otherwise
        """
        return self.subscriptions\
            .filter(status=SubscriptionStatus.PROCESSED, date_ended__gt=datetime.datetime.now())\
            .exists()

    def create_default_subscription(self):
        """
        Creates User subscription with default subscription type
        """
        default_subscription = Subscription.objects.only("days").get(code=settings.SUBSCRIPTION_DEFAULT)

        UserSubscription.objects.create(
            user=self, subscription=default_subscription,
            date_ended=datetime.datetime.now() + datetime.timedelta(days=default_subscription.days),
            status=SubscriptionStatus.PROCESSED
        )


class Book(models.Model):
    author = models.CharField(max_length=254)
    name = models.CharField(max_length=254)
    isbn = models.CharField(max_length=254)

    def __str__(self):
        return f"{self.author} - {self.name}"
