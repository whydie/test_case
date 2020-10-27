import datetime

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import UserSubscription, User, Subscription, SubscriptionStatus


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def payment_processed(request):
    data = request.data
    if data["status"] == "error":
        # Idk what to do in this case.
        # Could cancel `pending` user subscription object, i guess
        return Response(status=200)

    if data["status"] == "ok":
        handle_payment_ok(data)
        return Response(status=201)

    return Response(status=404)


def handle_payment_ok(data):
    """
    Creates or updates `UserSubscription` object with `SubscriptionStatus.PROCESSED` status.
    :param data: Dictionary containing given information.
    """
    user = User.objects.get(id=data["user_id"])
    subscription = Subscription.objects.get(code=data["period"])
    date_subscription_end = \
        datetime.datetime.now() + datetime.timedelta(days=subscription.days)

    UserSubscription.objects.update_or_create(
        user=user, subscription=subscription,
        date_ended=date_subscription_end, status=SubscriptionStatus.PROCESSED
    )
