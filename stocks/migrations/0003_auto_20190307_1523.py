# Generated by Django 2.0.3 on 2019-03-07 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0002_trade_idea_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trade_idea',
            name='user',
            field=models.CharField(max_length=30),
        ),
    ]