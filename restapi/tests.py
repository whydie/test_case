import json

from rest_framework.test import APITestCase
from django.urls import reverse

from .models import User, UserSubscription, Subscription, SubscriptionStatus
from .webhooks import handle_payment_ok


class UserTest(APITestCase):
    fixtures = ["test"]

    def setUp(self):
        username = "www.test@test.ru"
        password = "password"

        # Create user
        self.client.post(
            reverse("user_list"), {"username": username, "password": password}
        )

        self.user = User.objects.get(username=username)

        # Obtain user token
        response = self.client.post(
            reverse("token"), {"username": username, "password": password}
        )

        self.user_token = json.loads(response.content)["token"]
        self.headers = {
            "HTTP_AUTHORIZATION": f"Token {self.user_token}",
        }

    def test_unauthenticated(self):
        response = self.client.get(reverse("user_info", kwargs={"pk": 1}))

        self.assertEqual(response.status_code, 401)

    def test_user_has_active_subscription(self):
        self.user.create_default_subscription()

        self.assertTrue(self.user.has_active_subscription())

    def test_user_has_no_active_subscription(self):
        self.assertFalse(self.user.has_active_subscription())

    def test_user_create(self):
        username = "www.test2@test.ru"
        self.client.post(
            reverse("user_list"), {"username": username, "password": "password"},
        )

        does_exist = User.objects.filter(username=username).exists()
        self.assertTrue(does_exist)

    def test_payment_processed_error(self):
        response = self.client.post(reverse("payment"), {"status": "error"}, **self.headers)

        self.assertEqual(response.status_code, 200)

    def test_payment_processed_ok(self):
        period = "month"
        data = {
            "user_id": self.user.id,
            "status": "ok",
            "period": period
        }
        handle_payment_ok(data=data)

        subscription = Subscription.objects.get(code=period)
        user_subscription = UserSubscription.objects.get(user=self.user, subscription=subscription)

        self.assertEqual(user_subscription.status, SubscriptionStatus.PROCESSED)
