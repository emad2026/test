from django.db import models

# from apps.Users.models import User


class NotificationsTypes(models.Choices):
    orders = "orders"
    news_feed = "news_feed"


class NotificationsModel(models.Model):
    # user = models.ForeignKey(
    #     User, on_delete=models.CASCADE, related_name="notifications"
    # )
    type = models.CharField(max_length=20, choices=NotificationsTypes.choices)
    message = models.TextField()
    """
    user_name & profile_picture_url to the user that notifection realted to
    not the user will recept the notifection
    user name like McDonalds that is mean you recived notifection form McDonalds
    """
    user_name = models.CharField(max_length=100)
    profile_picture_url = models.CharField(max_length=250)

    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message[:20]}"

    def mark_as_read(self):
        self.is_read = True
        self.save()
