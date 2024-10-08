# Generated by Django 5.1 on 2024-08-28 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itemstripe', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('stripe_payment_id', models.CharField(blank=True, max_length=255, null=True)),
                ('items', models.ManyToManyField(to='itemstripe.item')),
            ],
        ),
    ]
