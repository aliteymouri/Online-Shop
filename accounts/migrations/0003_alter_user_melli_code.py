# Generated by Django 4.1.7 on 2023-04-12 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_card_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='melli_code',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='کد ملی'),
        ),
    ]