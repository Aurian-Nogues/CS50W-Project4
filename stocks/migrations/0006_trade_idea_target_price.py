# Generated by Django 2.0.3 on 2019-03-07 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0005_trade_idea_current_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='trade_idea',
            name='target_price',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=8),
            preserve_default=False,
        ),
    ]
