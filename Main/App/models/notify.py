from django.db import models
from Users.models import MyUsers


NOTIFY_STATUS = [
    (1, "Chưa xem"),
    (2, "Đã xem")
]


class Notify(models.Model):
    user = models.ForeignKey(MyUsers, on_delete=models.CASCADE)
    head = models.CharField(max_length=100)
    content = models.TextField(max_length=1000)
    status = models.IntegerField(choices=NOTIFY_STATUS, default=1)
    time_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user) + ": " + self.head