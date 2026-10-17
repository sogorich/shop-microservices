from tortoise import fields, models


class Deal(models.Model):
    id = fields.IntField(primary_key=True)

    order_id = fields.IntField()
    user_id = fields.IntField()

    is_completed = fields.BooleanField(default=False)

    def __str__(self):
        return f"User_id {self.user_id}, Order_id {self.order_id}, Deal Status: {self.is_completed}"