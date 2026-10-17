from tortoise import migrations
from tortoise.migrations import operations as ops
from tortoise import fields

class Migration(migrations.Migration):
    initial = True

    operations = [
        ops.CreateModel(
            name='Deal',
            fields=[
                ('id', fields.IntField(generated=True, primary_key=True, unique=True, db_index=True)),
                ('order_id', fields.IntField()),
                ('user_id', fields.IntField()),
                ('is_completed', fields.BooleanField(default=False)),
            ],
            options={'table': 'deal', 'app': 'models', 'pk_attr': 'id'},
            bases=['Model'],
        ),
    ]
